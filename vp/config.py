"""Reads vp.toml (workshop settings) and .env (student settings). Standard library only, so `vp check`
can still diagnose a laptop where the project packages failed to install."""
import os
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / ".env"


def workshop() -> dict:
    with open(ROOT / "vp.toml", "rb") as f:
        return tomllib.load(f)


def read_env() -> dict:
    """KEY=value lines from .env (no shell expansion), overridden by real environment variables."""
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    for k in ("VITHUPRO_API_KEY", "VITHUPRO_API_BASE", "VITHUPRO_MODEL", "VITHUPRO_PHONE"):
        if os.environ.get(k):
            env[k] = os.environ[k]
    return env


def write_env(values: dict) -> None:
    """Update or add keys in .env, keeping any other lines the student added."""
    lines = ENV_FILE.read_text(encoding="utf-8").splitlines() if ENV_FILE.exists() else []
    seen = set()
    out = []
    for line in lines:
        key = line.split("=", 1)[0].strip() if "=" in line and not line.lstrip().startswith("#") else None
        if key in values:
            out.append(f"{key}={values[key]}")
            seen.add(key)
        else:
            out.append(line)
    out += [f"{k}={v}" for k, v in values.items() if k not in seen]
    ENV_FILE.write_text("\n".join(out) + "\n", encoding="utf-8")
