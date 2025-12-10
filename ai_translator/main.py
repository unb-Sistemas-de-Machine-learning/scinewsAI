import sys
import os
import argparse
import time
from dotenv import load_dotenv

load_dotenv()

from src.ingest import ingest_paper
from src.rag import query_rag, query_rag_with_context
from src.tracking import setup_mlflow, log_common_params
from src.metrics import log_basic_metrics, maybe_load_reference
import mlflow

def main():
    parser = argparse.ArgumentParser(description="AI Translator & Summarizer for Scientific Papers")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    file_parser = subparsers.add_parser("file", help="File related commands")
    file_parser.add_argument("file_path", help="Path to the PDF file")
    
    db_parser = subparsers.add_parser("db", help="Database related commands (Process pending articles)")
    db_parser.add_argument("--loop", action="store_true", help="Run in continuous loop mode")

    args = parser.parse_args()
    
    if args.command == "file":
        tracking_enabled = setup_mlflow()
        run_active = False
        try:
            run_name = f"file:{os.path.basename(args.file_path)}"
            if tracking_enabled:
                mlflow.start_run(run_name=run_name)
                run_active = True
                log_common_params({"input_source": "file"})
                mlflow.log_param("input_file", args.file_path)

            ingest_meta = ingest_paper(args.file_path)
            print(f"Inserido com sucesso {ingest_meta['file_path']} com {ingest_meta['chunks']} chunks.")

            if tracking_enabled:
                mlflow.log_metrics({
                    "pages": ingest_meta["pages"],
                    "chunks": ingest_meta["chunks"],
                    "ingest_time_s": ingest_meta["ingest_time_s"],
                    "split_time_s": ingest_meta["split_time_s"],
                })

            rag_start = time.time()
            print("Processando consulta...")
            rag_result = query_rag_with_context()
            answer = rag_result["answer"]
            contexts = rag_result["contexts"]
            rag_time = time.time() - rag_start

            print("\n=== Resposta ===\n")
            print(answer)
            print("\n=============\n")

            if tracking_enabled:
                mlflow.log_metric("rag_time_s", rag_time)
                mlflow.log_text(answer, "summary.md")
                ref_path = os.getenv("REFERENCE_SUMMARY_PATH")
                reference = maybe_load_reference(ref_path)
                log_basic_metrics(answer, contexts, reference)
        except Exception as e:
            print(f"Erro durante o processamento: {e}")
            sys.exit(1)
        finally:
            if run_active:
                mlflow.end_run()
            
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
