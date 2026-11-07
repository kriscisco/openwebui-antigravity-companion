---
name: openwebui-antigravity-companion
description: Universal deployment and management skill for Open WebUI as an autonomous, seamless backup companion for Antigravity with two-way sync, ITIL RFC lifecycle, and zero-defect baseline.
---

# OPEN WEBUI ANTIGRAVITY COMPANION SKILL

> [!IMPORTANT]
> **MANDATORY AI OPERATING DIRECTIVE: PHASED & METHODICAL EXECUTION**
> When you (the AI Agent) are tasked with deploying or adopting Open WebUI using this repository, **DO NOT RUSH**. Speed is not the goal. Your primary objective is **100% precision, surgical stability, and Zero-Defect certification (10/10 PASS)**.
> Execute each phase sequentially, inspect every output, and never proceed to the next phase if a defect or warning is detected.

---

## 1. PURPOSE & CAPABILITIES
This skill equips any AI Agent (Google Antigravity, Claude Code, Cursor, Copilot, or CLI agent) to:
1. Probe and analyze the target host environment (Docker, UIDs, ports, OpenCode presence, Ollama presence).
2. Choose the optimal adoption strategy (Transition OpenCode vs Clean Greenfield).
3. Synthesize host-tailored `docker-compose.yml`, `.env`, and systemd service templates.
4. Launch Open WebUI and atomically seed its SQLite database with the autonomous `workspace_bridge` v2 tool and `lkt-hermes-orchestrator` model preset.
5. Activate the Real-Time Background Watcher Daemon for two-way Antigravity ⟷ Open WebUI sync.
6. Verify the installation against the 10-Gate ECC Zero-Defect Baseline.

---

## 2. STEP-BY-STEP PHASED WORKFLOW (STRICT ORDER)

### Phase 1: Environment Probe & Discovery
Run the deterministic host scanner:
```bash
python3 engine/probe_environment.py
```
*Action*: Read `probe_result.json`. Note the recommended strategy (`STRATEGY_A_OPENCODE_TRANSITION` or `STRATEGY_B_GREENFIELD`), recommended port, host UID/GID, and Ollama status.

### Phase 2: If OpenCode Exists (Strategy A Only)
If `opencode_status.detected == true`:
1. Safely stop the OpenCode service (`systemctl --user stop opencode` or `docker stop opencode`).
2. Snapshot the existing OpenCode workspace to `/opt/backup-opencode-legacy/`.
3. Inform the Human Principal that OpenCode has been safely decommissioned and ready for Open WebUI failover.

### Phase 3: Configuration Synthesis
Generate host-tailored configuration:
```bash
python3 engine/synthesize_config.py --workspace "<PATH_TO_PROJECT_WORKSPACE>"
```
*Validation*: Inspect the generated `docker-compose.yml`, `.env`, and `lkt-webui-watcher.service`. Ensure paths and ports match host requirements.

### Phase 4: Container Launch & Healthcheck
Start the Open WebUI container:
```bash
docker compose up -d
```
Wait 10-15 seconds, then verify container is healthy:
```bash
docker ps --filter "name=open-webui"
curl -s http://127.0.0.1:<PORT> | head -n 10
```

### Phase 5: Database Seeding (Atomic Ingestion)
Inject the autonomous tools, model presets, and architectural knowledge:
```bash
docker exec -i open-webui python3 < engine/seed_webui_db.py
```
*Validation*: Confirm output reports registration of `workspace_bridge` (6 functions), `lkt-system-mastery` knowledge base, and `lkt-hermes-orchestrator` preset.

### Phase 6: Background Watcher Daemon Activation
Deploy and activate the real-time two-way synchronization service:
```bash
mkdir -p ~/.config/systemd/user/
cp lkt-webui-watcher.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now lkt-webui-watcher.service
systemctl --user status lkt-webui-watcher.service
```

### Phase 7: Zero-Defect ECC Verification
Execute the automated test harness:
```bash
python3 engine/verify_deployment.py
```
*Target*: **Total: 10 | Passed: 10 | Defects: 0 (100% PASS)**.
If any gate fails, inspect the defect message, apply surgical remediation, and re-run until 10/10 PASS is achieved.

---

## 3. CORE PRINCIPLES & GUARDRAILS
1. **Ponytail Minimalist Standard**: All engine scripts use Python Standard Library only (`os`, `sys`, `json`, `sqlite3`, `urllib`, `subprocess`, `secrets`, `socket`). Do NOT install external pip packages.
2. **Host Permission Preservation**: Files written by the container are given `chmod 0664` to prevent permission conflicts with non-root host users.
3. **Autonomous RFC Lifecycle**: Whenever asked to write code or modify config in Open WebUI, the model must autonomously call `create_system_rfc`, apply changes, and close via `verify_and_close_rfc`.
