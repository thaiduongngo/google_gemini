from pprint import pprint
from langchain.vectorstores.pgvector import PGVector
from langchain.chains import LLMChain
from langchain.schema import Document
from dotenv import load_dotenv
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseLLM, BaseChatModel
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
from google_genai.configs import LLM_CONFIG, PROMPTS, PERSISTENCE, SAFETY_SETTINGS
import json


HR = "-" * 140


load_dotenv()


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
    otherwise response None.\n\n

    List: \n{list}\n
    Document: \n{document}\n\n

    The output should be a json formatted in the following schema:\n
    "context": string  // response
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


def load_vectorstore(collection_name: str):
    return PGVector.from_existing_index(
        embedding=init_embeddings(),
        collection_name=collection_name,
        connection_string=PERSISTENCE["CONNECTION_STRING"],
    )


def semantic_search(
        query: str,
        k: int,
        collection_name: str,
):
    vs = load_vectorstore(collection_name)

    return vs.similarity_search(
        query=query,
        k=k,
    )


def semantic_search_with_score(
        query: str,
        k: int,
        collection_name: str,
):
    vs = load_vectorstore(collection_name)

    return vs.similarity_search_with_score(
        query=query,
        k=k,
    )


def get_products(as_string: bool = False):
    products = []
    products_str = ""

    docs = semantic_search(
        query=PERSISTENCE["PRODUCTS"],
        k=50,
        collection_name=PERSISTENCE["PRODUCTS"],
    )

    for doc in docs:
        if as_string:
            products_str = "{}- {}\n".format(products_str, doc.page_content)
        else:
            products.append({"product_name": doc.page_content})

    if as_string:
        return products_str
    else:
        return products


def get_pre_context(chat_history: [{}]) -> str:
    if chat_history is not None:
        rev_chat_history = chat_history[::-1]
        for chat_entry in rev_chat_history:
            if chat_entry["context"] != LLM_CONFIG["NULL"]:
                return chat_entry["context"]
    return LLM_CONFIG["NULL"]


def find_relevant_context(document: str) -> {}:
    products = get_products(as_string=True)
    llm_chain = LLMChain.from_string(
        llm=init_llm(),
        template=init_retrieval_template()
    )
    llm_chain.verbose = LLM_CONFIG["VERBOSE"]
    ctx = json.loads(llm_chain.run({"list": products, "document": document}))
    return ctx


def reduce(document: str) -> str:
    return find_relevant_context(document=document)["context"]


def qna(question: str, chat_history: [{}] = None) -> {str: str}:
    recent_chat_history = []

    if chat_history is not None:
        recent_chat_history = chat_history[LLM_CONFIG["MEMORY_K"] * -1:]

    pre_context = get_pre_context(recent_chat_history)
    context = find_relevant_context(document=question)["context"]

    if context == LLM_CONFIG["NULL"]:
        context = pre_context

    if LLM_CONFIG["VERBOSE"]:
        print(HR)
        print(" >>> Context >>> {}".format(context))
        print(HR)

    if context != LLM_CONFIG["NULL"]:
        docs = semantic_search(
            query=question,
            k=LLM_CONFIG["SEMANTIC_K"],
            collection_name=context,
        )
    else:
        docs = [
            Document(page_content=LLM_CONFIG["NULL"], )
        ]

    chain = init_qa_chain(
        init_prompt_template(
            template=init_qa_template("en"),
            input_vars=init_input_vars(),
            output_format=init_output_format()
        )
    )

    inputs = {
        "role": PROMPTS["ROLE"],
        "company_name": PROMPTS["COMPANY_NAME"],
        "domain": PROMPTS["DOMAIN"],
        "language": PROMPTS["LANGUAGE"],
        "input_documents": docs,
        "question": question,
    }

    response = chain.run(inputs)
    out_response = {
        "context": context,
        "response": response,
    }

    if LLM_CONFIG['VERBOSE']:
        print(HR)
        pprint(out_response)
        print(HR)
    return out_response
