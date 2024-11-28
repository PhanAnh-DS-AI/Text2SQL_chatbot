import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv(".env")
MODEL_QUERY_API_KEY = os.getenv("MODEL_QUERY_API_KEY")
MODEL_VALID_API_KEY = os.getenv("MODEL_VALID_API_KEY")
MODEL_ANSWER_API_KEY = os.getenv("MODEL_ANSWER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Models Configuration
model_query = ChatGoogleGenerativeAI(
    api_key=MODEL_QUERY_API_KEY,
    model="gemini-1.5-pro",
    temperature=0,
)

model_valid = ChatGoogleGenerativeAI(
    api_key=MODEL_VALID_API_KEY,
    model="gemini-1.5-flash",
    temperature=0,
)

model_answer = ChatGoogleGenerativeAI(
    api_key=MODEL_ANSWER_API_KEY,
    model="gemini-1.5-pro",
    temperature=0,
)

model_retrival = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.2-3b-preview",
    streaming=True,
)
