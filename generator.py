import json
import requests
from config import config

SYSTEM_PROMPT = """You are a prompt engineer for DeepSeek V4 Flash.
Generate a pack of optimized prompts for a specific niche.

Rules:
- Each prompt must include: role instruction, context placeholder, output format
- Cover different use cases within the niche
- Return ONLY valid JSON, no markdown wrapping
- All content in English"""

USER_PROMPT_TEMPLATE = """Generate a pack of 50 optimized prompts for DeepSeek V4 Flash in the niche: {niche}.

Already covered titles (AVOID these exact themes/topics):
{avoid}

Return JSON with this exact structure:
{{
  "title": "50 DeepSeek Prompts for [Niche]",
  "niche": "niche_name",
  "description": "2-3 sentence description of the pack",
  "price": 7.99,
  "tags": ["deepseek", "niche", "ai-prompts", "relevant-tag"],
  "prompts": [
    {{"category": "CategoryName", "prompts": ["prompt1", "prompt2", ...]}}
  ],
  "seo_title": "SEO title max 60 chars",
  "seo_description": "SEO description max 160 chars",
  "pinterest_description": "Pin description with emojis and CTA to Gumroad"
}}
"""

def generate(niche: str, avoid_titles: list[str] | None = None) -> dict:
    avoid_block = "\n".join(f"- {t}" for t in (avoid_titles or [])) or "(none yet)"
    resp = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {config.openrouter_api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": config.deepseek_model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT_TEMPLATE.format(niche=niche, avoid=avoid_block)},
            ],
            "temperature": 0.7,
            "max_tokens": 8000,
        },
        timeout=120,
    )
    resp.raise_for_status()
    content = resp.json()["choices"][0]["message"]["content"]
    content = content.strip().removeprefix("```json").removeprefix("```").removesuffix("```")

    data = json.loads(content)
    data.setdefault("price", 7.99)
    return data
