"""
Text summarisation workflow — uses LiteLLM to summarise arbitrary text.
Registered as 'agent.summarise_text'.
"""

import logging
import os
import httpx

logger = logging.getLogger(__name__)


async def summarise_text(input_data: dict) -> dict:
    """
    Summarise text using configured LLM provider.
    input_data: { text, max_words (optional, default 100) }
    """
    text      = input_data.get("text", "")
    max_words = int(input_data.get("max_words", 100))

    if not text:
        return {"summary": "", "word_count": 0}

    api_key   = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY", "")
    model     = os.getenv("AGENT_MODEL", "deepseek/deepseek-chat-v3-0324:free")
    base_url  = "https://openrouter.ai/api/v1" if os.getenv("OPENROUTER_API_KEY") else "https://api.openai.com/v1"

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": f"Summarise the following text in {max_words} words or fewer. Be concise and factual."},
                    {"role": "user", "content": text},
                ],
                "max_tokens": max_words * 2,
            },
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()

    summary = result["choices"][0]["message"]["content"].strip()
    logger.info(f"Summarised {len(text)} chars -> {len(summary.split())} words")
    return {"summary": summary, "word_count": len(summary.split())}
