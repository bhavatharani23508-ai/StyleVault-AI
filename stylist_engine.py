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


def generate_outfit(wardrobe, occasion, preference):

    if not wardrobe:
        return {
            "status": "empty",
            "message": "Your wardrobe is empty."
        }

    wardrobe_items = []

    for index, item in enumerate(wardrobe, start=1):

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

    wardrobe_text = "\n".join(wardrobe_items)

    prompt = f"""
You are StyleVault AI, a professional personal
fashion stylist.

USER'S WARDROBE:
{wardrobe_text}

USER REQUEST:
Occasion: {occasion}
Style Preference: {preference}

RULES:
- Only use clothing items from the wardrobe.
- Never invent clothing items.
- Create a practical outfit.
- Explain why the outfit works.
- Give 3 styling tips.
- Give one alternative outfit if possible.
- If the wardrobe is insufficient, explain what is missing.

Use this format:

OUTFIT
List the selected clothing items.

WHY IT WORKS
Explain the combination.

STYLING TIPS
1. Tip
2. Tip
3. Tip

ALTERNATIVE
Give another combination using available items.
"""

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b:groq",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are StyleVault AI, "
                        "a professional personal fashion stylist."
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