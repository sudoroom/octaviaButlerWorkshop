# from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser


## this is a basic example that comes from the documentation for Langchain- Ollama
### https://python.langchain.com/v0.2/docs/integrations/llms/ollama/ the open-source AI a question and have it explain step by step\n")

user_input = input("Give a topic that the AI will explain to you in steps\n")
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

print(result)

