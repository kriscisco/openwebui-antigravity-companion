# LKT CYBER & AI UNIFIED SYSTEM - ARCHITECTURAL KNOWLEDGE & RFC EXEMPLARS

> [!IMPORTANT]
> Dokumen ini merupakan bank pengetahuan baku arsitektur sistem, memuat seluruh riwayat rekayasa (97+ RFC ITIL v4) dan 19 keahlian teknis (Skills) resmi yang dijalankan oleh AI Agent Hermes dan tim. Dokumen ini menjadi pedoman memori operasional Open WebUI agar memiliki kapabilitas 1:1 identik dengan Antigravity.

---

## 1. ATURAN SIKLUS HIDUP RFC OTOMATIS (MANDATORY AUTONOMOUS LIFECYCLE)
Setiap kali Model / Hermes di Open WebUI diminta melakukan konfigurasi, coding, perbaikan, atau penambahan fitur, Hermes WAJIB mengeksekusi urutan 3-tahap tanpa menunggu pengingat manual:
1. **Buka RFC**: Panggil tool `create_system_rfc(title, affected_files_csv, description)`. Dapatkan `RFC_ID`.
2. **Eksekusi Perubahan**: Tulis/edit kode dengan `write_workspace_file` atau jalankan bash yang diaudit dengan `run_workspace_command`.
3. **Verifikasi & Tutup RFC**: Panggil tool `verify_and_close_rfc(rfc_id, qa_summary)` yang secara otomatis memvalidasi 15 Gate Zero-Defect ECC Baseline dan menutup tiket RFC dengan status SUCCESS.

---

## 2. BANK SKILLS SISTEM (28 ACTIVE SKILLS)

### Skill: `a11y-debugging`
- **Path**: `/home/kristian.admin/.gemini/config/plugins/chrome-devtools-plugin/skills/a11y-debugging/SKILL.md`
- **Deskripsi**: Uses Chrome DevTools MCP for accessibility (a11y) debugging and auditing based on web.dev guidelines. Use when testing semantic HTML, ARIA labels, focus states, keyboard navigation, tap targets, and color contrast.
```markdown
---
name: a11y-debugging
description: Uses Chrome DevTools MCP for accessibility (a11y) debugging and auditing based on web.dev guidelines. Use when testing semantic HTML, ARIA labels, focus states, keyboard navigation, tap targets, and color contrast.
---

## Core Concepts

**Accessibility Tree vs DOM**: Visually hiding an element (e.g., `CSS opacity:
0`) behaves differently for screen readers than `display: none` or
`aria-hidden="true"`. The `take_snapshot` tool returns the accessibility tree of
the page, which represents what assistive technologies "see", making it the most
reliable source of truth for semantic structure.

**Reading web.dev documentation**: If you need to research specific
accessibility guidelines (like
`https://web.dev/articles/accessible-tap-targets`), you can append ...
```

### Skill: `accidental-data-loss-prevention`
- **Path**: `/opt/ai-agent/omni-agent-os/skills/accidental-data-loss-prevention/SKILL.md`
- **Deskripsi**: STOP AND VERIFY before running any command or tool that results in irreversible data loss, data wiping, schema destruction, or mass deletions. Explicit user consent must be obtained.
```markdown
---
name: accidental-data-loss-prevention
description: STOP AND VERIFY before running any command or tool that results in irreversible data loss, data wiping, schema destruction, or mass deletions. Explicit user consent must be obtained.
---

# Accidental Data Loss Prevention (Guardrail Kritis)

> [!CAUTION]
> **ATURAN MUTLAK:** Sebelum menjalankan perintah apa pun yang menyebabkan kehilangan data permanen, kerusakan skema, atau penghapusan sumber daya tak terpulihkan, agen **WAJIB BERHENTI DAN MEMINTA PERSETUJUAN EKSPLISIT DARI USER / OWNER**.

## 1. Operasi yang Memerlukan Konfirmasi Wajib:
- **Database:** `DROP DATABASE`, `DROP TABLE`, `DROP SCHEMA`, `TRUNCATE`, atau `DELETE` massal tanpa klausa WHERE.
- **Sistem File:** `rm -rf /`, `rm -rf` pada folder root proyek atau direktori data p...
```

### Skill: `bento-uiux-spatial-design`
- **Path**: `/opt/ai-agent/omni-agent-os/skills/bento-uiux-spatial-design/SKILL.md`
- **Deskripsi**: Bento Grid UI/UX design rules, high-contrast pop-up styling, Pantone Pastel palette, responsive 50/50 desktop split, and rigid static height container with internal scroll down.
```markdown
---
name: bento-uiux-spatial-design
description: Bento Grid UI/UX design rules, high-contrast pop-up styling, Pantone Pastel palette, responsive 50/50 desktop split, and rigid static height container with internal scroll down.
---

# Bento Grid UI/UX & Spatial Design Standard

## 1. Prinsip Desain Antarmuka
- **Clean White Bento Grid:** Menggunakan kartu berbasis grid modular dengan border tegas (`border-2 border-slate-200`) dan elevasi pop-up kontras tinggi pada interaksi hover.
- **Palet Warna Pastel Pantone:**
  - Mint (`#10b981`): Status aktif, performa prima, RAM.
  - Sky (`#0ea5e9`): Telemetri jaringan, latensi, live stream.
  - Lavender / Indigo (`#6366f1` / `#7c3aed`): AI Agent Assistant, Dify Engine.
  - Butter / Amber (`#f59e0b`): Utilisasi penyimpanan, storage warning.
  - Rose ...
```

### Skill: `chrome-devtools`
- **Path**: `/home/kristian.admin/.gemini/config/plugins/chrome-devtools-plugin/skills/chrome-devtools/SKILL.md`
- **Deskripsi**: Uses Chrome DevTools via MCP for efficient debugging, troubleshooting and browser automation. Use when debugging web pages, automating browser interactions, analyzing performance, or inspecting network requests. This skill does not apply to `--slim` mode (MCP configuration).
```markdown
---
name: chrome-devtools
description: Uses Chrome DevTools via MCP for efficient debugging, troubleshooting and browser automation. Use when debugging web pages, automating browser interactions, analyzing performance, or inspecting network requests. This skill does not apply to `--slim` mode (MCP configuration).
---

## Core Concepts

**Browser lifecycle**: Browser starts automatically on first tool call using a persistent Chrome profile. Configure via CLI args in the MCP server configuration: `npx chrome-devtools-mcp@latest --help`.

**Page selection**: Tools operate on the currently selected page. Use `list_pages` to see available pages, then `select_page` to switch context.

**Element interaction**: Use `take_snapshot` to get page structure with element `uid`s. Each element has a uniqu...
```

### Skill: `cybersecurity-awareness`
- **Path**: `/home/kristian.admin/.gemini/config/skills/cybersecurity-awareness/SKILL.md`
- **Deskripsi**: Manage cybersecurity awareness presentation material, awareness training server, and engagement telemetry tracking. Use when editing or regenerating interactive awareness presentation HTML slides, checking the awareness backend on port 8888, verifying tracker metrics on port 5000, or updating training modules.
```markdown
---
name: cybersecurity-awareness
description: Manage cybersecurity awareness presentation material, awareness training server, and engagement telemetry tracking. Use when editing or regenerating interactive awareness presentation HTML slides, checking the awareness backend on port 8888, verifying tracker metrics on port 5000, or updating training modules.
---

# Cybersecurity Awareness & Presentation Management

## 1. Overview
This skill guides the AI agent in maintaining and operating the Cybersecurity Awareness presentation materials and real-time tracking services on server `10.121.1.21`.

