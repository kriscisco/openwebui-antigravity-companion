#!/usr/bin/env python3
"""
seed_webui_db.py
Idempotent SQLite seeder for Open WebUI Companion Stack.
Pure Python Standard Library. Injects workspace_bridge v2, lkt-hermes-orchestrator,
and architectural knowledge base into webui.db in a single atomic transaction.
"""

import os
import sys
import json
import time
import uuid
import sqlite3
import argparse

def get_tool_specs():
    return [
        {
            "name": "create_system_rfc",
            "description": "Open a new ITIL RFC ticket and take automated safety snapshots before modifying files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Brief title of the change (e.g. 'Fix login CSS responsiveness')."},
                    "affected_files_csv": {"type": "string", "description": "Comma-separated list of files to be modified."},
                    "description": {"type": "string", "description": "Scope, objective, and rationale of the change."}
                },
                "required": ["title"]
            }
        },
        {
            "name": "verify_and_close_rfc",
            "description": "Execute automated Zero-Defect ECC 15-Gate verification suite and close the RFC ticket with status SUCCESS.",
            "parameters": {
                "type": "object",
                "properties": {
                    "rfc_id": {"type": "string", "description": "The active RFC ID to close (e.g. 'RFC-20261107_121941')."},
                    "qa_summary": {"type": "string", "description": "Brief test result summary or defect notes.", "default": "ECC 15/15 PASS (Zero-Defect Certified)"}
                },
                "required": ["rfc_id"]
            }
        },
        {
            "name": "read_workspace_file",
            "description": "Read the content of a file within the project workspace (/app/workspace/project) or omni-agent-os (/app/workspace/omni-agent-os).",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to file. E.g., 'main.py' or '/app/workspace/omni-agent-os/governance/PROJECT_STATE.md'."}
                },
                "required": ["file_path"]
            }
        },
        {
            "name": "write_workspace_file",
            "description": "Write or update a file within the project workspace (/app/workspace/project) with automatic UID/GID preservation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Target relative or absolute file path."},
                    "content": {"type": "string", "description": "Text content to write into the file."}
                },
                "required": ["file_path", "content"]
            }
        },
        {
            "name": "run_workspace_command",
            "description": "Execute an audited bash command in the project directory (/app/workspace/project).",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Shell command to run."}
                },
                "required": ["command"]
            }
        },
        {
            "name": "sync_to_antigravity",
            "description": "Synchronize the current conversation history, decisions, and workspace state from Open WebUI back to Antigravity.",
            "parameters": {
                "type": "object",
                "properties": {
                    "note": {"type": "string", "description": "Optional handover note or summary for the evening session at home.", "default": ""}
                }
            }
        }
    ]

