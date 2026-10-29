# wa_template_sender

Quick CLI to send an approved WhatsApp Business template via the Cloud API.
No dependencies beyond Python 3.

```bash
export WA_TOKEN=EAAG...            # system-user access token
export WA_PHONE_NUMBER_ID=1234567890
export WA_TEMPLATE_NAME=delivery_notice
export WA_TEMPLATE_LANG=en_US      # must match the template's language exactly (e.g. he, en_US)

python send_wa.py +972501234567 "Dana Cohen" "Herzl"
python send_wa.py +972501234567 "Dana Cohen" "Herzl" --dry-run   # print payload only
```

The template body should use `{{1}}` (customer name) and `{{2}}` (street name).
If your template uses named variables, pass `--named` (expects
`{{customer_name}}` and `{{street_name}}`).
