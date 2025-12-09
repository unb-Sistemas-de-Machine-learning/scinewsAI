import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

S2_API_KEY = os.getenv("S2_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
PDF_STORAGE_PATH = "articles_pdf"

# Cria a pasta de PDFs se não existir
if not os.path.exists(PDF_STORAGE_PATH):
    os.makedirs(PDF_STORAGE_PATH)

CS_MACRO_TOPICS = [
    "Software Engineering", "Computer Security", "Distributed Systems",
    "Artificial Intelligence", "Computer Vision", "Database Systems",
    "Human Computer Interaction", "Computer Networks", "Operating Systems"
]