## 2. Infrastructure & Services
- **Awareness Web Server**: `http://10.121.1.21:8888` (Docker container: `awareness-server`)
- **Awareness Telemetry Tracker**: `http://10.121.1.21:5000` (Docker conta...
```

### Skill: `debug-optimize-lcp`
- **Path**: `/home/kristian.admin/.gemini/config/plugins/chrome-devtools-plugin/skills/debug-optimize-lcp/SKILL.md`
- **Deskripsi**: Guides debugging and optimizing Largest Contentful Paint (LCP) using Chrome DevTools MCP tools. Use this skill whenever the user asks about LCP performance, slow page loads, Core Web Vitals optimization, or wants to understand why their page's main content takes too long to appear. Also use when the user mentions "largest contentful paint", "page load speed", "CWV", or wants to improve how fast their hero image or main content renders.
```markdown
---
name: debug-optimize-lcp
description: Guides debugging and optimizing Largest Contentful Paint (LCP) using Chrome DevTools MCP tools. Use this skill whenever the user asks about LCP performance, slow page loads, Core Web Vitals optimization, or wants to understand why their page's main content takes too long to appear. Also use when the user mentions "largest contentful paint", "page load speed", "CWV", or wants to improve how fast their hero image or main content renders.
---

## What is LCP and why it matters

Largest Contentful Paint (LCP) measures how quickly a page's main content becomes visible. It's the time from navigation start until the largest image or text block renders in the viewport.

- **Good**: 2.5 seconds or less
- **Needs improvement**: 2.5–4.0 seconds
- **Poor**: gr...
```

### Skill: `enterprise-change-enablement`
- **Path**: `/opt/ai-agent/omni-agent-os/skills/enterprise-change-enablement/SKILL.md`
- **Deskripsi**: ITIL v4 Change Enablement & ISO/IEC 27001 Audit Trail standard. Enforces automated RFC ticket creation, pre-change file snapshots, automatic disaster rollback on QA defect, and local LLM executive summaries.
```markdown
---
name: enterprise-change-enablement
description: ITIL v4 Change Enablement & ISO/IEC 27001 Audit Trail standard. Enforces automated RFC ticket creation, pre-change file snapshots, automatic disaster rollback on QA defect, and local LLM executive summaries.
---

# Enterprise Change Enablement & Automated Rollback

## 1. Alur Siklus Hidup Perubahan (RFC Lifecycle)
1. **Registrasi RFC (`create_rfc`):**
   Mendaftarkan nomor tiket perubahan (format: `RFC-YYYYMMDD_HHMMSS`), mengamankan backup snapshot file asli ke folder `snapshots/<RFC_ID>/`.
2. **Eksekusi Perubahan:**
   Worker agent menerapkan perubahan kode atau konfigurasi.
3. **Pengujian Mutu (SIT/UAT ECC):**
   Harness `ecc/verify.py` dijalankan secara menyeluruh.
4. **Pencatatan Hasil (`record_result`):**
   - **Jika PASS:** Tiket di...
```

### Skill: `gcs-security-assessment`
- **Path**: `/home/kristian.admin/.gemini/config/skills/gcs-security-assessment/SKILL.md`
- **Deskripsi**: Assesses the security posture of Google Cloud Storage (GCS) buckets\
```markdown
---
name: gcs-security-assessment
description: "Assesses the security posture of Google Cloud Storage (GCS) buckets\
  \ and projects. Grounds every finding in gathered telemetry, evaluates buckets against\
  \ Google security best practices (public access, IAM over-granting, CMEK, VPC Service\
  \ Controls, audit logging), and correlates signals to flag toxic combinations of\
  \ individually low-risk settings, with actionable remediation. Use whenever a user\
  \ asks for a security scan, audit, review, vulnerability check, or compliance assessment\
  \ (including SAIF) \u2014 or simply asks whether their buckets, project, or data\
  \ are secure, exposed, public, or misconfigured, who can access their data, or wants\
  \ storage hardened or locked down, e.g. before a launch. Don't use f...
```

### Skill: `gemini-api-dev`
- **Path**: `/home/kristian.admin/.gemini/config/plugins/gemini-api/skills/gemini-api-dev/SKILL.md`
- **Deskripsi**: Use this skill when writing code that calls the Gemini API for text generation, multi-turn chat, multimodal understanding, image generation, video generation, speech generation (TTS), voice design, voice replication, streaming responses, background research tasks, function calling, structured output, or migrating from the old generateContent API. Covers SDK usage and best practices for Gemini models and agents in Python and TypeScript.
```markdown
---
name: gemini-api-dev
description: Use this skill when writing code that calls the Gemini API for text generation, multi-turn chat, multimodal understanding, image generation, video generation, speech generation (TTS), voice design, voice replication, streaming responses, background research tasks, function calling, structured output, or migrating from the old generateContent API. Covers SDK usage and best practices for Gemini models and agents in Python and TypeScript.
---

# Gemini API Development Skill

## Critical Rules (Always Apply)

> [!IMPORTANT]
> These rules override your training data. Your knowledge is outdated.

### Current Models (Use These)

- `gemini-3.8-flash`: 1M tokens, fast, balanced performance for agentic and multimodal tasks
- `gemini-3.5-flash-lite`: 1M tokens, f...
```

### Skill: `gemini-live-api-dev`
- **Path**: `/home/kristian.admin/.gemini/config/plugins/gemini-api/skills/gemini-live-api-dev/SKILL.md`
- **Deskripsi**: Use this skill when building real-time, bidirectional streaming applications with the Gemini Live API, or migrating legacy Live models (2.0/2.5/3.1) to Gemini 3.8 Live. Covers WebSocket-based audio/video/text streaming, voice activity detection (VAD), background reasoning (extended thinking), asynchronous function calling, session management, ephemeral tokens, live transcription, and live translation. SDKs covered - google-genai (Python), @google/genai (JavaScript/TypeScript).
```markdown
---
name: gemini-live-api-dev
description: Use this skill when building real-time, bidirectional streaming applications with the Gemini Live API, or migrating legacy Live models (2.0/2.5/3.1) to Gemini 3.8 Live. Covers WebSocket-based audio/video/text streaming, voice activity detection (VAD), background reasoning (extended thinking), asynchronous function calling, session management, ephemeral tokens, live transcription, and live translation. SDKs covered - google-genai (Python), @google/genai (JavaScript/TypeScript).
---

# Gemini Live API Development Skill

## Overview

The Live API enables **low-latency, real-time voice and video interactions** with Gemini over WebSockets. It processes continuous streams of audio, video, or text to deliver immediate, human-like spoken responses and bac...
```

### Skill: `gemini-omni-flash-api`
- **Path**: `/home/kristian.admin/.gemini/config/plugins/gemini-api/skills/gemini-omni-flash-api/SKILL.md`
- **Deskripsi**: Use this skill for generative video editing, text-to-video, image-referenced video generation, first-frame-to-video, first-and-last-frame transitions, and video extensions using Gemini Omni 1.1 Flash (gemini-omni-1.1-flash) via the official google-genai SDK. Includes workflows for pre-processing/optimizing high-resolution or long source videos with ffmpeg, stripping audio for full sound regeneration, and handling turn-by-turn video editing and parallel execution.
```markdown
---
name: gemini-omni-flash-api
description: Use this skill for generative video editing, text-to-video, image-referenced video generation, first-frame-to-video, first-and-last-frame transitions, and video extensions using Gemini Omni 1.1 Flash (gemini-omni-1.1-flash) via the official google-genai SDK. Includes workflows for pre-processing/optimizing high-resolution or long source videos with ffmpeg, stripping audio for full sound regeneration, and handling turn-by-turn video editing and parallel execution.
---

# Gemini Omni Flash Skill

This skill uses the Gemini Omni 1.1 Flash model (`gemini-omni-1.1-flash`) to perform text to video generation, image to video generation (first frame and last frame transitions), video extensions (up to 40s), and video editing.

> [!WARNING]
> **Important...
```

### Skill: `google-antigravity-sdk`
- **Path**: `/home/kristian.admin/.gemini/config/plugins/google-antigravity-sdk/skills/google-antigravity-sdk/SKILL.md`
- **Deskripsi**: Design, implement, and debug autonomous AI agents and multi-agent systems using the Google Antigravity (AGY) SDK. ACTIVATE this skill when the user wants to create, configure, or orchestrate Google Antigravity agents.
```markdown
---
name: google-antigravity-sdk
description: "Design, implement, and debug autonomous AI agents and multi-agent systems using the Google Antigravity (AGY) SDK. ACTIVATE this skill when the user wants to create, configure, or orchestrate Google Antigravity agents."
---

# Google Antigravity SDK

## Installation & Setup

Before proceeding with any Google Antigravity tasks, ensure the environment is
ready:

-   **Verify Applicability**: If operating in an existing codebase, verify that
    using this Python SDK is possible and appropriate for the project.
-   **Check Dependencies**: Check if `google-antigravity` is listed in the
    project's dependencies (e.g., `requirements.txt`, `pyproject.toml`).
-   **Install Package**: Ensure the `google-antigravity` Python package is
    installed.
- ...
```

### Skill: `google-cloud-auth-verification`
- **Path**: `/home/kristian.admin/.gemini/config/skills/google-cloud-auth-verification/SKILL.md`
- **Deskripsi**: Mandatory Step 0 pre-flight execution order and authentication verification
```markdown
---
name: google-cloud-auth-verification
description: Mandatory Step 0 pre-flight execution order and authentication verification
  for Google Cloud Platform (GCP), Application Default Credentials (ADC), gcloud CLI,
  Spark, Dataproc, BigQuery, GCS, and notebook runtimes. Use whenever interacting
  with GCP resources, running Spark/PySpark pipelines, BigQuery queries, GCS paths
  (gs://), or creating/running notebooks.
license: Apache-2.0
metadata:
  version: v2
  publisher: google
---

# Google Cloud Authentication Guidelines

## Mandatory Pre-Flight Execution & Auth Hierarchy

> [!IMPORTANT] **Pre-Flight Execution Priority Order**: Before generating code,
> implementation plans, or executing tasks for any GCP or Notebook workload:
>
> 1.  **Verify Shell, Script & Notebook Credentials**: ...
```

### Skill: `gophish-landing-autofill`
- **Path**: `/home/kristian.admin/.gemini/config/skills/gophish-landing-autofill/SKILL.md`
- **Deskripsi**: Manage, generate, and synchronize Gophish phishing simulation landing pages with credential autofill and tracking capabilities. Use when updating landing page templates, synchronizing HTML to Gophish API or database, testing form autofill, or checking phishing campaign capture endpoints on port 80/3333/8000/8025.
```markdown
---
name: gophish-landing-autofill
description: Manage, generate, and synchronize Gophish phishing simulation landing pages with credential autofill and tracking capabilities. Use when updating landing page templates, synchronizing HTML to Gophish API or database, testing form autofill, or checking phishing campaign capture endpoints on port 80/3333/8000/8025.
---

# Gophish Landing Page Autofill & Synchronization

## 1. Overview
This skill guides the AI agent in managing, generating, and synchronizing landing pages for security awareness and simulated phishing assessments using Gophish on server `10.121.1.21`.

## 2. Infrastructure & Endpoints
- **Gophish Admin Interface**: `http://10.121.1.21:3333` (Docker container: `gophish`)
- **Simulation Web Server**: Port `80` / `8000` / `8025`
- *...
```

### Skill: `hierarchical-multi-agent-delegation`
- **Path**: `/opt/ai-agent/omni-agent-os/skills/hierarchical-multi-agent-delegation/SKILL.md`
- **Deskripsi**: Strict 3-Tier Hierarchical Asynchronous Multi-Agent Delegation Protocol. Owner -> Director translates & assigns brief to Lead Architect -> Lead Architect & Analis Token collaborate on 3-Tier LLM selection, token budgeting, agent matrix, and 4 Velocity SLAs -> Reports Pre-Flight Assessment to Owner -> Director & Lead Architect enter STANDBY mode awaiting Owner approval before any execution.
```markdown
---
name: hierarchical-multi-agent-delegation
description: Strict 3-Tier Hierarchical Asynchronous Multi-Agent Delegation Protocol. Owner -> Director translates & assigns brief to Lead Architect -> Lead Architect & Analis Token collaborate on 3-Tier LLM selection, token budgeting, agent matrix, and 4 Velocity SLAs -> Reports Pre-Flight Assessment to Owner -> Director & Lead Architect enter STANDBY mode awaiting Owner approval before any execution.
---

# Hierarchical Asynchronous Multi-Agent Delegation Protocol

## 1. Arsitektur Hirarki & Alur Kerja Lengkap (Mandat Standby Owner)

```
[1. OWNER (User)]
       │ (1. Memberikan Prompt / Request Baru)
       ▼
[2. AI GOVERNANCE DIRECTOR (Chief Orchestrator)]
       │ • Menterjemahkan visi & kebutuhan bisnis Owner menjadi sasaran teknis yang t...
```

### Skill: `managing-python-dependencies`
- **Path**: `/opt/ai-agent/omni-agent-os/skills/managing-python-dependencies/SKILL.md`
- **Deskripsi**: Ensures proper Python dependency isolation and packaging, avoiding global pip install conflicts and maintaining project virtual environments.
```markdown
---
name: managing-python-dependencies
description: Ensures proper Python dependency isolation and packaging, avoiding global pip install conflicts and maintaining project virtual environments.
---

# Managing Python Dependencies (Standar Isolasi Dependensi)

## 1. Aturan Dasar
- **DILARANG** melakukan instalasi paket global secara serampangan menggunakan `sudo pip install` yang dapat merusak paket sistem operasi Ubuntu/Debian (`PEP 668: externally-managed-environment`).
- Gunakan virtual environment terisolasi (`venv`) untuk setiap modul proyek:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

## 2. Kebutuhan Library Eksternal
Sebelum menyarankan atau mengeksekusi kode Python dengan `import` pihak ketiga:
1. Periksa ketersediaan library ...
```

### Skill: `matrix-element-chat`
- **Path**: `/home/kristian.admin/.gemini/config/skills/matrix-element-chat/SKILL.md`
- **Deskripsi**: Manage and monitor the on-premise Matrix Synapse homeserver and Element Web chat application stack. Use when checking Matrix chat services on port 8081 (Element Web) and port 8008 (Synapse), inspecting Postgres/Redis chat databases, troubleshooting user registration or messaging issues, or configuring chat bot integrations.
```markdown
---
name: matrix-element-chat
description: Manage and monitor the on-premise Matrix Synapse homeserver and Element Web chat application stack. Use when checking Matrix chat services on port 8081 (Element Web) and port 8008 (Synapse), inspecting Postgres/Redis chat databases, troubleshooting user registration or messaging issues, or configuring chat bot integrations.
---

# Matrix Synapse & Element Web Chat Management

## 1. Overview
This skill provides operational knowledge and troubleshooting workflows for the self-hosted decentralized chat stack running on server `10.121.1.21`.

## 2. Infrastructure & Endpoints
- **Element Web UI**: `http://10.121.1.21:8081` (Docker container: `matrix-element`)
- **Matrix Synapse API**: `http://10.121.1.21:8008` (Docker container: `matrix-synapse`)
- **B...
```

### Skill: `memory-leak-debugging`
- **Path**: `/home/kristian.admin/.gemini/config/plugins/chrome-devtools-plugin/skills/memory-leak-debugging/SKILL.md`
- **Deskripsi**: Diagnoses and resolves memory leaks in JavaScript/Node.js applications. Use when a user reports high memory usage, OOM errors, or wants to analyze heapsnapshots or run memory leak detection tools like memlab.
```markdown
---
name: memory-leak-debugging
description: Diagnoses and resolves memory leaks in JavaScript/Node.js applications. Use when a user reports high memory usage, OOM errors, or wants to analyze heapsnapshots or run memory leak detection tools like memlab.
---

# Memory Leak Debugging

This skill provides expert guidance and workflows for finding, diagnosing, and fixing memory leaks in JavaScript and Node.js applications.

## Core Principles

- **Prefer `memlab`:** Do NOT attempt to read raw `.heapsnapshot` files directly, as they are extremely large and will consume too many tokens. Always recommend and use `memlab` to process snapshots and identify leak traces.
- **Isolate the Leak:** Determine if the leak is in the browser (client-side) or Node.js (server-side).
- **Common Culprits:** Look...
```

### Skill: `ml-best-practices`
- **Path**: `/home/kristian.admin/.gemini/config/skills/ml-best-practices/SKILL.md`
- **Deskripsi**: |
```markdown
---
name: ml-best-practices
description: |
  CRITICAL RULE: You MUST use this skill whenever the task involves any machine learning tasks or data analysis.
  Use this skill if the user's prompt or requirements mention any of the following:
    * Clustering
    * Classification
    * Regression
    * Time series forecasting
    * Statistical testing
    * Model comparison
    * ML
    * Data analysis

  SQL/BigQuery ML HANDOFF: If the user requires a SQL solution, use this skill to dictate the ANALYSIS STEPS (e.g., markdown analysis cells, visualization logic), but defer to `bigquery` for all SQL syntax.
license: Apache-2.0
metadata:
  version: v1
  publisher: google
---

# ML Best Practices

I want to read a story about the data, not just run code. Ensure every code cell
is followed by a m...
```

### Skill: `openvas-vulnerability-scanner`
- **Path**: `/home/kristian.admin/.gemini/config/skills/openvas-vulnerability-scanner/SKILL.md`
- **Deskripsi**: Manage and operate the OpenVAS / Greenbone Vulnerability Management scanner container in Docker. Use when checking OpenVAS status on port 8080 (GVM Web UI mapped to 9392), managing vulnerability scan tasks, triggering feed synchronization, restarting the scanner container, or reviewing scan report outputs.
```markdown
---
name: openvas-vulnerability-scanner
description: Manage and operate the OpenVAS / Greenbone Vulnerability Management scanner container in Docker. Use when checking OpenVAS status on port 8080 (GVM Web UI mapped to 9392), managing vulnerability scan tasks, triggering feed synchronization, restarting the scanner container, or reviewing scan report outputs.
---

# OpenVAS Vulnerability Scanner Management

## 1. Overview
This skill guides the AI agent in operating and maintaining the OpenVAS (Greenbone) security scanner running in Docker on server `10.121.1.21`.

## 2. Infrastructure & Endpoints
- **Greenbone Security Assistant (GSA Web UI)**: `https://10.121.1.21:8080` (mapped to container port `9392`)
- **Docker Container**: `openvas` (Image: `immauss/openvas:26.06.28.01`)
- **Configurat...
```

### Skill: `ponytail-minimalist`
- **Path**: `/opt/ai-agent/omni-agent-os/skills/ponytail-minimalist/SKILL.md`
- **Deskripsi**: Ponytail Anti-Overengineering Framework. Enforces the 7-step Decision Ladder of the "lazy senior developer" to generate the absolute minimal, zero-bloat solution before writing code. Reduces output tokens by 40-60% while strictly protecting security boundaries and error handling.
```markdown
---
name: ponytail-minimalist
description: Ponytail Anti-Overengineering Framework. Enforces the 7-step Decision Ladder of the "lazy senior developer" to generate the absolute minimal, zero-bloat solution before writing code. Reduces output tokens by 40-60% while strictly protecting security boundaries and error handling.
---

# Ponytail Anti-Overengineering & Minimalist Code Framework

## 1. Filosofi & Paradigma Utama
Model AI sering kali menghasilkan kode berlebihan (*over-engineering*): menambahkan kelas kompleks, membuat boilerplate berlembar-lembar, atau menginstal pustaka eksternal yang tidak diperlukan.

**Ponytail** memaksa AI coding agent untuk berpikir seperti *"Lazy Senior Developer"*:
> **"Kode terbaik adalah kode yang tidak perlu ditulis. Solusi paling stabil dan cepat adalah ...
```

### Skill: `report-mimic-synthesizer`
- **Path**: `/opt/ai-agent/omni-agent-os/skills/report-mimic-synthesizer/SKILL.md`
- **Deskripsi**: Automatically generates new reports by mimicking the exact structure, tone, format, and section depth of an existing reference report, while synthesizing relevant data extracted from multiple files (CSV, JSON, Markdown, text, logs).
```markdown
---
name: report-mimic-synthesizer
description: Automatically generates new reports by mimicking the exact structure, tone, format, and section depth of an existing reference report, while synthesizing relevant data extracted from multiple files (CSV, JSON, Markdown, text, logs).
---

# Report Mimic & Data Synthesizer Skill

## 1. Konsep & Tujuan
Skill ini dirancang untuk menyelesaikan tugas penyusunan laporan berbasis acuan (*Reference-Conditioned Document Synthesis*):
1. **Meniru Gaya Laporan Sebelumnya (*Style & Structure Mimicry*):**
   Menganalisis dokumen acuan untuk mengekstraksi hirarki judul (`#`, `##`, `###`), pola ringkasan eksekutif, susunan tabel, gaya bahasa (*tone* formal/teknis/manajemen), serta tingkat kedalaman analisis.
2. **Kombinasi Data Multi-Sumber (*Multi-Source Dat...
```

### Skill: `reverse-engineer-anything`
- **Path**: `/home/kristian.admin/.gemini/config/skills/reverse-engineer-anything/SKILL.md`
- **Deskripsi**: Reverse engineer native, managed, Electron/JavaScript, packaged, firmware, and browser targets with REA. Use shipped-artifact or requested runtime evidence to explain features, compare versions, decompile code, or guide a reconstruction. Skip REA for ordinary source-repository architecture analysis.
```markdown
---
name: reverse-engineer-anything
description: Reverse engineer native, managed, Electron/JavaScript, packaged, firmware, and browser targets with REA. Use shipped-artifact or requested runtime evidence to explain features, compare versions, decompile code, or guide a reconstruction. Skip REA for ordinary source-repository architecture analysis.
metadata:
  version: "42"
  tool_count: 207
---

# REA

Use REA when a claim depends on a shipped binary or package, decompilation,
passive application runtime evidence, or comparison with
behavior not established by available source. For ordinary analysis of a
complete source repository, use normal repository tools and do not run REA
readiness or provider commands.

## Connect only when needed

Installing this skill supplies instructions; it doe...
```

### Skill: `ruang-3d-virtual-office`
- **Path**: `/opt/ai-agent/omni-agent-os/skills/ruang-3d-virtual-office/SKILL.md`
- **Deskripsi**: Integrates Hermes Agent 3D Virtual Office and Three.js spatial digital twin for real-time visual monitoring of multi-agent activities on port 3001.
```markdown
---
name: ruang-3d-virtual-office
description: Integrates Hermes Agent 3D Virtual Office and Three.js spatial digital twin for real-time visual monitoring of multi-agent activities on port 3001.
---

# Ruang 3D Virtual Office Integration

## 1. Konsep & Arsitektur
*Ruang* adalah kantor virtual 3D berbasis WebGL (Three.js) yang memvisualisasikan seluruh agen di meja kerja mereka secara live di port `:3001`.
- Agen yang sedang mengeksekusi tugas digambarkan sedang mengetik aktif di meja kerja.
- Agen yang sedang idle/standby berada di area lounge kantor.
- Memberikan transparansi visual langsung kepada pimpinan/Owner mengenai agen mana yang sedang bekerja.

## 2. Cara Kerja & Integrasi
- Engine Ruang berjalan sebagai user service systemd (`ruang.service`).
- Menggunakan adaptor `hermes` CLI ...
```

### Skill: `skill-repair`
- **Path**: `/home/kristian.admin/.gemini/config/skills/skill-repair/SKILL.md`
- **Deskripsi**: |
```markdown
---
name: skill-repair
description: |
  Use this to fix and re-install agent skills that have failed installation.
  This skill provides the necessary context and permissions to surgically update
  the `manifest.json` after a fix has been applied.
license: Apache-2.0
metadata:
  version: v1
  publisher: google
---

# Skill Repair Assistant

You have been tasked with fixing a broken agent skill. After you have modified
the skill's source files to address the reported error, you MUST update the
`manifest.json` to reflect that the skill is now repaired.

## Skill Context

-   **Skill ID**: The unique identifier for the skill (e.g., `my-skill`).
-   **Source Path**: Where the skill's source files are located.
-   **Installed Path**: Where the skill is installed/replicated.
-   **Manifest Path*...
```

### Skill: `troubleshooting`
- **Path**: `/home/kristian.admin/.gemini/config/plugins/chrome-devtools-plugin/skills/troubleshooting/SKILL.md`
- **Deskripsi**: Uses Chrome DevTools MCP and documentation to troubleshoot connection and target issues. Trigger this skill when list_pages, new_page, or navigate_page fail, or when the server initialization fails.
```markdown
---
name: troubleshooting
description: Uses Chrome DevTools MCP and documentation to troubleshoot connection and target issues. Trigger this skill when list_pages, new_page, or navigate_page fail, or when the server initialization fails.
---

## Troubleshooting Wizard

You are acting as a troubleshooting wizard to help the user configure and fix their Chrome DevTools MCP server setup. When this skill is triggered (e.g., because `list_pages`, `new_page`, or `navigate_page` failed, or the server wouldn't start), follow this step-by-step diagnostic process:

### Step 1: Find and Read Configuration

Your first action should be to locate and read the MCP configuration file. Search for the following files in the user's workspace: `.mcp.json`, `gemini-extension.json`, `.claude/settings.json`, `.v...
```

### Skill: `ui-ux-pro-max`
- **Path**: `/opt/ai-agent/omni-agent-os/skills/ui-ux-pro-max/SKILL.md`
- **Deskripsi**: UI/UX design intelligence for web, mobile, and desktop. This skill should be used when designing, building, reviewing, or fixing interfaces, including pages, components, design systems, accessibility, interaction, responsive layout, typography, color, charts, and stack-specific UI implementation. Searchable local data: 79 searchable styles (50 active), 192 product palettes and reasoning profiles, 74 font pairings, 119 UX guidelines, 105 icons, 17 GSAP presets, 25 chart types, and 22 stacks.
```markdown
---
name: ui-ux-pro-max
description: "UI/UX design intelligence for web, mobile, and desktop. This skill should be used when designing, building, reviewing, or fixing interfaces, including pages, components, design systems, accessibility, interaction, responsive layout, typography, color, charts, and stack-specific UI implementation. Searchable local data: 79 searchable styles (50 active), 192 product palettes and reasoning profiles, 74 font pairings, 119 UX guidelines, 105 icons, 17 GSAP presets, 25 chart types, and 22 stacks."
---

# UI/UX Pro Max - Design Intelligence

Searchable local UI/UX guidance: 79 searchable styles (50 active), 192 product palettes and exact reasoning profiles, 74 font pairings, 119 UX guidelines, 105 curated icons, 17 GSAP presets, 25 chart types, and 22 technol...
```

### Skill: `zero-defect-ecc-testing`
- **Path**: `/opt/ai-agent/omni-agent-os/skills/zero-defect-ecc-testing/SKILL.md`
- **Deskripsi**: Enforces TDD multi-gate zero-defect automated testing harness (ECC - Enhanced Coding Capabilities). Ensures 100% PASS with 0 defects before any code change is released to production.
```markdown
---
name: zero-defect-ecc-testing
description: Enforces TDD multi-gate zero-defect automated testing harness (ECC - Enhanced Coding Capabilities). Ensures 100% PASS with 0 defects before any code change is released to production.
---

# Zero-Defect ECC Testing Framework (SIT/UAT QA Standard)

## 1. Filosofi Zero-Defect
Sistem menolak rilis kode yang cacat atau berhalusinasi. Seluruh perubahan kode harus melewati **Verification Gate Harness** melalui skrip `ecc/verify.py` dengan hasil akhir **100% PASS (0 Defect)**.

## 2. Struktur 5-Gate Standar
- **[Gate 1] Static Code Integrity & Syntax Check (L1):**
  Kompilasi Python (`py_compile`) tanpa error sintaks dan validasi elemen DOM antarmuka web.
- **[Gate 2] Component Logic & Metric Calculation Unit Tests (L2):**
  Pengujian unit kalkulasi d...
```

---

## 3. RIWAYAT & REKAM JEJAK RFC ARSITEKTURAL (98 HISTORICAL RFCS)

| RFC ID | Waktu | Judul Perubahan | Pelaksana | Status | File Terdampak Utama |
| :--- | :--- | :--- | :--- | :---: | :--- |
| `RFC-20261021_073913` | 21 October 2026, 07:39:14 WIB | Integrasi NusaGate AI Gateway ke DeepSeek V4.1 Flash dan V4 Pro | Lead Software Architect | **SUCCESS** | `.env, .env, token_analyzer.py` |
| `RFC-20261021_080935` | 21 October 2026, 08:09:35 WIB | Pemberlakuan Kebijakan Wajib Logging Agen, Model, Token, dan RPM pada Change Management | Lead Software Architect & Change Management | **SUCCESS** | `STANDAR_SOP_RFC_GOVERNANCE.md, STANDAR_SOP_RFC_GOVERNANCE.md, 04_change_management.md` |
| `RFC-20261021_232005` | 21 October 2026, 23:20:05 WIB | Deployment Hermes Agent sebagai Engine Lead Arsitek, Ingesti Knowledge 9 Agen & History Change Management | Lead Arsitek (Hermes) & Analis Token & Change Management | **SUCCESS** | `02_lead_architect.md, STANDAR_SOP_RFC_GOVERNANCE.md, STANDAR_SOP_RFC_GOVERNANCE.md` |
| `RFC-20261022_001310` | 22 October 2026, 00:13:10 WIB | Pembaruan Model Director ke Gemini-3.5-Flash-Lite (Primary 30 RPM) dan Gemini-3.8-Flash (Fallback) | Lead Arsitek (Hermes) & Analis Token & Change Management | **SUCCESS** | `01_director.md, token_analyzer.py, token_analyzer.py` |
| `RFC-20261022_002216` | 22 October 2026, 00:22:16 WIB | Deployment Ponytail Anti-Overengineering Framework pada Lead Arsitek Hermes, FinOps, dan SOP Tata Kelola | Lead Arsitek (Hermes) & Analis Token & Change Management | **SUCCESS** | `SKILL.md, 02_lead_architect.md, token_analyzer.py` |
| `RFC-20261022_015317` | 22 October 2026, 01:53:17 WIB | Deployment Chrome DevTools MCP Server untuk Otomasi UI, Visual QA, dan Web Debugging | Lead Arsitek (Hermes) & Design UX & SIT/UAT QA | **SUCCESS** | `config.yaml, 05_qa_ecc.md, 06_ui_ux_designer.md` |
| `RFC-20261023_000757` | 23 October 2026, 00:07:57 WIB | Implementasi Box Widget Gophish Phishing Controller pada Dashboard Unified Portal Bento Grid | Lead Arsitek (Hermes), Red Team, Design UX, Change Management | **SUCCESS** | `server.py, gophish_bridge.py, index.html` |
| `RFC-20261024_032239` | 24 October 2026, 03:22:39 WIB | Integrasi & Deployment Offline Tooling ui-ux-pro-max-skill | Lead Architect & Design UX | **SUCCESS** | `06_ui_ux_designer.md` |
| `RFC-20261024_042522` | 24 October 2026, 04:25:22 WIB | OpenVAS Feed Parallel Sync, Backend Engine Tuning & Portal Live Progress Dashboard | Lead Architect (Hermes) & Red Team & Design UX | **SUCCESS** | `openvas_bridge.py, openvas_bridge.py, server.py` |
| `RFC-20261024_070713` | 24 October 2026, 07:07:13 WIB | OpenVAS Real-Time Database Ingestion Telemetry Integration | Lead Architect & Subagent | **SUCCESS** | `openvas_bridge.py, openvas_bridge.py, index.html` |
| `RFC-20261024_081124` | 24 October 2026, 08:11:24 WIB | REA (Reverse Engineer Anything) MCP & Skill Deployment | Lead Architect & Subagent | **SUCCESS** | `mcp_config.json, SKILL.md` |
| `RFC-20261024_110451` | 24 October 2026, 11:04:51 WIB | OpenVAS Feed Status Portal Synchronization & GMP Single Source of Truth | Lead Architect (Hermes) | **SUCCESS** | `openvas_bridge.py, openvas_bridge.py, openvas_feed_sync.json` |
| `RFC-20261024_121935` | 24 October 2026, 12:19:35 WIB | OpenVAS Feed Automatic Scheduler & Portal UI Control Integration | Lead Architect (Hermes) | **SUCCESS** | `openvas_bridge.py, openvas_bridge.py, server.py` |
| `RFC-20261024_124112` | 24 October 2026, 12:41:12 WIB | Build LKT Network OSD macOS App & DMG Installer (Sonoma - Golden Gate) | Lead Architect (Hermes) & Red Team | **SUCCESS** | `server.py, server.py` |
| `RFC-20261026_084014` | 26 October 2026, 08:40:14 WIB | Integrate Hermes Agent Gateway to Telegram with Autonomous Tool Calling & Feedback Loop | Lead Arsitek (Hermes) | **SUCCESS** | `config.yaml, .env, bot.py` |
| `RFC-20261027_142933` | 27 October 2026, 14:29:33 WIB | Adopsi 8-Point Website Discovery Assessment Protocol ke General Rules | Lead Architect (Hermes) & Director | **SUCCESS** | `general_rules.md, general_rules.md, AGENTS.md` |
| `RFC-20261028_181444` | 28 October 2026, 18:14:44 WIB | Integrasi Matriks Operasional & Jadwal Pemadaman Listrik Site Sumatera ke LKT AI Agent Portal | Lead Architect (Hermes) | **SUCCESS** | `site_operations_matrix.json, it_support_bridge.py, semantic_cache.json` |
| `RFC-20261028_181636` | 28 October 2026, 18:16:36 WIB | Integrasi Matriks Jaringan Head Office & Regional Hub ke LKT AI Agent Portal | Lead Architect (Hermes) | **SUCCESS** | `head_office_network_matrix.json, it_support_bridge.py, semantic_cache.json` |
| `RFC-20261028_182112` | 28 October 2026, 18:21:12 WIB | Integrasi Quick-Access Admin & Tools Link Directory ke LKT AI Agent Portal | Lead Architect (Hermes) | **SUCCESS** | `quick_links_directory.json, it_support_bridge.py, semantic_cache.json` |
| `RFC-20261028_182848` | 28 October 2026, 18:28:48 WIB | Gabungan: Ping Diagnostic 15x Looping & Dual Action URL Handler (Copy & Buka Tab Baru) | Lead Architect (Hermes) | **SUCCESS** | `index.html, server.py, index.html` |
| `RFC-20261028_184534` | 28 October 2026, 18:45:34 WIB | Intelligent Fuzzy Disambiguation & Knowledge Graph Matrix Expansion | Lead Architect (Hermes) | **SUCCESS** | `it_support_bridge.py, graph_database.json, semantic_cache.json` |
| `RFC-20261028_185423` | 28 October 2026, 18:54:23 WIB | Integrasi 230 Site Topologi Core (Termasuk SAU 1 & SAU 2) & Auto-Ping Action Card | Lead Architect (Hermes) | **SUCCESS** | `graph_database.json, it_support_bridge.py, semantic_cache.json` |
| `RFC-20261028_190837` | 28 October 2026, 19:08:37 WIB | Integrasi Tombol Aksi (Ping & Salin) Head Office & Pemulihan IP Publik SAM-1 | Lead Architect (Hermes) | **SUCCESS** | `it_support_bridge.py, graph_database.json, semantic_cache.json` |
| `RFC-20261029_074921` | 29 October 2026, 07:49:21 WIB | Integrasi 6 Tombol Quick-Launch Top Bar & Tombol WhatsApp Web (Msg) IT Support | Lead Architect (Hermes) | **SUCCESS** | `index.html, it_support_bridge.py, quick_links_directory.json` |
| `RFC-20261029_080805` | 29 October 2026, 08:08:05 WIB | Normalisasi Gateway .4.1 & Perbaikan Router URL WhatsApp Web Direct Chat | Lead Architect (Hermes) | **SUCCESS** | `it_support_bridge.py, site_operations_matrix.json, graph_database.json` |
| `RFC-20261029_090123` | 29 October 2026, 09:01:23 WIB | Repair WhatsApp Direct Chat Routing Protocol | Hermes (Lead Architect) | **SUCCESS** | `it_support_bridge.py, index.html, semantic_cache.json` |
| `RFC-20261029_092621` | 29 October 2026, 09:26:21 WIB | Meta API WhatsApp Algorithm with Site Down Auto-Template | Hermes (Lead Architect) | **SUCCESS** | `it_support_bridge.py, index.html, semantic_cache.json` |
| `RFC-20261029_095459` | 29 October 2026, 09:54:59 WIB | Vertical Resizing Engine for LKT AI Agent Chat Box | Hermes (Lead Architect) | **SUCCESS** | `index.html` |
| `RFC-20261029_114922` | 29 October 2026, 11:49:22 WIB | Update IT Support Directory 2026 with Contact Telephones & Direct Msg Actions | Hermes (Lead Architect) | **SUCCESS** | `it_support_directory.json, it_support_bridge.py, semantic_cache.json` |
| `RFC-20261029_120106` | 29 October 2026, 12:01:06 WIB | Interactive Reverse-IP Topology & Deep Personnel Placement Engine | Hermes (Lead Architect) | **SUCCESS** | `it_support_bridge.py, semantic_cache.json` |
| `RFC-20261029_122526` | 29 October 2026, 12:25:26 WIB | Multi-Device Isolated Layout Sessions & Windows PC Size Normalization | Hermes (Lead Architect) | **SUCCESS** | `server.py, index.html, layout.json` |
| `RFC-20261029_130322` | 29 October 2026, 13:03:22 WIB | Universal Height Engine, Retro/Pastel Theme with Manual Color Customizer, Clean Buttons & Buka Semua Fix | Hermes (Lead Architect) | **SUCCESS** | `index.html, index.html` |
| `RFC-20261029_132406` | 29 October 2026, 13:24:06 WIB | Hotfix JS Syntax Error, High-Contrast Retro/Pastel Palettes & Windows Layout Normalization | Hermes (Lead Architect) | **SUCCESS** | `index.html, index.html` |
| `RFC-20261029_135053` | 29 October 2026, 13:50:53 WIB | Optimasi Responsive Mobile Multi-Browser (Android & iOS) | Lead Architect Hermes | **SUCCESS** | `index.html, index.html` |
| `RFC-20261029_152109` | 29 October 2026, 15:21:09 WIB | Engine Log Vault Dinamis (!log & !bukalog) | Lead Architect Hermes | **SUCCESS** | `server.py, server.py, index.html` |
| `RFC-20261029_153401` | 29 October 2026, 15:34:01 WIB | Multi-Entity Batch Log Parser & Retroactive Decomposition | Lead Architect Hermes | **SUCCESS** | `log_vault_bridge.py, log_vault_bridge.py` |
| `RFC-20261029_154701` | 29 October 2026, 15:47:01 WIB | Pembersihan Tag Coding/HTML dari Formatter !bukalog | Lead Architect Hermes | **SUCCESS** | `log_vault_bridge.py, log_vault_bridge.py` |
| `RFC-20261030_183204` | 30 October 2026, 18:32:04 WIB | Implementasi Hermes Orchestrator Bridge & Validasi Orkestrasi Paralel Multi-Agent | Lead Architect Hermes | **SUCCESS** | `hermes_orchestrator.py` |
| `RFC-20261031_025600-REV1` | 31 October 2026, 02:56:00 WIB | Implementasi RFC State Machine, Antigravity Live Progress & Interactive Approval di Telegram Bot | Lead Architect Hermes | **SUCCESS** | `bot.py` |
| `RFC-20261031_052500-VISION` | 31 October 2026, 05:25:00 WIB | Implementasi AI Multimodal Vision (Gemini 3.8 Flash) pada Telegram Bot Gateway | Lead Architect Hermes | **SUCCESS** | `bot.py` |
| `RFC-20261031_063800-CLEAN-UI` | 31 October 2026, 06:38:00 WIB | Pembersihan Tombol Opsi Cepat Telegram (Clean UI) & Perbaikan NameError execute_approved_rfc | Lead Architect Hermes | **SUCCESS** | `bot.py` |
| `RFC-20261031_075500-MULTI-TURN-MEMORY` | 31 October 2026, 07:55:00 WIB | Aktivasi Multi-Turn Rolling Memory Buffer & High-Speed Dual-Engine Hermes AI di Telegram | Lead Architect Hermes | **SUCCESS** | `bot.py` |
| `RFC-20261031_085000-TELEGRAM-GITHUB-INTEL` | N/A | Integrasi Native GitHub AI Forum & Config Intelligence pada Hermes Telegram Bot | Lead Architect | **SUCCESS** | `-` |
| `RFC-20261031_092000-TELEGRAM-SEAMLESS-DISCUSS` | N/A | Implementasi Conversational Question Guard & Hermes Advisory Styling di Telegram Bot | Lead Architect | **SUCCESS** | `-` |
| `RFC-20261031_093000-HERMES-DEEP-TECH-INTEL` | N/A | Aktivasi Kemampuan Diskusi Mendalam General IT, Coding, Software, Hardware & 7 DeepSeek Power Capabilities | Lead Architect | **SUCCESS** | `-` |
| `RFC-20261031_101000-HERMES-NATURAL-INDONESIAN` | N/A | Implementasi Skill Persona Bahasa Indonesia Natural & Mobile Viewport Clean Formatter | Lead Architect | **SUCCESS** | `-` |
| `RFC-20261031_102000-HERMES-AUTONOMOUS-TOOL-LOOP` | N/A | Implementasi Autonomous Tool Loop Interceptor & Sanitizer pada Hermes Telegram Bot | Lead Architect | **SUCCESS** | `-` |
| `RFC-20261031_140000-HERMES-SHELL-EXEC-GROUNDING` | N/A | Penguatan Hak Eksekusi Shell Host, Perpanjangan Timeout NusaGate 60s & Smart Audit Patch Hook | Lead Architect | **SUCCESS** | `-` |
| `RFC-20261103_001441` | 03 November 2026, 00:14:41 WIB | Integrasi Generator Mgnt Report DOCX di Box Portal PentAGI | Lead Architect (Hermes) & Design UX | **SUCCESS** | `pentagi_bridge.py, pentagi_bridge.py, server.py` |
| `RFC-20261103_003151` | 03 November 2026, 00:31:51 WIB | Hotfix Routing Unduhan DOCX dan Penyelarasan Format 10 Bagian | Lead Architect (Hermes) & Design UX | **SUCCESS** | `server.py, server.py, dynamic_pentest_docx.py` |
| `RFC-20261103_004248` | 03 November 2026, 00:42:48 WIB | Hotfix Unduhan Browser Blob Handler & Socket Buffer Flush | Lead Architect (Hermes) & Design UX | **SUCCESS** | `server.py, server.py, index.html` |
| `RFC-20261103_010000` | 03 November 2026, 01:00:00 WIB | Penambahan Kolom Prompt Automation & Tombol Jalankan Pentest di Box PentAGI | Lead Architect (Hermes) & Design UX | **SUCCESS** | `pentagi_bridge.py, pentagi_bridge.py, server.py` |
| `RFC-20261103_120354` | 03 November 2026, 12:03:54 WIB | Integrasi 4 Top-Tier Pentest LLM ke PentAGI dan Portal Controller | Lead Architect (Hermes) & Design UX | **SUCCESS** | `docker-compose.override.yml, .env, pentagi_bridge.py` |
| `RFC-20261103_122258` | 03 November 2026, 12:22:58 WIB | Rangkai Ulang List LLM PentAGI: Eksklusif Top-4 Cloud Pentest Models | Lead Architect (Hermes) & Design UX | **SUCCESS** | `pentagi_bridge.py, pentagi_bridge.py, index.html` |
| `RFC-20261103_124652` | 03 November 2026, 12:46:52 WIB | Perbaikan Pemetaan Model Sub-Agent PentAGI Multi-Provider | Lead Architect (Hermes) & Red Team | **SUCCESS** | `docker-compose.override.yml, .env` |
| `RFC-20261103_125945` | 03 November 2026, 12:59:45 WIB | Penghentian Flow 59 & Hardening Bersih Sistem untuk Demo Manajemen | Lead Architect (Hermes) & Red Team | **SUCCESS** | `pentagi_bridge.py, pentagi_bridge.py` |
| `RFC-20261104_042146` | 04 November 2026, 04:21:46 WIB | Dynamic Pentest Mgmt Report Findings Synthesizer | Hermes & Red Team | **IN_PROGRESS** | `dynamic_pentest_docx.py` |
| `RFC-20261104_042200` | 04 November 2026, 04:22:00 WIB | Dynamic Pentest Mgmt Report Findings Synthesizer | Hermes & Red Team | **SUCCESS** | `dynamic_pentest_docx.py` |
| `RFC-20261104_143005` | 04 November 2026, 14:30:05 WIB | Pembaruan Template Prompt Pentest PentAGI Portal | Lead Architect & Design UX | **SUCCESS** | `index.html, index.html, index.html` |
| `RFC-20261104_151306` | 04 November 2026, 15:13:06 WIB | Hot-Swap LLM Model & State Recovery Flow 63 PentAGI | Lead Architect & Red Team | **SUCCESS** | `pentagi_bridge.py, .env` |
| `RFC-20261104_154813` | 04 November 2026, 15:48:13 WIB | Optimasi Hybrid FinOps Asymmetric Role Mapping PentAGI Flow 63 | Lead Architect & Analis Token | **SUCCESS** | `custom.provider.yml, pentagi_bridge.py` |
| `RFC-20261105_012720` | 05 November 2026, 01:27:20 WIB | Hot-Switch Live Provider Flow 64 ke cc/claude-sonnet-5 | Lead Architect & Analis Token | **SUCCESS** | `.env, pentagi_bridge.py` |
| `RFC-20261105_023322` | 05 November 2026, 02:33:22 WIB | Migrasi Arsitektur Multi-Tier PentAGI (Groq + Local + NusaGate) & Unblock Flow 64 | Lead Architect & Analis Token | **SUCCESS** | `pentagi_bridge.py, pentagi_bridge.py, index.html` |
| `RFC-20261105_032701` | 05 November 2026, 03:27:01 WIB | Konfigurasi Hybrid Multi-LLM PentAGI & Smart Gateway Router | Lead Architect & Analis Token | **SUCCESS** | `server.py, server.py, pentagi_bridge.py` |
| `RFC-20261105_063527` | 05 November 2026, 06:35:27 WIB | Unblock Flow 65, Rename Custom ke Hybrid, dan Eliminasi Full Claude Sonnet PentAGI | Lead Architect & Analis Token | **SUCCESS** | `index-BF4EUade.js, provider.tsx, .env` |
| `RFC-20261105_090647` | 05 November 2026, 09:06:47 WIB | Unblock Subtask 1205 and Hot-Swap Flow 66 to DeepSeek V4 Pro | Lead Architect (Hermes) & Red Team | **SUCCESS** | `.env` |
| `RFC-20261105_130826` | 05 November 2026, 13:08:26 WIB | Smart Gateway Router Anti-413 and PentAGI Anti-Stuck Prompt Standard | Lead Architect (Hermes) & Red Team | **SUCCESS** | `hybrid_llm_router.py, pentagi_bridge.py` |
| `RFC-20261105_131323` | 05 November 2026, 13:13:23 WIB | Recreate PentAGI Container with Hybrid Gateway Binding | Lead Architect (Hermes) & Red Team | **SUCCESS** | `docker-compose.override.yml` |
| `RFC-20261105_131638` | 05 November 2026, 13:16:38 WIB | Train and Specialize Local Qwen 7B Pentest Operator from 4016 Msglogs | Lead Architect (Hermes) & Red Team | **SUCCESS** | `Modelfile.pentest-operator` |
| `RFC-20261105_132721` | 05 November 2026, 13:27:21 WIB | Integrate PentAGI Hybrid Workflow with Local Qwen Pentest Operator | Lead Architect (Hermes) & Red Team | **SUCCESS** | `custom.provider.yml, hybrid_llm_router.py` |
| `RFC-20261105_134248` | 05 November 2026, 13:42:48 WIB | Engine Parser Semantik PDF dan Generator DOCX Dinamis | Lead Architect (Hermes) | **SUCCESS** | `dynamic_pentest_docx.py, pentagi_bridge.py, pentagi_bridge.py` |
| `RFC-20261105_141202` | 05 November 2026, 14:12:02 WIB | Active LLM Telemetry Realtime dan Auto-Lock Form Pentagi | Lead Architect (Hermes) & Design UX | **SUCCESS** | `hybrid_llm_router.py, hybrid_llm_router.py, pentagi_bridge.py` |
| `RFC-20261105_144412` | 05 November 2026, 14:44:12 WIB | Integrasi Expert LLM dan Pipeline CISO DOCX Generator PentAGI | Lead Architect (Hermes) & Red Team | **SUCCESS** | `dynamic_pentest_docx.py, pentagi_bridge.py, pentagi_bridge.py` |
| `RFC-20261105_151750` | 05 November 2026, 15:17:50 WIB | Penyelarasan Presisi Evidence Cookie F-03 dan Skoring CISO DOCX | Lead Architect (Hermes) & Red Team | **SUCCESS** | `pdf_report_parser.py, dynamic_pentest_docx.py` |
| `RFC-20261105_153934` | 05 November 2026, 15:39:34 WIB | Upgrade Generator Report CISO ke DeepSeek-V4-Pro | Lead Architect (Hermes) | **SUCCESS** | `pdf_report_parser.py` |
| `RFC-20261105_231039` | 05 November 2026, 23:10:39 WIB | Penghapusan Overfitting Template & Sinkronisasi Severity Dinamis Generator CISO DOCX | Lead Architect (Hermes) | **SUCCESS** | `pdf_report_parser.py, dynamic_pentest_docx.py` |
| `RFC-20261105_233035` | 05 November 2026, 23:30:35 WIB | High-Fidelity Pentest Report Synthesizer Upgrade (99-100% Alignment) | Lead Architect (Hermes) & Red Team | **SUCCESS** | `dynamic_pentest_docx.py, pdf_report_parser.py` |
| `RFC-20261106_001045` | 06 November 2026, 00:10:45 WIB | Universal Pure-Data Pentest Synthesizer Pipeline | Lead Architect (Hermes) & Red Team | **SUCCESS** | `pdf_report_parser.py, dynamic_pentest_docx.py` |
| `RFC-20261106_010806` | 06 November 2026, 01:08:06 WIB | Rollback Pipeline Report Synthesizer ke Kondisi RFC-20261105_2359 | Lead Architect (Hermes) & Red Team | **SUCCESS** | `pdf_report_parser.py, dynamic_pentest_docx.py` |
| `RFC-20261106_012725` | 06 November 2026, 01:27:25 WIB | Perbaikan Timeout Subprocess dan Penanganan Eksepsi Generator DOCX PentAGI | Lead Architect (Hermes) & Red Team | **SUCCESS** | `pentagi_bridge.py, pentagi_bridge.py, pdf_report_parser.py` |
| `RFC-20261106_074222` | 06 November 2026, 07:42:22 WIB | Default Hybrid Multi-LLM & Real-Time Auto-Lock Grey Box PentAGI | Lead Architect (Hermes) & Design UX & Change Management | **SUCCESS** | `pentagi_bridge.py, index.html` |
| `RFC-20261106_075801` | 06 November 2026, 07:58:01 WIB | Hotfix Hybrid LLM Gateway Router PentAGI | Lead Architect (Hermes) & Red Team & Change Management | **SUCCESS** | `hybrid_llm_router.py` |
| `RFC-20261106_114657` | 06 November 2026, 11:46:57 WIB | Remediasi Failover Gateway Router & Pencegahan Stuck PentAGI | Lead Architect (Hermes) & Red Team & Change Management | **SUCCESS** | `hybrid_llm_router.py` |
| `RFC-20261106_131531` | 06 November 2026, 13:15:31 WIB | Optimalisasi Provider Enricher & Failover NusaGate 128k | Lead Architect (Hermes) & Red Team & Change Management | **SUCCESS** | `hybrid_llm_router.py, custom.provider.yml` |
| `RFC-20261106_170456` | 06 November 2026, 17:04:56 WIB | Pembagian Formasi PentAGI Hybrid Lite (NusaGate + Ollama Qwen bash) dengan Koeksistensi Hybrid Asli | Lead Architect Hermes & Red Team | **SUCCESS** | `custom.provider.yml, hybrid_llm_router.py, pentagi_bridge.py` |
| `RFC-20261106_173312` | 06 November 2026, 17:33:12 WIB | Restore Hybrid Classic and Enable Dynamic Coexistence | Lead Architect (Hermes) | **SUCCESS** | `hybrid_llm_router.py, pentagi_bridge.py` |
| `RFC-20261107_020357` | 07 November 2026, 02:03:57 WIB | Deploy Hybrid 4 LLM Optimized Formation to PentAGI | Lead Architect (Hermes) | **SUCCESS** | `custom.provider.yml, hybrid_llm_router.py` |
| `RFC-20261107_024849` | 07 November 2026, 02:48:49 WIB | Hotfix PentAGI Login Alias & Groq Model Normalizer | Lead Arsitek (Hermes) | **SUCCESS** | `hybrid_llm_router.py, hybrid_llm_router.py` |
| `RFC-20261107_065837` | 07 November 2026, 06:58:37 WIB | Dedicated Groq-Pentest API Key Migration | Lead Arsitek (Hermes) | **SUCCESS** | `.env, docker-compose.override.yml, .env` |
| `RFC-20261107_081631` | 07 November 2026, 08:16:31 WIB | DEPLOYMENT OPEN WEBUI & OPENROUTER FAILOVER INTEGRATION | Lead Architect (Hermes) | **SUCCESS** | `docker-compose.yml, .env` |
| `RFC-20261107_104947` | 07 November 2026, 10:49:47 WIB | FASE 1: WORKSPACE & GOVERNANCE BIND-MOUNT KE OPEN WEBUI | Lead Architect (Hermes) | **SUCCESS** | `docker-compose.yml` |
| `RFC-20261107_105656` | 07 November 2026, 10:56:56 WIB | FASE 2: MASTER RULES, PERSONA & LIVING STATE INTEGRATION | Lead Architect (Hermes) | **SUCCESS** | `PROJECT_STATE.md` |
| `RFC-20261107_110651` | 07 November 2026, 11:06:51 WIB | FASE 3: HOST TOOL BRIDGE PLUGIN (READ, WRITE, RUN COMMAND) | Lead Architect (Hermes) | **SUCCESS** | `register_tool_bridge.py` |
| `RFC-20261107_111158` | 07 November 2026, 11:11:58 WIB | FASE 4: TWO-WAY TRANSCRIPT & SESSION TRANSPORTER DAEMON | Lead Architect (Hermes) | **SUCCESS** | `sync_antigravity_to_webui.py` |
| `RFC-20261107_112339` | 07 November 2026, 11:23:39 WIB | REVERSE SYNC ENGINE: OPEN WEBUI TO ANTIGRAVITY | Lead Architect (Hermes) | **SUCCESS** | `sync_webui_to_antigravity.py, register_tool_bridge.py` |
| `RFC-20261107_113718` | 07 November 2026, 11:37:18 WIB | REAL-TIME BACKGROUND WATCHER DAEMON | Lead Architect (Hermes) | **SUCCESS** | `auto_sync_watcher.py, lkt-webui-watcher.service` |
| `RFC-20261107_115640` | 07 November 2026, 11:56:40 WIB | TWO-WAY REAL-TIME ZERO-TOUCH WATCHER DAEMON | Lead Architect (Hermes) | **SUCCESS** | `auto_sync_watcher.py` |
| `RFC-20261107_121941` | 07 November 2026, 12:19:41 WIB | Open WebUI Autonomous RFC Lifecycle and Knowledge Training | Lead Architect (Hermes) | **IN_PROGRESS** | `generate_rfc_exemplars.py, RFC_KNOWLEDGE_EXEMPLARS.md, register_tool_bridge.py` |

### Pola Solusi Rekayasa Berulang (Key Engineering Patterns)
1. **Dual-Repository Sync Pattern**: Setiap update di `/opt/ai-agent/unified-portal/` wajib di-mirror ke `/opt/ai-agent/omni-agent-os/portal/` agar Gate 1 ECC test tidak gagal.
2. **Bento Grid Layout Pattern**: Komponen box baru harus memiliki `widget-<id>`, atribut drag-and-drop, `.layout-edit-controls`, dan terdaftar di `DEFAULT_WIDGET_CONFIG`.
3. **Daemon Service Pattern**: Service user systemd dimanage dengan `systemctl --user restart <service>` dan diverifikasi dengan `systemctl --user is-active <service>`.
4. **Zero-Defect Verification**: Eksekusi `python3 /opt/ai-agent/omni-agent-os/ecc/verify.py` wajib 15/15 PASS sebelum melaporkan penutupan tugas ke Owner.