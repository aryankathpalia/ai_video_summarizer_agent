from dotenv import load_dotenv
import os
from groq import Groq

# Load environment variables (e.g. GROQ_API_KEY)
load_dotenv()

def summarize_text(text, model_name="llama-3.1-8b-instant"):
    """
    Summarize long transcripts quickly using Groq's API.
    """
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""
    Summarize the following video transcript clearly and naturally.
    Focus on the main ideas, tone, and humor if relevant.
    Make the summary concise and engaging, around 3–6 sentences.

    Transcript:
    {text}
    """

    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=800,
    )

    return response.choices[0].message.content.strip()
