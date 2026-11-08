#!/usr/bin/env python3
"""
Antigravity to Open WebUI Two-Way Transcript Synchronizer
Auto-detects the latest active Antigravity session and synchronizes it into Open WebUI SQLite database.
"""
import os
import sys
import json
import re
import time
import uuid
import subprocess
from datetime import datetime

BRAIN_DIR = "/home/kristian.admin/.gemini/antigravity-cli/brain"
PAYLOAD_PATH = "/opt/ai-agent/omni-agent-os/governance/synced_chat_payload.json"

def get_latest_conversation_id():
    if not os.path.exists(BRAIN_DIR):
        return None
    conv_dirs = [d for d in os.listdir(BRAIN_DIR) if os.path.isdir(os.path.join(BRAIN_DIR, d))]
    valid = []
    for d in conv_dirs:
        tpath = os.path.join(BRAIN_DIR, d, '.system_generated', 'logs', 'transcript.jsonl')
        if os.path.exists(tpath):
            valid.append((d, os.path.getmtime(tpath)))
    if not valid:
        return None
    valid.sort(key=lambda x: x[1], reverse=True)
    return valid[0][0]

def parse_iso_to_epoch(iso_str):
    if not iso_str:
        return int(time.time())
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return int(dt.timestamp())
    except Exception:
        return int(time.time())

def clean_user_content(text):
    if not text:
        return ""
    clean = re.sub(r'<USER_REQUEST>\s*', '', text)
    clean = re.sub(r'\s*</USER_REQUEST>', '', clean)
    clean = re.sub(r'<ADDITIONAL_METADATA>[\s\S]*?</ADDITIONAL_METADATA>', '', clean)
    clean = re.sub(r'<USER_SETTINGS_CHANGE>[\s\S]*?</USER_SETTINGS_CHANGE>', '', clean)
    return clean.strip()

def build_chat_payload(conv_id):
    transcript_path = os.path.join(BRAIN_DIR, conv_id, '.system_generated', 'logs', 'transcript.jsonl')
    if not os.path.exists(transcript_path):
        print(f"Error: Transcript {transcript_path} not found.")
        return None

    with open(transcript_path, 'r', encoding='utf-8') as f:
        steps = [json.loads(line) for line in f if line.strip()]

    raw_turns = []
    for s in steps:
        stype = s.get('type')
        src = s.get('source')
        content = s.get('content', '')
        ts = parse_iso_to_epoch(s.get('created_at'))

        if stype == 'USER_INPUT' and src == 'USER_EXPLICIT':
            clean_text = clean_user_content(content)
            if clean_text and not clean_text.startswith("Comments on artifact URI"):
                raw_turns.append(('user', clean_text, ts))
        elif stype == 'PLANNER_RESPONSE' and src == 'MODEL':
            if content and content.strip():
                raw_turns.append(('assistant', content.strip(), ts))

    messages = []
    parent_id = None
    for i, (role, text, ts) in enumerate(raw_turns):
        msg_id = f"msg_{conv_id[:8]}_{i:04d}"
        msg_obj = {
            'id': msg_id,
            'parentId': parent_id,
            'childrenIds': [],
            'role': role,
            'content': text,
            'timestamp': ts,
            'models': ['lkt-hermes-orchestrator']
        }
        if parent_id and messages:
            messages[-1]['childrenIds'].append(msg_id)

        messages.append(msg_obj)
        parent_id = msg_id

    first_ts = raw_turns[0][2] if raw_turns else int(time.time())

    payload = {
        'id': f"chat_{conv_id}",
        'title': "LKT Cyber Security Project — Continuum",
        'created_at': first_ts,
        'updated_at': int(time.time()),
        'messages': messages
    }
    return payload

def main():
    target_conv_id = sys.argv[1] if len(sys.argv) > 1 else get_latest_conversation_id()
    if not target_conv_id:
        print("Error: No active Antigravity conversation found.")
        sys.exit(1)

    print(f"🔄 Synchronizing active conversation: {target_conv_id}")
    payload = build_chat_payload(target_conv_id)
    if not payload:
        sys.exit(1)

    with open(PAYLOAD_PATH, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"Payload compiled with {len(payload['messages'])} messages to {PAYLOAD_PATH}.")

    cmd = [
        "docker", "exec", "open-webui",
        "python3", "/app/workspace/omni-agent-os/governance/import_payload_to_db.py"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print("[STDERR]:", res.stderr)

    if res.returncode == 0:
        print(f"🎉 Antigravity-to-OpenWebUI synchronization complete for session {target_conv_id}!")
    else:
        print(f"❌ Synchronization failed with code {res.returncode}")
        sys.exit(res.returncode)

if __name__ == '__main__':
    main()
