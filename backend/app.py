"""
AI-Powered Security Operations Center (SOC) Assistant
Backend: Flask + Claude API

Improvements over the original draft:
- Configurable Claude model via ANTHROPIC_MODEL env var (defaults to a valid model).
- Graceful "offline / mock" mode when no ANTHROPIC_API_KEY is set, so the whole
  app is runnable and demoable end-to-end without a key.
- Centralised Claude JSON-calling helper with robust markdown-fence stripping.
- Clean app factory + CONFIG block.
"""

import os
import json
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS

try:
    from dotenv import load_dotenv
    load_dotenv()  # load backend/.env if present
except ImportError:  # pragma: no cover
    pass

try:
    import anthropic
except ImportError:  # pragma: no cover
    anthropic = None

# ---------------------------------------------------------------------------
# Configuration  —  multi-provider LLM support (Claude OR Hugging Face/Mistral)
# ---------------------------------------------------------------------------
# LLM_PROVIDER: "auto" (default), "huggingface", "claude", or "offline".
#   auto -> use Hugging Face if HF_API_KEY is set, else Claude if its key is set,
#           else offline/mock mode.
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "auto").strip().lower()

# --- Anthropic / Claude ---
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "").strip()
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")

# --- Hugging Face / Mistral (OpenAI-compatible router) ---
HF_API_KEY = (os.environ.get("HF_API_KEY") or os.environ.get("HUGGINGFACE_API_KEY") or "").strip()
HF_MODEL = os.environ.get("HF_MODEL", "meta-llama/Llama-3.1-8B-Instruct")
HF_BASE_URL = os.environ.get("HF_BASE_URL", "https://router.huggingface.co/v1")

try:
    from openai import OpenAI  # used as an OpenAI-compatible client for the HF router
except ImportError:  # pragma: no cover
    OpenAI = None


def _resolve_provider() -> str:
    """Decide which LLM backend to use based on config + available keys."""
    if LLM_PROVIDER == "offline":
        return "offline"
    if LLM_PROVIDER == "huggingface":
        return "huggingface" if (HF_API_KEY and OpenAI) else "offline"
    if LLM_PROVIDER == "claude":
        return "claude" if (ANTHROPIC_API_KEY and anthropic) else "offline"
    # auto
    if HF_API_KEY and OpenAI:
        return "huggingface"
    if ANTHROPIC_API_KEY and anthropic:
        return "claude"
    return "offline"


PROVIDER = _resolve_provider()
OFFLINE = PROVIDER == "offline"
MODEL = HF_MODEL if PROVIDER == "huggingface" else ANTHROPIC_MODEL

app = Flask(__name__)
CORS(app)

# Instantiate the active client lazily.
anthropic_client = None
hf_client = None
if PROVIDER == "claude":
    anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
elif PROVIDER == "huggingface":
    hf_client = OpenAI(base_url=HF_BASE_URL, api_key=HF_API_KEY)

# ---------------------------------------------------------------------------
# Sample SIEM alert data (stand-in for a real SIEM feed)
# ---------------------------------------------------------------------------
SAMPLE_ALERTS = [
    {
        "id": 1, "type": "SQL Injection Attempt", "source": "IDS-01",
        "severity": "critical", "timestamp": "2024-06-24T10:15:30Z",
        "description": "SQL injection pattern detected in HTTP request to /api/users endpoint",
        "source_ip": "192.168.1.100", "target": "web-server-01", "payload": "' OR '1'='1",
    },
    {
        "id": 2, "type": "Brute Force Login", "source": "Authentication Log",
        "severity": "high", "timestamp": "2024-06-24T10:12:15Z",
        "description": "Multiple failed login attempts from single IP within 5 minutes",
        "source_ip": "203.0.113.45", "target": "mail-server", "attempts": 47,
    },
    {
        "id": 3, "type": "Suspicious Process Execution", "source": "EDR-01",
        "severity": "high", "timestamp": "2024-06-24T10:05:20Z",
        "description": "Unknown process executing with system privileges",
        "host": "workstation-42", "process": "powershell.exe", "parent_process": "svchost.exe",
        "command_line": "powershell.exe -ExecutionPolicy Bypass -NoProfile -Command IEX(New-Object Net.WebClient).DownloadString(...)",
    },
    {
        "id": 4, "type": "Data Exfiltration Detected", "source": "DLP-01",
        "severity": "critical", "timestamp": "2024-06-24T09:58:45Z",
        "description": "Large volume of data transfer to external IP detected",
        "source_ip": "10.0.1.50", "destination_ip": "185.220.101.45",
        "data_volume": "2.3 GB", "file_types": ["xlsx", "pdf", "docx"],
    },
    {
        "id": 5, "type": "Privilege Escalation Attempt", "source": "Auditd",
        "severity": "high", "timestamp": "2024-06-24T09:45:10Z",
        "description": "Sudoedit vulnerability exploitation attempt detected",
        "user": "www-data", "target_user": "root", "host": "database-server-03",
    },
    {
        "id": 6, "type": "Malware Detected", "source": "Antivirus",
        "severity": "critical", "timestamp": "2024-06-24T09:32:00Z",
        "description": "Known malware signature matched",
        "file_path": "/tmp/.cache/update.exe", "malware_name": "Emotet",
        "host": "client-workstation-15",
    },
    {
        "id": 7, "type": "Unusual Network Activity", "source": "Network IDS",
        "severity": "medium", "timestamp": "2024-06-24T09:20:30Z",
        "description": "Port scanning activity detected from internal network",
        "source_ip": "10.0.2.100", "scan_type": "SYN sweep", "ports_scanned": 65535,
    },
    {
        "id": 8, "type": "Ransomware Behavior", "source": "Behavioral Analysis",
        "severity": "critical", "timestamp": "2024-06-24T09:10:15Z",
        "description": "Process showing ransomware indicators (file encryption, extension changes)",
        "process": "svchost.exe", "host": "file-server-01", "files_affected": 15000,
    },
]

