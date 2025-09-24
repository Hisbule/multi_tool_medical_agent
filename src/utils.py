import os
from typing import Literal
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# --- Load GitHub token ---
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise RuntimeError(
        "GITHUB_TOKEN not found in environment. "
        "Please create a .env file with GITHUB_TOKEN=your_pat_here"
    )

# --- Init model from GitHub ---
MODEL_NAME = "openai/gpt-4.1-mini"
llm = ChatOpenAI(
    model=MODEL_NAME,
    openai_api_key=GITHUB_TOKEN,
    openai_api_base="https://models.github.ai/inference",
    temperature=0.0,   # keep deterministic for routing
)

# --- Routing prompt ---
prompt = PromptTemplate.from_template("""
You are a router. Classify the user question into one of two tools:
- "db" → if it requires statistical / numerical / dataset-based answers
- "web" → if it is about medical, general knowledge, or requires searching

Question: {question}
Answer with only "db" or "web".
""")

# --- Decide tool ---
def decide_tool_for_question(question: str) -> Literal["db", "web"]:
    response = llm.invoke(prompt.format(question=question))
    return response.content.strip().lower()
