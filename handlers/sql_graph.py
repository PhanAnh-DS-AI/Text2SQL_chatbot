import sys
sys.path.append("D:/Text2SQL/")
from helpers.text2sql_pipeline import QueryChain, ValidateChain, AnswerChain, CustomGraphState, db, model_query, model_valid, model_answer
from typing import Literal
from langgraph.graph import StateGraph, START, END

def retry_continue(state: CustomGraphState) -> Literal["query_chain", "pass_through"]:
    """
    Determines the next step in the graph based on the state.
    Returns the name of the next node to execute.
    """
    if state["context"] is None and state["counter"] < 2:
        return "query_chain"
    # elif state["is_valid"] and state["context"] is not None:
    #     return "answer_chain"  
    else:
        return "pass_through"

def pass_through(state: CustomGraphState) -> CustomGraphState:
    return state


# Define node graph
query_chain = QueryChain(db=db, model_query=model_query)
validate_chain = ValidateChain(model_valid=model_valid)
answer_chain = AnswerChain(model_answer=model_answer)
                                                     
# Create Graph
"""def build_sql_graph() -> StateGraph:
    builder = StateGraph(CustomGraphState)
    builder.add_node("query_chain", query_chain.process)
    builder.add_node("valid_chain", validate_chain.process)
    builder.add_node("answer_chain", answer_chain.process)
    builder.add_node("list_answer", list_answer)
    builder.add_node("save_result", save_result)

    builder.add_edge(START, "query_chain")
    builder.add_edge("query_chain", "valid_chain")
    builder.add_conditional_edges("valid_chain", retry_continue)
    builder.add_edge("answer_chain", "save_result")
    builder.add_edge("list_answer", "save_result")
    # builder.add_edge("save_result", END)
    return builder
"""