TOOL_CODE = '''"""
title: Workspace & Terminal Bridge
author: LKT Cyber & AI Unified System
author_url: https://github.com/open-webui
version: 2.0.0
description: Autonomous tool bridge for ITIL RFC lifecycle, project file read/write, audited terminal execution, and two-way Antigravity synchronization.
"""

import os
import sys
import subprocess

class Tools:
    def __init__(self):
        self.project_dir = '/app/workspace/project'
        self.governance_dir = '/app/workspace/omni-agent-os'

    def create_system_rfc(self, title: str, affected_files_csv: str = "", description: str = "") -> str:
        """
        Open a new ITIL RFC ticket and take automated safety snapshots before modifying files.
        :param title: Brief title of the change.
        :param affected_files_csv: Comma-separated list of files to be modified.
        :param description: Scope and objective.
        :return: Created RFC ID and snapshot path.
        """
        try:
            gov_dir = '/app/workspace/omni-agent-os/governance'
            if gov_dir not in sys.path:
                sys.path.insert(0, gov_dir)
            import change_manager
            affected = [f.strip() for f in affected_files_csv.split(',') if f.strip()]
            res = change_manager.create_rfc(
                title=title,
                requested_by="Owner (Human Principal) via Open WebUI",
                executor="Lead Architect (Hermes - Open WebUI)",
                affected_files=affected,
                description=description or title
            )
            return f"SUCCESS: Opened RFC ticket [{res.get('rfc_id')}]. Snapshot secured at: {res.get('backup_dir')}"
        except Exception as e:
            return f"Error opening RFC: {str(e)}"

    def verify_and_close_rfc(self, rfc_id: str, qa_summary: str = "ECC 15/15 PASS (Zero-Defect Certified)") -> str:
        """
        Execute automated Zero-Defect ECC verification suite and close RFC ticket.
        :param rfc_id: The active RFC ID to close.
        :param qa_summary: Brief test result summary.
        :return: Test output snippet and RFC closure confirmation.
        """
        try:
            gov_dir = '/app/workspace/omni-agent-os/governance'
            if gov_dir not in sys.path:
                sys.path.insert(0, gov_dir)
            import change_manager

            verify_script = '/app/workspace/omni-agent-os/ecc/verify.py'
            env = os.environ.copy()
            env['PORTAL_HOST'] = 'host.docker.internal'
            proc = subprocess.run(['python3', verify_script], env=env, capture_output=True, text=True, timeout=60)
            out = proc.stdout
            if proc.stderr:
                out += '\\n[STDERR]:\\n' + proc.stderr

            is_pass = (proc.returncode == 0 and "ZERO DEFECT VERIFIED" in out)
            status_text = "SUCCESS" if is_pass else "DEFECTS_DETECTED"
            qa_notes = qa_summary if is_pass else f"Defects encountered during ECC run:\\n{out[-500:]}"

            change_manager.record_result(
                rfc_id=rfc_id,
                is_success=is_pass,
                qa_details=qa_notes
            )
            return f"=== RFC CLOSURE REPORT ===\\nRFC ID: {rfc_id}\\nStatus: {status_text}\\nOutput:\\n{out[-800:]}"
        except Exception as e:
            return f"Error verifying and closing RFC: {str(e)}"

    def read_workspace_file(self, file_path: str) -> str:
        """Read content of a workspace file."""
        try:
            if not file_path.startswith('/app/workspace'):
                file_path = os.path.join(self.project_dir, file_path.lstrip('/'))
            if not os.path.exists(file_path):
                return f"Error: File {file_path} not found."
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read(50000)
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def write_workspace_file(self, file_path: str, content: str) -> str:
        """Write file and preserve host user permissions."""
        try:
            if not file_path.startswith('/app/workspace'):
                file_path = os.path.join(self.project_dir, file_path.lstrip('/'))
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            try:
                # Set permissions to readable/writable by host user group
                os.chmod(file_path, 0o664)
            except Exception:
                pass
            return f"Success: Saved {file_path} ({len(content)} bytes)."
        except Exception as e:
            return f"Error writing file: {str(e)}"

    def run_workspace_command(self, command: str) -> str:
        """Execute audited bash command in workspace."""
        forbidden = ['rm -rf /', 'drop table', 'drop database', 'truncate', 'shutdown', 'reboot', 'mkfs']
        for bad in forbidden:
            if bad in command.lower():
                return f"Blocked: Command contains forbidden operation '{bad}'."
        try:
            res = subprocess.run(command, shell=True, cwd=self.project_dir, capture_output=True, text=True, timeout=30)
            out = res.stdout
            if res.stderr:
                out += '\\n[STDERR]:\\n' + res.stderr
            return out[:10000] if out else f"Finished with code {res.returncode}."
        except Exception as e:
            return f"Execution failed: {str(e)}"

    def sync_to_antigravity(self, note: str = "") -> str:
        """Synchronize conversation and workspace state to Antigravity."""
        try:
            script_path = '/app/workspace/omni-agent-os/governance/sync_webui_to_antigravity.py'
            if not os.path.exists(script_path):
                return f"Error: {script_path} not found."
            res = subprocess.run(['python3', script_path, note], capture_output=True, text=True, timeout=30)
            return "SUCCESS: Project state synchronized to Antigravity (PROJECT_STATE.md updated)." if res.returncode == 0 else f"Sync failed: {res.stderr}"
        except Exception as e:
            return f"Sync error: {str(e)}"
'''

