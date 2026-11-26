import os
from openai import OpenAI
from .models import AICache, generate_cache_key
from django.conf import settings

# Initialize Groq client using the OpenAI SDK
client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

MODEL_NAME = "openai/gpt-oss-20b"

PROMPT = """You are a strict news classifier. Categorize the following text into exactly ONE of these categories: 'tech', 'programming', 'science', 'business', or 'world'. Return ONLY the category word in lowercase. Do not include punctuation or explanation."""

def classify_item(title, snippet=""):
    text_to_classify = f"{title} {snippet}".strip()[:1000]
    
    # 1. Check Cache
    cache_key = generate_cache_key(PROMPT, MODEL_NAME, text_to_classify)
    cached_response = AICache.objects.filter(key=cache_key).first()
    if cached_response:
        return cached_response.response.get("category")

    # 2. Call LLM
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": text_to_classify}
            ],
            temperature=0.0,
            max_tokens=10,
        )
        category = response.choices[0].message.content.strip().lower()
        
        # Fallback if LLM hallucinates
        valid_categories = ['tech', 'programming', 'science', 'business', 'world']
        if category not in valid_categories:
            category = 'tech' # Default fallback

        # 3. Save to Cache
        AICache.objects.create(
            key=cache_key,
            response={"category": category}
        )
        
        return category

    except Exception as e:
        print(f"LLM API Error: {e}")
        # Rule-based fallback if API fails
        text_lower = text_to_classify.lower()
        if "python" in text_lower or "code" in text_lower or "developer" in text_lower:
            return "programming"
        return "tech"