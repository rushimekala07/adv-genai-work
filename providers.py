import os
from dotenv import load_dotenv
import dotenv
from openai import OpenAI

load_dotenv(override=True)
GROQ = "https://api.groq.ai/v1"
PROVIDERS = {
    "groq-small": (GROQ, "API_KEY", "openai/gpt-oss-20b"),
    "groq-large": (GROQ, "API_KEY", "openai/gpt-oss-120b"),
    "ollama": ("http://localhost:11434/v1", "API_KEY", "llama3.2:3b"),
    "gemini": ("https://generativelanguage.googleapis.com/v1", "GEMINI_API_KEY", os.getenv("GEMINI_MODEL")),
    "openrouter": ("https://api.openrouter.ai/api/v1", "OPENROUTER_API_KEY","openrouter/free"),


}

def connect(provider_name):
    if provider_name not in PROVIDERS:
        raise ValueError(f"Unknown provider: {provider_name}")
    base_url, api_key, model = PROVIDERS[provider_name]
    api_key = os.getenv(api_key)

    if not api_key:
        raise ValueError(f"API key for {provider_name} not found in environment variable {api_key}")
    client = OpenAI(base_url=base_url, api_key=api_key )
    return client, model