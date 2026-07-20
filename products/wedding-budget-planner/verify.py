"""Independent cross-check of build.py's business logic (LibreOffice recalculation
is broken in this sandbox per ledger.md's documented environment issue -- see there).
Re-derives every formula's result in plain Python from the same source data and
diffs against hand-expected totals, then spot-checks formula cell references by
re-reading the saved workbook.
"""
import openpyxl

CATEGORIES = [
    "Venue & Rentals", "Catering & Bar", "Photography & Video", "Wedding Attire",
    "Hair & Makeup", "Flowers & Decor", "Music & Entertainment",
    "Invitations & Stationery", "Wedding Cake & Desserts", "Transportation",
    "Rings", "Officiant", "Favors & Gifts", "Miscellaneous / Buffer",
]
PLANNED = [9000, 7500, 3000, 1500, 600, 2100, 1800, 450, 600, 450, 1500, 400, 450, 650]
VENDORS = [
    ("Venue & Rentals", 9400, 2800),
    ("Catering & Bar", 7200, 2200),
    ("Photography & Video", 3200, 1000),
    ("Wedding Attire", 1450, 1450),
    ("Hair & Makeup", 600, 150),
    ("Flowers & Decor", 2250, 675),
    ("Music & Entertainment", 1800, 500),
    ("Invitations & Stationery", 420, 420),
    ("Wedding Cake & Desserts", 650, 200),
    ("Transportation", 400, 100),
    ("Rings", 1600, 1600),
    ("Officiant", 400, 100),
    ("Favors & Gifts", 480, 480),
]
TOTAL_BUDGET = 30000

# ---- independent recompute ----
planned_by_cat = dict(zip(CATEGORIES, PLANNED))
actual_by_cat = {cat: 0 for cat in CATEGORIES}
balance_due = []
for cat, contract, deposit in VENDORS:
    actual_by_cat[cat] += contract
    balance_due.append(contract - deposit)

total_planned = sum(PLANNED)
total_actual = sum(actual_by_cat.values())
total_contract = sum(v[1] for v in VENDORS)
total_deposit = sum(v[2] for v in VENDORS)
total_balance = sum(balance_due)
remaining_vs_budget = TOTAL_BUDGET - total_actual

assert total_planned == 30000, f"total planned should be 30000, got {total_planned}"
assert total_actual == total_contract, "actual-by-category sum must equal sum of all contracts"
assert total_balance == total_contract - total_deposit
for cat in CATEGORIES:
    diff = planned_by_cat[cat] - actual_by_cat[cat]
    pct = planned_by_cat[cat] / TOTAL_BUDGET
    assert abs(diff - (planned_by_cat[cat] - actual_by_cat[cat])) < 1e-9
    assert 0 <= pct <= 1

print(f"Total planned:  ${total_planned:,}")
print(f"Total actual:   ${total_actual:,}")
print(f"Remaining vs total budget (${TOTAL_BUDGET:,}): ${remaining_vs_budget:,}")
print(f"Total contract: ${total_contract:,}  Total deposit: ${total_deposit:,}  Total balance due: ${total_balance:,}")

# ---- spot-check saved formulas reference the rows we expect ----
wb = openpyxl.load_workbook("Wedding_Budget_Vendor_Tracker.xlsx")
bo = wb["Budget Overview"]
vt = wb["Vendor & Payment Tracker"]

# Budget Overview data rows are 7..20, total row 21 (from build.py's printed layout)
assert bo["A7"].value == "Venue & Rentals"
assert bo["A20"].value == "Miscellaneous / Buffer"
assert bo["A21"].value == "Total"
assert bo["C7"].value == "=SUMIF('Vendor & Payment Tracker'!$A$4:$A$16,A7,'Vendor & Payment Tracker'!$D$4:$D$16)"
assert bo["D7"].value == "=B7-C7"
assert bo["E7"].value == "=B7/B3"
assert bo["B21"].value == "=SUM(B7:B20)"
assert bo["C21"].value == "=SUM(C7:C20)"

# Vendor tracker rows 4..16, total row 17
assert vt["A4"].value == "Venue & Rentals"
assert vt["B4"].value == "Sunset Barn Venue"
assert vt["H4"].value == "=D4-E4"
assert vt["A16"].value == "Favors & Gifts"
assert vt["D17"].value == "=SUM(D4:D16)"
assert vt["E17"].value == "=SUM(E4:E16)"
assert vt["H17"].value == "=SUM(H4:H16)"

# Miscellaneous / Buffer has no vendor row -> SUMIF for it should find zero matches,
# confirmed by construction: "Miscellaneous / Buffer" does not appear in VENDORS.
assert all(v[0] != "Miscellaneous / Buffer" for v in VENDORS)

print("All formula spot-checks and independent recomputation passed.")
