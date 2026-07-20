# Revenue Agent Ledger

Ledger: $0 verified | $0 pending | $0 spent | Net $0 of $100 | Strategy: micro digital product (2 listings LIVE on Payhip); no-secret dry-run relay PROVEN end-to-end on GitHub Actions; content-marketing site built and pushed, awaiting one Pages toggle to go live | Next action: awaiting human on TWO independent items — (1) Lemon Squeezy API key + GitHub Actions secret (blocks autonomous publishing of future products), (2) a 1-click GitHub Pages toggle (blocks the new discoverability site from being reachable) — see morning-queue.md for exact copy-paste steps on both | Needs human: **yes, two items, neither is identity/money for item 2.** (1) File a Lemon Squeezy API key and add it as a GitHub Actions secret named `LEMONSQUEEZY_API_KEY` — that key cannot be scoped to products-only (no restricted-key feature exists), so the workflow's endpoint whitelist is the real enforcement layer and revoking the secret is the off-switch. (2) Settings → Pages → Deploy from branch → main /docs — no identity or money involved, the sandbox's GitHub API access is proxy-restricted from doing this itself.

## State
- Status: iteration 8 complete
- Active strategy: **Micro digital product**, live on Payhip (unchanged, $0 verified sales). In parallel, executing the human-approved pivot to an autonomous publish relay (GitHub Actions executes commerce API calls on the human's behalf; the agent's sandbox never holds a credential).
- Strategy graveyard: empty.
- Product #1: `products/airbnb-roi-calculator/Airbnb_STR_ROI_Calculator.xlsx` — **LIVE**: https://payhip.com/b/EIy4L — $19. Sales: $0 verified.
- Product #2: `products/wedding-budget-planner/Wedding_Budget_Vendor_Tracker.xlsx` — **LIVE**: https://payhip.com/b/orgX0 — $15. Sales: $0 verified.
- Repo: racinel200/revenue-agent, branch main, all work pushed as of this run.
- Standing directive (human, commit `ac7cc3e`) + approved architecture (human, commit `d57df25`, verified authored by the real `racinel200` GitHub account — see `morning-queue.md` for full text): EXECUTION RELAY via GitHub Actions. Agent commits `publish-requests/*.json` intents; a human-approved GitHub Actions workflow (holding the only credential, in Actions Secrets) validates against an endpoint whitelist (product/price/payment-link/listing only — no refund/payout/transfer/account/key-management) and executes. Sequencing required by the human: (1) channel research, (2) no-secret dry-run of the full relay loop, (3) only then a single consolidated setup request.
- **Iteration 6 — channel research (step 1 of the human's sequencing), DONE:**
  - **Gumroad: ruled out.** Product creation via API is not supported — the create-product endpoint returns 404; product creation is dashboard-only. Confirmed via an open GitHub issue (antiwork/gumroad#4019, filed 2026) requesting this as a future feature. File upload API exists but is useless without product creation.
  - **Lemon Squeezy: selected.** Full REST API for Products, Variants, and Checkouts (`POST /v1/checkouts`, variant/price control via `product_options.enabled_variants`). Digital files (up to 5GB per product) attach to variants and are delivered to buyers automatically post-purchase — no manual fulfillment step. Payouts are Lemon Squeezy's own merchant-of-record flow (bank wire or PayPal, twice monthly) — no separate Stripe Connect setup needed. This is currently the only candidate found with API support for all three required legs: product creation, digital delivery, and payout to the human's account.
  - **Safety-relevant finding, flag before setup:** searched and fetched Lemon Squeezy's public API docs for evidence of scoped/restricted API keys (e.g. a key limited to products/checkouts, excluding payout/refund/account endpoints). Found none — the docs describe API keys as live/test-mode credentials valid for a year, with no mention of granular scopes. **This means the "least-privilege" requirement in the standing directive cannot be satisfied at the key level** — a Lemon Squeezy API key, once issued, likely has full account access regardless of what the GitHub Actions workflow chooses to call. The endpoint whitelist + rate cap + logging in the approved architecture would be the *only* enforcement layer, not a backstop to key-level restriction. This doesn't block the plan (the workflow-level whitelist was always meant to be doing this work), but the human should know the credential itself is not narrowly scoped before approving the workflow file, since revocation (the stated off-switch) is doing more safety work than a scoped key would. Did not attempt to verify this claim by creating a Lemon Squeezy account or key — that's still a human checkpoint and out of scope for research.
  - Did not re-test the 8 commerce hosts blocked from the sandbox (settled in iteration 5, not relitigated) — moot anyway, since the relay design means the sandbox never calls these APIs directly.
- Resume state for next session: channel is picked (Lemon Squeezy). Per the human's step 2, next iteration should build the **no-secret dry-run skeleton**: a `publish-requests/` intent schema (JSON: product name, price, description, file ref), a `.github/workflows/` file that triggers on new files under `publish-requests/`, validates the intent against the whitelist/price-bounds/rate-cap rules, and — since no secret exists yet — echoes a dummy "would have called POST /v1/products with {...}" result back to a `publish-results/` file instead of calling the real API. Prove intent-in → validate → result-out completely before drafting any setup/credential request. Do not add a real Lemon Squeezy API call to the workflow until the human has provisioned and approved a secret (step 3) — the dry-run must stay secret-free by construction, not just by discipline, so an early/leaked workflow run can't accidentally hit a real endpoint.
- **Iteration 7 — no-secret dry-run relay, DONE (human's step 2 complete):**
  - Built `publish-requests/SCHEMA.md` (intent format: `id`/`type`/`platform`/`product`; whitelist = `product_create`/`price_update`/`payment_link_create`/`listing_update`; price bounds $5–$49; rate cap 3 `product_create`/UTC day; hard rejection of any field named `api_key`/`secret`/`token`/`credential`/`password` at any nesting depth).
  - Built `.github/scripts/validate_and_echo.py`: pure validation + echo, zero network calls, zero secret/env reads. Unit-tested locally first (good intent, out-of-bounds price, non-whitelisted type, smuggled `api_key` field, and a 4-in-a-day rate-cap trip) — all five cases behaved correctly before anything touched the real repo.
  - Built `.github/workflows/publish-relay.yml`: triggers on push to `publish-requests/**.json`, runs the validator, commits any new `publish-results/*.json` back using the default `GITHUB_TOKEN` (repo-scoped, auto-provided by Actions — not a commerce credential). The workflow file contains **no secret reference of any kind** — structurally incapable of a real API call, per the human's requirement.
  - **Proved the loop live, both paths, on actual GitHub Actions (not just locally):**
    - Positive: committed `publish-requests/dryrun-test-0001.json` (valid `product_create`, $19) → within 10s the relay committed `publish-results/dryrun-test-0001.json` with `status: "validated_dry_run"` and the correct `would_call: "lemonsqueezy: POST /v1/products"`, authored by the `revenue-agent-relay` bot identity, no human/secret involved.
    - Negative: committed `publish-requests/dryrun-test-0002-badprice.json` (`price_usd: 999`) → within 20s got back `status: "rejected"`, `reasons: ["price_usd 999 outside allowed bounds $5-$49"]`. Confirms the workflow enforces its own rules under real Actions execution, not just in the local unit test.
  - Per the human's step 3, filed the single consolidated setup request in `morning-queue.md`: exact account (Lemon Squeezy), exact key type (their one API-key type — no scoped variant exists, per iteration 6), exact secret name (`LEMONSQUEEZY_API_KEY`), and exact copy-paste steps to create the key and add the GitHub Actions secret. Did **not** create any account or key myself — checkpoint, human hands only.
  - Explicitly did not touch the workflow to add a real API call — even after the secret exists, wiring it in is a separate, human-reviewed change per the protocol ("changes to the workflow itself are a human checkpoint"), flagged as the next gated step in `morning-queue.md` rather than done silently.
  - Did not spend anything (spend budget remains $0). Did not create any marketplace/platform account.
- Resume state after iteration 7: **blocked on human** for the first time in this initiative — check `git log` / `morning-queue.md` for the human having added the `LEMONSQUEEZY_API_KEY` secret and confirmed here. If still no reply, do NOT re-ask in a new form (iteration 3/4's lesson) — instead spend the iteration on a no-human-required task: discoverability/marketing push for the two live Payhip listings (still $0 verified sales after 7 iterations — the tested strategy hasn't had a real distribution attempt yet), per the flag iteration 5 already left and never acted on. If the human *has* replied with the secret added: next iteration drafts the actual workflow diff that adds the real Lemon Squeezy API call (still gated on a human-reviewed PR/approval before it runs for real, per protocol) — do not have that diff auto-merge or auto-run against the live secret without a final explicit go-ahead recorded in `morning-queue.md`.
- **Iteration 8 — no-human-required discoverability push, DONE:**
  - Checked for a human reply since iteration 7 first: shallow-cloned `origin/main`, HEAD was still exactly `36f9e7a` (iteration 7's own last commit) — confirms no new commit landed, so no secret-added confirmation to integrate. Per iteration 7's own resume plan, did not re-ask about Lemon Squeezy in a new form; moved to the discoverability task instead.
  - Built `docs/index.html` (hub) + `docs/airbnb-str-roi-calculator/index.html` + `docs/wedding-budget-planner/index.html`: genuine plain-English explainers (cap rate / cash-on-cash / break-even-occupancy math for the STR guide; the "actual spent vs. planned, balance due, % of budget" argument for the wedding guide) each ending in a real, disclosed CTA linking to the matching live Payhip checkout (`https://payhip.com/b/EIy4L`, `https://payhip.com/b/orgX0`). Added `robots.txt` and `sitemap.xml`. No fabricated statistics, no fake reviews, no undisclosed affiliation claims — checked this against the legitimacy constraints before writing, since a content-marketing push is exactly the kind of thing that can slide into deceptive SEO spam if done carelessly. This is a GitHub Pages site, meant to be served from `/docs` on `main`.
  - Tried to enable GitHub Pages myself first rather than assuming it needs a human: called `GET https://api.github.com/repos/racinel200/revenue-agent/pages` directly — rejected by the sandbox's own proxy with "Access to this GitHub API path is not permitted through this proxy" (403). Confirms the sandbox's GitHub API access is deliberately scoped to the existing relay flow (reading `publish-results/*.json` via api.github.com) and does not extend to repo-admin actions like Pages config. This is not a Checkpoint under the protocol's definition (no identity, no money, no ToS, nothing irreversible — it's a single dashboard toggle) but it does require human hands given the sandbox's own restriction, so queued it in `morning-queue.md` as a clearly separate, lower-friction ask from the Lemon Squeezy one, so the human can act on either independently.
  - Did not touch the Lemon Squeezy relay work at all this iteration (workflow, validator, schema untouched) — that thread stays exactly where iteration 7 left it, waiting on its own separate checkpoint.
  - Did not create any account, spend anything, post to any external platform, or claim any affiliation with Airbnb/VRBO/any wedding platform (both guide pages explicitly disclaim affiliation in their footers). Spend budget remains $0.
  - Considered and rejected drafting Reddit/forum self-promo posts as an alternative: most of the relevant subreddits (r/AirBnBHosts, r/realestateinvesting, r/weddingplanning) restrict or ban vendor self-promotion outright, and posting itself would require the human's personal account/identity — a much higher-friction ask than a single Pages toggle, and riskier against the "no spam" legitimacy constraint if done carelessly. A genuine content site the human can decide whether to further promote (Pinterest, newsletters, etc.) felt like the safer first move; did not build those follow-on channels this iteration to keep the checkpoint list short.
- Resume state for next session: **two independent, unrelated blockers now** — check `git log` / `morning-queue.md` for progress on *either*: (a) the Lemon Squeezy secret (iteration 7's ask, unchanged), (b) the GitHub Pages toggle (iteration 8's ask, new). They don't depend on each other — the human could do one, both, or neither. If neither has moved: do not re-ask either in a new form a second time; instead look for a third genuinely independent no-human-required action (e.g., draft — but do not post — Pinterest pin copy for the wedding tracker, since Pinterest is a much stronger organic-discovery fit for that niche than Reddit and doesn't carry the same self-promo-ban risk, though posting it still needs the human's own account). If the Pages toggle *has* landed: verify the site is actually reachable at `https://racinel200.github.io/revenue-agent/` (read-only HTTP check, no account needed) before reporting it as live. If the Lemon Squeezy secret *has* landed: proceed exactly as iteration 7 specified — draft the workflow diff adding the real API call, gated on a separate explicit human go-ahead before it runs for real.

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

### 2026-07-20 — Iteration 8
- Read protocol + ledger. Checked `git log` for a human reply since iteration 7: HEAD was still
  exactly `36f9e7a` (iteration 7's own last commit) — no new commit, so still no confirmation of
  the Lemon Squeezy secret being added.
- Per iteration 7's own resume-state plan, did not re-ask about Lemon Squeezy in a new form.
  Spent the iteration on the no-human-required task it named: a discoverability/marketing push
  for the two live Payhip listings, which still had zero real distribution attempt after 7
  iterations.
- Built a small GitHub Pages content site under `docs/`: a hub page plus two genuine how-to
  guides (Airbnb/STR ROI math — cap rate, cash-on-cash, break-even occupancy, formulas shown;
  wedding budget/vendor-tracking principles — why a flat category list fails and what fixes it),
  each ending in a disclosed link to the corresponding live Payhip checkout. Added `robots.txt`
  and `sitemap.xml`. Checked the content against the legitimacy constraints before writing —
  no fabricated stats, no fake reviews, explicit non-affiliation disclaimers — since a
  marketing push is exactly where "no spam / no deception" is easiest to violate by accident.
- Tried enabling GitHub Pages myself before assuming it needed a human: a direct call to the
  repo's `/pages` GitHub API endpoint was rejected by the sandbox's own proxy (403, "not
  permitted through this proxy"). Confirmed the sandbox's GitHub API access is scoped to the
  existing relay read flow only, not repo-admin actions. Queued the one-time Pages toggle in
  `morning-queue.md` as a separate, lower-friction ask from the Lemon Squeezy one (no identity,
  no money, not a Checkpoint under the protocol's own definition — just gated by the sandbox's
  API restriction).
- Considered drafting Reddit/forum self-promo posts as an alternative distribution channel and
  rejected it: the relevant subreddits largely restrict/ban vendor self-promotion, and posting
  would require the human's own account/identity anyway — higher friction and more legitimacy
  risk than one Pages toggle. Did not build a Pinterest push either this iteration, to keep this
  round's ask list short; flagged as the next candidate if both current blockers stay unmoved.
- Did not touch the Lemon Squeezy relay work (schema/validator/workflow untouched this
  iteration). Did not create any account, spend anything, or post anything to any external
  platform. Spend budget remains $0.
- Committed 3 times this iteration (the three docs/ site files + robots/sitemap as one commit,
  the morning-queue.md update as a second, this ledger update as the third), pushing
  immediately after each.
- Flag for next run: see "Resume state for next session" above — two independent blockers now
  (Lemon Squeezy secret, Pages toggle), track them separately since the human may resolve either
  without the other.

### 2026-07-20 — Iteration 7
- Read protocol + ledger. `git log` showed no new human commit since iteration 6 (still at
  `f105ad5`) — nothing to integrate, proceeded on the resume-state plan as written.
- Built the full no-secret dry-run relay per the human's step 2: intent schema
  (`publish-requests/SCHEMA.md`), a pure-Python validator with zero network/secret access
  (`.github/scripts/validate_and_echo.py`), and a GitHub Actions workflow
  (`.github/workflows/publish-relay.yml`) that references no secret anywhere in its text.
- Unit-tested the validator locally first (good intent; over-bound price; non-whitelisted type;
  smuggled `api_key` field; 4th-in-a-day rate-cap trip) — all 5 cases correct — before letting
  anything run against the real repo.
- Pushed two real test intents and watched the live GitHub Actions relay handle both: a valid
  `product_create` came back `validated_dry_run` with the correct echoed endpoint in ~10s; a
  $999 `product_create` came back `rejected` with the price-bounds reason in ~20s. Both were
  committed back by the workflow itself (`revenue-agent-relay` identity via the default,
  repo-scoped `GITHUB_TOKEN`) — no human, no commerce credential, involved at any point.
- Per the human's step 3 (now unblocked since step 2 is proven), filed the single consolidated
  setup request in `morning-queue.md`: create a Lemon Squeezy account, generate its one API-key
  type (no scoped variant exists — flagged again), add it as a GitHub Actions secret named
  `LEMONSQUEEZY_API_KEY`. This is the first genuinely blocking human task this initiative has
  produced since the pivot.
- Did not touch the workflow to wire in a real API call (that remains a separate, human-reviewed
  change even after the secret exists, per protocol). Did not create any account, spend anything,
  or move money — spend budget remains $0.
- Committed 5 times this iteration (schema, validator, workflow, positive test intent, negative
  test intent), each pushed immediately; the relay's own 2 result commits came from GitHub
  Actions, not this sandbox. Committing this ledger + morning-queue update now as the final commit
  of the iteration.
- Flag for next run: see "Resume state for next session" above — branches on whether the human
  has added the secret yet.

### 2026-07-20 — Iteration 6
- Read protocol + ledger. Checked `git log` for a human reply since iteration 5: found commit
  `d57df25`, authored under the real `racinel200` GitHub account (not conversational input),
  delivering the human's decision on the iteration-5 question (pursue the autonomous-publish
  pivot, option (a)) and the approved architecture: an execution relay via GitHub Actions, so the
  sandbox's commerce-API network block (iteration 5) is now moot — the sandbox never calls those
  APIs, GitHub Actions does, using a credential the sandbox never holds.
- Per the human's required sequencing, did step 1: channel research. Compared Gumroad and Lemon
  Squeezy against the human's hard requirement (API support for product creation + digital
  delivery + payout to the human's account). Gumroad ruled out (no product-creation API, confirmed
  via open upstream GitHub issue). Lemon Squeezy selected (full API coverage for all three legs).
- Went a step further than "does the API exist" and checked whether Lemon Squeezy API keys can be
  scoped down (least-privilege, per the standing directive's explicit requirement). Public docs
  show no evidence of scoped keys — recorded as a flag for the human, not a blocker: it means the
  GitHub Actions workflow's own whitelist/rate-cap/logging is the sole enforcement layer, and
  secret revocation is doing more of the safety work than a narrowly-scoped key would have.
- Did not create any account, key, or workflow with real API calls; did not spend anything; did
  not file a setup/credential request (per the human's own sequencing, that's step 3, gated on
  step 2's dry-run first). Spend budget remains $0.
- Committed the ledger update. Also updating `morning-queue.md` — no new blocking task, but the
  API-key-scoping finding is logged there for the human to see before eventually approving a
  workflow file.
- Flag for next run: build the no-secret dry-run relay skeleton (intent JSON in → Actions
  workflow validates → dummy echo result committed back, read from the sandbox via
  api.github.com). Keep it structurally incapable of a real API call (no secret referenced in the
  workflow at all yet) rather than just relying on the workflow not doing so — that's a stronger
  guarantee for a system that will run unattended.

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
