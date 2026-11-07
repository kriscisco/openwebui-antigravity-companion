# 🚀 Universal Open WebUI Antigravity Companion Stack

An **Agent-Native Universal Appliance** designed to deploy and operate [Open WebUI](https://github.com/open-webui/open-webui) as a seamless, autonomous backup companion for Google Antigravity across any server environment.

---

## 🌟 Key Highlights
* **Autonomous ITIL RFC Lifecycle**: Pre-configured with `workspace_bridge` v2 tool (`create_system_rfc`, `verify_and_close_rfc`). The model automatically opens tickets, captures safety snapshots, edits files, and closes tickets upon passing verification.
* **Two-Way Real-Time Synchronization**: Seamless continuum between office (Open WebUI) and home (Antigravity) with zero human intervention (<0.1% CPU, 0 token consumption).
* **Multi-Brand AI Operability**: Ships with `SKILL.md` and `AGENT_GUIDE.md` so any AI agent (Antigravity, Claude Code, Cursor, Copilot) can clone this repository and deploy it autonomously without mistakes.
* **10-Gate ECC Zero-Defect Baseline**: Includes automated verification test harness (`verify_deployment.py`) guaranteeing 100% production readiness.

---

## 📋 Directory Structure
```text
openwebui-antigravity-companion/
├── SKILL.md                          # Antigravity/Agent Skill Manifest
├── AGENT_GUIDE.md                    # Deep Cognitive Runbook for AI Agents
├── README.md                         # Project Overview & Manual Instructions
├── .gitignore                        # Standard Git Ignore Rules
├── engine/
│   ├── probe_environment.py          # Host Scanner (Ports, OpenCode, Ollama, UIDs)
│   ├── synthesize_config.py          # Config Synthesizer (docker-compose & .env)
│   ├── seed_webui_db.py              # Atomic SQLite Seeder for Tools & Presets
│   ├── watcher_daemon.py             # Real-time Background Sync Daemon
│   └── verify_deployment.py          # 10-Gate Zero-Defect ECC Test Harness
├── templates/
│   ├── docker-compose.template.yml   # Docker Compose Template
│   ├── env.template                  # Environment Variables Template
│   └── systemd_watcher.service       # Systemd User Service Template
└── exemplars/
    ├── RFC_KNOWLEDGE_EXEMPLARS.md    # Memory Bank of 98+ RFCs & 28 Skills
    └── PROJECT_STATE_TEMPLATE.md     # Single Source of Truth Template
```

---

## 🛠️ Quickstart (For Human Operators)

### 1. Give 1 Prompt to Your AI Agent on the Target Server
Simply tell your AI agent:
> *"Clone repo `openwebui-antigravity-companion`, baca `SKILL.md` dan `AGENT_GUIDE.md`, analisa server ini secara bertahap, dan deploy Open WebUI sebagai backup kamu dengan standar Zero-Defect."*

### 2. Manual Command Sequence (If Preferred)
```bash
# 1. Scan environment
python3 engine/probe_environment.py

# 2. Synthesize configuration
python3 engine/synthesize_config.py --workspace "/path/to/your/project"

# 3. Start container
docker compose up -d

# 4. Seed database atomically
docker exec -i open-webui python3 < engine/seed_webui_db.py

# 5. Enable watcher daemon
mkdir -p ~/.config/systemd/user/
cp lkt-webui-watcher.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now lkt-webui-watcher.service

# 6. Verify zero defect
python3 engine/verify_deployment.py
```

---

## 🔒 Security & Privacy
* **Zero Hardcoded Secrets**: Secret keys are generated cryptographically on the fly (`secrets.token_urlsafe(24)`). API keys must be provided via environment variables or prompt.
* **Defensive Sandbox**: Risky bash commands (`rm -rf /`, `drop table`, `shutdown`, `mkfs`) are blocked at the bridge level.
