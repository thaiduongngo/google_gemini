import google.generativeai as genai
from google.generativeai import GenerativeModel
from generative_ai.configs import SAFETY_SETTINGS


VISION_MODEL = "gemini-pro-visions"


def init_vision_model() -> GenerativeModel:
    return genai.GenerativeModel(
        model_name=VISION_MODEL,
        safety_settings=SAFETY_SETTINGS,
    )
