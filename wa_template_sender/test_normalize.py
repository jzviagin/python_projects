from wa_sender_gui import normalize_phone

CASES = {
    "050-123-4567": "+972501234567",
    "0501234567": "+972501234567",
    "501234567": "+972501234567",
    "(050) 123 4567": "+972501234567",
    "+972 50-123-4567": "+972501234567",
    "+972-050-1234567": "+972501234567",
    "972501234567": "+972501234567",
    "00972501234567": "+972501234567",
    "‏050.123.4567‎": "+972501234567",
    "03-1234567": "+97231234567",
}

for raw, want in CASES.items():
    got, warn = normalize_phone(raw)
    assert got == want and not warn, (raw, got, warn)
assert normalize_phone("+1 415 555 1234") == ("+14155551234", "Not an Israeli number")
assert normalize_phone("05012")[1]
print("ok")
