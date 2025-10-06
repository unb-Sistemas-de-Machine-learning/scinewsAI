import os
from dotenv import load_dotenv
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Text,
    Date,
    ARRAY,
    TIMESTAMP,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Engine de conexão com o banco de dados
engine = create_engine(DATABASE_URL)

# Base declarativa para nossos modelos
Base = declarative_base()


# --- Definição do Modelo da Tabela 'articles' ---
class Article(Base):
    __tablename__ = 'articles'

    # O ID do arXiv (ex: '2305.12345') é uma string e nossa chave primária.
    id = Column(String, primary_key=True, index=True)
    
    title = Column(Text, nullable=False)
    
    # ARRAY(Text) é o tipo para listas de strings no PostgreSQL
    authors = Column(ARRAY(Text))
    
    publication_date = Column(Date)
    
    abstract = Column(Text)
    
    keywords = Column(ARRAY(Text))
    
    full_text = Column(Text)
    
    source_url = Column(Text)
    
    original_pdf_path = Column(Text)
    
    processing_status = Column(String(50), default='downloaded')
    
    simplified_text = Column(Text, nullable=True)

    # Define um valor padrão no lado do servidor para a data de criação
    created_at = Column(
        TIMESTAMP(timezone=True), 
        server_default=func.now()
    )

    def __repr__(self):
        return f"<Article(id='{self.id}', title='{self.title[:30]}...')>"


def init_db():
    print("Inicializando o banco de dados...")
    # O comando abaixo cria a tabela 'articles' se ela não existir
    Base.metadata.create_all(bind=engine)
    print("Banco de dados inicializado com sucesso.")


if __name__ == "__main__":
    init_db()