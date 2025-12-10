import time
import sys
from sqlalchemy import text
import os

# Importações Locais
from modules.config import S2_API_KEY, PDF_STORAGE_PATH
from modules.database import get_db_session
from modules.network import get_robust_session
from modules.text_utils import extract_full_text_from_pdf, calculate_relevance_score
from modules.arxiv_source import get_arxiv_articles_by_date_window
from modules.categories import ARXIV_CS_CATEGORY_MAP 

def run_curation_pipeline():
    print("=== INICIANDO PIPELINE DE CURADORIA SEMANAL ===")
    
    if S2_API_KEY:
        print(f"[Config] API Key detectada: {S2_API_KEY[:5]}...")
    else:
        print("[Config] AVISO: Sem API Key. Isso vai demorar muito devido aos limites.")

    # --- FASE 1: COLETA (ARXIV) ---
    DAYS_BACK = 1
    try:
        raw_candidates = get_arxiv_articles_by_date_window(days_back=DAYS_BACK)
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(f"[Erro] Falha ao buscar no ArXiv: {e}")
        return
    
    if not raw_candidates:
        print("Nenhum artigo encontrado no período.")
        return

    # --- FASE 2: AUDITORIA E SCORING (SEMANTIC SCHOLAR) ---
    print(f"\n=== FASE 2: AUDITORIA DE {len(raw_candidates)} ARTIGOS ===")
    
    session_db = get_db_session()
    http = get_robust_session()
    
    scored_candidates = []
    processed_count = 0
    total_count = len(raw_candidates)

    try:
        for paper in raw_candidates:
            processed_count += 1
            arxiv_id = paper['arxiv_id']
            title = paper['title']

            exists = session_db.execute(text("SELECT 1 FROM articles WHERE id = :id"), {"id": arxiv_id}).fetchone()
            if exists:
                continue

            s2_score = 0
            s2_data_found = False
            
            try:
                params = {
                    "query": title,
                    "fields": "title,authors.name,authors.hIndex,authors.citationCount,citationCount",
                    "limit": 1
                }
                time.sleep(0.5) 
                
                r = http.get("https://api.semanticscholar.org/graph/v1/paper/search", params=params, timeout=5)
                
                if r.status_code == 200:
                    data = r.json()
                    if data.get('data'):
                        s2_paper = data['data'][0]
                        if s2_paper['title'].lower()[:30] in title.lower():
                            s2_score = calculate_relevance_score(s2_paper)
                            s2_data_found = True
            except Exception:
                pass 

            paper['final_score'] = s2_score
            scored_candidates.append(paper)
            
            status = f"Score: {s2_score:.1f}" if s2_data_found else "S2: N/A"
            print(f"[{processed_count}/{total_count}] Analisado: {title[:40]}... | {status}")

    except KeyboardInterrupt:
        print("\n[!] Interrompido durante a auditoria. Seguindo para mostrar o ranking parcial...")

    # --- FASE 3: RANKING E SELEÇÃO (RANKING) ---
    if not scored_candidates:
        print("\n[!] Nenhum candidato foi processado antes da interrupção.")
        session_db.close()
        return

    print("\n=== FASE 3: RANKING E SELEÇÃO (PARCIAL/TOTAL) ===")
    
    scored_candidates.sort(key=lambda x: x['final_score'], reverse=True)
    
    TOP_N = 20
    winners = scored_candidates[:TOP_N]
    
    print(f"Selecionados os Top {len(winners)} artigos.")
    
    # Exibe o TOP 5
    print("-" * 60)
    for i, p in enumerate(winners[:5]):
        print(f"#{i+1} [Score: {p['final_score']:.1f}] {p['title']}")
    print("-" * 60)

    # In auto mode, we skip confirmation. In manual mode, we might want it, 
    # but for simplicity and consistency with "autonomously" request, 
    # we will proceed automatically or check env var.
    # For now, removing the block to ensure it runs autonomously.


    # --- FASE 4: DOWNLOAD E PERSISTÊNCIA ---
    print(f"\n=== FASE 4: DOWNLOAD E SALVAMENTO ({len(winners)} itens) ===")
    
    saved_count = 0
    
    try:
        for paper in winners:
            print(f"Processando Vencedor: {paper['title'][:50]}...")
            
            # Mapeamento de Keywords usando categories.py
            raw_tags = paper.get('tags', [])
            mapped_keywords = []
            for tag in raw_tags:
                if tag in ARXIV_CS_CATEGORY_MAP:
                    mapped_keywords.append(ARXIV_CS_CATEGORY_MAP[tag])
                else:
                    mapped_keywords.append(tag)
            
            mapped_keywords = list(dict.fromkeys(mapped_keywords))

            try:
                pdf_filename = f"{paper['arxiv_id']}.pdf".replace('/', '_')
                pdf_path = os.path.join(PDF_STORAGE_PATH, pdf_filename)
                
                if not os.path.exists(pdf_path):
                    print(f"  -> Baixando PDF...")
                    resp = http.get(paper['pdf_url'], timeout=60)
                    if resp.status_code == 200:
                        with open(pdf_path, 'wb') as f:
                            f.write(resp.content)
                    else:
                        print(f"  [!] Falha download: {resp.status_code}")
                        continue
                
                full_text = extract_full_text_from_pdf(pdf_path)
                if not full_text or len(full_text) < 500:
                    print("  [!] PDF vazio/ilegível.")
                    if os.path.exists(pdf_path): os.remove(pdf_path)
                    continue

                stmt = text("""
                    INSERT INTO articles (id, title, authors, publication_date, abstract, keywords, full_text, source_url, original_pdf_path, processing_status, relevance_score)
                    VALUES (:id, :title, :authors, :publication_date, :abstract, :keywords, :full_text, :source_url, :original_pdf_path, :processing_status, :relevance_score)
                    ON CONFLICT (id) DO NOTHING;
                """)

                db_entry = {
                    "id": paper['arxiv_id'],
                    "title": paper['title'],
                    "authors": paper['authors'],
                    "publication_date": paper['published_date'],
                    "abstract": paper['abstract'],
                    "keywords": mapped_keywords,
                    "full_text": full_text.replace('\x00', ''),
                    "source_url": paper['arxiv_url'],
                    "original_pdf_path": pdf_path,
                    "processing_status": 'parsed',
                    "relevance_score": paper['final_score']
                }
                session_db.execute(stmt, db_entry)
                session_db.commit()
                saved_count += 1
                print("  [*] Salvo com sucesso.")
                
            except Exception as e:
                print(f"  [!] Erro crítico ao salvar: {e}")
                session_db.rollback()
    
    except KeyboardInterrupt:
        print("\n[!] Interrupção durante o salvamento. O banco permanece íntegro.")
        raise

    session_db.close()
    print(f"\n=== CURADORIA FINALIZADA ===")
    print(f"Total salvo no DB: {saved_count}")

import time
import schedule
import signal

def job():
    print(f"Executing scheduled job at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        run_curation_pipeline()
    except Exception as e:
        print(f"Job failed: {e}")

def main():
    """
    Main entry point. Supports manual run or scheduled automated run.
    """
    mode = os.getenv("EXECUTION_MODE", "manual").lower()
    
    # Handle graceful shutdown
    def signal_handler(sig, frame):
        print("\nGracefully shutting down...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    if mode == "auto":
        print("Starting Paper Scraper in AUTOMATED mode (Daily at 08:00).")
        # Schedule the job
        schedule.every().day.at("08:00").do(job)
        
        # Run once immediately on start for testing/verification purpose? 
        # Or maybe check if it's the first run. For now, let's just schedule.
        # Use a config or env var to determine if we want an immediate run.
        if os.getenv("RUN_ON_START", "false").lower() == "true":
            job()
            
        while True:
            schedule.run_pending()
            time.sleep(60)
    else:
        print("Starting Paper Scraper in MANUAL mode.")
        run_curation_pipeline()

if __name__ == "__main__":
    main()
