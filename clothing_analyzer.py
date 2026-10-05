from PIL import Image
import numpy as np
from transformers import pipeline


# =========================================================
# LOAD AI VISION MODEL
# =========================================================

classifier = pipeline(
    "zero-shot-image-classification",
    model="openai/clip-vit-base-patch32"
)


# =========================================================
# HELPER FUNCTION
# =========================================================

def classify_image(image, labels):

    results = classifier(
        image,
        candidate_labels=labels
    )

    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    return results[0]["label"], results[0]["score"]


# =========================================================
# COLOR DETECTION
# =========================================================

def detect_color(image):

    image = image.resize((100, 100))

    image_array = np.array(image)

    # Ignore extremely bright and dark pixels
    pixels = image_array.reshape(-1, 3)

    average = pixels.mean(axis=0)

    r = average[0]
    g = average[1]
    b = average[2]

    # Basic color classification

    if r < 60 and g < 60 and b < 60:
        return "Black"

    elif r > 200 and g > 200 and b > 200:
        return "White"

    elif r > 150 and g < 100 and b < 100:
        return "Red"

    elif r > 150 and g > 100 and b < 100:
        return "Orange"

    elif r > 150 and g > 120 and b > 120:
        return "Pink"

    elif r > 150 and g > 150 and b < 100:
        return "Yellow"

    elif g > r * 1.2 and g > b * 1.1:
        return "Green"

    elif b > r * 1.2 and b > g * 1.1:
        return "Blue"

    elif r > 100 and g > 70 and b < 70:
        return "Brown"

    else:
        return "Mixed / Other"


# =========================================================
# MAIN CLOTHING ANALYZER
# =========================================================

def analyze_clothing(uploaded_file):

    # Read uploaded image
    image = Image.open(
        uploaded_file
    ).convert("RGB")

    # -----------------------------------------
    # Clothing Type
    # -----------------------------------------

    clothing_labels = [
        "t-shirt",
        "shirt",
        "blouse",
        "crop top",
        "dress",
        "skirt",
        "jeans",
        "trousers",
        "shorts",
        "jacket",
        "hoodie",
        "sweater",
        "kurti",
        "saree",
        "traditional clothing",
        "sportswear"
    ]

    clothing_type, clothing_score = classify_image(
        image,
        clothing_labels
    )

    # -----------------------------------------
    # Style
    # -----------------------------------------

    style_labels = [
        "casual clothing",
        "formal clothing",
        "party wear",
        "sportswear",
        "streetwear",
        "traditional clothing",
        "minimal clothing",
        "trendy fashion"
    ]

    style, style_score = classify_image(
        image,
        style_labels
    )

    # -----------------------------------------
    # Pattern
    # -----------------------------------------

    pattern_labels = [
        "plain solid color clothing",
        "striped clothing",
        "checked clothing",
        "floral clothing",
        "printed clothing",
        "graphic clothing",
        "patterned clothing"
    ]

    pattern, pattern_score = classify_image(
        image,
        pattern_labels
    )

    # -----------------------------------------
    # Sleeve
    # -----------------------------------------

    sleeve_labels = [
        "short sleeve clothing",
        "long sleeve clothing",
        "sleeveless clothing",
        "half sleeve clothing"
    ]

    sleeve, sleeve_score = classify_image(
        image,
        sleeve_labels
    )

    # -----------------------------------------
    # Color
    # -----------------------------------------

    color = detect_color(image)

    # -----------------------------------------
    # Result
    # -----------------------------------------

    result = {
        "clothing_type": clothing_type,
        "clothing_confidence": round(
            clothing_score * 100,
            1
        ),

        "color": color,

        "style": style,
        "style_confidence": round(
            style_score * 100,
            1
        ),

        "pattern": pattern,
        "pattern_confidence": round(
            pattern_score * 100,
            1
        ),

        "sleeve": sleeve,
        "sleeve_confidence": round(
            sleeve_score * 100,
            1
        )
    }

    return result