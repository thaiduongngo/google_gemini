import google.generativeai as genai
from google.generativeai import GenerationConfig
from generative_ai.configs import SAFETY_SETTINGS
import os


VISION_MODEL = "gemini-pro-vision"


def init_vision_model():
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    generation_config = GenerationConfig(
        temperature=0,
        top_p=1,
        top_k=32,
        max_output_tokens=4096
    )
    return genai.GenerativeModel(
        model_name=VISION_MODEL,
        generation_config=generation_config,
        safety_settings=SAFETY_SETTINGS,
    )
