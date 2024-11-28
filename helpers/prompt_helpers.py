from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate

##############################
     #~~~SQL Prompt~~~#
##############################

prompt_sql_query = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate(
                prompt= PromptTemplate.from_file("D:/Text2SQL/prompts/sql_query_system_message.txt")),    
            HumanMessagePromptTemplate(
                prompt = PromptTemplate.from_file("D:/Text2SQL/prompts/sql_query_human_message.txt"))
            ])


##############################
    #~~~Validate Prompt~~~#
##############################

promt_validate = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate(
        prompt= PromptTemplate.from_file("D:/Text2SQL/prompts/sql_valid_system_message.txt")),    

    HumanMessagePromptTemplate(
        prompt= PromptTemplate.from_file("D:/Text2SQL/prompts/sql_valid_human_message.txt")),
])


##############################
    #~~~Answer Prompt~~~#
##############################

answer_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate(
                prompt= PromptTemplate.from_file("D:/Text2SQL/prompts/answer_system_message.txt")),
            HumanMessagePromptTemplate(
                prompt= PromptTemplate.from_file("D:/Text2SQL/prompts/answer_human_message.txt"))
                            ])

##############################
     #~~~RAG Prompt~~~#
##############################

router_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate(
        prompt= PromptTemplate.from_file("D:/Text2SQL/prompts/router_system_message.txt")), 
    HumanMessagePromptTemplate(
        prompt = PromptTemplate.from_file("D:/Text2SQL/prompts/router_human_message.txt"))
                    ])


#### Example good prompt
"""You are a brilliant AI Assistant, an expert in answering questions with depth and precision.
Your responses should provide lots of specific details and must be crafted ONLY from the information you have been given. 
Here is what you have to work with:

1. Chat History: The last 5 messages from this conversation, helping you grasp the ongoing topic.
2. User Question: The raw question asked by the user, waiting for your insightful answer.
3. Document Context: Relevant documents retrieved from our Vector Database,
include metadata information (document_id, document_name, page)

Your mission is to provide detailed, informative answers in complete sentences, using only the Chat History and Document Context.

If the answer isn't in the information provided, gracefully respond example as:
"Sorry, I have no information about your question, so I cannot answer."

Guidelines for Excellence:
- Craft comprehensive and informative answers, weaving in as much relevant detail as possible.
- Maintain a respectful and professional tone throughout the conversation without explicitly referencing the provided context metadata information.
- ONLY use information from the "Chat History" and "Document Context" to respond. DO NOT use your general knowledge base.
- Steer clear of phrases like "Based on the context..." or "The context information...".
- Your response should be in MARKDOWN format if possible.

Go forth and provide answers that enlighten, coherent, inform, human-like, engage, and richly detailed answers!"""