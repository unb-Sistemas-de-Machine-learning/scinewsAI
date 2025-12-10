from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from src.config import get_llm, get_embeddings, get_settings

def get_vectorstore():
    from langchain_chroma import Chroma
    settings = get_settings()
    embeddings = get_embeddings()
    return Chroma(
        persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
        embedding_function=embeddings
    )

def get_retriever():
    vectorstore = get_vectorstore()
    return vectorstore.as_retriever(search_kwargs={"k": 7})

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

FINAL_PROMPT_TEMPLATE = """You are an expert science communicator and translator. Your goal is to explain complex scientific concepts
from the provided research paper in a clear, accessible, and friendly way to a general audience, while maintaining accuracy.

Analyse the provided text and generate a comprehensive summary structured into the following sections. Ensure each section is detailed yet easy to understand.

Structure your response as follows:

# Title & Overview
Give a catchy title and a brief high-level overview of what the paper is about.

## 1. Introduction & Problem Statement
- What is the context?
- What problem are the researchers trying to solve?
- Why is this important?

## 2. Methodology & Approach
- How did they approach the problem?
- What methods or experiments did they use? (Explain simply)

## 3. Key Results & Findings
- What did they find?
- Provide specific interesting data points or discoveries.

## 4. Conclusion & Implications
- What do these results mean?
- How does this impact the field or the real world?

Text to process:
{context}

Answer (in accessible, friendly, yet accurate markdown):"""

def query_rag(query: str = "Provide a comprehensive summary of this research paper") -> str:
    result = query_rag_with_context(query=query)
    return result["answer"]

def translate_text(text: str) -> str:
    """
    Translates/Simplifies the given text using the LLM directly, bypassing retrieval.
    """
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(FINAL_PROMPT_TEMPLATE)
    
    chain = (
        {"context": lambda x: x}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain.invoke(text)


def query_rag_with_context(query: str = "Provide a comprehensive summary of this research paper"):
    """
    Returns both the generated answer and the raw contexts used for retrieval.
    """
    llm = get_llm()
    retriever = get_retriever()

    prompt = ChatPromptTemplate.from_template(FINAL_PROMPT_TEMPLATE)

    # Pull contexts explicitly to log later
    docs = retriever.invoke(query)
    contexts = [doc.page_content for doc in docs]

    rag_chain = (
        {"context": lambda _: "\n\n".join(contexts), "query": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    answer = rag_chain.invoke(query)
    return {"answer": answer, "contexts": contexts}
