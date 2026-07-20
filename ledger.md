# Revenue Agent Ledger

Ledger: $0 verified | $0 pending | $0 spent | Net $0 of $100 | Strategy: micro digital product (2 listings now LIVE on Payhip); researching autonomous-publish pivot per new standing directive | Next action: human decides how to handle the confirmed network-policy block on every commerce API tested (see iteration 5) — allowlist one specific host, or accept the pivot isn't feasible in this sandbox and keep the (now lighter, batched) per-listing checkpoint model | Needs human: 1) confirm/paste actual payout amounts once Payhip reports a sale (sales are PENDING, not verified, until then), 2) a decision on the network-policy question below so research can target a channel that's actually reachable instead of guessing further

## State
- Status: iteration 5 complete
- Active strategy: **Micro digital product**, now live — spreadsheet templates sold on Payhip (human-owned account). A new standing directive (below) asks the agent to research a pivot to fully autonomous end-to-end publishing; that research is in progress, not yet actionable.
- Strategy graveyard: empty. The manual-checkpoint marketplace strategy is no longer untested — both listings are live for the first time (iteration 5), so the next real signal is whether either sells.
- Product #1: `products/airbnb-roi-calculator/Airbnb_STR_ROI_Calculator.xlsx` — Airbnb/STR ROI & cash flow calculator. **LIVE**: https://payhip.com/b/EIy4L — $19. Published by the human 2026-07-20. Sales: $0 verified (none reported yet).
- Product #2: `products/wedding-budget-planner/Wedding_Budget_Vendor_Tracker.xlsx` — wedding budget + vendor/payment tracker. **LIVE**: https://payhip.com/b/orgX0 — $15. Published by the human 2026-07-20. Sales: $0 verified (none reported yet).
- Repo: racinel200/revenue-agent, branch main, all work pushed as of this run.
- Standing directive (from human, via commit `ac7cc3e` on `main`, 2026-07-20 — see `morning-queue.md`): pivot toward the human doing ONE-TIME setup (account/ToS/payment/API key) after which the agent publishes new products end-to-end with no per-product human action. Requires: feasibility confirmed before any setup is requested, one consolidated minimal-scope setup ask, all existing protocol rules still bind, explicit credential-storage/risk statement, and a distribution/discoverability plan (a listing nobody sees earns $0).
- Feasibility finding (iteration 5, see History): **every commerce/payment API host tested from this sandbox is blocked at the network-proxy level** (403 policy denial, confirmed via `$HTTPS_PROXY/__agentproxy/status`) — Stripe, Gumroad, Payhip, Lemon Squeezy, Shopify, PayPal, Ko-fi. Non-commerce hosts in the same test (api.github.com, pypi.org) returned 200 normally, so this isn't a general outage — it looks like a deliberate category-level block on payment/commerce APIs specifically. Per this session's own proxy README: "do not retry or route around it — report the blocked host." No autonomous-publish channel has been confirmed reachable yet, so per the directive's own requirement 1, **no credential/setup request has been drafted** — asking the human to provision a key for a channel this sandbox can't even reach would be premature and possibly unusable.
- Resume state for next session: iteration 5 found the human's reply (commit `ac7cc3e`, genuine — authored under the real `racinel200` GitHub account, not conversational input) confirming both listings are live and delivering the standing directive above. Recorded live status for both products. Ran feasibility checks for 8 candidate commerce/publish APIs; all blocked by this session's egress policy; github.com/pypi.org unaffected, so the block looks targeted rather than a general network fault. Did not draft a consolidated setup request (nothing confirmed reachable to request it for). Next iteration should: (a) not re-test the same 8 hosts again — that's confirmed and stable, don't re-litigate like the LibreOffice issue; (b) instead consider channels that don't need a *blocked* commerce API at product-publish time — e.g. GitHub Pages (confirmed reachable, already used for this repo) serving a static product page, with checkout handled by a widget/link the human creates manually just *once per platform* rather than once per product — and assess whether that satisfies "no per-product human action" well enough to propose; (c) in parallel, since both listings are now actually live, also consider a no-human-required distribution/marketing pass (write social/forum posts respecting the no-spam rule) to give the live strategy an actual chance to produce a first sale before over-investing in the autonomous-publish pivot.

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

