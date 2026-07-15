"""
IDA Vision & Art Module
Handles image analysis (Vision) and image generation (DALL-E).
"""

import base64

from dotenv import load_dotenv

from logger import log_error
from providers import create_provider

load_dotenv()


def _get_client():
    """Return the underlying OpenAI-compatible client from the configured provider."""
    return create_provider()._get_client()


def analyze_image(image_path, prompt="Что на этом изображении?"):
    """Analyze image using GPT-4o Vision."""

    def encode_image(path):
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    base64_image = encode_image(image_path)

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                        },
                    ],
                }
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content
    except Exception as e:
        log_error("Vision error", e)
        return f"Ошибка зрения: {str(e)}"

def generate_image(prompt):
    """Generate image using DALL-E 3."""
    try:
        client = _get_client()
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        log_error("Image generation error", e)
        return f"Ошибка генерации: {str(e)}"