# ---------------------------------------------------------------------------
# Claude helper
# ---------------------------------------------------------------------------
def _coerce_text(value) -> str:
    """Flatten dicts/lists that some models return into readable text, so the
    React UI (which renders these fields directly) never receives an object."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, list):
        return "; ".join(_coerce_text(v) for v in value)
    if isinstance(value, dict):
        return "; ".join(f"{k}: {_coerce_text(v)}" for k, v in value.items())
    return str(value)


def _coerce_str_list(value) -> list:
    """Normalise a field into a list of plain strings."""
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [_coerce_text(value)]
    if isinstance(value, list):
        return [_coerce_text(v) for v in value]
    return [str(value)]


def _strip_json_fence(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1] if "```" in text[3:] else text[3:]
        if text.lstrip().startswith("json"):
            text = text.lstrip()[4:]
    return text.strip()


def _ask_claude_json(prompt: str, max_tokens: int, fallback: dict) -> dict:
    """Call the active LLM provider and parse a JSON response, with a safe fallback."""
    if OFFLINE:
        return fallback
    try:
        if PROVIDER == "huggingface":
            resp = hf_client.chat.completions.create(
                model=HF_MODEL,
                max_tokens=max_tokens,
                temperature=0.2,
                messages=[
                    {"role": "system",
                     "content": "You are a precise security analyst. Respond with ONLY valid JSON, no prose, no markdown fences."},
                    {"role": "user", "content": prompt},
                ],
            )
            text = resp.choices[0].message.content
        else:  # claude
            message = anthropic_client.messages.create(
                model=ANTHROPIC_MODEL,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
            text = message.content[0].text
        return json.loads(_strip_json_fence(text))
    except Exception:
        return fallback


# ---------------------------------------------------------------------------
# Deterministic offline/mock analysis (used when no API key is present)
# ---------------------------------------------------------------------------
_MITRE_HINTS = {
    "SQL Injection Attempt": {
        "tactics": ["Initial Access"],
        "techniques": ["T1190: Exploit Public-Facing Application"],
    },
    "Brute Force Login": {
        "tactics": ["Credential Access"],
        "techniques": ["T1110: Brute Force"],
    },
    "Suspicious Process Execution": {
        "tactics": ["Execution", "Defense Evasion"],
        "techniques": ["T1059.001: PowerShell", "T1140: Deobfuscate/Decode Files or Information"],
    },
    "Data Exfiltration Detected": {
        "tactics": ["Exfiltration"],
        "techniques": ["T1041: Exfiltration Over C2 Channel"],
    },
    "Privilege Escalation Attempt": {
        "tactics": ["Privilege Escalation"],
        "techniques": ["T1068: Exploitation for Privilege Escalation"],
    },
    "Malware Detected": {
        "tactics": ["Execution"],
        "techniques": ["T1204: User Execution"],
    },
    "Unusual Network Activity": {
        "tactics": ["Discovery"],
        "techniques": ["T1046: Network Service Discovery"],
    },
    "Ransomware Behavior": {
        "tactics": ["Impact"],
        "techniques": ["T1486: Data Encrypted for Impact"],
    },
}
_SEV_SCORE = {"critical": 9, "high": 7, "medium": 5, "low": 3}


def _mock_analysis(alert: dict) -> dict:
    sev = str(alert.get("severity", "medium")).lower()
    atype = alert.get("type", "Security Event")
    mitre = _MITRE_HINTS.get(atype, {"tactics": [], "techniques": []})
    return {
        "threat_summary": (
            f"A '{atype}' alert was raised by {alert.get('source', 'a sensor')} "
            f"with {sev} severity. {alert.get('description', '')}".strip()
        ),
        "risk_level": sev.upper(),
        "risk_score": _SEV_SCORE.get(sev, 5),
        "attack_techniques": mitre["techniques"],
        "recommendation": (
            "Isolate the affected host, preserve volatile evidence, and begin triage "
            "per the relevant incident playbook."
        ),
        "evidence": [v for k, v in alert.items()
                     if k in ("source_ip", "destination_ip", "payload", "command_line",
                              "file_path", "malware_name", "process")],
        "investigation_steps": [
            "Validate the alert is a true positive against raw logs.",
            "Identify all hosts/accounts involved and their blast radius.",
            "Check threat-intel reputation for any external IOCs.",
            "Determine initial access vector and timeline.",
            "Escalate to IR if confirmed malicious.",
        ],
    }


def _mock_mitre(alert: dict) -> dict:
    atype = alert.get("type", "Security Event")
    base = _MITRE_HINTS.get(atype, {"tactics": [], "techniques": []})
    return {
        "tactics": base["tactics"],
        "techniques": base["techniques"],
        "mitigations": [
            "Apply least-privilege access controls.",
            "Patch and harden exposed services.",
            "Deploy network segmentation and egress filtering.",
        ],
        "detection_recommendations": [
            "Alert on anomalous process lineage and command-line arguments.",
            "Monitor authentication failures and impossible-travel logins.",
            "Inspect large or unusual outbound transfers.",
        ],
    }


def _mock_ir_plan(alert: dict) -> dict:
    return {
        "immediate_actions": [
            "Isolate affected host(s) from the network.",
            "Disable compromised credentials.",
            "Preserve memory and disk images for forensics.",
            "Notify the on-call IR lead.",
        ],
        "containment_steps": [
            "Block malicious IPs/domains at the firewall and proxy.",
            "Quarantine malicious files and processes.",
        ],
        "eradication_steps": [
            "Remove malware, persistence mechanisms, and attacker tooling.",
            "Patch the exploited vulnerability.",
        ],
        "recovery_steps": [
            "Restore systems from known-good backups.",
            "Reset affected credentials and rotate secrets.",
            "Monitor for re-infection for at least 14 days.",
        ],
        "lessons_learned": [
            "Close the initial access vector permanently.",
            "Add detections for the observed TTPs.",
        ],
        "communication_template": (
            f"A {alert.get('severity', 'security')} incident ({alert.get('type')}) "
            "was detected and is being contained. No action is required from you at this time; "
            "updates will follow every 60 minutes."
        ),
        "escalation_criteria": (
            "Escalate to management/legal if PII is exfiltrated, if critical systems are "
            "encrypted, or if the attacker retains persistent access after containment."
        ),
    }


# ---------------------------------------------------------------------------
# Claude-backed analysis functions (use mock fallback automatically)
# ---------------------------------------------------------------------------
def analyze_alert_with_claude(alert_data, context="general"):
    prompt = f"""You are an expert SOC analyst. Analyze this security alert and provide structured output in JSON format.

