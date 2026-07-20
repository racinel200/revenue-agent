#!/usr/bin/env python3
"""Relay validator — dry-run only, structurally no secret access.

Reads new files under publish-requests/, validates each against the endpoint
whitelist / price bounds / rate cap / forbidden-key rules described in
publish-requests/SCHEMA.md, and writes a result file under publish-results/.

This script never imports a secret, never reads an environment variable named
like a credential, and never makes an outbound network call. A validated
intent gets a "validated_dry_run" result describing what *would* be called —
nothing is actually published. Real execution is a future, separately
approved change.
"""
import glob
import json
import os
from datetime import datetime, timezone

REQUESTS_DIR = "publish-requests"
RESULTS_DIR = "publish-results"

WHITELIST_TYPES = {"product_create", "price_update", "payment_link_create", "listing_update"}
PRICE_MIN, PRICE_MAX = 5, 49
RATE_CAP_PRODUCT_CREATE_PER_DAY = 3
FORBIDDEN_KEYS = {"api_key", "apikey", "secret", "token", "credential", "password"}

ENDPOINT_MAP = {
    "product_create": "POST /v1/products",
    "price_update": "PATCH /v1/variants/{product_id}",
    "payment_link_create": "POST /v1/checkouts",
    "listing_update": "PATCH /v1/products/{product_id}",
}


def contains_forbidden_keys(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, str) and k.lower() in FORBIDDEN_KEYS:
                return True
            if contains_forbidden_keys(v):
                return True
        return False
    if isinstance(obj, list):
        return any(contains_forbidden_keys(x) for x in obj)
    return False


def today_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def count_today_product_creates():
    count = 0
    today = today_utc()
    for path in glob.glob(os.path.join(RESULTS_DIR, "*.json")):
        try:
            with open(path) as f:
                r = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        if (
            r.get("intent_type") == "product_create"
            and r.get("status") == "validated_dry_run"
            and str(r.get("processed_at", "")).startswith(today)
        ):
            count += 1
    return count


def validate(intent, intent_id):
    errors = []
    if intent.get("id") != intent_id:
        errors.append(f"'id' field ({intent.get('id')!r}) must match filename stem ({intent_id!r})")
    itype = intent.get("type")
    if itype not in WHITELIST_TYPES:
        errors.append(f"type {itype!r} is not in the endpoint whitelist {sorted(WHITELIST_TYPES)}")
    if contains_forbidden_keys(intent):
        errors.append("intent contains a forbidden key (api_key/secret/token/credential/password) — refusing to process")
    product = intent.get("product")
    price = product.get("price_usd") if isinstance(product, dict) else None
    if price is not None:
        if not isinstance(price, (int, float)) or isinstance(price, bool) or not (PRICE_MIN <= price <= PRICE_MAX):
            errors.append(f"price_usd {price!r} outside allowed bounds ${PRICE_MIN}-${PRICE_MAX}")
    if itype == "product_create" and not errors:
        if count_today_product_creates() >= RATE_CAP_PRODUCT_CREATE_PER_DAY:
            errors.append(f"rate cap exceeded: max {RATE_CAP_PRODUCT_CREATE_PER_DAY} product_create per UTC day")
    return errors


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    processed = []
    for path in sorted(glob.glob(os.path.join(REQUESTS_DIR, "*.json"))):
        intent_id = os.path.splitext(os.path.basename(path))[0]
        result_path = os.path.join(RESULTS_DIR, f"{intent_id}.json")
        if os.path.exists(result_path):
            continue  # already processed — relay is idempotent

        now = datetime.now(timezone.utc).isoformat()
        try:
            with open(path) as f:
                intent = json.load(f)
        except json.JSONDecodeError as e:
            result = {
                "id": intent_id,
                "status": "rejected",
                "reasons": [f"invalid JSON: {e}"],
                "processed_at": now,
            }
            with open(result_path, "w") as rf:
                json.dump(result, rf, indent=2)
                rf.write("\n")
            processed.append(intent_id)
            continue

        errors = validate(intent, intent_id)
        itype = intent.get("type")
        if errors:
            result = {
                "id": intent_id,
                "intent_type": itype,
                "status": "rejected",
                "reasons": errors,
                "processed_at": now,
            }
        else:
            result = {
                "id": intent_id,
                "intent_type": itype,
                "status": "validated_dry_run",
                "would_call": f"{intent.get('platform', '?')}: {ENDPOINT_MAP.get(itype)}",
                "payload_echo": intent,
                "note": "DRY RUN — this workflow references no credential; no real network call was made.",
                "processed_at": now,
            }
        with open(result_path, "w") as rf:
            json.dump(result, rf, indent=2)
            rf.write("\n")
        processed.append(intent_id)

    print(f"processed={processed}")


if __name__ == "__main__":
    main()
