"""`vp check`: verifies that the laptop is ready for the workshop and reports the result to VithuPro.

Standard library only. Sends: phone number, workshop, OS, and the pass/fail of each check (no files, code or keys).
Use `vp check --no-report` to skip sending."""
import importlib
import json
import platform
import shutil
import subprocess
import sys
import urllib.error
import urllib.request

from . import __version__, config

OK, WARN, FAIL = "ok", "warn", "fail"
ICON = {OK: "✅", WARN: "⚠️ ", FAIL: "❌"}
HELP = "https://vithuproai.com/setup#troubleshooting"


def sh(*cmd: str, timeout: int = 20) -> tuple[int, str]:
    exe = shutil.which(cmd[0])
    if not exe:
        return 127, ""
    try:
        p = subprocess.run([exe, *cmd[1:]], capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout + p.stderr).strip()
    except Exception as e:  # noqa: BLE001
        return 1, str(e)


def reach(url: str, headers: dict | None = None, timeout: int = 10) -> tuple[int, str]:
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers or {}), timeout=timeout) as r:
            return r.status, r.read(2000).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:  # noqa: BLE001
        return 0, str(e)


def run(report: bool = True) -> int:
    ws = config.workshop()
    env = config.read_env()
    chk = ws["check"]
    results: list[tuple[str, str, str]] = []   # (name, status, detail)
    add = lambda name, status, detail="": results.append((name, status, detail))

    # Python inside the project environment
    v = sys.version_info
    add("Python", OK if v >= (3, 11) else FAIL, f"{v.major}.{v.minor}.{v.micro}" + ("" if v >= (3, 11) else " (need 3.11+: re-run the installer)"))

    code, out = sh("uv", "--version")
    add("uv (package manager)", OK if code == 0 else WARN, out.split("\n")[0] if code == 0 else "not found (only needed to reinstall packages)")

    code, out = sh("git", "--version")
    add("Git", OK if code == 0 else FAIL, out if code == 0 else "not installed")
    if code == 0:
        name = sh("git", "config", "--global", "user.name")[1]
        email = sh("git", "config", "--global", "user.email")[1]
        add("Git identity", OK if name and email else WARN, f"{name} <{email}>" if name and email else 'set it: git config --global user.name "Your Name" and user.email')

    code, out = sh("code", "--version")
    if code == 0:
        add("VS Code", OK, out.split("\n")[0])
        exts = {e.lower().split("@")[0] for e in sh("code", "--list-extensions")[1].split()}
        missing = [e for e in chk["extensions_required"] if e.lower() not in exts]
        add("VS Code extensions", OK if not missing else FAIL, "Python + Jupyter installed" if not missing else "missing: " + ", ".join(missing))
        opt = [e for e in chk.get("extensions_optional", []) if e.lower() in exts]
        add("AI assistant in VS Code", OK if opt else WARN, "GitHub Copilot installed" if opt else "optional: install GitHub Copilot (free plan) in VS Code")
    else:
        add("VS Code", FAIL, "the `code` command was not found (install VS Code, then restart the terminal)")

    bad = []
    for pkg in chk["packages"]:
        try:
            importlib.import_module(pkg)
        except Exception:  # noqa: BLE001
            bad.append(pkg)
    add("Workshop packages", OK if not bad else FAIL, f"{len(chk['packages'])} installed" if not bad else "missing: " + ", ".join(bad) + " (run: uv sync)")

    try:
        importlib.import_module("ipykernel")
        add("Jupyter kernel", OK, "ready (pick '.venv' as the kernel in VS Code)")
    except Exception:  # noqa: BLE001
        add("Jupyter kernel", FAIL, "ipykernel missing (run: uv sync)")

    status, _ = reach("https://github.com")
    add("GitHub reachable", OK if status and status < 500 else FAIL, "yes" if status else "cannot reach github.com (network/proxy?)")

    key, base, model = env.get("VITHUPRO_API_KEY", ""), env.get("VITHUPRO_API_BASE", ws["ai"]["base_url"]), env.get("VITHUPRO_MODEL", ws["ai"]["model"])
    if not key:
        add("AI access key", FAIL, "not saved yet (run: vp setup)")
    else:
        status, _ = reach(base.rstrip("/") + "/models", {"Authorization": f"Bearer {key}"})
        add("AI access key", OK if status == 200 else FAIL,
            f"works ({model})" if status == 200 else ("key rejected: check the key on WhatsApp and run vp setup" if status in (401, 403) else f"AI service not reachable (status {status or 'none'})"))

    if chk.get("docker", "no") != "no":
        code, out = sh("docker", "info", "--format", "{{.ServerVersion}}", timeout=30)
        need = chk["docker"] == "required"
        add("Docker", OK if code == 0 else (FAIL if need else WARN),
            f"running ({out})" if code == 0 else ("start Docker Desktop (or use the Codespaces option)" if need else "optional for this workshop"))

    # Print the report
    print(f"\nVithuPro setup check · {ws['workshop']['title']}\n")
    for name, status, detail in results:
        print(f"  {ICON[status]} {name:<26} {detail}")
    fails = [r for r in results if r[1] == FAIL]
    print()
    if fails:
        print(f"  {len(fails)} item(s) to fix. Help: {HELP}  or WhatsApp us 'Need help'.")
    else:
        print("  You're ready for the workshop! 🎉")

    if report:
        payload = {"phone": env.get("VITHUPRO_PHONE", ""), "workshop": ws["workshop"]["slug"], "ready": not fails,
                   "os": f"{platform.system()} {platform.release()}", "vp": __version__,
                   "checks": [{"name": n, "status": s, "detail": d[:160]} for n, s, d in results]}
        try:
            req = urllib.request.Request(ws["report"]["url"], json.dumps(payload).encode(), {"Content-Type": "application/json"}, method="POST")
            urllib.request.urlopen(req, timeout=10).read()
            print("  Result shared with VithuPro so we can help if needed.")
        except Exception:  # noqa: BLE001
            print("  (Could not send the result to VithuPro. That's fine: tell us on WhatsApp.)")
        if not payload["phone"]:
            print("  Tip: run `vp setup` so we know this check is yours.")
    print()
    return 1 if fails else 0
