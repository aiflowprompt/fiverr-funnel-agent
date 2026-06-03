import os
import httpx
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])

SYSTEM = """You are a world-class social media growth strategist and copywriter.
You specialise in creating high-converting content that funnels followers into
paying clients on Fiverr. Every post you write has a clear hook, value, and a
subtle call-to-action that drives traffic to a Fiverr profile. You write with
authority, personality, and platform-native style. Never sound generic or robotic."""

PLATFORM_SPECS = {
    "facebook": {
        "label": "Facebook Post",
        "words": 80,
        "notes": "Conversational, storytelling-driven. Include 1 question to drive comments. End with a soft CTA linking to Fiverr. Use line breaks for readability. 3–5 relevant hashtags at the end."
    },
    "instagram": {
        "label": "Instagram Caption",
        "words": 60,
        "notes": "Hook in first line (stops the scroll). Use emojis strategically. Line breaks every 1–2 sentences. CTA: 'Link in bio 👉'. End with 10–15 niche hashtags on a new line."
    },
    "linkedin": {
        "label": "LinkedIn Post",
        "words": 150,
        "notes": "Professional but personal. Start with a bold insight or contrarian take. Use short paragraphs (1–2 lines). Share a mini-story or result. End with a CTA driving to Fiverr profile. No hashtag spam — max 3 hashtags."
    },
    "twitter": {
        "label": "Twitter/X Thread (3 tweets)",
        "words": 90,
        "notes": "Tweet 1: Bold hook under 280 chars. Tweet 2: The value/insight. Tweet 3: CTA to Fiverr. Label each as Tweet 1, Tweet 2, Tweet 3. Each under 280 characters."
    },
    "tiktok": {
        "label": "TikTok Video Script",
        "words": 120,
        "notes": "Format as a script. Include: [HOOK - 0-3s], [PROBLEM - 3-8s], [VALUE/TIP - 8-25s], [CTA - 25-30s]. Conversational, fast-paced. Written as spoken words. Include 1 on-screen text suggestion per section."
    }
}


def web_search(query: str) -> str:
    try:
        r = httpx.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json", "no_html": "1"},
            timeout=8
        )
        data = r.json()
        results = [d["Text"] for d in data.get("RelatedTopics", [])[:3] if "Text" in d]
        return "\n".join(results) or "No results found."
    except Exception:
        return "Search unavailable."


def generate_batch(
    niche: str,
    service: str,
    fiverr_url: str,
    tone: str = "Professional yet approachable",
    angle: str = ""
) -> dict:
    """
    Generate one post per platform in a single batch.
    Returns a dict keyed by platform name.
    """
    research = web_search(f"{niche} {service} tips trends 2024")

    results = {}
    for platform, spec in PLATFORM_SPECS.items():
        prompt = f"""
Niche: {niche}
Service being sold: {service}
Fiverr profile URL: {fiverr_url}
Content angle / topic: {angle or f"Why clients need {service} for their {niche} business"}
Tone: {tone}
Platform: {spec['label']}
Target word count: {spec['words']} words
Platform-specific rules: {spec['notes']}
Research context: {research}

Write ONE {spec['label']} NOW. Follow all platform rules exactly.
Self-review for conversion power, score 0-10. If below 8, revise once.
Return ONLY the final post — no commentary, no labels, no meta text.
"""
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024
        )
        results[platform] = response.choices[0].message.content.strip()

    return results
