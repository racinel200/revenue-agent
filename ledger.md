# Revenue Agent Ledger

Ledger: $0 verified | $0 pending | $0 spent | Net $0 of $100 | Strategy: micro digital product (spreadsheet templates) | Next action: human publishes both product listings (Payhip now recommended over Gumroad — faster/cheaper, see morning-queue.md); agent holds on product #3 until a listing is live | Needs human: pick a marketplace (Payhip recommended, ~5 min, no review queue) and publish both existing products — see morning-queue.md for exact steps

## State
- Status: iteration 3 complete
- Active strategy: **Micro digital product** — spreadsheet templates sold on an existing marketplace (menu item #1). Human owns the marketplace account per Checkpoints rule; agent builds the product and copy.
- Strategy graveyard: empty (no strategy has failed 3 iterations yet — and per the note below, the strategy still hasn't actually been tested, since no listing has ever gone live)
- Product #1: `products/airbnb-roi-calculator/Airbnb_STR_ROI_Calculator.xlsx` — Airbnb/short-term-rental ROI & cash flow calculator. Built, committed, pushed. NOT yet listed anywhere (blocked on human — see Checkpoints). Still unpublished after 3 iterations.
- Product #2: `products/wedding-budget-planner/Wedding_Budget_Vendor_Tracker.xlsx` — wedding budget overview (SUMIF category rollups) + vendor/deposit/balance-due payment tracker. Built, committed, pushed. NOT yet listed anywhere (blocked on human — see Checkpoints). Still unpublished after 2 iterations.
- Repo: racinel200/revenue-agent, branch main, all work pushed as of this run.
- Resume state for next session: checked for a reply (git log, repo state) — none found; both products remain unpublished with zero human action on the checkpoint for a 3rd straight iteration. Per the plan laid out in iteration 2, did NOT build product #3 and did NOT treat this as a failed/buried strategy (it's never had a live listing, so there's no market signal against it, only against the publish step being slow). Instead spent this iteration reducing the friction on the actual blocker: researched faster/cheaper alternatives to Gumroad and found Payhip (~5 min signup, no review queue, 5% fee vs Gumroad's 10%) — added as the recommended path in `morning-queue.md`, with Gumroad kept as a fine alternative. Next session: if still no reply, that's 4 iterations — worth directly asking the human (via ledger/queue note) whether the blocker is platform friction, time/priority, or the strategy itself, rather than researching yet another marketplace option unprompted.

## Known environment issue (read before next run)
LibreOffice (`soffice`) cannot load documents via the CLI in this sandbox when given a
**freshly-created** `-env:UserInstallation` profile — the process hangs indefinitely (tested
up to 190s, never resolves; `--convert-to` fails instantly with "source file could not be
loaded" instead of hanging). This breaks the xlsx skill's normal `recalc.py` verification step
for every future spreadsheet product built in this environment, not just this one.
- Workaround used this run: independently re-derived every formula's math in a standalone
  Python script using the same default input values, and cross-checked the break-even
  algebra by plugging the solved break-even occupancy back into the full model and confirming
  the resulting cash flow is ~0. This caught logic errors but NOT typos in cell references
  that Excel/Sheets would catch at open-time (e.g. a formula pointing at the wrong row).
- Do NOT burn another 30+ minutes re-litigating this in the next session — it is confirmed
  environment-level, not a fluke. If recalc.py needs to work again, that requires a fix
  outside this agent's reach (e.g. the runtime sandbox allowing whatever `soffice` needs to
  open files headlessly), not a retry-harder approach.
- Practical implication for future products: after building any spreadsheet, do the
  independent-Python-recompute cross-check (see `build.py` for the pattern — build the
  formulas with named row variables from Python, then separately hand-compute the same
  business logic and diff), and spot-check a handful of formula cell references by eye before
  shipping. It's not as strong as LibreOffice recalculation but it is the best available
  substitute here.

## History (append-only, newest first)

### 2026-07-20 — Iteration 3
- Read protocol + ledger. Checked repo state for any sign the human published product #1 or #2
  (git log, working tree) — no new commits, no listing URL, no reply anywhere. Confirmed: 3rd
  straight iteration with zero human action on the publish checkpoint.
- Per iteration 2's own resume-state plan, did not build product #3 — no evidence yet that the
  *strategy* (spreadsheet templates on a marketplace) is the problem, since neither product has
  ever actually gone live; building more inventory nobody can buy would just compound the
  blocker, not test it.
- Instead treated "the checkpoint itself might be the friction" as the highest-EV thing to
  investigate that needs no human hands: researched (WebSearch) faster/cheaper alternatives to
  Gumroad for a first-time seller. Findings: Payhip signs up in ~5 min with no review queue and
  takes 5% per sale (vs Gumroad's ~10 min signup and 10% fee); Lemon Squeezy was considered and
  ruled out — its account verification can reportedly take weeks, which would make the friction
  worse, not better.
- Updated `morning-queue.md` with a "Fastest path" callout recommending Payhip while leaving the
  original Gumroad instructions intact as a fallback (same files, same copy-paste listing copy
  work on either platform).
- Did not create any account, upload anything, or spend anything — same as prior iterations, all
  still gated by Checkpoints (spend budget remains $0).
- Committed morning-queue.md and this ledger update separately, pushed both to `main`.
- Flag for next run: if iteration 4 still finds no reply, stop unilaterally researching more
  marketplace options and instead directly ask the human (this ledger's top line / the queue)
  whether the real blocker is platform friction, time, or the strategy choice itself — 4 rounds
  of "here's an even easier way" without a response is a signal to ask, not to keep guessing.

### 2026-07-20 — Iteration 2
- Read protocol + ledger. Product #1 (Airbnb ROI calculator) was still unpublished — no
  listing URL, no human reply recorded. Per ledger's own stated next action and the protocol's
  "execute directly everything you can" rule, did not wait idle: started product #2 while
  product #1 remains queued for the human.
- Chose product #2 from the same low-friction "micro digital product" strategy (menu item #1)
  rather than switching strategies — product #1 has not actually been market-tested yet (it was
  never published), so there is no evidence against the strategy itself, only against the
  publishing checkpoint being slow. Switching strategies now would be premature; the protocol's
  3-failed-iteration graveyard rule applies to a *tested* strategy, and this one hasn't been
  tested.
- Picked **Wedding Budget & Vendor Payment Tracker** (spreadsheet): different niche from product
  #1 (broader, more emotionally urgent buyer intent per the iteration-1 market research), and
  deliberately simpler math than the ROI calculator (sums, subtraction, percentages — no
  algebraic break-even solve) to reduce formula-error risk given the recalculation limitation
  below.
- Built `Wedding_Budget_Vendor_Tracker.xlsx`: 3 tabs (Read Me, Budget Overview, Vendor & Payment
  Tracker). Budget Overview auto-rolls up Actual Spent per category via SUMIF against the vendor
  tab; Vendor tab computes Balance Due as Contract − Deposit. Pre-filled with a realistic
  14-category, 13-vendor, $30,000-budget example ($150 under budget).
- Hit the same LibreOffice sandbox issue as iteration 1 (documented below, confirmed
  environment-level — did not re-litigate it). Used the same workaround: independently
  recomputed every total in plain Python (`verify.py`) from the same source data as `build.py`,
  plus spot-checked formula cell references against the actual saved workbook layout. All checks
  passed (see `verify.py` output: total planned $30,000, total actual $29,850, remaining $150,
  balance-due total $18,175 — matches hand computation).
- Wrote full listing copy (`listing-copy.md`) following the same structure as product #1: title,
  description, price ($15 launch / $22 list — priced below product #1 since this is a household
  budgeting aid rather than an investment-underwriting tool), Gumroad + Etsy tags, cover-image
  brief, first-review-request message.
- Committed in 2 steps (product files + verify script, then listing copy) and pushed both to
  `main` immediately after each commit.
- Did NOT create any marketplace account, upload anything, or spend anything — same as
  iteration 1, all gated by Checkpoints. Updated `morning-queue.md` with the second listing's
  copy-paste instructions and a note that product #1 is now 2 iterations overdue on the queue.

### 2026-07-20 — Iteration 1
- Read protocol + ledger (ledger was empty/initialized, first-ever run).
- Researched Gumroad/Etsy digital-product trends for 2026 (WebSearch). Low-competition,
  premium-pricing niches: real estate/Airbnb ROI tools, fitness/health trackers, event
  budgeters. Chose Airbnb/STR ROI calculator: real utility, no deception risk, buyers with
  actual budget (property investors), fits a spreadsheet format I can build well.
- Built `Airbnb_STR_ROI_Calculator.xlsx`: 4 tabs (Read Me, Inputs, ROI Dashboard, Monthly Cash
  Flow). Formulas cover NOI, cap rate, cash-on-cash return, break-even occupancy (solved
  algebraically), and a 5-year projection. Tuned example default inputs so the demo shows a
  realistic, modestly positive deal (cap rate ~7%, CoC ~3.4%, +$258/mo cash flow) rather than
  a random/losing example.
- Hit the LibreOffice sandbox issue documented above; substituted independent Python
  cross-verification of the formula logic. Confirmed break-even formula is internally
  consistent (residual ~0 when solved occupancy is plugged back into the full model).
- Wrote full listing copy (`listing-copy.md`): title, description, price ($19 launch / $27
  list), tags for both Gumroad and Etsy, cover-image brief, first-review-request message.
- Committed in 2 steps (product file, then listing copy) and pushed both to `main`.
- Did NOT create any marketplace account, upload anything, or spend anything — all of that is
  queued for the human per the Checkpoints rule (spend budget is $0; account creation is
  gated). See `morning-queue.md`.
