import urllib.parse
import feedparser
import time
from datetime import datetime, timedelta

def get_arxiv_articles_by_date_window(days_back=3):
    """
    Busca TODOS os artigos de CS no arXiv dentro da janela de dias especificada.
    """
    search_query = 'cat:cs.*' 
    base_url = 'http://export.arxiv.org/api/query'
    
    # Data de corte em UTC
    cutoff_date = (datetime.utcnow() - timedelta(days=days_back)).date()
    print(f"[ArXiv] Buscando artigos publicados a partir de: {cutoff_date}")

    all_articles = []
    start = 0
    batch_size = 100 
    keep_fetching = True

    while keep_fetching:
        print(f"[ArXiv] Buscando lote {start} a {start+batch_size}...")
        
        params = {
            'search_query': search_query,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending',
            'start': start,
            'max_results': batch_size
        }

        query_url = f"{base_url}?{urllib.parse.urlencode(params)}"
        feed = feedparser.parse(query_url)

        if not feed.entries:
            print("[ArXiv] Fim do feed encontrado.")
            break

        batch_articles = []
        
        for entry in feed.entries:
            try:
                published = datetime.strptime(entry.published, '%Y-%m-%dT%H:%M:%SZ').date()

                if published < cutoff_date:
                    keep_fetching = False
                    continue

                arxiv_id = entry.id.split('/abs/')[-1]
                
                pdf_link = None
                for link in entry.links:
                    if link.get('title') == 'pdf':
                        pdf_link = link.href
                        break
                if not pdf_link:
                    pdf_link = entry.link.replace('/abs/', '/pdf/') + ".pdf"

                clean_title = entry.title.replace('\n', ' ').strip()
                clean_abstract = entry.summary.replace('\n', ' ').strip()
                author_names = [a.name for a in entry.authors]

                # --- CAPTURA DAS TAGS BRUTAS ---
                # O feedparser retorna tags como uma lista de objetos: [{'term': 'cs.AI', ...}, ...]
                raw_tags = [t.term for t in entry.tags]

                batch_articles.append({
                    "arxiv_id": arxiv_id,
                    "title": clean_title,
                    "abstract": clean_abstract,
                    "authors": author_names,
                    "published_date": published,
                    "pdf_url": pdf_link,
                    "arxiv_url": entry.link,
                    "tags": raw_tags
                })
            except Exception as e:
                print(f"[ArXiv Warning] Erro ao processar entrada: {e}")
                continue

        all_articles.extend(batch_articles)
        start += batch_size
        time.sleep(3)

    print(f"[ArXiv] Total de artigos coletados na janela de {days_back} dias: {len(all_articles)}")
    return all_articles