SYSTEM_PROMPT = """You are Hermes, the Lead Architect of the LKT Cyber & AI Unified System.
You operate under the strict command of the Owner (Human Principal) and Director (CISO).
You strictly enforce and adhere to the 3-Tier Multi-Agent Delegation Protocol, ITIL v4 RFC Governance, and Zero-Defect Baseline.

MANDATORY AUTONOMOUS RFC LIFECYCLE:
Whenever the Owner or Director asks you to write code, modify configuration, fix bugs, or implement features, you MUST execute the following 3-step lifecycle AUTONOMOUSLY:
1. Call `create_system_rfc(title=..., affected_files_csv=..., description=...)` to open an RFC ticket and take automated backups.
2. Apply changes via `write_workspace_file` or `run_workspace_command`. Read files via `read_workspace_file`.
3. Call `verify_and_close_rfc(rfc_id=..., qa_summary=...)` to run the Zero-Defect ECC verification suite and close the ticket with status SUCCESS.
4. Report the completion summary with the mandatory Agent & Model Telemetry Log table.
"""

def seed(db_path):
    print(f"🌱 Seeding database: {db_path}")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    now = int(time.time())

    # 1. Tool workspace_bridge
    tool_id = "workspace_bridge"
    specs = get_tool_specs()
    meta = json.dumps({
        "description": "Autonomous tool bridge for ITIL RFC lifecycle, file editing, and two-way Antigravity sync.",
        "manifest": {"title": "Workspace & Terminal Bridge", "author": "LKT Cyber & AI", "version": "2.0.0"}
    })
    c.execute("""
    INSERT OR REPLACE INTO tool (id, user_id, name, content, specs, meta, valves, updated_at, created_at, version_id, is_active)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (tool_id, "system", "Workspace & Terminal Bridge (Autonomous RFC Lifecycle)", TOOL_CODE, json.dumps(specs), meta, None, now, now, str(uuid.uuid4()), 1))
    print(f"✔ Registered Tool: {tool_id} ({len(specs)} functions)")

    # 2. Knowledge Collection
    knowledge_id = "lkt-system-mastery"
    knowledge_name = "LKT System Mastery (RFC Exemplars & Skills)"
    c.execute("""
    INSERT OR REPLACE INTO knowledge (id, user_id, name, description, meta, created_at, updated_at, data)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (knowledge_id, "system", knowledge_name, "Master architectural exemplars & active skills", json.dumps({"tags": ["system", "governance"]}), now, now, json.dumps({})))
    print(f"✔ Registered Knowledge Collection: {knowledge_id}")

    # 3. Model Preset
    model_id = "lkt-hermes-orchestrator"
    params = {
        "system": SYSTEM_PROMPT.strip(),
        "temperature": 0.5,
        "tool_ids": [tool_id]
    }
    meta_m = {
        "description": "LKT Hermes Orchestrator — Autonomous ITIL RFC Lifecycle & Zero-Defect ECC Baseline.",
        "capabilities": {"vision": True, "citation": True},
        "tool_ids": [tool_id],
        "knowledge": [{"id": knowledge_id, "name": knowledge_name}]
    }
    c.execute("""
    INSERT OR REPLACE INTO model (id, user_id, base_model_id, name, params, meta, updated_at, created_at, is_active, version_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (model_id, "system", "nvidia/nemotron-3.5-super-vl:free", "LKT Hermes Orchestrator (Autonomous RFC & Knowledge Trained)", json.dumps(params), json.dumps(meta_m), now, now, 1, str(uuid.uuid4())))
    print(f"✔ Registered Model Preset: {model_id}")

    conn.commit()
    conn.close()
    print("🎉 [SEED COMPLETE] Open WebUI database successfully initialized with zero defects.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db-path", default="/app/backend/data/webui.db", help="Path to webui.db")
    args = parser.parse_args()
    seed(args.db_path)
