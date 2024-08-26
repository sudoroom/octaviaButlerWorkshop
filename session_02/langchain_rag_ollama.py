import argparse
import os
import shutil 

from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import DirectoryLoader, Docx2txtLoader
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
# https://api.python.langchain.com/en/latest/embeddings/langchain_huggingface.embeddings.huggingface.HuggingFaceEmbeddings.html
# new- HuggingFace sentence_transformers embedding models.
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS

from langchain_ollama import ChatOllama

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DOCS_DIR = os.path.join(SCRIPT_DIR, "pdfs")
DEFAULT_INDEX_DIR = os.path.join(SCRIPT_DIR, "pdfs_index")
EMBED_MODEL = "BAAI/bge-small-en-v1.5"
DOCUMENT_PDF = "BigRedLaser.pdf"
# workaround for hugging face fast tokenzier
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs_dir", type=str, default=DEFAULT_DOCS_DIR)
    parser.add_argument("--persist_dir", type=str, default=DOCUMENT_PDF)
    args = parser.parse_args()

    print(f"Using data dir {args.docs_dir}")
    print(f"Using index path {args.persist_dir}")
  
    # model_name = "mixedbread-ai/mxbai-embed-large-v1"
    model_name = "RUCAIBox/mtl-data-to-text"
    embedding = HuggingFaceEmbeddings(
        model_name=model_name
    )
    
    print(f"Using Embedding: {embedding.model_name}")

    # there's a security issue with de-serialization so i'll just
    # delete the previous directory
    if os.path.exists(args.persist_dir):
        # print(f"Loading FAISS index from {args.persist_dir}")
        # vectorstore = FAISS.load_local(args.persist_dir, embedding)
        # print("done")
        print(f"Deleting the existing index at {args.persist_dir}")
        shutil.rmtree(args.persist_dir)

    print(f"Building FAISS index from documents in {args.docs_dir}")
    # print out files for debuggin
    for file in os.listdir(args.docs_dir):
        if os.path.isfile(os.path.join(args.docs_dir, file)):
            print(f"- {file}")

    ## could preprocess but we're not
    loader = DirectoryLoader(args.docs_dir, 
                                loader_cls = PyPDFLoader,
                                recursive=True,
                                silent_errors=True,
                                show_progress=True,
                                glob="**/*.pdf")

    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=75
    )

    frags=text_splitter.split_documents(docs)

    print(f"Populating vector store with {len(docs)} docs in {len(frags)} framgents")
    vectorstore = FAISS.from_documents(frags, embedding)
    print(f"Persisting vector store to: {args.persist_dir}")
    vectorstore.save_local(args.persist_dir)
    print(f"Saved FAISS index to {args.persist_dir}")

    llm = ChatOllama(model="llama3.1:latest",
                     temperature=0.9)
    # uses explicit memory for the overall chat using the conversational buffer memory class - each item is stored in memory and tagged with an identifier where it appends accumulated messages
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    memory.load_memory_variables({})
    # this class is deprecated
    # https://medium.com/@ypredofficial/rag-updated-q-a-and-converstaional-99b6af6ddd8b
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        memory=memory,
        retriever=vectorstore.as_retriever()
    )

    # start a REPL loop
    while True:
        user_input = input("Ask a question about the document. Type 'exit' to quit.\n> ")
        if user_input=="exit":
            break
        memory.chat_memory.add_user_message(user_input)
        result = qa_chain({"question": user_input})
        response = result["answer"]
        memory.chat_memory.add_ai_message(response)
        print("AI:", response)

if __name__ == "__main__":
    main()