from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from typing import Annotated
import os
import operator
import json
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.document_loaders import WikipediaLoader
from langchain_community.tools import TavilySearchResults
from langchain_openai import ChatOpenAI

load_dotenv()

openai_api = os.getenv("OPENAI_API_KEY")
tavily_api = os.getenv("TAVILY_API_KEY")

llm = ChatOpenAI(
    model='gpt-4o-mini',
    api_key=openai_api
)


class State(TypedDict):
    question: str
    answer: str
    context: Annotated[list, operator.add]


def search_web(state):
    try:
        tavily_search = TavilySearchResults(max_results=3)
        search_docs = tavily_search.invoke(state['question'])
        formatted = [
            f'<Document href="{doc["url"]}">\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
        return {"context": formatted}
    except Exception as e:
        print(f"[ERROR] Web search failed: {e}")
        return {"context": []}


def search_wikipedia(state):
    try:
        search_docs = WikipediaLoader(query=state['question'], load_max_docs=2).load()
        formatted = [
            f'<Document href="Wikipedia">\n{doc.page_content}\n</Document>'
            for doc in search_docs
        ]
        return {"context": formatted}
    except Exception as e:
        print(f"[ERROR] Wikipedia search failed: {e}")
        return {"context": []}


def generate_answer(state):
    # Deduplicate context
    all_contexts = list(set(state['context']))
    merged_context = "\n\n---\n\n".join(all_contexts)

    question = state['question']
    prompt = f"""
You are a helpful assistant. Use the following context to answer the user's question concisely and accurately.
Always cite the source if it is available (URL or "Wikipedia").

Question: {question}

Context:
{merged_context}

Give a clear answer below:
"""

    response = llm.invoke([
        SystemMessage(content=prompt),
        HumanMessage(content="Answer the question.")
    ])

    # Logging
    log = {
        "question": question,
        "context_sources": all_contexts,
        "answer": response.content
    }
    with open("query_log.json", "a", encoding="utf-8") as f:
        json.dump(log, f, indent=2)
        f.write(",\n")
    with open("query_log.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(log) + "\n")


    return {'answer': response}


# Graph building
builder = StateGraph(State)

builder.add_node("search_web", search_web)
builder.add_node("search_wikipedia", search_wikipedia)
builder.add_node("generate_answer", generate_answer)

# Flow
builder.add_edge(START, "search_web")
builder.add_edge(START, "search_wikipedia")
builder.add_edge("search_web", "generate_answer")
builder.add_edge("search_wikipedia", "generate_answer")
builder.add_edge("generate_answer", END)

graph = builder.compile()

if __name__ == "__main__":
    question_input = input("Ask your question: ")
    results = graph.invoke({'question': question_input})
    print("\n--- Answer ---\n")
    print(results['answer'].content)
