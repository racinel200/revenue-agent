# Revenue Agent Ledger

Ledger: $0 verified | $0 pending | $0 spent | Net $0 of $100 | Strategy: micro digital product (Airbnb/STR ROI calculator) | Next action: human publishes listing on Gumroad or Etsy (see morning-queue.md), then agent starts product #2 while waiting on sales | Needs human: create/use marketplace account, upload file, publish listing — see morning-queue.md for exact steps

## State
- Status: iteration 1 complete
- Active strategy: **Micro digital product** — spreadsheet templates sold on an existing marketplace (menu item #1). Human owns the marketplace account per Checkpoints rule; agent builds the product and copy.
- Strategy graveyard: empty (no strategy has failed 3 iterations yet)
- Product #1: `products/airbnb-roi-calculator/Airbnb_STR_ROI_Calculator.xlsx` — Airbnb/short-term-rental ROI & cash flow calculator. Built, committed, pushed. NOT yet listed anywhere (blocked on human — see Checkpoints).
- Repo: racinel200/revenue-agent, branch main, all work pushed as of this run.

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
