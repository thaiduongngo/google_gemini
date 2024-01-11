from generative_ai.audios import init_openai_client, init_whisper_model, OPENAPI_AUDIO_MODEL
import base64
import uuid
import whisper
import os
from generative_ai.configs import LLM_CONFIG


def b64_to_file(b64_string: str) -> str:
    b64_str = b64_string.split(",")[1]
    file_name = "tmp_audio_{}.webm".format(uuid.uuid4().hex)
    with open(file_name, "wb") as f:
        f.write(base64.b64decode(b64_str))
    f.close()
    return file_name


def transcript_openai_b64(b64_string: str) -> str:
    file_name = b64_to_file(b64_string=b64_string)
    res = transcript_openai(file_name=file_name)
    os.remove(file_name)
    return res


def transcript_openai(file_name: str) -> str:
    audio_file = open(file_name, "rb")
    client = init_openai_client()
    return client.audio.transcriptions.create(
        model=OPENAPI_AUDIO_MODEL,
        file=audio_file,
        response_format="text",
    )


def transcribe_whisper_b64(b64_string: str) -> str:
    file_name = b64_to_file(b64_string=b64_string)
    res = transcribe_whisper(file_name=file_name)
    os.remove(file_name)
    return res


def transcribe_whisper(file_name: str) -> str:
    audio_file = whisper.load_audio(file_name)
    model = init_whisper_model()
    res = model.transcribe(
        audio_file,
        language="vi",
        fp16=False,
        verbose=LLM_CONFIG["VERBOSE"],
    )
    return res["text"]
