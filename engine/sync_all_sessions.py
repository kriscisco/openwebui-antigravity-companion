#!/usr/bin/env python3
"""
sync_all_antigravity_to_webui.py
Batch synchronizes ALL historical Antigravity conversations (14+ sessions)
into Open WebUI SQLite database for all registered users.
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
DB_PATH = "/app/backend/data/webui.db"

def clean_user_content(text):
    if not text:
        return ""
    clean = re.sub(r'<USER_REQUEST>\s*', '', text)
    clean = re.sub(r'\s*</USER_REQUEST>', '', clean)
    clean = re.sub(r'<ADDITIONAL_METADATA>[\s\S]*?</ADDITIONAL_METADATA>', '', clean)
    clean = re.sub(r'<USER_SETTINGS_CHANGE>[\s\S]*?</USER_SETTINGS_CHANGE>', '', clean)
    return clean.strip()

def parse_iso_to_epoch(iso_str):
    if not iso_str:
        return int(time.time())
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return int(dt.timestamp())
    except Exception:
        return int(time.time())

def generate_session_title(first_prompt, conv_id):
    if not first_prompt:
        return f"Sesi Antigravity ({conv_id[:8]})"
    
    first_line = first_prompt.split('\n')[0].strip()
    first_line = re.sub(r'@\[conversation:\"([^\"]+)\"\]', r'\1', first_line)
    first_line = re.sub(r'\[SYSTEM ROLE\]', 'System Role Initialization', first_line)
    first_line = re.sub(r'[#*`]', '', first_line).strip()
    
    if len(first_line) > 55:
        first_line = first_line[:55] + "..."
    return first_line if first_line else f"Sesi Antigravity ({conv_id[:8]})"

def process_conversation(conv_id):
    tpath = os.path.join(BRAIN_DIR, conv_id, '.system_generated', 'logs', 'transcript.jsonl')
    if not os.path.exists(tpath):
        return None

    raw_turns = []
    first_user_prompt = ""
    with open(tpath, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            try:
                s = json.loads(line)
                stype = s.get('type')
                src = s.get('source')
                content = s.get('content', '')
                ts = parse_iso_to_epoch(s.get('created_at'))

                if stype == 'USER_INPUT' and src == 'USER_EXPLICIT':
                    ctext = clean_user_content(content)
                    if ctext and not ctext.startswith("Comments on artifact URI"):
                        if not first_user_prompt:
                            first_user_prompt = ctext
                        raw_turns.append(('user', ctext, ts))
                elif stype == 'PLANNER_RESPONSE' and src == 'MODEL':
                    if content and content.strip():
                        raw_turns.append(('assistant', content.strip(), ts))
            except Exception:
                pass

    if not raw_turns:
        return None

    title = generate_session_title(first_user_prompt, conv_id)
    if conv_id == "bad89492-334c-4fae-a9b9-5808ba4a2c3f":
        title = "LKT Cyber Security Project — Continuum"

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

    created_at = raw_turns[0][2]
    updated_at = raw_turns[-1][2]

    return {
        'id': f"chat_{conv_id}",
        'title': title,
        'created_at': created_at,
        'updated_at': updated_at,
        'messages': messages
    }

def main():
    if not os.path.exists(BRAIN_DIR):
        print(f"Error: {BRAIN_DIR} not found.")
        sys.exit(1)

    conv_dirs = [d for d in os.listdir(BRAIN_DIR) if os.path.isdir(os.path.join(BRAIN_DIR, d)) and d != 'tempmediaStorage']
    print(f"🔍 Found {len(conv_dirs)} conversation directories in brain storage.")

    all_payloads = []
    for d in conv_dirs:
        payload = process_conversation(d)
        if payload and payload['messages']:
            all_payloads.append(payload)

    # Sort payloads by updated_at ascending so latest appears at top
    all_payloads.sort(key=lambda x: x['updated_at'])
    print(f"📦 Successfully parsed {len(all_payloads)} valid conversation sessions.")

    # Script to run inside Docker Open WebUI container
    db_importer = '''
import sqlite3, json, time, sys

payloads = json.loads(sys.stdin.read())
conn = sqlite3.connect('/app/backend/data/webui.db')
c = conn.cursor()

# Get all registered users
c.execute("SELECT id FROM user;")
user_rows = c.fetchall()
target_users = [row[0] for row in user_rows] if user_rows else ['default_owner']

synced_count = 0
for data in payloads:
    chat_id = data['id']
    title = data['title']
    created_at = data['created_at']
    updated_at = data['updated_at']
    messages = data['messages']

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
        # Insert or replace chat (pinned = 0 so it appears in standard date categories)
        c.execute("""
        INSERT OR REPLACE INTO chat (
            id, user_id, title, chat, created_at, updated_at,
            share_id, archived, pinned, meta, folder_id, tasks,
            summary, last_read_at, current_message_id, variables, timer_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            chat_id, user_id, title, json.dumps(chat_dict),
            created_at, updated_at, None, False, 0,
            json.dumps({'source': 'antigravity_continuum', 'internal': False}),
            None, None,
            title, updated_at, messages[-1]['id'] if messages else None,
            json.dumps({}), None
        ))

        # Clear old chat_messages for this chat to avoid duplicate buildup
        c.execute("DELETE FROM chat_message WHERE chat_id = ? AND user_id = ?;", (chat_id, user_id))

        # Insert messages
        for m in messages:
            c.execute("""
            INSERT OR REPLACE INTO chat_message (
                id, chat_id, user_id, role, parent_id, content,
                output, model_id, files, sources, embeds, done,
                status_history, error, usage, created_at, updated_at,
                context_summary, meta
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                m['id'], chat_id, user_id, m['role'], m.get('parentId'),
                m['content'], None, 'lkt-hermes-orchestrator', json.dumps([]),
                json.dumps([]), json.dumps([]), True, json.dumps([]), None,
                json.dumps({}), m.get('timestamp', updated_at), m.get('timestamp', updated_at),
                None, json.dumps({})
            ))

    synced_count += 1

conn.commit()
conn.close()
print(f"SUCCESS: Synchronized {synced_count} historical sessions into Open WebUI database for {len(target_users)} user(s).")
'''
    json_input = json.dumps(all_payloads)
    cmd = ["docker", "exec", "-i", "open-webui", "python3", "-c", db_importer]
    res = subprocess.run(cmd, input=json_input, capture_output=True, text=True, timeout=60)
    print(res.stdout)
    if res.stderr:
        print("[STDERR]:", res.stderr)

    if res.returncode == 0:
        print(f"🎉 All {len(all_payloads)} Antigravity sessions successfully synced to Open WebUI!")
    else:
        print(f"❌ Batch sync failed with exit code {res.returncode}")

if __name__ == '__main__':
    main()
