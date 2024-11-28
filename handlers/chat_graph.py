import sys
sys.path.append("D:/Text2SQL/")
from basic.schema import CustomGraphState
from langgraph.graph import StateGraph, START, END
from helpers.text2sql_pipeline import query_chain, validate_chain, answer_chain
from config import model_retrival
from helpers.prompt_helpers import router_prompt
from handlers.sql_graph import pass_through, retry_continue
from handlers.rag_graph import retrival_nodes, decision_node, list_answer
from typing import Literal

# Router model
router_model = model_retrival.with_structured_output(CustomGraphState)

def router_node(state: CustomGraphState) -> CustomGraphState:
    messages_prompt = router_prompt
    prompt_value = messages_prompt.format(input=state["input"])
    attempt = 0
    max_attempts = 2
    while attempt < max_attempts:
        try:
            result = router_model.invoke(prompt_value)
            if result and "route" in result:
                state["route"] = result["route"]
                return state
            else:
                raise ValueError("Invalid response from model.")
        except Exception as e:
            print(f"Attempt {attempt + 1}: Error - {e}")
            attempt += 1

    state["route"] = "subgraph_sql"
    return state


def decission_router(state: CustomGraphState) -> Literal["subgraph_sql", "subgraph_rag"]:
    if state["route"] == "subgraph_sql":
        return "subgraph_sql"
    else:
        return "subgraph_rag"


# SubGraph SQL
def sql_subgraph() -> StateGraph:
    sql_builder = StateGraph(CustomGraphState)
    # Add node
    sql_builder.add_node("query_chain", query_chain.process)
    sql_builder.add_node("valid_chain", validate_chain.process)
    sql_builder.add_node("pass_through", pass_through)
    # Add edge
    sql_builder.add_edge(START, "query_chain")
    sql_builder.add_edge("query_chain", "valid_chain")
    sql_builder.add_conditional_edges("valid_chain", retry_continue)   
    return sql_builder.compile()

# SubGraph RAG
def rag_subgraph() -> StateGraph:
    rag_builder = StateGraph(CustomGraphState)
    rag_builder.add_node("retrival_nodes", retrival_nodes)
    rag_builder.add_edge(START, "retrival_nodes")
    return rag_builder.compile()

# call subgraph
sql = sql_subgraph()
rag = rag_subgraph()

def call_subgraph_sql(state: CustomGraphState) -> CustomGraphState:
    state = sql.invoke({"input": state["input"]})
    return state

def call_subgraph_rag(state: CustomGraphState) -> CustomGraphState:
    state = rag.invoke({"input": state["input"]})
    return state


# Graph Chatbot
def chatbot_graph():
    parent_graph = StateGraph(CustomGraphState)
    # Add nodes
    parent_graph.add_node("router_node", router_node)
    parent_graph.add_node("subgraph_sql", call_subgraph_sql)
    parent_graph.add_node("subgraph_rag", call_subgraph_rag)
    parent_graph.add_node("pass_through", pass_through)
    parent_graph.add_node("list_answer", list_answer)
    parent_graph.add_node("answer_chain", answer_chain.process)
    # Add edges
    parent_graph.add_edge(START, "router_node")
    parent_graph.add_conditional_edges("router_node", decission_router)
    parent_graph.add_edge("subgraph_sql", "pass_through")
    parent_graph.add_edge("subgraph_rag", "pass_through")
    parent_graph.add_conditional_edges("pass_through", decision_node)
    parent_graph.add_edge("list_answer", END)
    parent_graph.add_edge("answer_chain", END)
    # Compile graph
    return parent_graph.compile()

