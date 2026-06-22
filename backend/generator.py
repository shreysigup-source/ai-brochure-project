import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def build_brochure_prompt(structured_data):
    json_text = json.dumps(structured_data, indent=2)

    prompt = f"""
You are an expert marketing copywriter.

You will be given structured company data in JSON format below. Using ONLY this data, write a professional company brochure.

Write exactly these 5 sections, in this order, using Markdown "##" headings:
## Overview
## Services
## Industries
## Why Us
## Contact
 
Rules:
- Keep the tone professional throughout the entire brochure.
- In the Services section, naturally include both the company's services and products together. Do not create a separate "Products" section.
- Use ONLY the information provided in the JSON data below. Do not invent or assume any facts, names, numbers, or contact details that are not present in the data.
- If a field is empty or missing, either skip that point or write one short generic line. Never make up specific details to fill the gap.
- Return ONLY the brochure content itself. Do not add any preamble, explanation, or closing remarks like "Here is your brochure" or "I hope this helps".

Company data (JSON):
{json_text}
"""
    return prompt

def generate_brochure_text(structured_data):
    prompt = build_brochure_prompt(structured_data)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000
    )

    return response.choices[0].message.content.strip()
