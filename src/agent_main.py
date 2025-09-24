import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, AgentExecutor


from db_tools import HeartDiseaseDBTool, CancerDBTool, DiabetesDBTool
from web_search_tool import search_web
from utils import decide_tool_for_question

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise RuntimeError(
        "GITHUB_TOKEN not found in environment. "
        "Please create a .env file with GITHUB_TOKEN=your_pat_here"
    )

# --- GitHub Models Setup ---
MODEL_NAME = "openai/gpt-4.1-mini"  # You can switch to gpt-4o-mini etc.
llm = ChatOpenAI(
    model_name=MODEL_NAME,
    openai_api_key=GITHUB_TOKEN,
    openai_api_base="https://models.github.ai/inference",
    temperature=0.5,
)

# --- Initialize DB tools ---
heart = HeartDiseaseDBTool()
cancer = CancerDBTool()
diabetes = DiabetesDBTool()




def make_tools():
    """Return all tools as callable functions."""
    def heart_query_fn(sql: str) -> str:
        return heart.run_sql(sql)

    def cancer_query_fn(sql: str) -> str:
        return cancer.run_sql(sql)

    def diabetes_query_fn(sql: str) -> str:
        return diabetes.run_sql(sql)

    def web_search_fn(query: str) -> str:
        return search_web(query)

    return [heart_query_fn, cancer_query_fn, diabetes_query_fn, web_search_fn]


def interactive_loop():
    tools = make_tools()
    print("\n=== Multi-Tool Medical Agent (GitHub Models) ===")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("Question: ").strip()
        if not question:
            continue
        if question.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        route = decide_tool_for_question(question)

        if route == "db":
            # Generate SQLite-compatible SQL using LLM with default table context
            prompt = (
                "You are an assistant that converts user questions into a single SQL query.\n"
                f"User question: {question}\n"
                "Rules:\n"
                "1. This must be a valid SQLite query.\n"
                "2. If the user mentions 'heart' or 'cardiac', use the 'heart' table by default.\n"
                "3. If the user mentions 'cancer', 'tumor', or 'tumour', use the 'cancer' table by default.\n"
                "4. If the user mentions 'diabetes' or 'glucose', use the 'diabetes' table by default.\n"
                "5. Respond ONLY with SQL on one line, no explanation.\n"
                "6. Assume the default table mentioned above if the database is not explicitly specified."
            )
            try:
                sql = llm.invoke(prompt).content.strip()
            except Exception as e:
                print("LLM Error:", e)
                continue


            # Determine which DB to use
            q_lower = question.lower()
            if "heart" in q_lower or "cardiac" in q_lower:
                result = tools[0](sql)
            elif "cancer" in q_lower or "tumor" in q_lower or "tumour" in q_lower:
                result = tools[1](sql)
            elif "diabetes" in q_lower or "glucose" in q_lower:
                result = tools[2](sql)
            else:
                # Ask user if DB is unclear
                print("Which DB should I use? (heart/cancer/diabetes)")
                db_choice = input("DB: ").strip().lower()
                if db_choice == "heart":
                    result = tools[0](sql)
                elif db_choice == "cancer":
                    result = tools[1](sql)
                else:
                    result = tools[2](sql)

            print("\nResult:\n")
            print(result)

        else:
            # Use web search tool
            try:
                res = tools[3](question)
            except Exception as e:
                res = f"Web search error: {e}"
            print("\nWeb results:\n")
            print(res)


if __name__ == "__main__":
    interactive_loop()


