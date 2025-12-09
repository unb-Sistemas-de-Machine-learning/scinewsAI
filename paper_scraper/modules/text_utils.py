import math
import re
import fitz  # PyMuPDF

def clean_text(text_data):
    """Limpa espaços em branco e quebras de linha."""
    if not text_data: return None
    return re.sub(r'\s+', ' ', text_data).strip()

def extract_full_text_from_pdf(pdf_path):
    """Extrai texto de um arquivo PDF local."""
    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()
        return full_text
    except Exception:
        return None

def calculate_relevance_score(paper):
    """
    Calcula score logarítmico para evitar que autores 'Superstars' 
    monopolizem o ranking e esmaguem pesquisadores bons porém menos famosos.
    """
    # 1. Citações do Paper (Peso alto, mas raríssimo em papers novos)
    # Usamos log(x + 1) para evitar erro matemático se for 0
    paper_citations = paper.get('citationCount', 0) or 0
    paper_score = math.log1p(paper_citations) * 10  # Peso 10 no log

    authors = paper.get('authors', [])
    max_author_citations = 0
    max_author_hindex = 0
    
    for author in authors:
        c = author.get('citationCount', 0) or 0
        h = author.get('hIndex', 0) or 0
        if c > max_author_citations: max_author_citations = c
        if h > max_author_hindex: max_author_hindex = h

    # 2. Autoridade do Autor (Escala Logarítmica)
    # Ex: 
    # 100 citações -> log10(100) = 2
    # 10.000 citações -> log10(10000) = 4
    # 100.000 citações -> log10(100000) = 5
    # O peso é 5, então a diferença entre um sênior e um superstar é pequena (20 vs 25 pontos)
    author_cit_score = math.log1p(max_author_citations) * 5

    # 3. H-Index (Métrica Linear é aceitável aqui, pois h-index já é difícil de subir)
    # H-index 10 vs 50 é uma diferença real de qualidade de carreira.
    h_index_score = max_author_hindex * 0.5

    total_score = paper_score + author_cit_score + h_index_score
    return total_score
