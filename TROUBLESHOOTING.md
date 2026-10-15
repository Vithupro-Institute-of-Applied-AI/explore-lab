# Troubleshooting

| Problem | Fix |
|---|---|
| **Windows: "running scripts is disabled on this system"** | Open PowerShell and run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, answer **Y**, then run the installer again. |
| **`winget` is not recognized** (Windows) | Install **App Installer** from the Microsoft Store, restart PowerShell, run the installer again. |
| **`code`, `git` or `uv` "not found" right after installing** | Close **all** terminals and VS Code, open them again (the PATH updates on restart). Still missing? Restart the laptop. |
| **Mac: "xcode-select: install command line tools" pop-up** | Click **Install**, wait for it to finish, run the installer again. |
| **Jupyter: no kernel / ".venv" not in the list** | In VS Code press Ctrl+Shift+P → **Python: Select Interpreter** → choose `.venv`. Then reopen the notebook and pick the kernel again. If `.venv` doesn't exist, run `uv sync` in the terminal. |
| **`vp check` says packages missing** | In the lab folder run `uv sync`, then `uv run vp check`. |
| **AI access key rejected** | Copy the key again from WhatsApp (no spaces), run `uv run vp setup`. Still rejected? Reply **Need help** on WhatsApp. |
| **GitHub sign-in keeps looping** | In VS Code: Accounts icon (bottom left) → Sign in with GitHub → allow in the browser. Corporate laptop? Try your personal browser profile. |
| **Office or college network blocks downloads** | Use a mobile hotspot for the installation, or use the Codespaces backup (see README). |
| **Antivirus blocks the installer** | Allow it once, or install the tools manually with the links in the setup guide. |
| **"No space left on device"** | Free at least 5 GB of disk space and run the installer again. |
| **Laptop has 4 GB RAM and feels slow** | Close other apps and browser tabs during the workshop. Docker labs (Engineer) run better in the Codespaces backup. |
| **Docker: "WSL 2 is not installed" or "virtualization disabled"** (Engineer) | Run `wsl --install` in an admin PowerShell and restart. If virtualization is disabled in BIOS, use the Codespaces backup. |

Still stuck? Reply **Need help** on WhatsApp and choose your problem: the bot or a VithuPro mentor will help.
