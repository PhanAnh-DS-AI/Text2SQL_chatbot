import sys
sys.path.append("D:/Text2SQL/")
from handlers.chat_graph import chatbot_graph
def main():
    chatbot_model = chatbot_graph()
    input_question = input("Enter your question: ")
    print("Please, waiting for response...")
    test = chatbot_model.invoke({"input": input_question})
    print("\n Response: \n\n",test["answer"])
if __name__ == "__main__":
    main()
