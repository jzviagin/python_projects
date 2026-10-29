#!/usr/bin/env python3
"""Tiny GUI: fill phone / customer name / street, open the templated message
in WhatsApp Web (your business account) ready to send.

No API, no tokens: it opens https://web.whatsapp.com/send?phone=...&text=...
in your default browser, where WA Web is already logged in. You press Enter
in WhatsApp to actually send.
"""
import json
import re
import tkinter as tk
import urllib.parse
import webbrowser
from pathlib import Path
from tkinter import messagebox

CONFIG_PATH = Path.home() / ".wa_sender.json"
DEFAULT_TEMPLATE = "שלום {name}, הטכנאי שלנו בדרך אליך לרחוב {street}."


def normalize_phone(raw):
    """Turn any pasted Israeli number into +972XXXXXXXXX.

    Handles 050-123-4567, (050) 1234567, 0501234567, 501234567,
    +972 50-123-4567, 972-0501234567, 00972501234567, stray spaces,
    dashes, dots and invisible RTL marks. Returns (number, warning).
    """
    digits = re.sub(r"\D", "", raw)
    if not digits:
        return "", "No digits found"
    if digits.startswith("00"):
        digits = digits[2:]
    if digits.startswith("972"):
        digits = digits[3:]
    elif raw.strip().startswith("+"):
        # Explicit foreign country code: leave it alone.
        return "+" + digits, "Not an Israeli number"
    digits = digits.lstrip("0")
    number = "+972" + digits
    if len(digits) not in (8, 9):
        return number, f"Unusual length ({len(digits)} digits after 972)"
    return number, ""


def load_config():
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_config(cfg):
    try:
        CONFIG_PATH.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        pass


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WA Sender")
        self.minsize(460, 420)
        self.cfg = load_config()

        pad = {"padx": 10, "pady": 4}
        frm = tk.Frame(self)
        frm.pack(fill="both", expand=True, padx=8, pady=8)
        frm.columnconfigure(1, weight=1)

        self.phone = tk.StringVar()
        self.name = tk.StringVar()
        self.street = tk.StringVar()

        tk.Label(frm, text="Phone").grid(row=0, column=0, sticky="w", **pad)
        phone_entry = tk.Entry(frm, textvariable=self.phone)
        phone_entry.grid(row=0, column=1, sticky="ew", **pad)
        self.phone_info = tk.Label(frm, text="", fg="gray")
        self.phone_info.grid(row=1, column=1, sticky="w", padx=10)

        tk.Label(frm, text="Customer name").grid(row=2, column=0, sticky="w", **pad)
        tk.Entry(frm, textvariable=self.name, justify="right").grid(row=2, column=1, sticky="ew", **pad)

        tk.Label(frm, text="Street").grid(row=3, column=0, sticky="w", **pad)
        tk.Entry(frm, textvariable=self.street, justify="right").grid(row=3, column=1, sticky="ew", **pad)

        tk.Label(frm, text="Template  ({name}, {street})").grid(row=4, column=0, columnspan=2, sticky="w", **pad)
        self.template = tk.Text(frm, height=5, wrap="word")
        self.template.tag_configure("rtl", justify="right")
        self.template.insert("1.0", self.cfg.get("template", DEFAULT_TEMPLATE), "rtl")
        self.template.grid(row=5, column=0, columnspan=2, sticky="nsew", **pad)

        tk.Label(frm, text="Preview").grid(row=6, column=0, columnspan=2, sticky="w", **pad)
        self.preview = tk.Label(frm, text="", justify="right", anchor="e", wraplength=420,
                                bg="#dcf8c6", fg="black", padx=8, pady=6)
        self.preview.grid(row=7, column=0, columnspan=2, sticky="ew", **pad)
        frm.rowconfigure(5, weight=1)

        btns = tk.Frame(frm)
        btns.grid(row=8, column=0, columnspan=2, sticky="e", pady=(8, 0))
        tk.Button(btns, text="Clear", command=self.clear).pack(side="left", padx=4)
        tk.Button(btns, text="Copy message", command=self.copy).pack(side="left", padx=4)
        tk.Button(btns, text="Open in WhatsApp Web", command=self.send, default="active").pack(side="left", padx=4)

        for var in (self.phone, self.name, self.street):
            var.trace_add("write", lambda *_: self.refresh())
        self.template.bind("<<Modified>>", self._template_changed)
        self.bind("<Return>", lambda e: None if e.widget is self.template else self.send())

        self.refresh()
        phone_entry.focus_set()

    def _template_changed(self, _event):
        self.template.edit_modified(False)
        self.template.tag_add("rtl", "1.0", "end")
        self.refresh()

    def message(self):
        tpl = self.template.get("1.0", "end-1c")
        return tpl.replace("{name}", self.name.get().strip()).replace("{street}", self.street.get().strip())

    def refresh(self):
        raw = self.phone.get()
        if raw.strip():
            number, warning = normalize_phone(raw)
            self.phone_info.config(text=f"→ {number}" + (f"   ⚠ {warning}" if warning else ""),
                                   fg="#b36b00" if warning else "#1a7f37")
        else:
            self.phone_info.config(text="")
        self.preview.config(text=self.message())

    def copy(self):
        self.clipboard_clear()
        self.clipboard_append(self.message())

    def clear(self):
        for var in (self.phone, self.name, self.street):
            var.set("")

    def send(self):
        number, warning = normalize_phone(self.phone.get())
        if not number:
            messagebox.showerror("WA Sender", "Enter a phone number")
            return
        if warning and not messagebox.askyesno("WA Sender", f"{number}\n{warning}\n\nOpen anyway?"):
            return
        self.cfg["template"] = self.template.get("1.0", "end-1c")
        save_config(self.cfg)
        url = "https://web.whatsapp.com/send?" + urllib.parse.urlencode(
            {"phone": number.lstrip("+"), "text": self.message()}, quote_via=urllib.parse.quote
        )
        webbrowser.open(url)


if __name__ == "__main__":
    App().mainloop()
