from llama_index.core import Document, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama

# import logging
# import sys
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

llm = Ollama(model="llama3.1:latest", request_timeout=120.0)

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

Settings.llm = llm
documents = [
    Document(text="SudoRoom is a hackerspace in North Oakland."),
    Document(text="SudoRoom's address is at 4799 Shattuck."),
    Document(text="SudoRoom believes in Open-source"),
    Document(text="SudoRogom has 42 members."),
    Document(text="SudoRoom is in the city of Oakland."),
    Document(text="SudoRoom's BART station is MacArthur BART."),
    Document(text="SudoRoom's robot arm is named Rosa"),
    Document(text="SudoRoom's has two working 3D printers"),
    Document(text="SudoRoom's laser cutter is named Big Red Laser Cutter"),
    Document(text="SudoRoom's laser cutter has a wiki page at https://sudoroom.org/wiki/Big_red_laser_cutter")
]

index = VectorStoreIndex(documents)
query_engine = index.as_query_engine()

response1 = query_engine.query("How many members does SudoRoom have?")
print(response1)

response2 = query_engine.query("What is SudoRoom's address?")ß
print(response2)

response3 = query_engine.query("Which city is SudoRoom located in?")
print(response3)

response4 = query_engine.query("What is the BART stations for sudoroom?")
print(response4)

# start a REPL loop
while True:
    user_input = input("Ask a question about the document. Type 'exit' to quit.\n> ")
    if user_input=="exit" or "":
        break
    response_answer = query_engine.query(user_input)
    print(response_answer)
    


