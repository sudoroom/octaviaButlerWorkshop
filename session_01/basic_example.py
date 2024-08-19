from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

## this is a basic example that comes from the documentation for Langchain- Ollama
### https://python.langchain.com/v0.2/docs/integrations/llms/ollama/
template = """Question: {question}
Answer: Let's think step by step.
"""
prompt = ChatPromptTemplate.from_template(template)

llm = OllamaLLM(model="llama3.1:latest")
print(prompt.output_schema)

chain = prompt | llm

result = chain.invoke({"question": "What is Afro-futurism?"})

print(llm.input_schema)

print(result)

