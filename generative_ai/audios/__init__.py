from openai import OpenAI
import os
import whisper
import torch


AUDIO_MODEL = "large"
OPENAPI_AUDIO_MODEL = "whisper-1"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def init_whisper_model():
    return whisper.load_model(AUDIO_MODEL).to(DEVICE)


def init_openai_client():
    return OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
