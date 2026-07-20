# Morning Queue — human checkpoints

## RESOLVED — Iteration 10 (2026-07-20): honest conclusion on autonomous publishing

You asked for research + an honest call on whether full autonomous product creation is
achievable anywhere. Answer: **no, not on any platform checked, without a much bigger new
build.**

- **Lemon Squeezy:** `/v1/checkouts` needs an existing `variant_id` — it customizes a checkout
  for a product that already exists, it can't originate one. Confirmed against the docs and
  against an open Lemon Squeezy feature request for this exact gap
  (lemonsqueezy.nolt.io/279 — "API to create and update products and variants"), still open.
  Matches the live 405 you already saw on `/v1/products`.
- **Payhip** (where both current listings already live): the public API only covers Coupons and
  License Keys. No product-creation endpoint exists at all — checked this first since it would
  have been the simplest possible fix (no new platform needed) if it existed.
- **Stripe:** the one exception — `POST /v1/products`, `/v1/prices`, and Payment Links genuinely
  do support full programmatic creation, this part works as advertised. But Stripe has no
  built-in digital-file delivery like Lemon Squeezy/Gumroad's automatic post-purchase fulfillment
  — you'd need a webhook receiver (public, always-on, listening for `checkout.session.completed`)
  plus a delivery step. That's a genuinely different, bigger build than the current GitHub
  Actions relay (which only reacts to repo commits, no public endpoint needed) — did not start
  building this without your go-ahead, flagging it below instead.

**No action required from you** — this doesn't change anything you've already set up. Two
optional things, no rush:

1. **Working model going forward:** hybrid — agent builds products + writes listing copy, you
   do the ~5-10 min dashboard publish step per new product. The test-mode Lemon Squeezy relay
   stays armed and useful for a narrower job: price updates / listing-metadata changes on
   products that already exist there (once you or the agent-flagged process creates one by hand).
   Say the word if you'd rather fully decommission the relay instead of keeping it for that
   narrower use — otherwise it stays as-is, no code changes made this iteration.
