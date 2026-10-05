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


def generate_packing_plan(
    wardrobe,
    destination,
    days,
    purpose
):

    if not wardrobe:
        return {
            "status": "empty",
            "message": "Your wardrobe is empty. Add some clothes first."
        }

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
"""
        )

    wardrobe_text = "\n".join(
        wardrobe_items
    )

    prompt = f"""
You are StyleVault AI, a smart travel
packing assistant.

USER WARDROBE:

{wardrobe_text}

TRIP DETAILS:

Destination: {destination}
Number of Days: {days}
Purpose: {purpose}

RULES:

1. Only use clothing items from the wardrobe.
2. Do not invent clothes.
3. Create a practical packing plan.
4. Avoid unnecessary duplicate items.
5. Consider the trip purpose.
6. Try to create outfits that can be mixed and matched.
7. Mention if the wardrobe is insufficient.
8. Keep the answer clear and organized.

Use this format:

PACKING PLAN

CLOTHING
- Item

OUTFIT COMBINATIONS
1. Outfit
2. Outfit
3. Outfit

WHY THESE ITEMS
Explain why they are useful.

PACKING TIPS
1. Tip
2. Tip
3. Tip

MISSING ITEMS
Mention anything important that is unavailable.
"""

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b:groq",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are StyleVault AI, "
                        "a professional smart packing "
                        "assistant."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            max_tokens=700,
            temperature=0.7
        )

        answer = response.choices[0].message.content

        if not answer:

            return {
                "status": "error",
                "message": "The AI returned an empty response."
            }

        return {
            "status": "success",
            "response": answer
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }