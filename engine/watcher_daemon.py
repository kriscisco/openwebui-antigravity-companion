#!/usr/bin/env python3
"""
watcher_daemon.py
Real-Time Two-Way Background Watcher Daemon (Zero-Touch & Zero-Token)
1. Direction A: Monitors Antigravity transcript.jsonl -> Syncs to Open WebUI SQLite.
2. Direction B: Monitors Open WebUI chat_message -> Syncs to PROJECT_STATE.md.
Dynamic path resolution, Anti-Looping Guard, CPU < 0.1%.
"""

import os
import sys
import time
import signal
import subprocess
import json

HOME_DIR = os.path.expanduser("~")
BRAIN_DIR = os.path.join(HOME_DIR, ".gemini", "antigravity-cli", "brain")
CONTAINER_NAME = os.getenv("WEBUI_CONTAINER_NAME", "open-webui")

POLL_INTERVAL = 2.5
WEBUI_CHECK_INTERVAL = 7.5
DEBOUNCE_DELAY = 1.5

running = True
sync_lock_until = 0.0

def signal_handler(signum, frame):
    global running
    print(f"\n[Watcher] Signal {signum} received. Stopping gracefully...")
    running = False

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def get_latest_transcript_info():
    if not os.path.exists(BRAIN_DIR):
        return None, 0, 0
    conv_dirs = [d for d in os.listdir(BRAIN_DIR) if os.path.isdir(os.path.join(BRAIN_DIR, d))]
    valid = []
    for d in conv_dirs:
        tpath = os.path.join(BRAIN_DIR, d, '.system_generated', 'logs', 'transcript.jsonl')
        if os.path.exists(tpath):
            try:
                st = os.stat(tpath)
                valid.append((tpath, st.st_mtime, st.st_size))
            except Exception:
                pass
    if not valid:
        return None, 0, 0
    valid.sort(key=lambda x: x[1], reverse=True)
    return valid[0]

def get_webui_db_state():
    try:
        cmd = [
            "docker", "exec", CONTAINER_NAME, "python3", "-c",
            "import sqlite3; conn=sqlite3.connect('/app/backend/data/webui.db'); print(conn.cursor().execute('SELECT COUNT(*), COALESCE(MAX(updated_at), 0) FROM chat_message;').fetchone())"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if res.returncode == 0 and res.stdout.strip():
            cleaned = res.stdout.strip().strip('()')
            parts = [p.strip() for p in cleaned.split(',')]
            return int(parts[0]), int(parts[1])
    except Exception:
        pass
    return None, None

def run_sync_to_webui(transcript_path):
    global sync_lock_until
    try:
        engine_dir = os.path.dirname(os.path.abspath(__file__))
        sync_script = os.path.join(engine_dir, "sync_antigravity.py")
        res = subprocess.run([sys.executable, sync_script], capture_output=True, text=True, timeout=30)
        if res.returncode == 0:
            print(f"[Watcher: A->B] Antigravity -> Open WebUI auto-sync OK at {time.strftime('%H:%M:%S')}")
            sync_lock_until = time.time() + 6.0
        else:
            print(f"[Watcher: A->B] Sync warning: {res.stderr or res.stdout}")
    except Exception as e:
        print(f"[Watcher: A->B] Error: {e}")

def run_sync_to_antigravity():
    global sync_lock_until
    try:
        cmd = [
            "docker", "exec", CONTAINER_NAME, "python3",
            "/app/workspace/omni-agent-os/governance/sync_webui_to_antigravity.py",
            "Otomatisasi Zero-Touch: Sesi kantor disinkronkan ke Antigravity"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if res.returncode == 0:
            print(f"[Watcher: B->A] Open WebUI -> Antigravity auto-sync OK at {time.strftime('%H:%M:%S')}")
            sync_lock_until = time.time() + 6.0
        else:
            print(f"[Watcher: B->A] Warning: {res.stderr or res.stdout}")
    except Exception as e:
        print(f"[Watcher: B->A] Error: {e}")

def main():
    global sync_lock_until
    print("[Watcher] Universal Two-Way Watcher Daemon started.")
    print(f" - Brain Dir: {BRAIN_DIR}")
    print(f" - Container: {CONTAINER_NAME}")

    last_file, last_mtime, last_size = get_latest_transcript_info()
    last_webui_count, last_webui_ts = get_webui_db_state()
    last_webui_check_time = time.time()

    while running:
        try:
            now = time.time()

            # Direction 1: Antigravity -> WebUI
            curr_file, curr_mtime, curr_size = get_latest_transcript_info()
            if curr_file and (curr_file != last_file or curr_mtime != last_mtime or curr_size != last_size):
                if now > sync_lock_until:
                    time.sleep(DEBOUNCE_DELAY)
                    try:
                        st = os.stat(curr_file)
                        last_mtime = st.st_mtime
                        last_size = st.st_size
                    except Exception:
                        pass
                    last_file = curr_file
                    run_sync_to_webui(curr_file)
                    last_webui_count, last_webui_ts = get_webui_db_state()

            # Direction 2: WebUI -> Antigravity
            if now - last_webui_check_time >= WEBUI_CHECK_INTERVAL:
                last_webui_check_time = now
                curr_count, curr_ts = get_webui_db_state()
                if curr_count is not None and last_webui_count is not None:
                    if curr_count > last_webui_count or (curr_ts > last_webui_ts and curr_count == last_webui_count):
                        if now > sync_lock_until:
                            time.sleep(DEBOUNCE_DELAY)
                            run_sync_to_antigravity()
                            last_webui_count, last_webui_ts = get_webui_db_state()
                    else:
                        last_webui_count = curr_count
                        last_webui_ts = curr_ts
                elif curr_count is not None:
                    last_webui_count = curr_count
                    last_webui_ts = curr_ts

            time.sleep(POLL_INTERVAL)
        except Exception:
            time.sleep(POLL_INTERVAL)

    print("[Watcher] Watcher Daemon cleanly stopped.")

if __name__ == "__main__":
    main()
