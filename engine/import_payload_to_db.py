#!/usr/bin/env python3
import sqlite3
import json
import time
import os

PAYLOAD_FILE = '/app/workspace/omni-agent-os/governance/synced_chat_payload.json'
DB_PATH = '/app/backend/data/webui.db'

def main():
    if not os.path.exists(PAYLOAD_FILE):
        print(f"Error: {PAYLOAD_FILE} not found.")
        return

    with open(PAYLOAD_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    chat_id = data.get('id', 'chat-lkt-cyber-continuum')
    title = data.get('title', 'LKT Cyber Security Project — Continuum')
    messages = data.get('messages', [])
    now = int(time.time())

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Find registered users
    c.execute("SELECT id FROM user;")
    user_rows = c.fetchall()
    target_users = [row[0] for row in user_rows] if user_rows else ['default_owner']

    for user_id in target_users:
        # Build Open WebUI chat document structure
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

        # Insert or replace into chat table
        c.execute('''
        INSERT OR REPLACE INTO chat (
            id, user_id, title, chat, created_at, updated_at,
            share_id, archived, pinned, meta, folder_id, tasks,
            summary, last_read_at, current_message_id, variables, timer_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            chat_id,
            user_id,
            title,
            json.dumps(chat_dict),
            data.get('created_at', now),
            now,
            None,
            False,
            0,  # Unpinned so it appears directly in sidebar Today list
            json.dumps({'source': 'antigravity_continuum', 'internal': False, 'tags': ['antigravity', 'continuum']}),
            None,
            None,
            'Percakapan aktif LKT Cyber Security Project yang disinkronkan otomatis dari Antigravity.',
            now,
            messages[-1]['id'] if messages else None,
            json.dumps({}),
            None
        ))

        # Clear old chat_messages for this chat to avoid duplicate buildup
        c.execute("DELETE FROM chat_message WHERE chat_id = ? AND user_id = ?;", (chat_id, user_id))

        # Insert each message into chat_message table for searchability and fast retrieval
        for m in messages:
            mid = m['id']
            composite_id = f"{chat_id}-{mid}"
            c.execute('''
            INSERT OR REPLACE INTO chat_message (
                id, chat_id, user_id, role, parent_id, content,
                output, model_id, files, sources, embeds, done,
                status_history, error, usage, created_at, updated_at,
                context_summary, meta
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                composite_id,
                chat_id,
                user_id,
                m['role'],
                m.get('parentId'),
                json.dumps(m['content']),  # Must be JSON-serialized string for SQLAlchemy Column(JSON)
                None,
                'lkt-hermes-orchestrator',
                json.dumps([]),
                json.dumps([]),
                json.dumps([]),
                True,
                json.dumps([]),
                None,
                json.dumps({}),
                m.get('timestamp', now),
                m.get('timestamp', now),
                None,
                json.dumps({})
            ))

    conn.commit()
    conn.close()
    print(f"SUCCESS: Synchronized {len(messages)} messages for user(s) {target_users} into Open WebUI chat {chat_id}.")

if __name__ == '__main__':
    main()
