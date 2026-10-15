"""One place to create the AI client used by every notebook and app.
Works with any OpenAI-compatible endpoint: the VithuPro gateway during the workshop, or a free tier afterwards
(change VITHUPRO_API_BASE / VITHUPRO_API_KEY / VITHUPRO_MODEL in .env; no code changes)."""
from . import config


def client():
    from openai import OpenAI

    env = config.read_env()
    if not env.get("VITHUPRO_API_KEY"):
        raise RuntimeError("No AI key yet: run `vp setup` in the VS Code terminal.")
    return OpenAI(api_key=env["VITHUPRO_API_KEY"], base_url=env.get("VITHUPRO_API_BASE") or config.workshop()["ai"]["base_url"])


def model() -> str:
    return config.read_env().get("VITHUPRO_MODEL") or config.workshop()["ai"]["model"]


def ask(prompt: str, system: str = "You are a helpful assistant.") -> str:
    r = client().chat.completions.create(model=model(), messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}])
    return r.choices[0].message.content
