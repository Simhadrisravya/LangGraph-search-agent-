from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.tools import TavilySearchResults

from typing import TypedDict, List
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.graph import StateGraph, END
from langchain_community.tools.tavily_search import TavilySearchResults

from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    google_api_key=GOOGLE_API_KEY
)

# -----------------------
# Tavily tool
# -----------------------
search = TavilySearchResults(tavily_api_key=TAVILY_API_KEY)

# -----------------------
# STATE (MUST BE FIRST)
# -----------------------
class AgentState(TypedDict):
    messages: List[BaseMessage]


# -----------------------
# Planner
# -----------------------
def planner_node(state: AgentState):
    user_input = state["messages"][-1].content

    prompt = "Return ONLY a search query if needed."

    response = llm.invoke([
        HumanMessage(content=prompt),
        HumanMessage(content=user_input)
    ])

    state["messages"].append(AIMessage(content=response.content))
    return state


# -----------------------
# Search
# -----------------------
def search_node(state):
    raw = state["messages"][-1].content

    # ✅ FORCE normalize to string
    if isinstance(raw, list):
        query = " ".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in raw
        )
    elif isinstance(raw, dict):
        query = raw.get("text") or raw.get("content") or str(raw)
    else:
        query = str(raw)

    # ✅ NOW safe for Tavily
    result = search.invoke(query)

    state["messages"].append(AIMessage(content=str(result)))
    return state


# -----------------------
# Responder
# -----------------------
def responder_node(state: AgentState):
    user_question = state["messages"][0].content
    search_results = state["messages"][1].content

    response = llm.invoke([
        HumanMessage(content="Use search results to answer."),
        HumanMessage(content=f"Q: {user_question}\nResults: {search_results}")
    ])

    state["messages"].append(AIMessage(content=response.content))
    return state


# -----------------------
# GRAPH
# -----------------------
graph = StateGraph(AgentState)

graph.add_node("Planner", planner_node)
graph.add_node("Search", search_node)
graph.add_node("Responder", responder_node)

graph.set_entry_point("Planner")

graph.add_edge("Planner", "Search")
graph.add_edge("Search", "Responder")
graph.add_edge("Responder", END)

agent = graph.compile()


# -----------------------
# RUN
# -----------------------
result = agent.invoke({
    "messages": [
        HumanMessage(content="Who is the current President of India?")
    ]
})

print(result)
