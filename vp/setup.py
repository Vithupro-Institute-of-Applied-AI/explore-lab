"""`vp setup`: asks for the student's WhatsApp number and VithuPro access key once and saves them in .env.
The key is never printed or sent anywhere except to the AI endpoint it belongs to."""
import getpass
import re

from . import config


def run() -> int:
    ws = config.workshop()
    env = config.read_env()
    print(f"\nVithuPro setup · {ws['workshop']['title']}\n")

    phone = env.get("VITHUPRO_PHONE", "")
    entered = input(f"Your WhatsApp number (the one you registered with){' [' + phone + ']' if phone else ''}: ").strip()
    if entered:
        digits = re.sub(r"\D", "", entered)
        phone = "91" + digits if len(digits) == 10 else digits
    if not re.fullmatch(r"\d{11,15}", phone or ""):
        print("  That doesn't look like a WhatsApp number with country code (e.g. 9198XXXXXXXX). Run `vp setup` again.")
        return 1

    has_key = bool(env.get("VITHUPRO_API_KEY"))
    key = getpass.getpass(f"VithuPro access key from WhatsApp{' (press Enter to keep the saved one)' if has_key else ''}: ").strip()
    values = {"VITHUPRO_PHONE": phone,
              "VITHUPRO_API_BASE": env.get("VITHUPRO_API_BASE") or ws["ai"]["base_url"],
              "VITHUPRO_MODEL": env.get("VITHUPRO_MODEL") or ws["ai"]["model"]}
    if key:
        values["VITHUPRO_API_KEY"] = key
    elif not has_key:
        print("  No key entered. You can add it later with `vp setup`; `vp check` will remind you.")
    config.write_env(values)
    print("\nSaved in .env (this file stays on your laptop and is never uploaded to GitHub).")
    print("Next: run  vp check\n")
    return 0
