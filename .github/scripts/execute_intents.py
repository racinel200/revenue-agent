#!/usr/bin/env python3
"""Relay executor — Lemon Squeezy TEST MODE ONLY.

Runs strictly AFTER .github/scripts/validate_and_echo.py and acts only on
publish-results/*.json files whose status is "validated_dry_run". It never
reads publish-requests/ directly — the validator is the only entry point.

Hard gates, all fail-closed (non-zero exit / no API call):
  1. RELAY_MODE must be exactly "execute", else the script is a no-op.
  2. LEMONSQUEEZY_API_KEY and LEMONSQUEEZY_STORE_ID must be present in env.
  3. assert_test_mode() runs before anything else touches the commerce API:
     GET /v1/users/me must succeed AND report test_mode=true, otherwise the
     whole run aborts. A live-mode key can never execute anything here.
  4. Only the product_create endpoint (POST /v1/products) is armed. Every
     other intent type — even ones the validator whitelists — is skipped.
  5. Price bounds ($5-$49), the type whitelist, the forbidden-key rule, and
     the daily product_create rate cap are re-enforced here independently;
     the validator's verdict is not trusted on its own.

The API key is never logged: it is read once, passed only into request
headers, and every message this script prints is passed through redact()
as a belt-and-braces measure.
"""
import glob
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

API_BASE = "https://api.lemonsqueezy.com"
RESULTS_DIR = "publish-results"

# Independent re-statement of the validator's rules — deliberately NOT
# imported from validate_and_echo.py, so a change there cannot silently
# widen what this script will execute.
WHITELIST_TYPES = {"product_create", "price_update", "payment_link_create", "listing_update"}
ENABLED_TYPES = {"product_create"}  # the ONLY armed endpoint
PRICE_MIN, PRICE_MAX = 5, 49
RATE_CAP_PRODUCT_CREATE_PER_DAY = 3
FORBIDDEN_KEYS = {"api_key", "apikey", "secret", "token", "credential", "password"}

_API_KEY = None  # set once in main(); used only by _redact and request headers


def _redact(text):
    text = str(text)
    if _API_KEY:
        text = text.replace(_API_KEY, "[REDACTED]")
    return text


def _say(msg):
    print(_redact(msg))


def _abort(msg):
    _say(f"EXECUTOR ABORT: {msg}")
    sys.exit(1)


def _api_request(method, path, payload=None):
    """Returns (http_status, parsed_json_or_None). Never raises; never logs headers."""
    data = None
    headers = {
        "Accept": "application/vnd.api+json",
        "Authorization": f"Bearer {_API_KEY}",
    }
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/vnd.api+json"
    req = urllib.request.Request(API_BASE + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode("utf-8"))
        except Exception:
            body = None
        return e.code, body
    except Exception as e:
        _abort(f"network error calling {method} {path}: {e}")


def assert_test_mode():
    """Abort the entire run unless the API key is a TEST MODE key.

    Lemon Squeezy responses carry meta.test_mode reflecting the key's mode.
    Anything other than an explicit True — live key, missing field, auth
    failure, unexpected response shape — aborts. Fail closed.
    """
    status, body = _api_request("GET", "/v1/users/me")
    if status != 200 or not isinstance(body, dict):
        _abort(f"could not verify account via GET /v1/users/me (HTTP {status}); refusing to execute anything")
    test_mode = body.get("meta", {}).get("test_mode")
    if test_mode is not True:
        _abort(
            f"account did not report test_mode=true (got {test_mode!r}); "
            "this executor only ever runs against a TEST MODE key"
        )
    _say("assert_test_mode: OK — API key confirmed as Lemon Squeezy TEST MODE")


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


def count_today_executed_product_creates():
    count = 0
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for path in glob.glob(os.path.join(RESULTS_DIR, "*.json")):
        try:
            with open(path) as f:
                r = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        if (
            r.get("intent_type") == "product_create"
            and r.get("status") == "executed_test_mode"
            and str(r.get("executed_at", "")).startswith(today)
        ):
            count += 1
    return count


def recheck_intent(intent):
    """Independent re-validation. Returns a list of errors; empty means OK to execute."""
    errors = []
    itype = intent.get("type")
    if itype not in WHITELIST_TYPES:
        errors.append(f"type {itype!r} is not in the endpoint whitelist")
    if intent.get("platform") != "lemonsqueezy":
        errors.append(f"platform {intent.get('platform')!r} is not 'lemonsqueezy'")
    if contains_forbidden_keys(intent):
        errors.append("intent contains a forbidden key — refusing to execute")
    product = intent.get("product")
    if not isinstance(product, dict):
        errors.append("missing or malformed 'product' object")
        return errors
    price = product.get("price_usd")
    if (
        not isinstance(price, (int, float))
        or isinstance(price, bool)
        or not (PRICE_MIN <= price <= PRICE_MAX)
    ):
        errors.append(f"price_usd {price!r} outside allowed bounds ${PRICE_MIN}-${PRICE_MAX}")
    if not product.get("name") or not isinstance(product.get("name"), str):
        errors.append("product.name is required and must be a non-empty string")
    return errors


