import os
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from src.config import get_embeddings, get_settings

def load_pdf(file_path: str) -> List[Document]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    
    loader = PyPDFLoader(file_path)
    return loader.load()

def split_documents(documents: List[Document]) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True,
    )
    return text_splitter.split_documents(documents)

def index_documents(documents: List[Document]) -> Chroma:
    settings = get_settings()
    embeddings = get_embeddings()

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=settings.CHROMA_PERSIST_DIRECTORY
    )
    return vector_store

def ingest_paper(file_path: str) -> str:
    print(f"Carregando {file_path}...")
    docs = load_pdf(file_path)
    print(f"Carregado {len(docs)} páginas.")
    
    chunks = split_documents(docs)
    print(f"Dividido em {len(chunks)} chunks.")
    
    print("Indexando no ChromaDB...")
    index_documents(chunks)
    
    return f"Inserido com sucesso {file_path} com {len(chunks)} chunks."
