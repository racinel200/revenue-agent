# Morning Queue — human checkpoints
Tasks the agent needs you for: accounts, payments, spending, signups.

## Quick question (iteration 4 — please answer, even briefly)
Four iterations, two finished products, zero listings live — because that one step needs your
hands (account/ToS/identity), not the agent's. Nothing else is blocking. Which is it?
- **(a) Time** — just haven't gotten to the ~10 minutes yet. No action needed, will do when you can.
- **(b) Friction** — the signup/upload steps feel like more than 10 min. Say what's hard and the
  agent will cut it down further.
- **(c) Doubt about the strategy** — you're not sold spreadsheet templates on Payhip/Gumroad is
  worth pursuing. Say so and the agent will pivot to a different item on the strategy menu
  instead of building a 3rd unpublished product.
- **(d) Something else** — just say what.

Any answer (even "(a)") is useful — it tells the agent whether to keep waiting quietly, cut
friction further, or change strategy. No answer is also fine; the agent will keep the products
ready and stop spending further iterations on this specific question after this one.

## Single fastest path (do this, ignore everything else below)
1. Go to **https://payhip.com**, sign up (~5 min, no review queue, 5% fee).
2. "New product" → upload `products/airbnb-roi-calculator/Airbnb_STR_ROI_Calculator.xlsx` →
   paste title/description/price/tags from `products/airbnb-roi-calculator/listing-copy.md` → publish.
3. Repeat for `products/wedding-budget-planner/Wedding_Budget_Vendor_Tracker.xlsx` using
   `products/wedding-budget-planner/listing-copy.md`.
4. Tell the agent the two listing URLs next time it runs (or just leave a note in this file) —
   it'll record them and treat any sale as pending until you confirm the payout actually landed.

Total hands-on time: **~10 minutes** for both listings combined.

---

**Status as of iteration 3 (2026-07-20):** neither product is published yet, 3 iterations
running with zero action on this checkpoint. Per the agent's own protocol this is *not* being
treated as a failed strategy (neither product has actually been market-tested — there's still
no live listing to get a signal from), but it did stop and re-check the ask rather than keep
building inventory nobody can buy yet. See "Fastest path" below — if Gumroad's signup was the
friction, this run found a faster/cheaper alternative. If something else is blocking (time,
priorities, wrong strategy entirely), just say so next time the agent runs.

## Fastest path (recommended): Payhip instead of Gumroad
Quick research this run found Payhip signs up in ~5 minutes with no review queue (vs Gumroad's
~10 min) and charges 5% per sale on its free plan vs Gumroad's 10% — strictly faster and
cheaper for this use case. (Lemon Squeezy was also considered and ruled out: its account
verification can reportedly take weeks.) Steps below are written for Gumroad since that's what
was originally queued, but the same two files/copy work identically on Payhip
(https://payhip.com) — sign up, "New product" → upload the .xlsx, paste the same title/
description/price/tags from each `listing-copy.md`, publish. Whichever platform you pick, only
do it once — no need to list on both.

## 1. Publish the first product listing (Gumroad — original recommendation, still fine)

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
