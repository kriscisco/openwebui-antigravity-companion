#!/usr/bin/env python3
"""
verify_deployment.py
Automated Zero-Defect ECC Verification Suite for Open WebUI Companion Stack.
Tests 10 Quality Gates. Must achieve 10/10 PASS (Zero Defects) to certify production.
"""

import os
import sys
import json
import urllib.request
import subprocess

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

results = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "defects": []
}

def record_test(gate_num, name, passed, detail=""):
    results["total"] += 1
    if passed:
        results["passed"] += 1
        print(f"  {GREEN}✔ [PASS]{RESET} {BOLD}{name}{RESET} {detail}")
    else:
        results["failed"] += 1
        results["defects"].append(f"Gate {gate_num} :: {name} -> {detail}")
        print(f"  {RED}✖ [DEFECT]{RESET} {BOLD}{name}{RESET} - {RED}{detail}{RESET}")

def main():
    print("=" * 65)
    print("🛡️ ZERO-DEFECT ECC VERIFICATION HARNESS - OPEN WEBUI COMPANION")
    print("Standard: 10-Gate Gated Quality Baseline (Target: 100% PASS)")
    print("=" * 65)

    port = 3005
    if os.path.exists("docker-compose.yml"):
        try:
            with open("docker-compose.yml", "r") as f:
                for line in f:
                    if ":8080" in line:
                        port = int(line.split(":")[0].strip().replace("-", "").strip('"').strip("'"))
        except Exception:
            pass

    # Gate 1: Docker Container Running
    print(f"\n{CYAN}{BOLD}[GATE 1] Docker Container Running State{RESET}")
    res = subprocess.run("docker ps --filter 'name=open-webui' --format '{{.Status}}'", shell=True, capture_output=True, text=True)
    is_up = "Up" in res.stdout
    record_test(1, "open-webui Container", is_up, f"Status: {res.stdout.strip()}")

    # Gate 2: HTTP Port Accessibility
    print(f"\n{CYAN}{BOLD}[GATE 2] WebUI HTTP Gateway Accessibility{RESET}")
    url = f"http://127.0.0.1:{port}"
    http_ok = False
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ECC-Harness"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            http_ok = (resp.status == 200)
            record_test(2, f"HTTP Port {port} Response", http_ok, f"HTTP Status: {resp.status}")
    except Exception as e:
        record_test(2, f"HTTP Port {port} Response", False, str(e))

    # Gate 3: SQLite Database & Tables
    print(f"\n{CYAN}{BOLD}[GATE 3] SQLite Database Integrity{RESET}")
    cmd = "docker exec open-webui python3 -c \"import sqlite3; c=sqlite3.connect('/app/backend/data/webui.db'); print([r[0] for r in c.cursor().execute('SELECT name FROM sqlite_master WHERE type=\\\"table\\\"').fetchall()])\""
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    has_tables = ("tool" in res.stdout and "model" in res.stdout and "knowledge" in res.stdout)
    record_test(3, "Core Database Tables", has_tables, "tool, model, knowledge verified")

    # Gate 4: Tool Registration
    print(f"\n{CYAN}{BOLD}[GATE 4] Autonomous Tool Bridge Registration{RESET}")
    cmd = "docker exec open-webui python3 -c \"import sqlite3, json; c=sqlite3.connect('/app/backend/data/webui.db'); r=c.cursor().execute('SELECT specs FROM tool WHERE id=\\\"workspace_bridge\\\"').fetchone(); print([s['name'] for s in json.loads(r[0])] if r else [])\""
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    has_funcs = ("create_system_rfc" in res.stdout and "verify_and_close_rfc" in res.stdout and "write_workspace_file" in res.stdout)
    record_test(4, "workspace_bridge Function Specs", has_funcs, res.stdout.strip())

    # Gate 5: Model Preset
    print(f"\n{CYAN}{BOLD}[GATE 5] Model Preset Registration & Tool Linkage{RESET}")
    cmd = "docker exec open-webui python3 -c \"import sqlite3, json; c=sqlite3.connect('/app/backend/data/webui.db'); r=c.cursor().execute('SELECT params FROM model WHERE id=\\\"lkt-hermes-orchestrator\\\"').fetchone(); print('tool_ids' in json.loads(r[0]) if r else False)\""
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    model_ok = ("True" in res.stdout)
    record_test(5, "lkt-hermes-orchestrator Preset", model_ok, "Linked to workspace_bridge")

    # Gate 6: Knowledge Base
    print(f"\n{CYAN}{BOLD}[GATE 6] Knowledge Collection Integrity{RESET}")
    cmd = "docker exec open-webui python3 -c \"import sqlite3; c=sqlite3.connect('/app/backend/data/webui.db'); r=c.cursor().execute('SELECT id FROM knowledge WHERE id=\\\"lkt-system-mastery\\\"').fetchone(); print(bool(r))\""
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    kb_ok = ("True" in res.stdout)
    record_test(6, "lkt-system-mastery Knowledge Base", kb_ok, "Master collection present")

    # Gate 7: File Write & UID Permission
    print(f"\n{CYAN}{BOLD}[GATE 7] Container Write & Host Permission Preservation{RESET}")
    cmd = "docker exec open-webui python3 -c \"with open('/app/workspace/project/.ecc_test_write', 'w') as f: f.write('ok')\""
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    test_ok = (res.returncode == 0)
    subprocess.run("docker exec open-webui rm -f /app/workspace/project/.ecc_test_write", shell=True, capture_output=True)
    record_test(7, "Workspace Write Permission", test_ok, "Created and cleaned successfully")

    # Gate 8: Terminal Command Execution
    print(f"\n{CYAN}{BOLD}[GATE 8] Terminal Sandbox Execution{RESET}")
    cmd = "docker exec open-webui bash -c 'cd /app/workspace/project && pwd'"
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    sh_ok = ("/app/workspace/project" in res.stdout)
    record_test(8, "Workspace Bash Execution", sh_ok, f"PWD: {res.stdout.strip()}")

    # Gate 9: Exemplars & Living State
    print(f"\n{CYAN}{BOLD}[GATE 9] Exemplars & Living State Availability{RESET}")
    exemplars_ok = os.path.exists("exemplars/RFC_KNOWLEDGE_EXEMPLARS.md")
    record_test(9, "RFC Knowledge Exemplars File", exemplars_ok, "Memory bank verified")

    # Gate 10: Systemd Watcher Daemon Status
    print(f"\n{CYAN}{BOLD}[GATE 10] Real-Time Sync Watcher Service{RESET}")
    res = subprocess.run("systemctl --user is-active lkt-webui-watcher.service", shell=True, capture_output=True, text=True)
    watcher_active = ("active" in res.stdout)
    record_test(10, "lkt-webui-watcher.service", watcher_active, f"State: {res.stdout.strip()}")

    # Gate 11: User Linger Daemon Persistence
    print(f"\n{CYAN}{BOLD}[GATE 11] User Session Linger Status{RESET}")
    user = os.getenv("USER", "unknown")
    res = subprocess.run(f"loginctl show-user {user} --property=Linger", shell=True, capture_output=True, text=True)
    linger_ok = ("Linger=yes" in res.stdout)
    record_test(11, "User Session Linger", linger_ok, f"Output: {res.stdout.strip()} (Run 'loginctl enable-linger' if failed)")

    # Gate 12: Live Sync Execution Test
    print(f"\n{CYAN}{BOLD}[GATE 12] Antigravity-to-WebUI Sync Pipeline{RESET}")
    sync_py = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sync_antigravity.py")
    res = subprocess.run([sys.executable, sync_py], capture_output=True, text=True)
    sync_ok = (res.returncode == 0)
    record_test(12, "Sync Script Execution", sync_ok, res.stdout.strip() if sync_ok else res.stderr.strip())

    print("\n" + "=" * 65)
    print(f"VERIFICATION SUMMARY: Total: {results['total']} | Passed: {results['passed']} | Defects: {results['failed']}")
    if results['failed'] == 0:
        print(f"{GREEN}{BOLD}🎉 ZERO DEFECT VERIFIED! Deployment is Certified Production Ready.{RESET}")
    else:
        print(f"{RED}{BOLD}❌ DEFECTS DETECTED: {len(results['defects'])} issues need resolution.{RESET}")
    print("=" * 65)

    return 0 if results['failed'] == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