### 2026-07-20 — Iteration 5
- Read protocol + ledger. Checked `morning-queue.md` and `git log` for a reply since iteration 4:
  found one — commit `ac7cc3e`, authored under the GitHub account `racinel200` (not something
  written in this conversation or by a prior agent run), confirming this is genuine external
  human input and not something to fabricate consent from.
- Human reply content: both listings are now LIVE on Payhip (Airbnb calculator
  https://payhip.com/b/EIy4L $19; wedding tracker https://payhip.com/b/orgX0 $15). Updated both
  product entries in the ledger from "unpublished" to LIVE with URLs. Per protocol, sales remain
  $0 verified (not just $0 pending, since none has been reported yet) until the human confirms
  an actual payout.
- Human also left a standing directive: pivot toward one-time human setup (account/ToS/payment/
  API key) followed by fully autonomous, no-per-product-checkpoint publishing for future
  products, with feasibility-first, minimal-scope-credential, and distribution-plan requirements
  attached (full text preserved in `morning-queue.md`).
- Per requirement 1 of the directive ("verify... before asking the human to provision
  anything"), tested reachability from this sandbox to 8 candidate commerce/publish API hosts
  before proposing any of them: Stripe, Gumroad, Payhip, Lemon Squeezy, Shopify, PayPal, Ko-fi,
  itch.io. **All 8 were rejected at the network-proxy layer with HTTP 403** (policy denial,
  confirmed via the proxy status endpoint, not a transient failure). Control checks to
  api.github.com and pypi.org both returned 200 in the same test, so this is not a general
  outage — it reads as a deliberate, category-level block on payment/commerce APIs from this
  session's environment.
- Per the proxy's own documented guidance ("do not retry or route around it — report the
  blocked host") and per the directive's own requirement 1, did **not** draft a consolidated
  setup/credential request this iteration — every channel checked is currently unreachable from
  here, so asking the human to provision a key for any of them would be premature. This is a
  hard finding to record honestly, not a failure to hide: the standing directive may not be
  executable as specified inside this particular sandbox, at least not via any commerce API.
- Did not create any account, move money, or spend anything (spend budget remains $0, unchanged).
- Committed the ledger update. Also updating `morning-queue.md` to acknowledge the reply was
  read/integrated and to hand the human a concrete decision point instead of silently continuing
  to research against hosts already confirmed blocked.
- Flag for next run: don't re-test the same 8 hosts (settled, like the LibreOffice issue).
  Instead evaluate a git-based/static-hosting pattern (GitHub Pages, already confirmed reachable)
  where checkout is a widget the human sets up once per platform rather than once per product —
  and separately, since two listings are now actually live for the first time, consider spending
  a no-human-required iteration on discoverability/marketing for the existing listings so the
  tested strategy gets an actual chance to produce a first sale.

### 2026-07-20 — Iteration 4
- Read protocol + ledger. Checked `git log origin/main`, working tree, and `morning-queue.md`
  for any human reply since iteration 3 — none found. 4th straight iteration with zero action
  on the publish checkpoint (product #1: 4 iterations unpublished; product #2: 3).
- Per the flag iteration 3 left for itself, did not research another marketplace alternative
  and did not build a 3rd product — neither would test the strategy or reduce the actual
  blocker, and more unpublished inventory only compounds the existing backlog.
- Judged the highest-EV no-human-required action to be reducing friction on the *ask* itself,
  not the platform: `morning-queue.md` had grown into two long numbered sections plus a
  "fastest path" callout — a lot to read for someone who may just be short on time. Rewrote the
  top of the file into (a) a single multiple-choice question (time / friction / doubt about the
  strategy / other) answerable in one word, and (b) one consolidated 4-step "single fastest
  path" (Payhip, ~10 min total for both listings), with the prior longer Gumroad-first
  instructions kept below as reference/fallback, not deleted.
- Did not create any account, upload anything, or spend anything — same as every prior
  iteration, all still gated by Checkpoints (spend budget remains $0).
- Committed `morning-queue.md` and this ledger update as separate commits, pushed both to
  `main` immediately after each.
- Flag for next run: if iteration 5 still finds no reply, this is the 5th ask in a row with no
  response — stop re-asking in the same form. Either read the silence as an implicit "not now"
  and hold state quietly until the human initiates, or explicitly flag in the ledger that the
  checkpoint-gated bootstrap approach may not be the right operating mode for this human right
  now, rather than generating a 5th variant of the same request.

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
