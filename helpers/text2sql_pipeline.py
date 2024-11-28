import sys
sys.path.append("D:/Text2SQL/")
from config import model_query, model_valid, model_answer
from helpers.prompt_helpers import prompt_sql_query, promt_validate, answer_prompt
from basic.schema import CustomGraphState, InputQueryChain, ValidateOutput
from sqlite3 import OperationalError
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.runnables import RunnableLambda

# Get the database
db_path = r"./Data/travel2.sqlite"
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
execute_query = QuerySQLDataBaseTool(db=db)
    
class GraphSQL:
    def process(self, state: CustomGraphState) -> CustomGraphState:
        raise NotImplementedError("Subclasses must implement the `process` method.")
    
######################
   #--Query Chain--#
######################

class QueryChain(GraphSQL):
    def __init__(self, db, model_query):
        self.db = db
        self.model_query = model_query
        self.pydantic_query = PydanticOutputParser(pydantic_object=InputQueryChain)
        self.prompt_sql_query = prompt_sql_query
        
    def process(self, state: CustomGraphState) -> CustomGraphState:
        """Processes the state to generate a SQL query."""
        if "counter" in state:
            print("Retry attempt:", state["counter"] + 1)
        table_info = self.db.get_table_info()
        input_info_runnable = RunnableLambda(lambda input_data: {
            "table_info": table_info,
            "input": input_data["input"]  
        })
        
        query_chain = (input_info_runnable 
                    | self.prompt_sql_query 
                    | self.model_query
                    | self.pydantic_query  
                    | RunnableLambda(lambda output: {**output.dict()})
                    ) 
        
        result = query_chain.invoke({"input": state["input"]})
        state["sql_query"] = result["sql_query"]
        return state

######################
 #--Validate Chain--#
######################

class ValidateChain(GraphSQL):
    def __init__(self, model_valid):
        self.model_valid = model_valid
        self.pydantic_parser = PydanticOutputParser(pydantic_object=ValidateOutput)
        self.prompt_validate = promt_validate
    
    def validate_and_execute_query(self, state: CustomGraphState) -> CustomGraphState:
        try:
            if not state["is_valid"]:
                state["context"] = None
            else:
                query_result = execute_query.invoke(state["sql_query"])  
                if not query_result or len(query_result) == 0:
                    state["context"] = None
                    state["is_valid"] = False
                else:
                    state["context"] = query_result
            return state

        except (OperationalError, Exception) as e:
            state["context"] = None
            state["is_valid"] = False
            print(e)
            return state

    def process(self, state: CustomGraphState) -> CustomGraphState:
        """Processes the state to valide the SQL query."""
        validate_chain = (
            self.prompt_validate
            | self.model_valid
            | self.pydantic_parser
            | RunnableLambda(lambda output: self.validate_and_execute_query({**output.model_dump()}))
        )
        
        valid_result = validate_chain.invoke({
            "input": state["input"],
            "sql_query": state["sql_query"]
        })
        state["is_valid"] = valid_result["is_valid"]
        state["context"] = valid_result["context"]
        
        if "counter" not in state:
            state["counter"] = 0
        else:
            state["counter"] += 1
            
        return state
    
######################
  #--Answer Chain--#
######################

class AnswerChain(GraphSQL):
    def __init__(self, model_answer):
        self.model_answer = model_answer
        self.answer_prompt = answer_prompt

    def process(self, state: CustomGraphState) -> CustomGraphState:
        """Processes the state to answer user from the sql result"""
        answer_chain = (
            self.answer_prompt
            | self.model_answer
            | StrOutputParser()
        )
        answer_result = answer_chain.invoke({
            "input": state["input"],
            "context": state["context"]
        })
        state["answer"] = answer_result
        return state
    
######################
   #--Pipe Line--#
######################

query_chain = QueryChain(db=db, model_query=model_query)
validate_chain = ValidateChain(model_valid=model_valid)
answer_chain = AnswerChain(model_answer=model_answer)

class GraphSQLPipeline(GraphSQL):
    def __init__(self, query_chain, validate_chain, answer_chain):
        self.query_chain = query_chain
        self.validate_chain = validate_chain
        self.answer_Chain = answer_chain

    def process(self, state: CustomGraphState) -> CustomGraphState:
        state = self.query_chain.process(state)
        state = self.validate_chain.process(state)
        state = self.answer_Chain.process(state)
        return state

