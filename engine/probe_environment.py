#!/usr/bin/env python3
"""
probe_environment.py
Host Scanner for Universal Open WebUI Antigravity Companion Stack.
Pure Python Standard Library. Generates structured environmental assessment JSON.
"""

import os
import sys
import json
import socket
import subprocess
import shutil

def check_command(cmd):
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        return res.returncode == 0, res.stdout.strip()
    except Exception as e:
        return False, str(e)

def is_port_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        res = s.connect_ex(('127.0.0.1', port))
        return res != 0

def find_available_port(start_port=3005, max_attempts=20):
    for p in range(start_port, start_port + max_attempts):
        if is_port_free(p):
            return p
    return None

def detect_opencode():
    indicators = []
    # 1. Process check
    ok, out = check_command("pgrep -l -i opencode")
    if ok and out:
        indicators.append(f"Running processes detected: {out}")
    
    # 2. Path checks
    home = os.path.expanduser("~")
    paths = [
        os.path.join(home, ".opencode"),
        os.path.join(home, ".config", "opencode"),
        "/opt/opencode",
        "/etc/opencode"
    ]
    found_paths = [p for p in paths if os.path.exists(p)]
    if found_paths:
        indicators.append(f"Directories found: {', '.join(found_paths)}")

    # 3. Systemd check
    ok, out = check_command("systemctl --user list-unit-files | grep -i opencode")
    if ok and out:
        indicators.append(f"Systemd user units found: {out}")

    return {
        "detected": len(indicators) > 0,
        "details": indicators,
        "found_paths": found_paths
    }

def detect_ollama():
    ollama_free = not is_port_free(11434)
    models = []
    if ollama_free:
        ok, out = check_command("curl -s http://127.0.0.1:11434/api/tags")
        if ok and out:
            try:
                data = json.loads(out)
                models = [m.get("name") for m in data.get("models", [])]
            except Exception:
                pass
    return {
        "online": ollama_free,
        "models": models,
        "has_nomic_embed": any("nomic-embed" in m for m in models)
    }

def main():
    print("🔍 [PROBE] Scanning Host Environment for Open WebUI Companion Stack...")

    uid = os.getuid()
    gid = os.getgid()
    user = os.getenv("USER", "unknown")
    home = os.path.expanduser("~")
    cwd = os.getcwd()

    docker_ok, docker_ver = check_command("docker --version")
    compose_ok, compose_ver = check_command("docker compose version")

    target_port = 3005
    port_3005_free = is_port_free(target_port)
    selected_port = target_port if port_3005_free else find_available_port(3006)

    opencode = detect_opencode()
    ollama = detect_ollama()

    assessment = {
        "host": {
            "user": user,
            "uid": uid,
            "gid": gid,
            "home": home,
            "cwd": cwd,
            "os": sys.platform
        },
        "prerequisites": {
            "docker": {"installed": docker_ok, "version": docker_ver},
            "docker_compose": {"installed": compose_ok, "version": compose_ver}
        },
        "ports": {
            "preferred_3005_free": port_3005_free,
            "recommended_port": selected_port
        },
        "opencode_status": opencode,
        "ollama_status": ollama,
        "recommended_strategy": (
            "STRATEGY_A_OPENCODE_TRANSITION" if opencode["detected"] else "STRATEGY_B_GREENFIELD"
        )
    }

    out_file = os.path.join(cwd, "probe_result.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(assessment, f, indent=2)

    print(f"✅ [PROBE SUCCESS] Assessment written to: {out_file}")
    print(f" - Recommended Strategy : {assessment['recommended_strategy']}")
    print(f" - Recommended Port     : {selected_port}")
    print(f" - OpenCode Detected    : {opencode['detected']}")
    print(f" - Local Ollama Online  : {ollama['online']} (Nomic Embed: {ollama['has_nomic_embed']})")
    print(f" - Host User UID:GID    : {uid}:{gid}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
