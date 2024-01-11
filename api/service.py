from generative_ai.configs import LLM_CONFIG
from generative_ai.llms.llm import qna, reduce, refine_text
import generative_ai.audios.audio as audio
import generative_ai.visions.vision as vision


def question_and_answer(
    question: str,
    chat_history: [{}] = None
) -> {}:
    q = question.lower()
    return qna(question=q, chat_history=chat_history)


def reduce_document(document: str) -> str:
    return reduce(document=document)


def get_memory_k() -> str:
    return "{}".format(LLM_CONFIG["MEMORY_K"])


def transcribe(b64_string: str) -> {}:
    res = audio.transcribe_whisper_b64(b64_string=b64_string)
    res = refine_text(text=res)
    return {"response": res}


def ocr(b64_string: str) -> str:
    return vision.ocr(b64_string=b64_string)
