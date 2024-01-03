from flask import Blueprint, request
from markupsafe import escape
import api.service as service


blueprint = Blueprint("routes", __name__)


@blueprint.route("/")
def home():
    return "<h1>LLM RESTful API</h1>"


@blueprint.route("/api/chat", methods=["POST"])
def post_chat():
    input_args = request.get_json()

    if input_args is None:
        return {"message": "empty payload"}

    text_message = input_args.get("text_message")
    chat_history = input_args.get("chat_history")

    if text_message is None:
        return {"message": "no text_message parameter in the payload"}

    return service.question_and_answer(question=escape(text_message), chat_history=chat_history)


@blueprint.route("/api/chat/<text_message>", methods=['GET'])
def get_chat_path(text_message: str):
    return service.question_and_answer(question=escape(text_message))


@blueprint.route("/api/chat/reduce/<document>", methods=['GET'])
def get_reduce_path(document: str):
    return service.reduce_document(document=escape(document))


@blueprint.route("/api/chat/history/memory_k/", methods=['GET'])
def get_memory_k():
    return service.get_memory_k()
