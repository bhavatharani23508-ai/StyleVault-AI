import easyocr
from PIL import Image
import numpy as np
import io


# Load OCR model once
reader = easyocr.Reader(
    ["en"],
    gpu=False
)


def extract_text(uploaded_file):

    # Convert Streamlit UploadedFile to bytes
    image_bytes = uploaded_file.getvalue()

    # Convert bytes to PIL image
    image = Image.open(
        io.BytesIO(image_bytes)
    ).convert("RGB")

    # Convert PIL image to NumPy array
    image_array = np.array(image)

    # Run OCR
    results = reader.readtext(
        image_array
    )

    detected_text = []

    for box, text, confidence in results:

        detected_text.append({
            "text": text,
            "confidence": round(
                float(confidence),
                2
            )
        })

    return detected_text