Alert Details:
{json.dumps(alert_data, indent=2)}

Context: {context}

Provide a JSON response with:
1. threat_summary: Brief explanation of the threat (2-3 sentences)
2. risk_level: CRITICAL, HIGH, MEDIUM, or LOW
3. risk_score: 1-10 numerical score
4. attack_techniques: List of likely MITRE ATT&CK techniques
5. recommendation: Specific action to take
6. evidence: Key indicators of compromise
7. investigation_steps: 3-5 investigation steps for analyst

Return ONLY valid JSON."""
    return _ask_claude_json(prompt, 1000, _mock_analysis(alert_data))


def map_to_mitre_attack(alert_data):
    prompt = f"""You are a MITRE ATT&CK expert. Map this security alert to relevant MITRE ATT&CK tactics and techniques.

Alert: {json.dumps(alert_data, indent=2)}

Return JSON with:
1. tactics: List of MITRE tactics
2. techniques: List of specific techniques (e.g., "T1190: Exploit Public-Facing Application")
3. mitigations: List of recommended mitigations
4. detection_recommendations: How to detect this activity

Return ONLY valid JSON."""
    return _ask_claude_json(prompt, 800, _mock_mitre(alert_data))


def incident_response_plan(alert_data, analysis):
    prompt = f"""You are an incident response expert. Create an immediate action plan for this security incident.

