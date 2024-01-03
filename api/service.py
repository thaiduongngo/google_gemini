from genai_llms.configs import LLM_CONFIG
from genai_llms.llm import qna, reduce


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
