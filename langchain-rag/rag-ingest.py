from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader , TextLoader
from langchain_chroma import Chroma
import shutil

DATA_DIR=Path("/Users/khushijain/Desktop/iitr /agentic_systems_assignments/langchain-rag/documents")
CHROMA_DIR=Path("/Users/khushijain/Desktop/iitr /agentic_systems_assignments/langchain-rag/chroma-db")
COLLECTION_NAME="hostel_policy_docs"
EMBEDDING_MODEL="gemini-embedding-001"

loader=DirectoryLoader(
    path=str(DATA_DIR),
    glob="**/*md",
    loader_cls=TextLoader,
    loader_kwargs= {"encoding":"utf-8"}
)
docs = loader.load()

text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=60,
    add_start_index=True,
)

chunks = text_splitter.split_documents(docs)

if CHROMA_DIR.exists():
    shutil.rmtree(CHROMA_DIR)

embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)

vector_store= Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=str(CHROMA_DIR)
)

ids = vector_store.add_documents(documents=chunks)