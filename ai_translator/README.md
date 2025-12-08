# Módulo de IA

Para executar:

1. Crie uma pasta `data` na raiz do repositório e coloque um artigo em pdf dentro dela.
2. Faça a build do docker compose

```bash
docker compose build
```

3. Insira o arquivo o arquivo no ChromaDB:

```bash
docker compose run app ingest data/arquivo.pdf
```

4. Envia uma pergunta ao RAG

```bash
docker compose run app query "summarize the main points of this articles"
```