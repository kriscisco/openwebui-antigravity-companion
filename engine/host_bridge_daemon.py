#!/usr/bin/env python3
"""
LKT Host Command Bridge Daemon
Exposes an audited Unix Domain Socket for Open WebUI to execute host commands
(e.g., systemctl, docker, package installations) with host user permissions.
Complies with Ponytail Minimalist Standard (Python stdlib only).
"""
import os
import sys
import json
import time
import socket
import signal
import subprocess

SOCKET_PATH = "/opt/ai-agent/omni-agent-os/governance/host_bridge.sock"
DEFAULT_CWD = "/home/kristian.admin/LKT Cyber Security Project"
LOG_PATH = "/opt/ai-agent/omni-agent-os/governance/host_bridge_audit.log"

running = True

def signal_handler(signum, frame):
    global running
    running = False

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def log_audit(cmd, cwd, exit_code, duration_ms):
    try:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_line = f"[{timestamp}] EXIT:{exit_code} ({duration_ms:.1f}ms) | CWD:{cwd} | CMD: {cmd}\n"
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(log_line)
    except Exception:
        pass

def handle_client(conn):
    try:
        raw_data = b""
        while True:
            chunk = conn.recv(65536)
            if not chunk:
                break
            raw_data += chunk
            if b"\n" in chunk or len(chunk) < 65536:
                break

        if not raw_data:
            return

        req = json.loads(raw_data.decode('utf-8'))
        command = req.get("command", "").strip()
        cwd = req.get("cwd") or DEFAULT_CWD
        timeout = int(req.get("timeout", 120))

        if not os.path.exists(cwd):
            cwd = "/home/kristian.admin"

        if not command:
            res = {"error": "Empty command provided", "exit_code": 1}
            conn.sendall(json.dumps(res).encode('utf-8'))
            return

        # Security check: Disallow destructive root deletion without explicit confirmation
        if command.startswith("rm -rf /") or command.startswith("rm -rf /*"):
            res = {"error": "Command blocked by Accidental Data Loss Prevention rule.", "exit_code": 126}
            conn.sendall(json.dumps(res).encode('utf-8'))
            return

        start_time = time.time()
        proc = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            executable="/bin/bash"
        )
        duration_ms = (time.time() - start_time) * 1000

        res = {
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "exit_code": proc.returncode,
            "duration_ms": round(duration_ms, 2)
        }

        log_audit(command, cwd, proc.returncode, duration_ms)
        conn.sendall(json.dumps(res).encode('utf-8'))

    except subprocess.TimeoutExpired:
        res = {"error": f"Command timed out after {timeout} seconds.", "exit_code": 124}
        conn.sendall(json.dumps(res).encode('utf-8'))
    except Exception as e:
        res = {"error": str(e), "exit_code": 1}
        try:
            conn.sendall(json.dumps(res).encode('utf-8'))
        except Exception:
            pass
    finally:
        conn.close()

def main():
    if os.path.exists(SOCKET_PATH):
        try:
            os.unlink(SOCKET_PATH)
        except OSError:
            pass

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    os.chmod(SOCKET_PATH, 0o666)  # Accessible from inside container mount
    server.listen(10)
    server.settimeout(1.0)

    print(f"[HostBridge] Listening on {SOCKET_PATH}")

    while running:
        try:
            conn, _ = server.accept()
            handle_client(conn)
        except socket.timeout:
            continue
        except Exception:
            break

    server.close()
    if os.path.exists(SOCKET_PATH):
        try:
            os.unlink(SOCKET_PATH)
        except OSError:
            pass
    print("[HostBridge] Daemon terminated.")

if __name__ == '__main__':
    main()