def execute_product_create(intent, store_id):
    """POST /v1/products — the only armed endpoint. Returns (ok, detail)."""
    product = intent["product"]
    payload = {
        "data": {
            "type": "products",
            "attributes": {
                "name": product["name"],
                "description": product.get("description", ""),
                "price": int(round(product["price_usd"] * 100)),  # API takes cents
            },
            "relationships": {
                "store": {"data": {"type": "stores", "id": str(store_id)}}
            },
        }
    }
    status, body = _api_request("POST", "/v1/products", payload)
    if 200 <= status < 300 and isinstance(body, dict):
        product_id = body.get("data", {}).get("id")
        return True, {"http_status": status, "product_id": product_id}
    detail = None
    if isinstance(body, dict):
        detail = body.get("errors")
    return False, {"http_status": status, "errors": _redact(json.dumps(detail)) if detail else "no error body"}


def write_result(path, result):
    with open(path, "w") as f:
        json.dump(result, f, indent=2)
        f.write("\n")


def main():
    global _API_KEY

    if os.environ.get("RELAY_MODE") != "execute":
        _say("RELAY_MODE is not 'execute' — executor is a no-op")
        return

    _API_KEY = os.environ.get("LEMONSQUEEZY_API_KEY")
    store_id = os.environ.get("LEMONSQUEEZY_STORE_ID")
    if not _API_KEY:
        _abort("LEMONSQUEEZY_API_KEY is not set (RELAY_MODE=execute requires it)")
    if not store_id:
        _abort("LEMONSQUEEZY_STORE_ID is not set (RELAY_MODE=execute requires it)")

    # Gate 3: verify test mode BEFORE any other API interaction.
    assert_test_mode()

    executed, skipped, failed = [], [], []
    for path in sorted(glob.glob(os.path.join(RESULTS_DIR, "*.json"))):
        try:
            with open(path) as f:
                result = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        if result.get("status") != "validated_dry_run":
            continue  # executor acts ONLY on validator-approved dry runs

        intent_id = result.get("id", os.path.splitext(os.path.basename(path))[0])
        intent = result.get("payload_echo")
        if not isinstance(intent, dict):
            _say(f"{intent_id}: no payload_echo in result — skipping")
            skipped.append(intent_id)
            continue

        itype = intent.get("type")
        if itype not in ENABLED_TYPES:
            _say(f"{intent_id}: type {itype!r} is not armed for execution (only {sorted(ENABLED_TYPES)}) — skipping")
            skipped.append(intent_id)
            continue

        errors = recheck_intent(intent)
        if errors:
            result["status"] = "execution_rejected"
            result["execution_errors"] = [_redact(e) for e in errors]
            result["executed_at"] = datetime.now(timezone.utc).isoformat()
            write_result(path, result)
            failed.append(intent_id)
            _say(f"{intent_id}: failed independent re-validation — {errors}")
            continue

        if count_today_executed_product_creates() >= RATE_CAP_PRODUCT_CREATE_PER_DAY:
            _say(
                f"{intent_id}: daily execution rate cap "
                f"({RATE_CAP_PRODUCT_CREATE_PER_DAY} product_create/day) reached — leaving for a later run"
            )
            skipped.append(intent_id)
            continue

        ok, detail = execute_product_create(intent, store_id)
        result["executed_at"] = datetime.now(timezone.utc).isoformat()
        if ok:
            result["status"] = "executed_test_mode"
            result["execution"] = {
                "endpoint": "POST /v1/products",
                "test_mode": True,
                **detail,
            }
            executed.append(intent_id)
            _say(f"{intent_id}: created test-mode product (id={detail.get('product_id')})")
        else:
            # Mark failed so the next run does NOT retry and double-create.
            result["status"] = "execution_failed"
            result["execution"] = {"endpoint": "POST /v1/products", **detail}
            failed.append(intent_id)
            _say(f"{intent_id}: execution failed — {detail}")
        write_result(path, result)

    _say(f"executor summary: executed={executed} skipped={skipped} failed={failed}")


if __name__ == "__main__":
    main()
