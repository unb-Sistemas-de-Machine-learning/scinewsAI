# Módulo de IA

Para executar:

1. Crie uma pasta `data` na raiz do repositório e coloque um artigo em pdf dentro dela.
2. Faça a build do docker compose

```bash
docker compose build
```

3. Rode o container passando o diretório do arquivo como argumento:

```bash
docker compose run app file data/arquivo.pdf
```