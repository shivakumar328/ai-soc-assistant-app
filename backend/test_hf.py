#!/usr/bin/env python3
"""
Quick connectivity test for your Hugging Face token + chosen model.

Usage:
    cd backend
    cp .env.example .env        # then put your HF_API_KEY in .env
    python test_hf.py

It reads HF_API_KEY / HF_MODEL / HF_BASE_URL from the environment (or .env)
and makes a single chat-completion call.
"""
import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import requests

HF_API_KEY = (os.environ.get("HF_API_KEY") or os.environ.get("HUGGINGFACE_API_KEY") or "").strip()
HF_MODEL = os.environ.get("HF_MODEL", "meta-llama/Llama-3.1-8B-Instruct")
HF_BASE_URL = os.environ.get("HF_BASE_URL", "https://router.huggingface.co/v1")

if not HF_API_KEY:
    print("❌ HF_API_KEY is not set. Add it to backend/.env or export it.")
    sys.exit(1)

print(f"Model     : {HF_MODEL}")
print(f"Endpoint  : {HF_BASE_URL}/chat/completions")
print("Sending a test prompt...\n")

resp = requests.post(
    f"{HF_BASE_URL}/chat/completions",
    headers={"Authorization": f"Bearer {HF_API_KEY}", "Content-Type": "application/json"},
    json={
        "model": HF_MODEL,
        "max_tokens": 60,
        "temperature": 0.2,
        "messages": [{"role": "user", "content": "Reply with one short sentence confirming you are reachable."}],
    },
    timeout=90,
)

if resp.status_code == 200:
    msg = resp.json()["choices"][0]["message"]["content"].strip()
    print("✅ SUCCESS:", msg)
else:
    print(f"❌ HTTP {resp.status_code}: {resp.text[:400]}")
    if "not a chat model" in resp.text or "not supported by any provider" in resp.text:
        print("\nℹ️  This model isn't available on HF serverless inference for your account.")
        print("   Try a known-working free model, e.g.:")
        print("     HF_MODEL=meta-llama/Llama-3.1-8B-Instruct")
        print("     HF_MODEL=Qwen/Qwen2.5-7B-Instruct")
    sys.exit(1)
