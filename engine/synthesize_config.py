#!/usr/bin/env python3
"""
synthesize_config.py
Generates tailored docker-compose.yml, .env, and systemd service
based on probe_result.json recommendations. Pure Python Standard Library.
"""

import os
import sys
import json
import secrets
import argparse

def main():
    parser = argparse.ArgumentParser(description="Synthesize Open WebUI Configuration")
    parser.add_argument("--workspace", default="", help="Path to project workspace")
    parser.add_argument("--omni-agent", default="/opt/ai-agent/omni-agent-os", help="Path to omni-agent-os governance")
    parser.add_argument("--port", type=int, default=0, help="Override WebUI port")
    parser.add_argument("--api-key", default="", help="OpenRouter API Key")
    args = parser.parse_args()

    probe_file = "probe_result.json"
    if not os.path.exists(probe_file):
        print("⚠️ probe_result.json not found. Running probe_environment.py first...")
        os.system(f"{sys.executable} engine/probe_environment.py")

    with open(probe_file, "r", encoding="utf-8") as f:
        probe = json.load(f)

    port = args.port or probe["ports"]["recommended_port"]
    workspace = args.workspace or probe["host"]["home"]
    omni_agent = args.omni_agent if os.path.exists(args.omni_agent) else workspace

    # 1. Synthesize docker-compose.yml
    template_compose = "templates/docker-compose.template.yml"
    with open(template_compose, "r", encoding="utf-8") as f:
        compose_content = f.read()

    compose_content = compose_content.replace("{{WEBUI_PORT}}", str(port))
    compose_content = compose_content.replace("{{PROJECT_WORKSPACE_PATH}}", workspace)
    compose_content = compose_content.replace("{{OMNI_AGENT_PATH}}", omni_agent)

    with open("docker-compose.yml", "w", encoding="utf-8") as f:
        f.write(compose_content)
    print(f"✔ Generated: docker-compose.yml (Port: {port}, Workspace: {workspace})")

    # 2. Synthesize .env
    secret_key = secrets.token_urlsafe(24)
    ollama_online = probe["ollama_status"]["online"]
    has_nomic = probe["ollama_status"]["has_nomic_embed"]

    template_env = "templates/env.template"
    with open(template_env, "r", encoding="utf-8") as f:
        env_content = f.read()

    api_key = args.api_key or os.getenv("OPENROUTER_API_KEY", "YOUR_OPENROUTER_API_KEY_HERE")

    env_content = env_content.replace("{{WEBUI_SECRET_KEY}}", secret_key)
    env_content = env_content.replace("{{OPENAI_API_BASE_URL}}", "https://openrouter.ai/api/v1")
    env_content = env_content.replace("{{OPENAI_API_KEY}}", api_key)
    env_content = env_content.replace("{{ENABLE_OLLAMA_API}}", "true" if ollama_online else "false")
    env_content = env_content.replace("{{OLLAMA_BASE_URL}}", "http://host.docker.internal:11434")
    env_content = env_content.replace("{{RAG_EMBEDDING_ENGINE}}", "ollama" if (ollama_online and has_nomic) else "")
    env_content = env_content.replace("{{RAG_EMBEDDING_MODEL}}", "nomic-embed-text:latest" if (ollama_online and has_nomic) else "")
    env_content = env_content.replace("{{RAG_OLLAMA_BASE_URL}}", "http://host.docker.internal:11434")

    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content)
    print("✔ Generated: .env (Cryptographic Secret Key & Embedding endpoints set)")

    # 3. Synthesize systemd service
    template_service = "templates/systemd_watcher.service"
    with open(template_service, "r", encoding="utf-8") as f:
        svc_content = f.read()

    py_path = sys.executable
    watcher_script = os.path.abspath("engine/watcher_daemon.py")

    svc_content = svc_content.replace("{{PYTHON_PATH}}", py_path)
    svc_content = svc_content.replace("{{WATCHER_SCRIPT_PATH}}", watcher_script)

    with open("lkt-webui-watcher.service", "w", encoding="utf-8") as f:
        f.write(svc_content)
    print(f"✔ Generated: lkt-webui-watcher.service (Watcher script: {watcher_script})")

    print("\n🎉 [SYNTHESIS COMPLETE] Ready to launch: docker compose up -d")

if __name__ == "__main__":
    main()
