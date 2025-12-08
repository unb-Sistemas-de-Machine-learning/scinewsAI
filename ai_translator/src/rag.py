from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough

from src.config import get_llm, get_embeddings, get_settings

def get_vectorstore() -> Chroma:
    settings = get_settings()
    embeddings = get_embeddings()
    return Chroma(
        persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
        embedding_function=embeddings
    )

def get_retriever():
    vectorstore = get_vectorstore()
    return vectorstore.as_retriever(search_kwargs={"k": 5})

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain():
    llm = get_llm()
    retriever = get_retriever()
    
    template = """You are an expert science communicator and translator. 
Your goal is to explain complex scientific concepts from the provided research paper context in a clear, accessible, and friendly way to a general audience, while maintaining accuracy.

Use the following pieces of retrieved context to answer the user's question or summarize the paper.
If you don't know the answer based on the context, just say that you don't know.

Context:
{context}

Question:
{question}

Answer (in accessible, friendly, yet accurate language):"""

    prompt = ChatPromptTemplate.from_template(template)
    
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

def query_rag(question: str) -> str:
    rag_chain = get_rag_chain()
    return rag_chain.invoke(question)