2. **Stripe + custom webhook fulfillment**, if you ever want true creation-API coverage: it's
   possible but is a new architecture (new infrastructure, new risk surface — a public endpoint
   the agent's side would need to keep running). Only worth starting if you explicitly want it;
   otherwise the hybrid model above is the standing plan.

Also still open, unchanged, no rush: the git-history purge question from iteration 9 (see below).

---

## MAJOR UPDATE — relay ARMED + first test fire done + critical API finding (2026-07-20)

Since your last iteration, the human + assistant completed the Lemon Squeezy setup you were
waiting on AND ran the first real test. Read all of this before planning — your ledger's
"awaiting Lemon Squeezy key" status is now STALE.

### What got done (you don't need to re-request any of it)
- Lemon Squeezy store created (ClearSheet Studio), **test-mode** API key generated.
- Two GitHub Actions secrets are set: `LEMONSQUEEZY_API_KEY` and `LEMONSQUEEZY_STORE_ID`.
- The relay was ARMED via a human-reviewed PR (#1, merged): `execute_intents.py` now runs
  after the validator, with a HARD test-mode guard (`assert_test_mode()` calls /v1/users/me
  and aborts unless test_mode=true). Endpoint whitelist, $5-$49 bounds, rate cap all intact.
- First test intent (`testfire-0001`, product_create) was committed and the workflow RAN
  SUCCESSFULLY end-to-end: validated -> test-mode confirmed -> executor attempted the call.

### THE CRITICAL FINDING — read this, it changes the strategy
The create call FAILED with **HTTP 405 Method Not Allowed**: `POST /v1/products` is NOT
supported — "Supported methods: GET, HEAD." **Lemon Squeezy's /products endpoint is
read-only. You cannot create products programmatically via that route.**

This invalidates the core assumption behind the autonomous-publish pivot (iteration 6 picked
Lemon Squeezy believing it had a product-creation API; it does not). The result file is at
`publish-results/testfire-0001.json` with the full 405 error.

### Your task next run: research the REAL API surface, then reassess honestly
Do NOT just retry a different endpoint blindly. Investigate and write findings to the ledger:
1. Does Lemon Squeezy's API support creating anything sellable programmatically? Check
   `POST /v1/checkouts` — but note checkouts typically require a product/variant that ALREADY
   EXISTS in the dashboard (i.e. created by hand). If so, autonomous end-to-end creation is
   NOT achievable here; a human dashboard step remains mandatory.
2. If Lemon Squeezy can't do autonomous product creation, evaluate whether ANY compliant
   platform lets a script create sellable products without a human (be skeptical — the pattern
   across every platform tried, incl. the payment-API proxy blocks since iteration 5, is that
   money-handling platforms deliberately require a human to create the things that take money).
3. Reach an HONEST conclusion and state it plainly, even if it's "fully autonomous publishing
   is not achievable on a compliant platform; the working model is hybrid — agent builds
   products + drafts listings, human does the ~10-min publish." That is a valid, useful result,
   not a failure. Do not manufacture a workaround that depends on deception or ToS violation.

### Context the human wants you to hold
- The relay ARCHITECTURE is proven and safe (test-mode guard works, no money touched). If a
  usable create/checkout endpoint exists, the relay is ready. The blocker is the PLATFORM API,
  not your pipeline.
- Going live (swapping to a live key) is explicitly OFF THE TABLE until (a) a working create
  path is proven in test mode, and (b) the human deliberately approves it. Do not request a
  live key next run.
- Both Payhip listings remain LIVE ($0 verified sales so far). Distribution (the Pages site,
  guide SEO) is still real, autonomous work you can do regardless of how the API question
  resolves — an unseen product earns $0.

### Still-open, low-urgency (unchanged): git-history purge of old .xlsx blobs
The human has NOT decided on the destructive history-rewrite. Default is leave-as-is. Do not
force-push history unless the human explicitly says go.

---
(Older resolved/superseded notes below this line are historical.)

## ACTION NEEDED — Iteration 9 (2026-07-20): optional, low-urgency — purge product files from git history?

Fixed the free-download issue from the note below: removed both compiled `.xlsx` files from the
current tree (commit `9e30ea6`). They're no longer visible in the repo's file browser or linked
from anywhere. Source (`build.py`) and a `NOTE.md` explaining the change + Payhip links stay in
each product folder.

**Residual risk, not fixed:** the files are still reachable via old commits (`f1623f0` and
after) — anyone who digs into git history or already has the raw-file URL from before today can
still get them free. Fully purging requires rewriting git history and force-pushing `main`. This
agent will not do that unilaterally — it's destructive/irreversible in a way that's outside the
"execute directly" scope, and could disrupt anything else depending on current history (forks,
local clones, open PRs). **Your call, no rush:**
- Leave as-is (low-traffic repo, unlikely anyone finds the old commits) — do nothing.
- Or ask this agent to do the history rewrite next iteration (`git filter-repo` + force-push) if
  you want the free copies fully gone. Say so here or in a commit and the next run will act on it.

Not re-queuing the Pages toggle question — see below, that part is done.

## RESOLVED — GitHub Pages is LIVE (human completed 2026-07-20)

The iteration-8 Pages toggle is DONE. The human made the repo public (free path — declined the
paid Enterprise trial GitHub was pushing) and enabled Pages from main /docs. The site should be
building/live at: **https://racinel200.github.io/revenue-agent/**

Note: this agent's sandbox cannot verify that URL is actually reachable — `racinel200.github.io`
is blocked at the sandbox's network-policy layer (403 at the proxy, same category as the
commerce-API hosts blocked since iteration 5), not something retrying fixes. If you have a
minute, a real browser check of that URL would confirm it's actually serving.

Implications for you:
- The two how-to guides now have a real public URL (pending the check above). Your
  content-marketing distribution path exists.
- Do NOT re-queue the Pages toggle — it's done.
- Next distribution steps this agent can do autonomously: improve the guides' SEO (titles, meta
  descriptions, headings), expand them with genuinely useful content, ensure each has a clear
  CTA to the Payhip checkout, and keep sitemap.xml current. All of this is commit-only, no human needed.

Still OPEN (unchanged): the Lemon Squeezy API key + Actions secret for autonomous publishing of
FUTURE products (iteration 7 request below). That one is real identity/money and remains the
human's decision — no rush, and the human should read the workflow file before provisioning.

## ACTION NEEDED — Iteration 7 (2026-07-20): the consolidated setup request

The no-secret dry-run relay is built and **proven end-to-end on real GitHub Actions** — both the
success path and the rejection path (bad price → correctly rejected). This is the one-time setup
your step 3 asked for. Nothing below moves money or publishes anything by itself.

**What to do (~5 minutes):**

1. Go to https://lemonsqueezy.com and create a store account (this is identity/ToS — has to be
   you, not the agent).
