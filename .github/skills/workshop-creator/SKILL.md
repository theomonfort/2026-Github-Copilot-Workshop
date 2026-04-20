---
name: workshop-creator
description: Create GitHub Copilot workshop repositories following William's (moulongzhang) structure. Use when creating a new hands-on workshop template repo for any language (Python, Node.js, etc.).
compatibility: Designed for GitHub Copilot CLI
metadata:
  author: theomonfort
  version: "1.0"
---

# Workshop Creator

You are tasked with creating a GitHub Copilot hands-on workshop repository, following the structure established by William (moulongzhang) in the reference repos below.

## Reference Repositories

- **Workshop hub (instructions site):** [github.com/moulongzhang/2026-Github-Copilot-Workshop](https://github.com/moulongzhang/2026-Github-Copilot-Workshop)
- **Python participant template:** [github.com/moulongzhang/2026-Github-Copilot-Workshop-Python](https://github.com/moulongzhang/2026-Github-Copilot-Workshop-Python)
- **Live workshop site:** [moulongzhang.github.io/2026-Github-Copilot-Workshop/github-copilot-workshop/](https://moulongzhang.github.io/2026-Github-Copilot-Workshop/github-copilot-workshop/)
- **Denso custom version:** [.../custom/denso/#1](https://moulongzhang.github.io/2026-Github-Copilot-Workshop/github-copilot-workshop/custom/denso/#1)
- **NRI custom version:** [.../custom/nri/](https://moulongzhang.github.io/2026-Github-Copilot-Workshop/github-copilot-workshop/custom/nri/)

---

## Architecture Overview

There are **two distinct repo types**:

### 1. Workshop Hub Repo (`2026-Github-Copilot-Workshop`)
Contains the GitHub Pages **instruction site** (Google Codelab format) and customer-specific variants.

```
.github/
  copilot-instructions.md   ← Custom Copilot context
  workflows/
    static.yml              ← Deploys GitHub Pages
.vscode/
  mcp.json                  ← MCP server config
github-copilot-workshop/
  index.html                ← Main Codelab entry point
  codelab.json              ← Codelab metadata
  versions.json             ← Version switcher config
  versions/
    v1.0.0/index.html
    v1.0.1/index.html
    v1.0.2/index.html
    v1.0.3/index.html       ← Latest (default)
  custom/
    denso/index.html        ← Denso-specific version
    nri/index.html          ← NRI-specific version
workshop.md                 ← Generic workshop source (Markdown → Codelab)
workshop-denso.md           ← Denso workshop source
workshop-nri.md             ← NRI workshop source
registrations/              ← Participant registration data
```

### 2. Participant Template Repo (`2026-Github-Copilot-Workshop-Python`)
A **GitHub Template Repository** that participants use as their coding workspace.

```
.devcontainer/
  devcontainer.json         ← One-click Codespaces environment
.vscode/
  mcp.json                  ← MCP server (GitHub Copilot MCP)
.github/
  copilot-instructions.md   ← Language + file placement rules
  agents/
    beastmode3.1.agent.md   ← Autonomous coding agent
  workflows/
    pomodoro-docs-sync.md   ← Copilot agent workflow (docs auto-sync)
1.pomodoro/
  app.py                    ← Empty starter file (participants fill in)
  pomodoro.png              ← Reference image for the exercise
README.md                   ← "Refer to instructor URL" (intentionally no link)
```

---

## Key Design Decisions

### Participant Template Repo
- **No hardcoded workshop URL** in README — instructor shares it during the session so it can be reused across customers
- **Marked as GitHub Template Repository** (Settings → "Template repository" ✅) so participants use "Use this template" instead of forking
- **`beastmode3.1.agent.md`** is language-agnostic — copy as-is for any language
- Starter files are minimal (just a title comment) — participants build with Copilot
- `copilot-instructions.md` enforces **Japanese responses** and defines file placement rules per exercise

### Codelab Site (Hub Repo)
- Built from **Markdown → Google Codelab HTML format**
- Versioned under `versions/` with a `versions.json` switcher
- Customer-specific versions under `custom/<customer>/`
- Deployed via a simple `static.yml` GitHub Pages workflow

---

## How to Create a New Participant Template Repo (e.g., Node.js)

### Step 1: devcontainer.json
Replace Python image with Node.js:
```json
{
  "name": "Node.js",
  "image": "mcr.microsoft.com/devcontainers/javascript-node:0-20",
  "customizations": {
    "vscode": {
      "extensions": [
        "vsls-contrib.codetour",
        "GitHub.copilot",
        "GitHub.copilot-chat"
      ],
      "settings": {
        "github.copilot.chat.mcp.discovery.enabled": true
      }
    }
  },
  "features": {
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "postCreateCommand": "gh extension install github/gh-copilot || true"
}
```
Note: Node.js is already in the base image — no need to add it as a feature.

### Step 2: .vscode/mcp.json (copy as-is)
```json
{
  "servers": {
    "github-mcp-server": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```

### Step 3: .github/copilot-instructions.md
Adapt file placement rules for Node.js exercises:
```markdown
# Copilot Instructions

## 重要：言語設定
**必ず日本語でレビューを行ってください。すべてのコメント、提案、説明は日本語で記述してください。**

## ファイル配置ルール
- **Pomodoro タイマー**に関する作業では、ファイルを `1.pomodoro/` 配下に保存してください。
```

### Step 4: .github/agents/beastmode3.1.agent.md (copy as-is)
The agent is fully language-agnostic.

### Step 5: Starter exercise file
Rename `app.py` → `app.js`:
```js
// Pomodoro Timer App
```

### Step 6: Mark as Template Repository
Go to repo **Settings → General → check "Template repository"**.

---

## Files That Are Language-Agnostic (copy as-is)
| File | Notes |
|---|---|
| `.github/agents/beastmode3.1.agent.md` | Pure prompting |
| `.vscode/mcp.json` | Same MCP endpoint |
| `1.pomodoro/pomodoro.png` | Reference image |
| `.gitignore` / `.gitattributes` | Minor tweaks only |

## Files That Need Adaptation
| File | Change needed |
|---|---|
| `.devcontainer/devcontainer.json` | Swap base image |
| `.github/copilot-instructions.md` | Update file paths if exercise names change |
| `1.pomodoro/app.py` → `app.js` | Rename + update comment |
| `.github/workflows/pomodoro-docs-sync.md` | Swap Python references → Node.js |

---

## Execution Steps

1. Confirm the target language and exercise name with the user
2. Create the repo structure locally or directly on GitHub
3. Populate files using the templates above
4. Mark the repo as a GitHub Template Repository
5. Optionally link it from the workshop hub repo README
