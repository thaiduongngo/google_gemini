from pprint import pprint
from langchain.vectorstores.pgvector import PGVector
from langchain.chains import LLMChain
from langchain.schema import Document
from genai_llms import init_embeddings, init_retrieval_template, init_llm, init_qa_chain, init_prompt_template, \
    init_qa_template, init_input_vars, init_output_format
from genai_llms.configs import LLM_CONFIG, PROMPTS, PERSISTENCE
import json


HR = "-" * 140


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
            products_str = "{}* {}\n".format(products_str, doc.page_content)
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
            if chat_entry["context"] != "None":
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
