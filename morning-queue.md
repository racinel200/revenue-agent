# Morning Queue — human checkpoints
Tasks the agent needs you for: accounts, payments, spending, signups.

**Status as of iteration 2 (2026-07-20):** neither product is published yet. Product #1 has now
been waiting 2 iterations with no listing URL or reply — if you're blocked or this feels like
too much friction, just say so next time the agent runs and it'll rethink the approach; the
point of this queue is to save you time, not create a backlog.

## 1. Publish the first product listing (Gumroad — recommended, fastest to set up)

**Why you, not the agent:** creating a marketplace account requires accepting a ToS and
verifying your identity — both are hard checkpoints the agent is not allowed to do itself.

**File to upload:** `products/airbnb-roi-calculator/Airbnb_STR_ROI_Calculator.xlsx`
(in the `revenue-agent` repo, already committed and pushed to `main`)

**Steps:**
1. Go to https://gumroad.com and sign up (or log in if you already have an account).
2. Click "New product" → choose "Digital product".
3. Upload `Airbnb_STR_ROI_Calculator.xlsx`.
4. Copy-paste the listing fields below (also saved in full at
   `products/airbnb-roi-calculator/listing-copy.md`):

   **Name:**
   ```
   Airbnb & Short-Term Rental ROI Calculator (Excel/Google Sheets)
   ```

   **Price:** `$19` (list at $27 and mark it on sale — see listing-copy.md for reasoning)

   **Description:** copy the entire "Full description" section from
   `products/airbnb-roi-calculator/listing-copy.md` — it's ready to paste as-is.

   **Tags:** `airbnb calculator, short term rental spreadsheet, real estate roi calculator,
   str analysis, rental property calculator, cash flow spreadsheet, airbnb investment, excel
   real estate, google sheets template, cap rate calculator`

5. Publish the listing.
6. Reply here (or just tell the agent next time it runs) with the live listing URL — the
   agent will record it in `ledger.md` and treat any future sale as **pending** until you
   confirm the payout actually landed in your account (per the protocol, the agent's own
   claim of a sale is worth $0 — only your confirmation against real payment records counts).

**Alternative:** Etsy works too and gets more organic traffic, but requires a shop setup
(business info, payment details) that takes longer. Etsy-specific tags are also in
`listing-copy.md` if you'd rather start there instead of or in addition to Gumroad.

**Time estimate:** ~10-15 minutes if you don't already have a Gumroad account, ~5 minutes if
you do.

---

## 2. Publish the second product listing (same marketplace account as #1)

**Why you, not the agent:** same reason as #1 — uploading to an account you own is a hard
checkpoint the agent doesn't do itself.

**File to upload:** `products/wedding-budget-planner/Wedding_Budget_Vendor_Tracker.xlsx`
(in the `revenue-agent` repo, already committed and pushed to `main`)

**Steps:**
1. In your Gumroad (or Etsy) account, click "New product" → "Digital product" again.
2. Upload `Wedding_Budget_Vendor_Tracker.xlsx`.
3. Copy-paste the listing fields below (also saved in full at
   `products/wedding-budget-planner/listing-copy.md`):

   **Name:**
   ```
   Wedding Budget & Vendor Payment Tracker (Excel/Google Sheets)
   ```

   **Price:** `$15` (list at $22 and mark it on sale — see listing-copy.md for reasoning)

   **Description:** copy the entire "Full description" section from
   `products/wedding-budget-planner/listing-copy.md` — it's ready to paste as-is.

   **Tags:** `wedding budget spreadsheet, wedding planner template, vendor payment tracker,
   wedding budget planner, excel wedding planner, google sheets wedding, wedding expense
   tracker, bride budget template, wedding planning spreadsheet, wedding finance tracker`

4. Publish the listing.
5. Reply here (or tell the agent next time it runs) with the live listing URL for **both**
   product #1 and product #2 — the agent will record them in `ledger.md` and treat any future
   sale as **pending** until you confirm the payout actually landed in your account.

**Time estimate:** ~5 minutes (you'll already have the Gumroad account from product #1).

---
(These are the only two blockers on the current strategy — both are the same "publish a
listing" action, just for two different files.)
