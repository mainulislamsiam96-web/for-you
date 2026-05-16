import json
import re
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

SYSTEM_PROMPT = """
You are an order parser for Victory Footwear, a wholesale shoe company in Bangladesh.
Salespersons send orders via WhatsApp in messy formats.
Extract clean order data and return ONLY valid JSON.

RULES:
1. Extract buyer name
2. Extract article numbers like 8-4021, 5-60167, 3-6335
3. Quantities: dui=2, tin=3, char=4, panch=5
4. Default unit is carton
5. Return only JSON, no explanation

Return this format:
{
  "buyer_name": "name",
  "salesperson": null,
  "items": [{"sku": "8-4021", "quantity": 5, "unit": "carton"}],
  "confidence": "high",
  "warnings": []
}
"""

def parse_order(message: str) -> dict:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Parse this order:\n\n{message}"}
        ],
        temperature=0
    )
    raw_text = response.choices[0].message.content
    clean = re.sub(r"```(?:json)?|```", "", raw_text).strip()
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        return {"buyer_name": "Unknown", "items": [], "confidence": "low", "warnings": [raw_text]}
