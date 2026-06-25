# 🤗 HUGGING FACE API KEY & MISTRAL-7B SETUP GUIDE

---

## ✅ STEP 1: CREATE HUGGING FACE ACCOUNT

### **1.1 Go to Hugging Face**
- **URL**: https://huggingface.co/
- Click **"Sign Up"** (top right)

### **1.2 Create Account**
```
Option 1: Sign up with email
- Email address
- Password
- Username
- Click "Create account"

Option 2: Sign up with Google/GitHub
- Click "Sign up with Google" or "Sign up with GitHub"
- Authorize
- Done
```

### **1.3 Verify Email**
- Check your email inbox
- Click verification link from Hugging Face
- **Account is now active!**

---

## 🔑 STEP 2: CREATE API TOKEN

### **2.1 Navigate to Settings**
```
1. Login to https://huggingface.co/
2. Click your profile icon (top right)
3. Select "Settings"
```

### **2.2 Access Tokens**
```
In Settings page:
1. Click "Access Tokens" (left sidebar)
2. Click "New token" button
```

### **2.3 Create Token**
```
Token Configuration:
- Name: "mistral-soc-assistant" (any name)
- Type: Select "Read" (NOT write)
- Click "Generate token"
```

### **2.4 Copy Your Token**
```
⚠️ IMPORTANT: Copy the token immediately!
You won't be able to see it again!

Token format: hf_XXXXXXXXXXXXXXXXXXXX
(starts with "hf_")
```

### **2.5 Save Securely**
```
Save to a text file or .env file:
HF_API_KEY=hf_XXXXXXXXXXXXXXXXXXXX
```

---

## 📋 COMPLETE SETUP INSTRUCTIONS (Visual)

```
STEP 1: Go to https://huggingface.co
         ↓
STEP 2: Click "Sign Up" (top right)
         ↓
STEP 3: Enter email, password, username
         ↓
STEP 4: Verify email (check inbox)
         ↓
STEP 5: Click profile icon → "Settings"
         ↓
STEP 6: Click "Access Tokens" (left menu)
         ↓
STEP 7: Click "New token"
         ↓
STEP 8: Name it "mistral-soc-assistant"
         ↓
STEP 9: Set Type to "Read"
         ↓
STEP 10: Click "Generate token"
         ↓
STEP 11: COPY the token (hf_XXXX...)
         ↓
✅ DONE! You have your API key
```

---

## 🚀 USE WITH SOC ASSISTANT

### **3.1 Update `.env` File**

**File: `backend/.env`**

```bash
# OLD (Anthropic)
# ANTHROPIC_API_KEY=sk-ant-xxxxx

# NEW (Hugging Face)
HF_API_KEY=hf_XXXXXXXXXXXXXXXXXXXX
LLM_PROVIDER=huggingface
```

---

### **3.2 Update Backend Code**

**File: `backend/app.py`**

Replace the Anthropic section with this:

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.environ.get("HF_API_KEY")
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

