"""LLM client using Google Gemini / Vertex AI generative API.

This module tries to use the official GenAI SDK (google.generativeai / google.genai).
To use:
1. Install the SDK: `pip install google-generative-ai` or `pip install google-genai` depending on the package name.
2. Create an API key in Google Cloud (or Google AI Studio) and set environment variable:
   - `GOOGLE_API_KEY=YOUR_API_KEY`
   - or configure application default credentials via `GOOGLE_APPLICATION_CREDENTIALS`.

This client exposes `generate_text(messages, model=..., **kwargs)` which accepts either a single prompt string
or a list of message dicts in Chat format: [{"role":"system"|"user","content":...}, ...].

It returns a dict: {"content": str, "raw": raw_response}
"""
import os, json

# Try the newer google.generativeai SDK first
try:
    import google.generativeai as genai
    SDK = "google.generativeai"
except Exception:
    genai = None
    SDK = None

# Try older import style
if genai is None:
    try:
        from google import genai as genai_client
        genai = genai_client
        SDK = "google.genai"
    except Exception:
        genai = None

# Configure
API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_CLOUD_API_KEY") or os.getenv("GOOGLE_API_KEY_JSON")
if genai and API_KEY:
    try:
        # some sdk variants use configure, others use Client()
        if hasattr(genai, "configure"):
            genai.configure(api_key=API_KEY)
        elif hasattr(genai, "Client"):
            client = genai.Client(api_key=API_KEY)
        else:
            # fallback: set env var for google auth if using ADC
            pass
    except Exception:
        pass

def _as_prompt_from_messages(messages):
    # If messages is a string then return as single prompt
    if isinstance(messages, str):
        return messages
    # If list of role/content -> convert to a single concatenated prompt
    if isinstance(messages, list):
        parts = []
        for m in messages:
            role = m.get("role","user")
            content = m.get("content","")
            parts.append(f"[{role}] {content}")
        return "\n".join(parts)
    return str(messages)

def generate_text(messages, model="gemini-1.5", max_output_tokens=512, temperature=0.2):
    """Generate text using Gemini via available SDK.

    messages: str or list of {role, content}
    model: model id, e.g. 'gemini-1.5', 'gemini-2.5-pro', 'gemini-2.5-flash'
    Returns: {content: str, raw: ...}
    """
    prompt = _as_prompt_from_messages(messages)
    if genai is None:
        raise RuntimeError("Google GenAI SDK not available. Install `google-generative-ai` and set GOOGLE_API_KEY.")

    # Preferred: use simple generate_content or models.generate_content if available
    try:
        # some SDKs provide genai.generate_text or genai.models.generate_content
        if hasattr(genai, "generate_text"):
            resp = genai.generate_text(model=model, prompt=prompt, temperature=temperature, max_output_tokens=max_output_tokens)
            # resp may have .text or .content
            text = getattr(resp, 'text', None) or getattr(resp, 'content', None) or str(resp)
            return {"content": text, "raw": resp}
        if hasattr(genai, "models") and hasattr(genai.models, "generate_content"):
            resp = genai.models.generate_content(model=model, content=prompt, temperature=temperature, max_output_tokens=max_output_tokens)
            text = resp.text if hasattr(resp, 'text') else json.dumps(resp)
            return {"content": text, "raw": resp}
        # older client style
        if hasattr(genai, "Client") and 'client' in globals():
            # client.models.generate_content
            resp = client.models.generate_content(model=model, contents=prompt)
            # resp may be a dict-like with 'candidates' etc.
            if isinstance(resp, dict):
                c = resp.get('candidates') or resp.get('outputs') or []
                if c:
                    first = c[0]
                    txt = first.get('content') or first.get('text') or str(first)
                    return {"content": txt, "raw": resp}
            return {"content": str(resp), "raw": resp}
    except Exception as e:
        # bubble up as runtime error with context
        raise RuntimeError(f"Gemini generation failed: {e}") from e

    # If none of the SDK entrypoints are present, raise informative error
    raise RuntimeError("No supported genai methods found in the installed SDK.")
