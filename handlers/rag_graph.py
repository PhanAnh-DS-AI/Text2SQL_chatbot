import sys
sys.path.append("D:/Text2SQL/")
from basic.schema import CustomGraphState
from langgraph.graph import StateGraph, START, END
from helpers.rag_pipeline import rag, retriever
from typing import Literal
import random

def retrival_nodes(state: CustomGraphState) -> CustomGraphState:
    user_input = state["input"]
    if not user_input or len(user_input) == 0:
        raise ValueError("Input is missing in state.")
    
    # Query Chroma retriever
    results = retriever.invoke(user_input)
    chunks = [res.page_content for res in results]
    state["context"] = chunks
    return state

# Check condition
def decision_node(state: CustomGraphState) -> Literal["list_answer", "answer_chain"]:
    if state["context"] is None or len(state["context"]) == 0:
        return "list_answer"
    return "answer_chain"

def list_answer(state: CustomGraphState) -> CustomGraphState:
    response = [
        "Apologies, but we couldn't find an answer to your question.",
        "We're sorry, but there isn't any information available for your request.",
        "Unfortunately, we don't have the answer you're looking for at the moment.",
        "Sorry, we couldn't locate relevant information for your question.",
        "Regrettably, we do not have a suitable response to your inquiry.",
    ]
    random_response = random.choice(response)   
    state["answer"] = random_response
    return state



"""def build_rag_graph() -> StateGraph:
    subgraph_builder = StateGraph(CustomGraphState)
    # Add nodes
    subgraph_builder.add_node("retrival_nodes", retrival_nodes)
    subgraph_builder.add_node("list_answer", list_answer)
    subgraph_builder.add_node("answer_chain", rag.rag_chain_answer)
    subgraph_builder.add_node("save_result", save_result)
    
    # Add edges
    subgraph_builder.add_edge(START, "retrival_nodes")
    subgraph_builder.add_conditional_edges("retrival_nodes", decision_node)
    subgraph_builder.add_edge("answer_chain", "save_result")
    subgraph_builder.add_edge("list_answer", "save_result")
    # subgraph_builder.add_edge("save_result", END)
    
    return subgraph_builder"""

"""testing = build_rag_graph()
question = {"input": "What items must be declared at customs upon arrival?"}
print(testing.invoke(question))"""

