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
    args = parser.parse_args()
    
    if args.command == "file":
        try:
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
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
