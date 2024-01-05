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
    return '''
A text in the List could be mentioned in the Document below.\n
Response with a complete text of item in the List if there is a mention referred in the Document;
otherwise response None.\n
\'Pru\' or \'Pru-\' is a typical prefix to indicate Prudential's products.\n\n
List: \n{list}\n\n
Document: \n{document}\n\n
The output should be a json formatted in the following schema:\n
\"context\": string  // response
'''


def init_qa_template(lang: str = "en") -> str:
    if lang == "en":
        return '''
You are a professional {role} for {company_name} in {domain}.\n
Your mission is to precisely and accurately answer customers' questions in {language} language.\n
You must answer questions by using Context below. Do not hallucinate an answer.\n
If the answer cannot be found in the Context, say 'Tôi xin lỗi, tôi không tìm thấy thông tin được yêu cầu'\n
The answer should be formatted and rendered as {output_format}.\n\n

Context: \n{context}?\n
Question: \n{question}\n
Answer:
'''
    elif lang == "vi":
        return '''
Bạn là {role} chuyên nghiệp cho {company_name} trong lĩnh vực {domain}.\n
Bạn có nhiệm vụ trả lời các thắc mắc của khách hàng một cách lịch sự nhất có thể.\n
Trả lời câu hỏi chính xác nhất có thể bằng {language} và bằng cách sử dụng Context được cung cấp.\n
Nếu không tìm thấy câu trả lời trong Context, hãy trả lời 'Tôi xin lỗi, tôi không tìm thấy thông tin được yêu cầu'.\n
Tuyệt đối không suy diễn.\n
Câu trả lời phải được hiển thị dưới dạng {output_format}.
\n\n
Context: \n{context}?\n
Question: \n{question}\n
Answer:
'''
    else:
        return ''


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