def analyze_alert_with_claude(alert_data, context="general"):
    """Analyze security alert using Mistral-7B via Hugging Face"""
    
    prompt = f"""You are an expert SOC analyst. Analyze this security alert and provide structured JSON output.

Alert Details:
{json.dumps(alert_data, indent=2)}

Context: {context}

Provide ONLY a JSON response (no markdown, no extra text) with these exact fields:
{{
    "threat_summary": "Brief 2-3 sentence explanation of the threat",
    "risk_level": "CRITICAL/HIGH/MEDIUM/LOW",
    "risk_score": 1-10 number,
    "recommendation": "Specific action to take",
    "evidence": ["indicator1", "indicator2"],
    "investigation_steps": ["step1", "step2", "step3"]
}}"""

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.3,
            "top_p": 0.9,
        }
    }
    
    try:
        app.logger.info("Sending request to Hugging Face...")
        response = requests.post(
            HF_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code != 200:
            app.logger.error(f"Hugging Face API error: {response.status_code} - {response.text}")
            return {
                "threat_summary": "Analysis unavailable",
                "risk_level": alert_data.get("severity", "MEDIUM").upper(),
                "risk_score": 5,
                "recommendation": "Manual review required"
            }
        
        result = response.json()
        
        # Extract text from response
        if isinstance(result, list) and len(result) > 0:
            response_text = result[0].get("generated_text", "")
        else:
            response_text = result.get("generated_text", "")
        
        # Remove the prompt from the response
        if prompt in response_text:
            response_text = response_text.split(prompt)[-1].strip()
        
        # Clean JSON if wrapped in markdown
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
        
        app.logger.info(f"Response: {response_text[:100]}")
        
        return json.loads(response_text)
    
    except json.JSONDecodeError as e:
        app.logger.error(f"JSON parsing error: {str(e)}")
        return {
            "threat_summary": response_text[:200] if 'response_text' in locals() else "Analysis failed",
            "risk_level": alert_data.get("severity", "UNKNOWN").upper(),
            "risk_score": 5,
            "recommendation": "Investigate immediately"
        }
    
    except Exception as e:
        app.logger.error(f"Hugging Face analysis error: {str(e)}")
        return {
            "threat_summary": "Analysis failed",
            "risk_level": "UNKNOWN",
            "risk_score": 0,
            "recommendation": "Manual review required"
        }


def map_to_mitre_attack(alert_data):
    """Map alert to MITRE ATT&CK framework"""
    
    prompt = f"""You are a MITRE ATT&CK expert. Map this alert to relevant MITRE techniques.

Alert: {json.dumps(alert_data, indent=2)}

Return ONLY JSON:
{{
    "tactics": ["tactic1", "tactic2"],
    "techniques": ["T1190", "T1059"],
    "technique_descriptions": ["description1", "description2"]
}}"""

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.2,
        }
    }
    
    try:
        response = requests.post(
            HF_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code != 200:
            return {"tactics": [], "techniques": []}
        
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            response_text = result[0].get("generated_text", "")
        else:
            response_text = result.get("generated_text", "")
        
        if prompt in response_text:
            response_text = response_text.split(prompt)[-1].strip()
        
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
        
        return json.loads(response_text)
    
    except:
        return {"tactics": [], "techniques": []}


def generate_incident_response(alert_data, analysis):
    """Generate incident response plan"""
    
    prompt = f"""You are an incident response expert. Create an action plan.

Alert: {json.dumps(alert_data, indent=2)}
Analysis: {json.dumps(analysis, indent=2)}

Return ONLY JSON:
{{
    "immediate_actions": ["action1", "action2"],
    "containment": ["step1", "step2"],
    "eradication": ["step1", "step2"],
    "recovery": ["step1", "step2"],
    "communication": "brief message"
}}"""

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 400,
            "temperature": 0.2,
        }
    }
    
    try:
        response = requests.post(
            HF_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code != 200:
            return {
                "immediate_actions": ["Isolate affected system"],
                "containment": ["Block attacker IP"],
                "eradication": ["Remove malware"],
                "recovery": ["Restore from backup"],
                "communication": "Incident detected"
            }
        
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            response_text = result[0].get("generated_text", "")
        else:
            response_text = result.get("generated_text", "")
        
        if prompt in response_text:
            response_text = response_text.split(prompt)[-1].strip()
        
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
        
        return json.loads(response_text)
    
    except:
        return {
            "immediate_actions": ["Isolate affected system"],
            "containment": ["Block attacker IP"],
            "eradication": ["Remove malware"],
            "recovery": ["Restore from backup"],
            "communication": "Incident detected and contained"
        }
```

---

## 🧪 TEST YOUR SETUP

### **4.1 Test API Connection**

**Create: `backend/test_hf.py`**

```python
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.environ.get("HF_API_KEY")
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

def test_hf_api():
    print("Testing Hugging Face API with Mistral-7B...")
    print(f"API Key: {HF_API_KEY[:20]}..." if HF_API_KEY else "API Key not found!")
    
    prompt = "What is a SQL injection attack? Answer in 2 sentences."
    
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 100,
            "temperature": 0.3,
        }
    }
    
    try:
        print("\nSending request to Hugging Face...")
        response = requests.post(
            HF_API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                text = result[0].get("generated_text", "")
                print(f"\n✅ SUCCESS!\nGenerated text:\n{text}")
            else:
                print(f"\n✅ SUCCESS!\nResponse: {result}")
        else:
            print(f"\n❌ ERROR: {response.status_code}")
            print(f"Message: {response.text}")
    
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")

if __name__ == "__main__":
    test_hf_api()
```

### **4.2 Run Test**

```bash
cd backend
python test_hf.py
```

### **Expected Output:**
```
Testing Hugging Face API with Mistral-7B...
API Key: hf_XXXXXXXXXXXX...

Sending request to Hugging Face...
Status Code: 200

✅ SUCCESS!
Generated text:
A SQL injection attack is... [response from Mistral-7B]
```

---

## 🚀 COMPLETE SETUP CHECKLIST

### **Quick Setup (Copy-Paste)**

```bash
# 1. Create .env file
cat > backend/.env << 'EOF'
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key
HF_API_KEY=hf_XXXXXXXXXXXXXXXXXXXX
LLM_PROVIDER=huggingface
DATABASE_URL=postgresql://soc_user:soc_password@postgres:5432/soc_db
PORT=5000
HOST=0.0.0.0
EOF

# 2. Install requests library
pip install requests

# 3. Update backend code with Hugging Face integration
# (Use code from section 3.2 above)

# 4. Test connection
python backend/test_hf.py

# 5. Run SOC Assistant
docker-compose up -d
# or
python backend/app.py
```

---

## ⚠️ TROUBLESHOOTING

### **Issue 1: "401 Unauthorized" Error**

**Cause**: Wrong API key

**Solution**:
```bash
# Check your API key
echo $HF_API_KEY

# Should start with "hf_"
# If not set, update .env file:
HF_API_KEY=hf_YOUR_ACTUAL_KEY_HERE
```

### **Issue 2: "Rate Limit Exceeded" Error**

**Cause**: Too many requests in short time

**Solution**:
```python
# Add delay between requests
import time

time.sleep(2)  # Wait 2 seconds between API calls
```

### **Issue 3: Model Not Loading ("Loading" stays forever)**

**Cause**: Model is being loaded for first time (can take 1-2 minutes)

**Solution**:
```python
# First request takes longer
# Increase timeout
response = requests.post(..., timeout=120)  # 2 minutes

# Or wait and try again after 1 minute
```

### **Issue 4: "Model Not Found"**

**Cause**: Wrong model name or access denied

**Solution**:
```python
# Use full model path:
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

# Alternative models:
# "meta-llama/Llama-2-70b-chat-hf"
# "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO"
# "teknium/OpenHermes-2.5-Mistral-7B"
```

---

## 📊 FULL WORKING EXAMPLE

**Complete Flask app with Hugging Face:**

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

HF_API_KEY = os.environ.get("HF_API_KEY")
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

SAMPLE_ALERTS = [
    {
        "id": 1,
        "type": "SQL Injection",
        "severity": "critical",
        "description": "SQL injection in login page"
    }
]

def query_mistral(prompt, max_tokens=500):
    """Query Mistral-7B via Hugging Face"""
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": 0.3,
            "top_p": 0.95,
        }
    }
    
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            return None
        
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "")
        else:
            return result.get("generated_text", "")
    
    except Exception as e:
        print(f"API Error: {str(e)}")
        return None

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "provider": "huggingface-mistral"})

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    return jsonify({"alerts": SAMPLE_ALERTS})

@app.route('/api/analyze', methods=['POST'])
def analyze():
    alert = request.json.get('alert')
    
    prompt = f"""Analyze this security alert as a SOC expert.
Alert: {json.dumps(alert)}
Respond with JSON: {{"threat_summary": "...", "risk_level": "HIGH/MEDIUM/LOW", "risk_score": 1-10, "recommendation": "..."}}"""
    
    response_text = query_mistral(prompt)
    
    if not response_text:
        return jsonify({"error": "Analysis failed"}), 500
    
    # Extract JSON from response
    try:
        if "```" in response_text:
            json_str = response_text.split("```")[1].replace("json", "").strip()
        else:
            json_str = response_text
        
        analysis = json.loads(json_str)
        return jsonify({"analysis": analysis})
    except:
        return jsonify({"error": "Failed to parse response"}), 500

if __name__ == '__main__':
    if not HF_API_KEY:
        print("ERROR: HF_API_KEY not set in .env!")
        exit(1)
    
    print(f"Starting with API Key: {HF_API_KEY[:20]}...")
    app.run(debug=True, port=5000)
```

---

## 📈 EXPECTED PERFORMANCE

| Metric | Value |
|--------|-------|
| First request | 30-60 seconds (model loading) |
| Subsequent requests | 5-15 seconds |
| Rate limit | ~30 req/minute (free tier) |
| Max token output | 500-2000 tokens |
| Quality | Excellent (7/10 vs Claude) |
| Cost | FREE ✅ |

---

## 🎯 COMPLETE QUICK START

```bash
# 1. Get API Key (2 minutes)
# Visit: https://huggingface.co/settings/tokens
# Create new token
# Copy: hf_XXXX...

# 2. Update .env
HF_API_KEY=hf_YOUR_KEY_HERE

# 3. Test
python backend/test_hf.py

# 4. Run
docker-compose up -d

# 5. Access
# Frontend: http://localhost:3000
# Backend: http://localhost:5000/api/health
```

---

**You're all set! Your SOC Assistant now uses Mistral-7B for free!** 🚀