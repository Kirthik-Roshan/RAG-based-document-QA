# pip install langgraph langchain-openai

"""
Minimal LangGraph example with 2 collaborating agents.

AGENT 1: ResearchAgent
- Reads the user's question.
- Produces factual notes.

AGENT 2: WriterAgent
- Takes the notes from ResearchAgent.
- Converts them into a final polished answer.

FLOW:
User Question
   ↓
ResearchAgent
   ↓
WriterAgent
   ↓
Final Answer
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

# ---------------------------------------------------
# 1. Define shared state
# ---------------------------------------------------
class AgentState(TypedDict):
    question: str
    research_notes: str
    final_answer: str


# ---------------------------------------------------
# 2. Initialize LLM
# ---------------------------------------------------
llm = ChatOpenAI(model="gpt-4.1-mini")  # or any model you have access to


# ---------------------------------------------------
# 3. Agent 1: Research Agent
# ---------------------------------------------------
def research_agent(state: AgentState) -> AgentState:
    question = state["question"]

    prompt = f"""
    You are a research assistant.
    Gather concise notes for this question:

    {question}
    """

    response = llm.invoke(prompt)

    return {
        "research_notes": response.content
    }


# ---------------------------------------------------
# 4. Agent 2: Writer Agent
# ---------------------------------------------------
def writer_agent(state: AgentState) -> AgentState:
    question = state["question"]
    notes = state["research_notes"]

    prompt = f"""
    You are a technical writer.

    Question:
    {question}

    Research Notes:
    {notes}

    Write a clear final answer.
    """

    response = llm.invoke(prompt)

    return {
        "final_answer": response.content
    }


# ---------------------------------------------------
# 5. Build graph
# ---------------------------------------------------
graph = StateGraph(AgentState)

# Add nodes (agents)
graph.add_node("research_agent", research_agent)
graph.add_node("writer_agent", writer_agent)

# Define execution order
graph.set_entry_point("research_agent")
graph.add_edge("research_agent", "writer_agent")
graph.add_edge("writer_agent", END)

# Compile graph
app = graph.compile()


# ---------------------------------------------------
# 6. Run the graph
# ---------------------------------------------------
result = app.invoke({
    "question": "Explain how neural networks learn."
})

print("\n=== RESEARCH NOTES ===")
print(result["research_notes"])

print("\n=== FINAL ANSWER ===")
print(result["final_answer"])