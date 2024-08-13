import os
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import ChatPromptTemplate

from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
import html 

def generate_response(user_input):
    application_prompt = """Given the following topic and then explain what it is step by step
    {user_input}
    """

    prompt = PromptTemplate(input_variables=["user_input"], 
                            template=application_prompt)

    llm = OllamaLLM(model="llama3.1:latest", 
                    temperature=1, 
                    max_tokens=1000)

    chain = prompt | llm | StrOutputParser()

    result = chain.invoke({"user_input": {user_input}})
    html_result = html.escape(result).replace('\n', '<br>')
    return f"<p>{html_result}</p>"
    # llm = OllamaLLM(model="llama3.1:latest")
    # prompt = ChatPromptTemplate.from_messages([
    #     SystemMessage(content="You are an explainer, very kind and knowledgable.Given the following topic and then explain what it is step by step"),
    #     HumanMessage(content=user_input)
    # ])

    # response = llm(prompt.format_messages)
    # response_message = response.content.strip().lower()
    # return response_message