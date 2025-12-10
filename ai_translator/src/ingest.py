import os
import time
from typing import List, Dict

from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from src.config import get_embeddings, get_settings


def load_pdf(file_path: str) -> List[Document]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo nao encontrado: {file_path}")

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


def ingest_paper(file_path: str) -> Dict[str, float]:
    """
    Loads a PDF, splits into chunks, and indexes them in Chroma.
    Returns ingestion metadata for observability/MLflow logging.
    """
    print(f"Carregando {file_path}...")
    start = time.time()
    docs = load_pdf(file_path)
    print(f"Carregado {len(docs)} paginas.")

    split_start = time.time()
    chunks = split_documents(docs)
    print(f"Dividido em {len(chunks)} chunks.")
    split_time = time.time() - split_start

    print("Indexando no ChromaDB...")
    index_documents(chunks)

    total_time = time.time() - start

    return {
        "file_path": file_path,
        "pages": len(docs),
        "chunks": len(chunks),
        "ingest_time_s": total_time,
        "split_time_s": split_time,
    }
