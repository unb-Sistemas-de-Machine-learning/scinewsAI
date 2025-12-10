import sys
import argparse
from dotenv import load_dotenv

load_dotenv()

from src.ingest import ingest_paper
from src.rag import query_rag

def main():
    parser = argparse.ArgumentParser(description="AI Translator & Summarizer for Scientific Papers")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    file_parser = subparsers.add_parser("file", help="File related commands")
    file_parser.add_argument("file_path", help="Path to the PDF file")
    
    db_parser = subparsers.add_parser("db", help="Database related commands (Process pending articles)")
    db_parser.add_argument("--loop", action="store_true", help="Run in continuous loop mode")

    args = parser.parse_args()
    
    if args.command == "file":
        try:
            from src.ingest import ingest_paper
            result = ingest_paper(args.file_path)
            print(result)
            print("Processando consulta...")
            answer = query_rag()
            print("\n=== Resposta ===\n")
            print(answer)
            print("\n=============\n")
        except Exception as e:
            print(f"Erro durante o processamento: {e}")
            sys.exit(1)
            
    elif args.command == "db":
        try:
            from src.db_processor import process_articles
            process_articles(loop=args.loop)
        except Exception as e:
            print(f"Error during database processing: {e}")
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
