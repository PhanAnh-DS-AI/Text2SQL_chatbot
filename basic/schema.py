from typing import TypedDict, Optional, Literal
from pydantic import BaseModel, Field

#######################
# Define Parent Graph #
#######################

class CustomGraphState(TypedDict):
    input: str  
    route: Literal["subgraph_sql", "subgraph_rag"] 
    answer: Optional[str]

    # Define Parent Graph
    context: Optional[str]
    sql_query: Optional[str | list[str]]
    is_valid: Optional[bool]
    counter: int

# Query chain
class InputQueryChain(BaseModel): 
    sql_query: str = Field(description = "Generate SQL Query from user question")
    
# Validate chain
class ValidateOutput(BaseModel): 
    sql_query: Optional[str] = Field(description="Final SQL query")
    is_valid: bool = Field(description="Indicates whether the query is valid or not")
    
    
## Define Child Graph
### Define Subgraph SQL
"""class SubgraphSQL(TypedDict):
    input: str
    sql_query: Optional[str]
    is_valid: Optional[bool]
    result: Optional[str]
    answer: Optional[str]
    counter: int

### Define Subgraph RAG 
class SubgraphRAG(TypedDict):
    input: str  
    answer: Optional[str]
    chunks: str
"""


