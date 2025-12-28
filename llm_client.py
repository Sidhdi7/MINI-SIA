import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # loads .env file

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY not found. Check your .env file."
    )

client = OpenAI(api_key=api_key)

def ask_llm(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip()
