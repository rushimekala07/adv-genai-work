"""Use Groq, Gemini, OpenRouter, or local Ollama through one OpenAI-style client."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI

from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(ENV_PATH, override=True)

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OLLAMA_BASE_URL = "http://localhost:11434/v1"


@dataclass(frozen=True)
class ProviderConfig:
    """Connection settings for one selectable model."""

    base_url: str
    model: str
    api_key_env: str | None = None
    fallback_api_key_env: str | None = None
    api_key: str | None = None
    timeout: float = 30.0
    max_retries: int = 2


PROVIDERS: dict[str, ProviderConfig] = {
    "groq-small": ProviderConfig(
        base_url=GROQ_BASE_URL,
        model=(
            os.getenv("GROQ_SMALL_MODEL")
            or os.getenv("MODEL")
            or "openai/gpt-oss-20b"
        ),
        api_key_env="GROQ_API_KEY",
        fallback_api_key_env="API_KEY",
    ),
    "groq-large": ProviderConfig(
        base_url=GROQ_BASE_URL,
        model=os.getenv("GROQ_LARGE_MODEL") or "openai/gpt-oss-120b",
        api_key_env="GROQ_API_KEY",
        fallback_api_key_env="API_KEY",
    ),
    "gemini": ProviderConfig(
        base_url=GEMINI_BASE_URL,
        model=os.getenv("GEMINI_MODEL") or "gemini-2.5-flash",
        api_key_env="GEMINI_API_KEY",
    ),
    "openrouter": ProviderConfig(
        base_url=OPENROUTER_BASE_URL,
        model=os.getenv("OPENROUTER_MODEL") or "",
        api_key_env="OPENROUTER_API_KEY",
    ),
    "ollama-qwen2.5:1.5b": ProviderConfig(
        base_url=OLLAMA_BASE_URL,
        model="qwen2.5:1.5b",
        api_key="ollama",
        timeout=60.0,
        max_retries=0,
    ),
}


def _get_api_key(name: str, config: ProviderConfig) -> str:
    if config.api_key is not None:
        return config.api_key

    key = os.getenv(config.api_key_env or "")
    if not key and config.fallback_api_key_env:
        key = os.getenv(config.fallback_api_key_env)
    if not key or "paste_your" in key.lower():
        expected = config.api_key_env or "an API key"
        raise ValueError(f"Provider {name!r} requires a valid {expected} in your .env file.")
    return key


def get_client(name: str) -> OpenAI:
    """Create an OpenAI-compatible client for a provider name in ``PROVIDERS``."""
    try:
        config = PROVIDERS[name]
    except KeyError:
        choices = ", ".join(PROVIDERS)
        raise ValueError(f"Unknown provider {name!r}. Choose one of: {choices}.") from None

    return OpenAI(
        base_url=config.base_url,
        api_key=_get_api_key(name, config),
        timeout=config.timeout,
        max_retries=config.max_retries,
    )


def get_provider(name: str) -> tuple[OpenAI, str]:
    """Return the configured client and model name for a provider."""
    try:
        config = PROVIDERS[name]
    except KeyError:
        choices = ", ".join(PROVIDERS)
        raise ValueError(f"Unknown provider {name!r}. Choose one of: {choices}.") from None

    if not config.model:
        raise ValueError(
            "Set OPENROUTER_MODEL in your .env file to the OpenRouter model ID you want to use."
        )
    return get_client(name), config.model


def main() -> None:
    """Send a small test prompt; optionally choose the provider on the command line."""
    name = sys.argv[1] if len(sys.argv) > 1 else "groq-small"
    client, model = get_provider(name)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Say hello in one short sentence."}],
    )
    print(response.choices[0].message.content or "")


if __name__ == "__main__":
    main()
