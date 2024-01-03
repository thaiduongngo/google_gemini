LLM_CONFIG = {
    "TEXT_MODEL": "gemini-pro",
    "EMBEDDINGS_MODEL": "models/embedding-001",
    "TEMPERATURE": 0,
    "SEMANTIC_K": 30,
    "MEMORY_K": 10,
    "VERBOSE": True,
    "ONLY_OUTPUT": True,
    "NULL": "None",
}


PROMPTS = {
    "ROLE": "Agent",
    "DOMAIN": "Insurance",
    "COMPANY_NAME": "Công ty TNHH một thành viên Prudential Việt Nam",
    "LANGUAGE": "Vietnamese",
    "OUT_FORMAT": "markdown and bold headlines",
}


PERSISTENCE = {
    "PRODUCTS": "PVA-PRODUCTS",
    "ANSWERS": "PVA-ANSWERS",
    "CONNECTION_STRING": "postgresql+psycopg://postgres:postgres@localhost:5432/postgres",
}


SAFETY_SETTINGS = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
]
