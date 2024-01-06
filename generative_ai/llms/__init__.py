from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseLLM, BaseChatModel
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
from generative_ai.configs import LLM_CONFIG, PROMPTS, SAFETY_SETTINGS


def init_input_vars() -> []:
    return [
        "role",
        "company_name",
        "domain",
        "language",
        "context",
        "question",
    ]


def init_output_format() -> {str: str}:
    return {
        "output_format": PROMPTS["OUT_FORMAT"]
    }


def init_retrieval_template() -> str:
    return """
Response a complete text of item in the ###LIST### if ###DOCUMENT### refers that item in ###LIST###;
Response the text \"None\" if ###DOCUMENT### do not refer any item in ###LIST###.
\"Pru\" or \"Pru-\" is a typical prefix to indicate Prudential's products.

###LIST###
{list}

###DOCUMENT###
{document}

The Response should be a JSON object, without appending markdown code block such as ```json, in the following schema:
\"response\": string  // Response
"""


def init_qa_template() -> str:
    return """
You are a professional {role} for {company_name} in {domain}.
Your task is to precisely answer customers' ###QUESTION### in {language} language.
You must answer ###QUESTION### with ###CONTEXT###. Do not hallucinate an answer.
If the answer cannot be found in the ###CONTEXT###, say \"Tôi xin lỗi, tôi không tìm thấy thông tin được yêu cầu\"

###CONTEXT###
{context}?

###QUESTION###
{question}

The answer must be formatted and rendered as {output_format}.
"""


def init_generation_config() -> {}:
    return {
        "safety_settings": SAFETY_SETTINGS
    }


def init_llm() -> BaseLLM:
    return GoogleGenerativeAI(
        model=LLM_CONFIG["TEXT_MODEL"],
        temperature=LLM_CONFIG["TEMPERATURE"],
        convert_system_message_to_human=True,
        generation_config=init_generation_config(),
        verbose=LLM_CONFIG["VERBOSE"],
    )


def init_chat_llm() -> BaseChatModel:
    return ChatGoogleGenerativeAI(
        model=LLM_CONFIG["TEXT_MODEL"],
        temperature=LLM_CONFIG["TEMPERATURE"],
        convert_system_message_to_human=True,
        generation_config=init_generation_config(),
        verbose=LLM_CONFIG["VERBOSE"],
    )


def init_prompt_template(template: str, input_vars: [str], output_format: {}) -> PromptTemplate:
    return PromptTemplate(
        template=template,
        input_variables=input_vars,
        partial_variables=output_format,
    )


def init_qa_chain(prompt_template: PromptTemplate) -> BaseCombineDocumentsChain:
    return load_qa_chain(
        llm=init_chat_llm(),
        chain_type="stuff",
        prompt=prompt_template,
        verbose=LLM_CONFIG["VERBOSE"],
    )


def init_embeddings() -> Embeddings:
    return GoogleGenerativeAIEmbeddings(
        model=LLM_CONFIG["EMBEDDINGS_MODEL"],
    )
