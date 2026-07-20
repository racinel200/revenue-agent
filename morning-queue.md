# Morning Queue — human checkpoints

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
