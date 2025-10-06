import os
import re
import time
from datetime import datetime, timedelta, timezone
import signal

import feedparser
import urllib.parse
import requests
import fitz
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from categories import ARXIV_CS_CATEGORY_MAP

shutdown_requested = False

# Função para lidar com interrupção do script (Ctrl+C)
def signal_handler(sig, frame):
    global shutdown_requested
    if not shutdown_requested:
        print("\n[!] Interrupção solicitada. O script será encerrado após a conclusão da tarefa atual...")
        shutdown_requested = True
    else:
        print("\n[!] Múltiplas interrupções recebidas. Encerrando forçadamente.")
        exit(1)

# Registro de função para lidar com interrupção do script (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

# Carrega as variáveis de ambiente (DATABASE_URL) do arquivo .env
load_dotenv()

# --- Configurações ---
DATABASE_URL = os.getenv("DATABASE_URL")
PDF_STORAGE_PATH = "articles_pdf"

# Verifica se a pasta para armazenar os PDFs existe, senão, cria.
if not os.path.exists(PDF_STORAGE_PATH):
    os.makedirs(PDF_STORAGE_PATH)

# Configuração do banco de dados com SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def clean_text(text_data):
    return re.sub(r'\s+', ' ', text_data).strip()

def extract_full_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()
        return full_text
    except Exception as e:
        print(f"  [!] Erro ao processar o PDF {pdf_path}: {e}")
        return None

def fetch_and_store_articles():
    print("Iniciando a busca por artigos da última semana no arXiv...")

    # Calcula as datas para a busca (últimos 7 dias)
    today = datetime.now(timezone.utc)
    seven_days_ago = today - timedelta(days=7)
    start_date = seven_days_ago.strftime('%Y%m%d%H%M%S')
    end_date = today.strftime('%Y%m%d%H%M%S')

    # Query para a API do arXiv
    # cat:cs.* -> Busca em todas as categorias de Computer Science
    # submittedDate:[...] -> Filtra pela data de envio
    query = f'cat:cs.* AND submittedDate:[{start_date} TO {end_date}]'
    
    base_url = 'http://export.arxiv.org/api/query'
    params = {
        'search_query': query,
        'start': 0,
        'max_results': 20  # Limite para não sobrecarregar.
    }

    encoded_params = urllib.parse.urlencode(params)
    final_url = f"{base_url}?{encoded_params}"

    print(f"Buscando na URL: {final_url}")

    try:
        response = feedparser.parse(final_url)
    except Exception as e:
        print(f"Erro ao conectar-se à API do arXiv: {e}")
        return

    if not response.entries:
        print("Nenhum artigo novo encontrado na última semana.")
        return

    print(f"Encontrados {len(response.entries)} artigos. Processando...")

    session = SessionLocal()
    
    for entry in response.entries:
        if shutdown_requested:
            print("[*] Encerrando o loop de processamento devido à solicitação do usuário.")
            break

        try:
            # Extrai os metadados do artigo
            article_id = entry.id.split('/abs/')[-1]
            title = clean_text(entry.title)
            abstract = clean_text(entry.summary)
            publication_date = datetime.strptime(entry.published, '%Y-%m-%dT%H:%M:%SZ').date()
            authors = [author.name for author in entry.authors]
            # As 'tags' no feed são as categorias/keywords
            keywords = [ARXIV_CS_CATEGORY_MAP[tag['term']] for tag in entry.tags if tag['term'] in ARXIV_CS_CATEGORY_MAP]
            
            # O link da página do artigo
            source_url = entry.link
            
            # O link direto para o PDF
            pdf_url = None
            for link in entry.links:
                if link.get('title') == 'pdf':
                    pdf_url = link.href
                    break

            if not pdf_url:
                print(f"  [!] Não foi possível encontrar o link do PDF para o artigo '{title}'. Pulando.")
                continue

            print(f"\nProcessando artigo: {title}")

            # --- Download do PDF ---
            pdf_filename = f"{article_id.replace('/', '_')}.pdf"
            pdf_path = os.path.join(PDF_STORAGE_PATH, pdf_filename)
            
            if not os.path.exists(pdf_path):
                print(f"  [*] Baixando PDF de: {pdf_url}")
                pdf_response = requests.get(pdf_url)
                pdf_response.raise_for_status() # Lança erro se o download falhar
                with open(pdf_path, 'wb') as f:
                    f.write(pdf_response.content)
                print(f"  [*] PDF salvo em: {pdf_path}")
            else:
                print(f"  [*] PDF já existe localmente: {pdf_path}")

            # --- Extração do Texto Completo ---
            print("  [*] Extraindo texto completo do PDF...")
            full_text = extract_full_text_from_pdf(pdf_path)
            if not full_text:
                # Se a extração falhar, pulamos para o próximo artigo
                continue

            # --- Limpando os caracteres nulos dos campos de texto
            title = title.replace('\x00', '')
            abstract = abstract.replace('\x00', '')
            full_text = full_text.replace('\x00', '')
            authors = [author.replace('\x00', '') for author in authors]
            keywords = [keyword.replace('\x00', '') for keyword in keywords]

            # --- Inserção no Banco de Dados ---
            print("  [*] Inserindo dados no banco de dados...")
            
            # Query SQL
            stmt = text("""
                INSERT INTO articles (id, title, authors, publication_date, abstract, keywords, full_text, source_url, original_pdf_path, processing_status)
                VALUES (:id, :title, :authors, :publication_date, :abstract, :keywords, :full_text, :source_url, :original_pdf_path, :processing_status)
                ON CONFLICT (id) DO NOTHING;
            """)

            db_entry = {
                "id": article_id,
                "title": title,
                "authors": authors,
                "publication_date": publication_date,
                "abstract": abstract,
                "keywords": keywords,
                "full_text": full_text,
                "source_url": source_url,
                "original_pdf_path": pdf_path,
                "processing_status": 'parsed' # Marcamos como 'parsed' pois já extraímos o texto
            }
            
            session.execute(stmt, db_entry)
            session.commit()
            print("  [*] Artigo salvo com sucesso!")

        except requests.exceptions.RequestException as e:
            print(f"  [!] Falha no download do PDF para o artigo '{title}': {e}")
            session.rollback()
        except IntegrityError:
            print(f"  [*] Artigo '{title}' já existe no banco de dados. Pulando.")
            session.rollback() # Desfaz a transação atual
        except Exception as e:
            print(f"  [!] Ocorreu um erro inesperado ao processar o artigo '{title}': {e}")
            session.rollback()

        # Pausa educada para não sobrecarregar a API do arXiv
        time.sleep(3) 

    session.close()

    if shutdown_requested:
        print("\nProcessamento interrompido de forma limpa pelo usuário.")
    else:   
        print("\nProcesso finalizado.")


if __name__ == "__main__":
    fetch_and_store_articles()