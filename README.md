# VithuPro workshop lab · Explore: GenAI & Agentic AI Engineering Toolkit

Everything you need for the workshop: notebooks, starter code and the `vp` helper.

## Get ready (about 20 minutes, before the workshop)

1. **Run the installer** from the setup guide: https://vithuproai.com/setup
   It installs VS Code, Git and Python tools, downloads this lab and installs the packages.
2. **Open this folder in VS Code** (File → Open Folder → `vithupro-lab`).
3. In VS Code open a terminal (**Terminal → New Terminal**) and run:
   ```
   uv run vp setup
   ```
   Enter your WhatsApp number and the access key we sent you on WhatsApp.
4. Open `notebooks/00_ready.ipynb`, pick the **.venv** kernel (top right) and run all cells.
5. Finally run:
   ```
   uv run vp check
   ```
   ✅ everywhere means you're ready. The result is shared with VithuPro so we can help if something is missing.

Stuck? See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or reply **Need help** on WhatsApp.

## No laptop setup possible? (backup)

Open this repo in **GitHub Codespaces** (green **Code** button → Codespaces → Create). The same environment opens in your browser; then run `uv run vp setup` and `uv run vp check`.

## After the workshop

Keep practising here. Your access key works for 30 days after the workshop. Then put any OpenAI-compatible key (for example a free Google Gemini or Groq key) in `.env`; see `.env.example`. No code changes needed.
