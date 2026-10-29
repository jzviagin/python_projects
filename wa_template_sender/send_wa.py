#!/usr/bin/env python3
"""Send a WhatsApp Business template message via the WhatsApp Cloud API.

Usage:
    python send_wa.py <phone> "<customer name>" "<street name>"

Config (env vars):
    WA_TOKEN            - permanent/system-user access token
    WA_PHONE_NUMBER_ID  - the sender's Phone Number ID (not the phone number itself)
    WA_TEMPLATE_NAME    - approved template name
    WA_TEMPLATE_LANG    - template language code (default: en_US)
    WA_API_VERSION      - Graph API version (default: v21.0)

The template body is expected to have two variables: {{1}} = customer name,
{{2}} = street name. Pass --named to use named params {{customer_name}} and
{{street_name}} instead.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request


def env(name, default=None):
    value = os.environ.get(name, default)
    if value is None:
        sys.exit(f"Missing env var {name}")
    return value


def normalize_phone(phone):
    # Cloud API wants digits only, with country code, no '+' or leading zeros.
    digits = re.sub(r"\D", "", phone)
    if digits.startswith("00"):
        digits = digits[2:]
    return digits


def build_payload(phone, name, street, template, lang, named):
    if named:
        params = [
            {"type": "text", "parameter_name": "customer_name", "text": name},
            {"type": "text", "parameter_name": "street_name", "text": street},
        ]
    else:
        params = [{"type": "text", "text": name}, {"type": "text", "text": street}]
    return {
        "messaging_product": "whatsapp",
        "to": normalize_phone(phone),
        "type": "template",
        "template": {
            "name": template,
            "language": {"code": lang},
            "components": [{"type": "body", "parameters": params}],
        },
    }


def main():
    p = argparse.ArgumentParser(description="Send a WhatsApp template message")
    p.add_argument("phone", help="recipient phone with country code, e.g. +972501234567")
    p.add_argument("name", help="customer name")
    p.add_argument("street", help="street name")
    p.add_argument("--template", help="override WA_TEMPLATE_NAME")
    p.add_argument("--lang", help="override WA_TEMPLATE_LANG")
    p.add_argument("--named", action="store_true", help="use named template params")
    p.add_argument("--dry-run", action="store_true", help="print payload, don't send")
    args = p.parse_args()

    template = args.template or env("WA_TEMPLATE_NAME")
    lang = args.lang or env("WA_TEMPLATE_LANG", "en_US")
    payload = build_payload(args.phone, args.name, args.street, template, lang, args.named)

    if args.dry_run:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    url = "https://graph.facebook.com/{}/{}/messages".format(
        env("WA_API_VERSION", "v21.0"), env("WA_PHONE_NUMBER_ID")
    )
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {env('WA_TOKEN')}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            print(json.dumps(json.load(resp), indent=2))
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
