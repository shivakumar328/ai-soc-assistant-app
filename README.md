# 🛡️ AI Security Operations Center (SOC) Assistant

A production-style, AI-powered SOC assistant: a **React dashboard** + **Flask/Claude API backend** that ingests SIEM alerts, performs AI threat analysis, maps activity to **MITRE ATT&CK**, and generates **incident-response plans**.

> ✅ **Runs out of the box with NO API key.** If `ANTHROPIC_API_KEY` is not set, the backend runs in deterministic **offline / mock mode** so you can demo the entire app immediately. Add a key to get live Claude analysis.

---

## 📂 Project structure

```
soc-assistant/
├── backend/                 # Flask + Claude API
│   ├── app.py               # Main API (8 endpoints, offline-mock fallback)
│   ├── advanced_integrations.py  # CrowdStrike, SentinelOne, threat hunting, OSINT, etc.
│   ├── requirements.txt     # Core deps (all you need to run)
│   ├── requirements-full.txt# Heavy deps for advanced_integrations connectors
│   ├── .env.example
│   └── Dockerfile
├── frontend/                # React (Vite) dashboard
│   ├── src/
│   │   ├── SOCAssistant.jsx # Dashboard component (alerts, AI analysis, MITRE, IR)
│   │   ├── main.jsx
│   │   └── index.css        # Dark-mode design tokens
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── nginx.conf
│   └── Dockerfile
├── docs/                    # All guides
│   ├── MASTER_BUILD_PROMPT.md
│   ├── BUILD_SUMMARY.md
│   ├── SOC_SETUP_GUIDE.md
│   ├── API_DEPLOYMENT_GUIDE.md
│   ├── CTF_ETHICAL_HACKING_COMPLETE_GUIDE.md
│   └── TOOLS_REFERENCE_GUIDE.md
├── k8s/deployment.yaml      # Kubernetes manifests
├── docker-compose.yml
└── README.md  (this file)
```

---

## 🚀 Quick start

### Option A — Docker (recommended)

```bash
cd soc-assistant

# (optional) add your key for live Claude analysis
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env

docker compose up -d --build
```

- Frontend → http://localhost:8080
- Backend API → http://localhost:5000/api/health

### Option A2 — One-shot script (no Docker)

```bash
cd soc-assistant
# (optional) pass your Hugging Face key inline; otherwise it uses backend/.env
HF_API_KEY=hf_your_token_here ./run.sh
```

`run.sh` creates the Python venv, installs backend + frontend deps, writes your key
into `backend/.env`, and launches both servers. Open http://localhost:5173.
Stop with `./stop.sh` (or Ctrl-C in the same terminal).

### Option B — Run locally (no Docker)

**1. Backend**
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # optionally add ANTHROPIC_API_KEY
python app.py                 # serves http://localhost:5000
```

**2. Frontend** (in a second terminal)
```bash
cd frontend
npm install
npm run dev                   # serves http://localhost:5173
```

Open the frontend URL, click an alert, and hit **Analyze**.

---

## 🔌 API endpoints

| Method | Path                     | Description                                   |
|--------|--------------------------|-----------------------------------------------|
| GET    | `/api/health`            | Health + current mode (offline-mock / claude) |
| GET    | `/api/alerts`            | List SIEM alerts (`?severity=critical` filter)|
| POST   | `/api/analyze`           | AI threat analysis + MITRE mapping            |
| POST   | `/api/mitre-mapping`     | MITRE ATT&CK mapping only                     |
| POST   | `/api/incident-response` | Generate an IR plan                           |
| GET    | `/api/logs`              | Sample log feed (`?limit=N`)                  |
| GET    | `/api/incidents`         | Open incidents                                |
| GET    | `/api/threat-intel`      | Threat-intel indicators (IOCs)                |

**Example:**
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"alert":{"id":1,"type":"SQL Injection Attempt","severity":"critical","source":"IDS-01","description":"SQLi detected","source_ip":"192.168.1.100"}}'
```

---

## 🤖 Claude / API key

- **No key** → offline mock mode (deterministic, realistic analysis). Great for demos and CI.
- **With key** → set `ANTHROPIC_API_KEY`. Get one at https://console.anthropic.com/account/keys
- **Model** → override with `ANTHROPIC_MODEL` (default `claude-sonnet-4-20250514`).

Check which mode you're in:
```bash
curl http://localhost:5000/api/health
```

---

## 🤖 LLM provider — Claude **or** Hugging Face (Mistral/Llama/Qwen)

The backend supports multiple LLM providers, selected with `LLM_PROVIDER` (`auto` | `huggingface` | `claude` | `offline`):

| Provider | Env vars | Notes |
|----------|----------|-------|
| **Hugging Face** | `HF_API_KEY`, `HF_MODEL`, `HF_BASE_URL` | Free serverless inference via the HF router (OpenAI-compatible). |
| **Claude** | `ANTHROPIC_API_KEY`, `ANTHROPIC_MODEL` | Anthropic API. |
| **Offline** | _(none)_ | Deterministic mock analysis. |

### Using Hugging Face
1. Create a token (read access): https://huggingface.co/settings/tokens
2. In `backend/.env`:
   ```env
   LLM_PROVIDER=huggingface
   HF_API_KEY=hf_your_token_here
   HF_MODEL=meta-llama/Llama-3.1-8B-Instruct
   ```
3. Test it: `cd backend && python test_hf.py`

### ⚠️ About `mistralai/Mistral-7B-Instruct-v0.3`
This exact model is **not currently served on Hugging Face's free serverless inference**. Its only mapped provider (`novita`) is in an error state, and the router reports it as "not a chat model." Verified working free chat models on the HF router are:

- `meta-llama/Llama-3.1-8B-Instruct`  ← default
- `Qwen/Qwen2.5-7B-Instruct`

To switch to Mistral once HF re-enables it (or if you enable a paid inference provider that serves it), just set:
```env
HF_MODEL=mistralai/Mistral-7B-Instruct-v0.3
```
No code changes needed.

---



`backend/advanced_integrations.py` contains connector classes for CrowdStrike, SentinelOne,
threat hunting, malware analysis (VirusTotal/Hybrid-Analysis/ANY.RUN), OSINT (Shodan), network
analysis, compliance mapping, and IR playbooks. These require third-party API keys and the
extra dependencies in `requirements-full.txt`. They are **optional** and not needed to run the core app.

---

## ☸️ Kubernetes

```bash
docker build -t soc-assistant-backend:latest ./backend
docker build -t soc-assistant-frontend:latest ./frontend
kubectl apply -f k8s/deployment.yaml
```

---

## 📚 Documentation

See the `docs/` folder for the full build prompt, setup, API/deployment, the CTF & ethical-hacking guide, and the tools reference.

---

## ⚠️ Notes & changes from the original draft

- Fixed an invalid Claude model name (`claude-opus-4-6`) → configurable, valid default.
- Added offline/mock mode so the app runs with zero configuration.
- Removed unsafe/buggy `eval()` calls in the frontend; severity styling now uses style objects.
- Added Vite project scaffolding, dark-mode CSS tokens, Docker/K8s, and split requirements.

The CTF / ethical-hacking material is for **authorized testing and education only.** Only test systems you own or have explicit written permission to assess.

**Version:** 1.0.0
