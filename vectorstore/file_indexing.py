from langchain_community.document_loaders import PyMuPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Milvus
from pymilvus import connections, utility
import os

def load_and_index_uploaded_file(file, collection_name="uploaded_docs"):
    os.makedirs("tmp", exist_ok=True)
    file_path = os.path.join("tmp", file.name)
    with open(file_path, "wb") as f:
        f.write(file.read())

    if file.name.endswith(".pdf"):
        loader = PyMuPDFLoader(file_path)
    elif file.name.endswith(".docx"):
        loader = Docx2txtLoader(file_path)
    else:
        raise ValueError("Unsupported file type")

    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    connections.connect(host="localhost", port="19530")
    if utility.has_collection(collection_name):
        utility.drop_collection(collection_name)

    embeddings = OpenAIEmbeddings()
    db = Milvus.from_documents(
        docs,
        embeddings,
        collection_name=collection_name,
        connection_args={"host": "localhost", "port": "19530"},
    )
    return db.as_retriever()
