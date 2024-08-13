import os
from langchain.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage

def generate_response(user_input):
    llm = OllamaLLM(model="llama3.1:latest", 
                    temperature=1, 
                    max_tokens=1000)
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="You are an explainer, very kind and knowledgable.Given the following topic and then explain what it is step by step"),
        HumanMessage(content=user_input)
    ])

    response = llm(prompt.format_messages)
    response_message = response.content.strip().lower()
    return response_message