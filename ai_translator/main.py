import sys
import argparse
from dotenv import load_dotenv

load_dotenv()

from src.ingest import ingest_paper
from src.rag import query_rag

def main():
    parser = argparse.ArgumentParser(description="AI Translator & Summarizer for Scientific Papers")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    ingest_parser = subparsers.add_parser("ingest", help="Ingest a PDF paper")
    ingest_parser.add_argument("file_path", help="Path to the PDF file")
    query_parser = subparsers.add_parser("query", help="Ask a question or summarize")
    query_parser.add_argument("question", help="The question or prompt")
    
    args = parser.parse_args()
    
    if args.command == "ingest":
        try:
            result = ingest_paper(args.file_path)
            print(result)
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")
            sys.exit(1)
            
    elif args.command == "query":
        try:
            print("Processando consulta...")
            answer = query_rag(args.question)
            print("\n=== Resposta ===\n")
            print(answer)
            print("\n=============\n")
        except Exception as e:
            print(f"Erro ao consultar: {e}")
            sys.exit(1)
            
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
