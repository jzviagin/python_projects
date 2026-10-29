# WA Sender

A Chrome extension that adds a small panel inside your open WhatsApp Web app
window. Paste a phone number (any format), type the customer name and street,
and click **Open chat**. The chat opens in the same window and the message is
typed into the box. **Nothing is sent**: you review it and press Enter yourself.

## Install (one time)

1. Open `chrome://extensions` in Chrome.
2. Turn on **Developer mode** (top right).
3. Click **Load unpacked** and choose the `extension` folder.
4. Reload your WhatsApp window (Ctrl+R / Cmd+R). A green button appears at the
   bottom left.

It only runs on `web.whatsapp.com`, and the panel only shows up in the
installed WhatsApp app window, not in normal tabs. To show it in tabs too, set
`ONLY_IN_APP_WINDOW = false` at the top of `extension/content.js`.

## How it opens the chat

1. **In place (fast):** it clicks WhatsApp's *New chat*, searches the number,
   and clicks the result showing that number. No reload, same session.
2. **Fallback:** if that doesn't work (WhatsApp changed its layout, or the
   result shows a saved contact's name instead of the number), it reloads
   **the same window** with WhatsApp's own `send?phone=…&text=…` link. That
   takes a few seconds but keeps you logged in. WhatsApp fills in the message
   and still waits for you to send.

## Phone normalization

Any of these become `+972501234567`:
`050-123-4567`, `0501234567`, `501234567`, `(050) 123 4567`,
`+972 50-123-4567`, `+972-050-1234567`, `00972501234567`.
Landlines work too (`03-1234567` → `+97231234567`). A number with a `+` and a
different country code is left alone. The panel warns you if the length looks wrong.

## Template

Edit it in the panel with `{name}` and `{street}`. It's remembered between uses.

## Development

- Phone tests: `node extension/phone.test.js`
- Regenerate icons: `python3 make_icon.py` (needs Pillow)
- After editing the extension, click the reload arrow on its card in
  `chrome://extensions`, then reload the WhatsApp window.
