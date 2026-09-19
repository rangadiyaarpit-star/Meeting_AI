import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def generate_notes(transcript):

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        return "Error: OPENROUTER_API_KEY not found. Please check your .env file."

    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )

    if not transcript or not transcript.strip():
        return "No transcript available to generate AI notes."

    transcript = transcript[:12000]

    prompt = f"""
You are an expert AI Meeting Assistant.

Analyze the transcript carefully.

Generate a professional report in EXACTLY this format:

📋 Executive Summary

Write a detailed but concise summary of the conversation in 3-5 sentences.

🔑 Key Discussion Points

• Point 1
• Point 2
• Point 3

✅ Action Items

List only real action items.

If there are no action items write:
• No action items identified.

🚀 Next Steps

Suggest reasonable next steps based only on the conversation.

📊 Meeting Insights

• Conversation Type
• Participants Mentioned
• Overall Tone
• Actionable Content (Yes/No)

Rules:

1. Use professional business language.
2. If the conversation is casual, mention that clearly.
3. Never invent facts not present in the transcript.
4. Detect participant names only if actually mentioned.
5. Make output visually attractive.
6. Use the emojis exactly as shown above.
7. Return only the final report.

Transcript:

{transcript}
"""

    try:
        response = client.chat.completions.create(
            model="google/gemini-2.5-flash",
            max_tokens=1000,
            temperature=0.4,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI Notes Error: {str(e)}"