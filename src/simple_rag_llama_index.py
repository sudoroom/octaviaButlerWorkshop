from llama_index.core import Document, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama

#import logging
#import sys
#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
#logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

llm = Ollama(model="llama3.1:latest", request_timeout=120.0)

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)
Settings.llm = llm
documents = [
    Document(text="Abraham Lincoln was the 16th president of the United States."),
    Document(text="Abraham Shakespeare was a Florida lottery winner in 2006."),
    Document(text="William Shakespeare married Anne Hathaway."),
]

index = VectorStoreIndex(documents)
query_engine = index.as_query_engine()
response1 = query_engine.query("Who was Shakespeare's wife?")
print(response1)

response2 = query_engine.query("Did William Shakespeare win the lottery?")
print(response2)
