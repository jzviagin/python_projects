# WA Sender

Small desktop app: paste a phone number (any format), type the customer name and
street, and it opens WhatsApp Web with the templated message ready to send.

## How it sends

It opens `https://web.whatsapp.com/send?phone=972...&text=...` in your default
browser. If WhatsApp Web is logged in to your **business** account there, the chat
opens with the message filled in, and you press Enter to send. There's no API
and no token, and your private WhatsApp app isn't involved.

## Phone normalization

Any of these become `+972501234567`:
`050-123-4567`, `0501234567`, `501234567`, `(050) 123 4567`,
`+972 50-123-4567`, `+972-050-1234567`, `00972501234567`.
Landlines work too (`03-1234567` → `+97231234567`). A number with a `+` and a
different country code is left alone. The app warns you if the length looks wrong.

## Template

Edit the template in the app using `{name}` and `{street}`. It's saved to
`~/.wa_sender.json` when you send.

## Install as an app

**Mac:** run the script below. It builds `WA Sender.app` with the icon and copies
it to `/Applications`.

```bash
./build_mac.sh
```

You need a Python that includes Tk. The python.org installer has it. With
Homebrew, run `brew install python-tk` first.

**Windows:** double-click `build_windows.bat`. It installs to
`%LOCALAPPDATA%\Programs\WA Sender` and adds Start Menu and Desktop shortcuts.

**Run without building:**

```bash
python3 wa_sender_gui.py
```

## Other files

- `send_wa.py`: command-line sender for the official WhatsApp Cloud API
  (needs your number registered with the API). Not used by the app.
- `make_icon.py`: regenerates `assets/icon.*` (needs Pillow).
- `test_normalize.py`: tests for phone normalization (`python3 test_normalize.py`).
