"""Entry point: `vp setup`, `vp check [--no-report]`."""
import sys


def main() -> int:
    # Windows terminals often default to a legacy code page that cannot print ✅/❌
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            pass
    args = sys.argv[1:]
    cmd = args[0] if args else "help"
    if cmd == "setup":
        from . import setup
        return setup.run()
    if cmd == "check":
        from . import check
        return check.run(report="--no-report" not in args)
    print("VithuPro helper\n  vp setup   save your WhatsApp number and access key\n  vp check   check your laptop is ready for the workshop")
    return 0


if __name__ == "__main__":
    sys.exit(main())
