import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError(
        "HF_TOKEN was not found in the .env file."
    )

client = InferenceClient(
    api_key=HF_TOKEN
)


def chat_with_wardrobe(
    wardrobe,
    question,
    chat_history=None
):

    if not wardrobe:
        return (
            "Your wardrobe is currently empty. "
            "Please add some clothing items first."
        )

    wardrobe_items = []

    for index, item in enumerate(
        wardrobe,
        start=1
    ):

        (
            item_id,
            clothing_type,
            color,
            style,
            pattern,
            sleeve,
            confidence,
            ocr_text,
            image_name,
            created_at
        ) = item

        wardrobe_items.append(
            f"""
Item {index}
Type: {clothing_type}
Color: {color}
Style: {style}
Pattern: {pattern}
Sleeve: {sleeve}
Label Text: {ocr_text or "None"}
"""
        )

    wardrobe_text = "\n".join(
        wardrobe_items
    )

    history_text = ""

    if chat_history:

        for message in chat_history:

            history_text += (
                f"{message['role']}: "
                f"{message['content']}\n"
            )

    prompt = f"""
You are StyleVault AI, a professional
personal fashion assistant.

The user's wardrobe is:

{wardrobe_text}

Previous conversation:

{history_text}

User's new question:

{question}

Rules:

1. Only recommend clothes that exist in the wardrobe.
2. Do not invent clothing items.
3. Give practical and simple fashion advice.
4. If the requested clothing is not available,
   clearly say so.
5. Use the clothing type, color, style,
   pattern and sleeve information when useful.
6. Keep the answer friendly and concise.

Answer the user's question directly.
"""

    try:

        response = client.chat.completions.create(

            model="openai/gpt-oss-120b:groq",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are StyleVault AI, "
                        "a professional personal "
                        "fashion assistant."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            max_tokens=500,
            temperature=0.7
        )

        answer = response.choices[0].message.content

        if not answer:

            return (
                "The AI returned an empty response."
            )

        return answer

    except Exception as e:

        return (
            f"AI Chat Error: {str(e)}"
        )