# Morning Queue — human checkpoints

## HUMAN REPLY — 2026-07-20 (read first, then integrate into ledger)

Answer to your iteration-4 question: **(d) — the per-product checkpoint model is the blocker.**

Both existing products ARE now LIVE — the human published them this morning:
- Airbnb & STR ROI Calculator — https://payhip.com/b/EIy4L — $19 on Payhip
- Wedding Budget & Vendor Payment Tracker — https://payhip.com/b/orgX0 — $15 on Payhip

Record both in the ledger. Payment details are connected on the Payhip account. Per protocol,
treat any sale as PENDING until the human confirms the payout actually landed.

## STANDING DIRECTIVE (new, from the human)

Pivot strategy to this shape: the human performs ONE-TIME setup (account creation, ToS,
payment wiring, API key generation — anything touching identity or money), and after that
the agent can create AND publish new products end-to-end automatically, with no per-product
human action. The two Payhip listings stay live, but Payhip's manual upload flow does not
satisfy this requirement going forward.

Requirements for your proposal:
1. FEASIBILITY FIRST: verify from your own sandbox that you can actually reach and drive the
   publish mechanism (API, CLI, git-based deploy, etc.) before asking the human to provision
   anything. Dry-run it. Do not request setup for a channel you have not confirmed you can use.
2. ONE CONSOLIDATED SETUP REQUEST: exact account to create, exact key to generate with exact
   minimal scopes, exactly where to place it so future runs can use it. Least privilege,
   revocable — the human's ability to kill the key IS the off-switch and must stay real.
3. ALL PROTOCOL RULES STILL BIND: legitimacy constraints, honest product claims, no deception,
   ledger discipline, sales pending until human-verified payout.
4. CREDENTIAL HANDLING: state the storage mechanism explicitly and flag its risks in the
   ledger before the human provisions anything.
5. DISTRIBUTION COUNTS: an auto-published product nobody sees earns $0. Discoverability or
   marketing must be part of the strategy, not an afterthought.

Next runs: research candidate channels, verify sandbox feasibility, then write the single
consolidated setup request into this file. That request becomes the human's next checkpoint.
