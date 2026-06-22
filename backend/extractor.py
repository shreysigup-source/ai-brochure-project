import os
import json
from groq import Groq
from dotenv import load_dotenv
import tiktoken

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def build_prompt(data):
    combined_text = ""
    for category, text in data.items():
        if text:
            combined_text += f"\n\n--- {category.upper()} PAGE CONTENT ---\n{text[:5000]}"

    prompt = f"""
You are given raw website content from different pages of a company.
Read the content carefully and extract structured information.

Return ONLY a valid JSON object in this exact format, with no extra text, no markdown, no explanation:

{{
  "company_name": "...",
  "overview": "...",
  "services": ["...", "..."],
  "products": ["...", "..."],
  "industries": ["...", "..."],
  "differentiators": ["...", "..."],
  "contact": {{
    "email": "...",
    "phone": "...",
    "address": "..."
  }}
}}

Rules:
- If some information is not found, use an empty string "" or empty list [].
- Do not invent information that is not present in the content.

Website content:
{combined_text}
"""
    return prompt

def extract_structured_data(crawled_data):
    prompt = build_prompt(crawled_data)

    # --- INPUT TOKEN COUNTING (tiktoken) ---
    # cl100k_base is the encoding used by most modern LLMs, close enough for estimation
    encoder = tiktoken.get_encoding("cl100k_base")
    input_tokens = len(encoder.encode(prompt))
    print(f"[EXTRACTOR] Input tokens (estimated via tiktoken): {input_tokens}")

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000
    )

    # --- OUTPUT TOKEN COUNTING (from API response metadata) ---
    # Groq returns exact token counts in response.usage
    print(f"[EXTRACTOR] Input tokens (exact from Groq): {response.usage.prompt_tokens}")
    print(f"[EXTRACTOR] Output tokens (exact from Groq): {response.usage.completion_tokens}")
    print(f"[EXTRACTOR] Total tokens used: {response.usage.total_tokens}")

    raw_output = response.choices[0].message.content.strip()

    if raw_output.startswith("```"):
        raw_output = raw_output.strip("`")
        raw_output = raw_output.replace("json", "", 1).strip()

    try:
        structured_data = json.loads(raw_output)
    except json.JSONDecodeError:
        print("JSON parse error. Raw output was:")
        print(raw_output)
        structured_data = None

    return structured_data


if __name__ == "__main__":
    from crawler import crawl_website

    crawled_data = crawl_website("https://webscraper.io")
    result = extract_structured_data(crawled_data)
    print(json.dumps(result, indent=2))