Alert: {json.dumps(alert_data, indent=2)}

Previous Analysis:
{json.dumps(analysis, indent=2)}

Provide JSON with:
1. immediate_actions
2. containment_steps
3. eradication_steps
4. recovery_steps
5. lessons_learned
6. communication_template
7. escalation_criteria

Return ONLY valid JSON."""
    return _ask_claude_json(prompt, 1200, _mock_ir_plan(alert_data))


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/api/alerts", methods=["GET"])
def get_alerts():
    severity_filter = request.args.get("severity")
    alerts = SAMPLE_ALERTS
    if severity_filter:
        alerts = [a for a in alerts if a["severity"].lower() == severity_filter.lower()]
    alerts = sorted(alerts, key=lambda x: x["timestamp"], reverse=True)
    return jsonify(alerts)


@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.json or {}
    alert = data.get("alert")
    context = data.get("context", "general")
    if not alert:
        return jsonify({"error": "No alert provided"}), 400
    try:
        analysis = analyze_alert_with_claude(alert, context)
        mitre = map_to_mitre_attack(alert)
        return jsonify({
            "alert_id": alert.get("id"),
            "threat_summary": _coerce_text(analysis.get("threat_summary")),
            "risk_level": _coerce_text(analysis.get("risk_level")).upper(),
            "risk_score": analysis.get("risk_score"),
            "attack_techniques": _coerce_str_list(analysis.get("attack_techniques")),
            "recommendation": _coerce_text(analysis.get("recommendation")),
            "evidence": _coerce_str_list(analysis.get("evidence")),
            "investigation_steps": _coerce_str_list(analysis.get("investigation_steps")),
            "mitre": {
                "tactics": _coerce_str_list(mitre.get("tactics")),
                "techniques": _coerce_str_list(mitre.get("techniques")),
                "mitigations": _coerce_str_list(mitre.get("mitigations")),
                "detection_recommendations": _coerce_str_list(mitre.get("detection_recommendations")),
            },
            "mode": "offline-mock" if OFFLINE else PROVIDER,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/mitre-mapping", methods=["POST"])
def mitre_mapping():
    data = request.json or {}
    alert = data.get("alert")
    if not alert:
        return jsonify({"error": "No alert provided"}), 400
    try:
        return jsonify(map_to_mitre_attack(alert))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/incident-response", methods=["POST"])
def incident_response():
    data = request.json or {}
    alert = data.get("alert")
    analysis = data.get("analysis", {})
    if not alert:
        return jsonify({"error": "No alert provided"}), 400
    try:
        return jsonify(incident_response_plan(alert, analysis))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().astimezone().isoformat(),
        "version": "1.0.0",
        "provider": PROVIDER,
        "mode": "offline-mock" if OFFLINE else PROVIDER,
        "model": None if OFFLINE else MODEL,
    })


@app.route("/api/logs", methods=["GET"])
def get_logs():
    limit = request.args.get("limit", 100, type=int)
    return jsonify({
        "logs": [
            {"timestamp": "2024-06-24T10:15:30Z", "level": "WARNING",
             "source": "web-server-01", "message": "Possible SQLi pattern in request body"},
            {"timestamp": "2024-06-24T10:12:15Z", "level": "ERROR",
             "source": "mail-server", "message": "47 failed auth attempts from 203.0.113.45"},
        ][:limit]
    })


@app.route("/api/incidents", methods=["GET"])
def get_incidents():
    return jsonify({
        "incidents": [
            {"id": "INC-1001", "title": "Ransomware on file-server-01",
             "status": "investigating", "severity": "critical",
             "assigned_to": "soc-analyst-01"}
        ]
    })


@app.route("/api/threat-intel", methods=["GET"])
def threat_intel():
    _ = request.args.get("type", "all")
    return jsonify({
        "indicators": [
            {"type": "IP", "value": "185.220.101.45", "reputation": "malicious",
             "sources": ["abuse.ch", "blocklist.org"], "last_seen": "2024-06-24T08:00:00Z"}
        ]
    })


if __name__ == "__main__":
    print("🛡️  AI Security Operations Center Backend")
    print("=" * 50)
    if OFFLINE:
        print("Mode : OFFLINE / MOCK (no LLM key set)")
    else:
        print(f"Mode : {PROVIDER}  (model: {MODEL})")
    print("URL  : http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
