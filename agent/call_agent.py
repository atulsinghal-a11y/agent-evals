import requests
import os
from dotenv import load_dotenv
import json
import ast

load_dotenv()

BASE_URL = "http://sit-prism-agent-service.dev.prismforce.local:8080"

HEADERS = {
    "x-client-id": "e8954980-e9c3-4100-a6e2-34480fe04779",
    "x-user-role": "RMGR",
    "x-user-id": "e39daa38-2782-4b00-875d-2a26dde6f2b7",
    "x-api-key": "prism_service_call_key_12345",
    "Content-Type": "application/json"
}


def create_thread():
    url = f"{BASE_URL}/threads"

    payload = {
        "metadata": {
            "source": "eval_script",
            "testdata": "auto"
        }
    }

    res = requests.post(url, headers=HEADERS, json=payload, timeout=60)
    res.raise_for_status()

    data = res.json()

    # adjust if key differs
    return data["thread_id"]


def run_agent(thread_id, prompt):
    url = f"{BASE_URL}/threads/{thread_id}/runs/stream"

    payload = {
        "configurable": {
            "temperature": 0.3
        },
        "input": {
            "messages": [
                {
                    "content": prompt,
                    "role": "user"
                }
            ]
        },
        "stream_mode": ["thinking"]
    }

    res = requests.post(
        url,
        headers=HEADERS,
        json=payload,
        stream=True,   # IMPORTANT for streaming
        timeout=120
    )

    res.raise_for_status()

    full_response = ""

    # Handle streaming chunks
    for line in res.iter_lines():
        if not line:
            continue
        
        decoded = line.decode("utf-8")
        if decoded.startswith("data:"):
            raw_data = decoded.replace("data:", "").strip()

            try:
                # Your API returns Python dict-like strings → use ast
                data = ast.literal_eval(raw_data)

                # ✅ BEST SOURCE → final response
                if "full_response" in data:
                    full_response = data["full_response"]

                # fallback (if needed)
                elif "delta" in data:
                    full_response += data["delta"]

            except:
                continue

    return full_response.strip()


def call_agent(prompt: str) -> str:
    """
    Main function used by eval system
    """

    try:
        thread_id = create_thread()
        response = run_agent(thread_id, prompt)

        return response if response else "NO_RESPONSE"

    except Exception as e:
        return f"ERROR: {str(e)}"