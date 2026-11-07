#!/usr/bin/env python3
"""
sync_antigravity.py
Universal Self-Contained Antigravity-to-OpenWebUI Transcript Synchronizer.
Scans ~/.gemini/antigravity-cli/brain for the latest session, parses turns,
and directly injects/updates the conversation in Open WebUI's SQLite database.
Pure Python Standard Library (0 external dependencies).
"""

import os
import sys
import json
import re
import time
import uuid
import subprocess
from datetime import datetime

HOME_DIR = os.path.expanduser("~")
BRAIN_DIR = os.path.join(HOME_DIR, ".gemini", "antigravity-cli", "brain")
CONTAINER_NAME = os.getenv("WEBUI_CONTAINER_NAME", "open-webui")

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
        msg_id = f"msg_{conv_id[:8]}_{i:03d}_{str(uuid.uuid4())[:8]}"
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

    return {
        'id': f"chat_{conv_id}",
        'title': "Antigravity Project — Live Continuum",
        'created_at': first_ts,
        'updated_at': int(time.time()),
        'messages': messages
    }

def inject_to_webui_db(payload):
    json_str = json.dumps(payload)
    python_script = """
import sqlite3, json, time, sys

payload = json.loads(sys.stdin.read())
chat_id = payload['id']
title = payload['title']
messages = payload['messages']
now = int(time.time())

conn = sqlite3.connect('/app/backend/data/webui.db')
c = conn.cursor()

c.execute("SELECT id FROM user;")
user_rows = c.fetchall()
target_users = [row[0] for row in user_rows] if user_rows else ['default_owner']

for user_id in target_users:
    chat_dict = {
        'id': chat_id,
        'title': title,
        'models': ['lkt-hermes-orchestrator'],
        'params': {},
        'messages': messages,
        'history': {
            'messages': {m['id']: m for m in messages},
            'currentId': messages[-1]['id'] if messages else None
        }
    }
    c.execute('''
    INSERT OR REPLACE INTO chat (
        id, user_id, title, chat, created_at, updated_at,
        share_id, archived, pinned, meta, folder_id, tasks,
        summary, last_read_at, current_message_id, variables, timer_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        chat_id, user_id, title, json.dumps(chat_dict),
        payload.get('created_at', now), now, None, False, True,
        json.dumps({'source': 'antigravity_continuum'}), None, None,
        'Percakapan aktif Antigravity disinkronkan secara real-time.',
        now, messages[-1]['id'] if messages else None, json.dumps({}), None
    ))
    for m in messages:
        c.execute('''
        INSERT OR REPLACE INTO chat_message (
            id, chat_id, user_id, role, parent_id, content,
            output, model_id, files, sources, embeds, done,
            status_history, error, usage, created_at, updated_at,
            context_summary, meta
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            m['id'], chat_id, user_id, m['role'], m.get('parentId'),
            m['content'], None, 'lkt-hermes-orchestrator', json.dumps([]),
            json.dumps([]), json.dumps([]), True, json.dumps([]), None,
            json.dumps({}), m.get('timestamp', now), m.get('timestamp', now),
            None, json.dumps({})
        ))

conn.commit()
conn.close()
print(f"SUCCESS: Injected {len(messages)} turns into Open WebUI chat {chat_id}.")
"""
    cmd = ["docker", "exec", "-i", CONTAINER_NAME, "python3", "-c", python_script]
    res = subprocess.run(cmd, input=json_str, capture_output=True, text=True, timeout=30)
    if res.returncode == 0:
        print(res.stdout.strip())
        return True
    else:
        print(f"Failed to inject: {res.stderr or res.stdout}")
        return False

def sync_now(conv_id=None):
    cid = conv_id or get_latest_conversation_id()
    if not cid:
        print("[Sync] No Antigravity conversation found.")
        return False
    payload = build_chat_payload(cid)
    if not payload:
        print(f"[Sync] Failed to parse transcript for {cid}.")
        return False
    return inject_to_webui_db(payload)

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else None
    ok = sync_now(target)
    sys.exit(0 if ok else 1)
