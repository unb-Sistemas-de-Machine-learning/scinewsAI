import os
from enum import Enum
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel

class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"

class Settings(BaseSettings):
    LLM_PROVIDER: LLMProvider = LLMProvider.OPENAI
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
    OPENAI_MODEL: str = "gpt-4o"
    ANTHROPIC_MODEL: str = "claude-3-opus-20240229"
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()

def get_llm() -> BaseChatModel:
    settings = get_settings()
    
    if settings.LLM_PROVIDER == LLMProvider.OPENAI:
        if not settings.OPENAI_API_KEY:
            raise ValueError("A chave OPENAI_API_KEY é necessária para o provedor OpenAI")
        return ChatOpenAI(
            model=settings.OPENAI_MODEL, 
            api_key=settings.OPENAI_API_KEY,
            temperature=0
        )
        
    elif settings.LLM_PROVIDER == LLMProvider.ANTHROPIC:
        if not settings.ANTHROPIC_API_KEY:
            raise ValueError("A chave ANTHROPIC_API_KEY é necessária para o provedor Anthropic")
        return ChatAnthropic(
            model=settings.ANTHROPIC_MODEL, 
            api_key=settings.ANTHROPIC_API_KEY,
            temperature=0
        )
        
    elif settings.LLM_PROVIDER == LLMProvider.OLLAMA:
        return ChatOllama(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL,
            temperature=0
        )
        
    raise ValueError(f"Provedor LLM não suportado: {settings.LLM_PROVIDER}")

def get_embeddings() -> Embeddings:
    settings = get_settings()
    
    if settings.LLM_PROVIDER == LLMProvider.OPENAI:
         if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required for OpenAI embeddings")
         return OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)
         
    elif settings.LLM_PROVIDER == LLMProvider.ANTHROPIC:
        if settings.OPENAI_API_KEY:
             return OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)
        raise ValueError("Provedor Anthropic selecionado, mas nenhuma chave OpenAI para embeddings. Por favor, configure um provedor de embeddings separado ou adicione a chave OpenAI.")

    elif settings.LLM_PROVIDER == LLMProvider.OLLAMA:
        return OllamaEmbeddings(
            base_url=settings.OLLAMA_BASE_URL,
            model="nomic-embed-text" # A good default for embeddings in Ollama
        )
    
    raise ValueError(f"Provedor LLM não suportado para Embeddings: {settings.LLM_PROVIDER}")