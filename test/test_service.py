from api.service import question_and_answer


CHAT_HISTORY = [
    {
        "input": "Quyền lợi của Pru vững chắc",
        "context": "Sản phẩm bảo hiểm liên kết chung PRU VỮNG CHẮC",
        "output": "",
    },
    {
        "input": "Quyền lợi của Pru đầu tư linh hoạt",
        "context": "Sản phẩm bảo hiểm liên kết đơn vị PRU ĐẦU TƯ LINH HOẠT",
        "output": ""
    },
    {
        "input": "PVA",
        "context": "None",
        "output": ""
    },
    {
        "input": "Các điều khoản loại trừ",
        "context": "None",
        "output": ""
    },
    {
        "input": "Quyền lợi",
        "context": "None",
        "output": ""
    },
]

res = question_and_answer(
    question="Quyền lợi của Pru cuộc sống bình an",
    chat_history=CHAT_HISTORY
)
