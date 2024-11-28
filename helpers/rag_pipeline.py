import sys
sys.path.append("D:/Text2SQL/")
from langchain_core.output_parsers import StrOutputParser
from basic.schema import CustomGraphState
from helpers.prompt_helpers import answer_prompt
from config import model_retrival
from helpers.chroma_helpers import create_huggingface_embedding
from langchain_chroma import Chroma

class RAGPipeline:
    def __init__(self, model_retrival, answer_prompt):
        self.model_retrival = model_retrival
        self.answer_prompt = answer_prompt
    def rag_chain_answer(self, state: CustomGraphState) -> CustomGraphState:
        rag_chain = (
            self.answer_prompt
            | self.model_retrival
            | StrOutputParser())
        
        result = rag_chain.invoke(
            {"input": state["input"], 
             "context": state["context"]})
        
        state["answer"] = result
        return state

# Load Chroma Database
chroma = Chroma(
    persist_directory="./chroma_langchain_db/vector_db",
    collection_name="swiss_faq_vectordb",
    embedding_function=create_huggingface_embedding(model_name="sentence-transformers/all-MiniLM-L12-v1")
)
# Create retriever
retriever = chroma.as_retriever(search_type="mmr", search_kwargs={"k": 4})

rag = RAGPipeline(model_retrival,answer_prompt)

"""# Testing
input_question = "What is the baggage weight limit for international flights?"
state = {
    "input": input_question,
    "chunks": retriever.invoke(input_question)
}
print(state)
try:
    result_state = rag.rag_chain_answer(state)
    print("----------------------")
    print("Answer:", result_state["answer"])
    print("----------------------")
    
except Exception as e:
    print(f"Error: {e}")
"""