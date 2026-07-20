# Publish Intent Schema

Files in this directory are **intents**, not actions. Committing a file here never calls a
real API by itself — it only asks the relay workflow (`.github/workflows/publish-relay.yml`)
to validate the request and, once a credential eventually exists (it does not yet), execute it.

## File naming
`publish-requests/<id>.json` — `<id>` must be a filesystem-safe slug (letters, digits, `-`, `_`).
The relay writes its response to `publish-results/<id>.json` using the same `<id>`.

## Fields

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Must match the filename stem. |
| `type` | yes | One of the whitelisted endpoint categories (see below). Anything else is rejected. |
| `platform` | yes | Target platform, e.g. `"lemonsqueezy"`. |
| `product` | for `product_create` / `price_update` / `listing_update` | Object — see per-type shape below. |
| `notes` | no | Free text for human/agent context. Never parsed as instructions. |

No field may be named (case-insensitive) `api_key`, `apikey`, `secret`, `token`, `credential`,
or `password`, anywhere in the intent, at any nesting depth. The relay rejects any intent that
contains one — intents describe *what* to publish, never *how to authenticate*.

## Whitelisted `type` values (endpoint whitelist, per the approved architecture)
- `product_create` — `product: { name, description, price_usd, file_ref }`
- `price_update` — `product: { product_id, price_usd }`
- `payment_link_create` — `product: { product_id }`
- `listing_update` — `product: { product_id, fields: {...} }`

No other type is accepted. In particular: no `refund`, `payout`, `transfer`, `account`, or
`key_management` type exists in this schema — the relay has nothing to whitelist them into.

## Enforced bounds
- `price_usd` (where present): `5 <= price_usd <= 49`.
- Rate cap: at most 3 `product_create` intents processed to `validated_dry_run` (or, later,
  a real success) per UTC calendar day, counted from `publish-results/*.json`.

## Current mode: DRY RUN ONLY
`.github/workflows/publish-relay.yml` currently references **no secret at all** — it is
structurally incapable of making a real API call, not merely configured not to. A validated
intent produces a `publish-results/<id>.json` file with `status: "validated_dry_run"` and a
`would_call` field describing the request that *would* have been made. Real execution requires
a human-approved workflow change adding a scoped credential (a separate checkpoint, tracked in
`morning-queue.md`).