2. In the Lemon Squeezy dashboard: **Settings → API**, generate an API key.
   - Note: Lemon Squeezy has no scoped/restricted key option (flagged in iteration 6) — this key
     will have full account access. The endpoint whitelist enforced in
     `.github/workflows/publish-relay.yml` (product/price/payment-link/listing only — no refund,
     payout, transfer, account, or key-management calls) is the real safety layer, not the key
     itself. Revoking this key is your off-switch and it will fully halt publishing.
3. In this repo on GitHub: **Settings → Secrets and variables → Actions → New repository
   secret**.
   - Name: `LEMONSQUEEZY_API_KEY` (exact — the future workflow change will look for this name)
   - Value: the API key from step 2
4. Reply here (or just leave the secret added — the next run checks for it) to confirm it's done.

**What happens after that:** adding the secret does *not* immediately enable real publishing.
Per the standing directive, changing the workflow itself to actually call the Lemon Squeezy API
is a separate step this agent will draft as a reviewable diff — flagged here, not silently
merged — for your one-time approval before it ever runs for real. So this step 3 setup and the
"go live" approval are two separate checkpoints, not one.

## FYI — Iteration 6 update (2026-07-20), no action required yet

Channel picked: **Lemon Squeezy** (Gumroad has no product-creation API — dashboard-only,
confirmed via an open upstream issue). Next iteration builds the no-secret dry-run relay
skeleton per your step 2 — still nothing for you to do yet.

**One thing worth reading before you eventually approve the workflow file:** Lemon Squeezy's
public docs show no evidence of scoped/restricted API keys — a key looks like it's full-account
access, not limited to products/checkouts. That means the "least-privilege" protection you asked
for will live entirely in the GitHub Actions workflow's own endpoint whitelist + rate cap +
logging, not in the credential itself. Revoking the secret (your stated off-switch) is doing more
of the safety work than a narrowly-scoped key would have. Not a blocker — just flagging it now so
it's not a surprise when the workflow file lands for your one-time approval.

## HUMAN DECISION — 2026-07-20 (answers your iteration-5 question)

**Answer: (a) — pursue the autonomous-publish pivot.** For the record: the human's advisor
recommended (b); the human heard that case and chose (a). The human accepts the trade-off
that agent-authored listings will go live under the human's identity without pre-review,
mitigated by the constraints below.

**Approved architecture: EXECUTION RELAY via GitHub Actions.** Do not route around your
sandbox's network block — you don't need to. Your sandbox never touches a commerce API and
never sees a credential. Instead:

1. You author structured publish-intents as files (e.g. `publish-requests/*.json`) and
   commit them.
2. A GitHub Actions workflow — which runs on GitHub's infrastructure with unrestricted
   network, triggered by your commits — validates each intent and executes the API calls.
3. The API credential lives ONLY in GitHub Actions Secrets: never in the repo, never
   readable from your sandbox. You read results via api.github.com (confirmed reachable).

The workflow file is the constitution of this system and MUST enforce, deterministically:
- Endpoint whitelist: product / price / payment-link / listing creation and updates ONLY.
  No refund, payout, transfer, account, or key-management endpoints, ever.
- Price bounds: $5–$49 per product.
- Rate cap: max 3 new products per day.
- Full logging: every executed intent appears in the Actions log and as a result file
  committed back to the repo.
The human reviews and approves the workflow file once; after that, changes to the workflow
itself are a human checkpoint (never modify it silently — flag proposed changes in this file).

**Sequencing for your next iterations:**
1. CHANNEL RESEARCH: pick the platform. Hard requirements: real API support for creating
   products AND delivering the digital file to the buyer, payouts to the human's account.
   Verify API docs claims carefully.
2. DRY-RUN FIRST (your feasibility rule still binds): build the full relay skeleton with a
   NO-SECRET echo workflow — intent file in, workflow triggers, validated, dummy result
   committed back, you read it from your sandbox. Prove the whole loop before requesting
   anything.
3. THEN file the single consolidated setup request here: exact account, exact key type,
   exact minimal scopes, exact secret name. The human's one-time setup is: create restricted
   key + add one GitHub Actions secret. Revoking that secret is the off-switch; it must
   remain sufficient to halt all publishing.

Both Payhip listings stay live throughout. All prior protocol rules and the standing
directive below remain in force.

## STANDING DIRECTIVE (unchanged, from the human)

One-time human setup (identity/money), then autonomous end-to-end publishing. Feasibility
first; one consolidated setup request; least-privilege revocable credentials; legitimacy
constraints and ledger discipline always; distribution counts — an unseen product earns $0.
