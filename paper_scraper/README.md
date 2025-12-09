# Paper Scraper

Este diretório contém os scripts responsáveis por buscar, processar e armazenar artigos científicos (atualmente focados no **Arxiv**) em um banco de dados PostgreSQL. O projeto foi refatorado para uma estrutura modular.

## Métrica de Relevância (Scoring)

Para garantir que o feed de artigos seja relevante, utilizamos um algoritmo de pontuação personalizado. O objetivo é equilibrar artigos novos de autores consolidados com descobertas de pesquisadores emergentes, evitando que autores "Superstars" monopolizem o ranking.

A pontuação total ($S_{total}$) é calculada pela soma ponderada de três fatores:

$$
S_{total} = S_{paper} + S_{author} + S_{hindex}
$$

Onde a fórmula detalhada é:

$$
S_{total} = 10 \cdot \ln(C_{paper} + 1) + 5 \cdot \ln(C_{author\_max} + 1) + 0.5 \cdot H_{index\_max}
$$

### Componentes do Algoritmo:

1.  **Citações do Artigo ($S_{paper}$)**
    * **Peso:** 10 (Alto)
    * **Lógica:** Utiliza escala logarítmica ($\ln$). Artigos novos geralmente têm 0 citações, mas se um artigo recente já possui citações, ele recebe um "boost" significativo, pois indica impacto imediato.

2.  **Autoridade do Autor ($S_{author}$)**
    * **Peso:** 5 (Médio)
    * **Lógica:** Baseada no número de citações do autor mais citado do paper.
    * **Por que Logarítmico?** Para "achatar" a curva. Um autor com 100.000 citações não é necessariamente 100x mais relevante para um paper novo do que um autor com 1.000 citações. O logaritmo diminui a distância entre o "Sênior" e o "Superstar", permitindo competição justa.

3.  **H-Index ($S_{hindex}$)**
    * **Peso:** 0.5 (Baixo/Linear)
    * **Lógica:** Escala linear. O *H-Index* já é uma métrica difícil de subir (logarítmica por natureza). Uma diferença de 10 vs 50 no H-Index reflete uma disparidade real de consistência na carreira, por isso mantemos a progressão linear.

> [!NOTE]
> **O que é o H-Index?**
> É uma métrica que representa o número de artigos ($h$) de um autor que receberam pelo menos o mesmo número ($h$) de citações.
>
> *Exemplo:* Um pesquisador com **H-Index 10** significa que ele publicou pelo menos **10 artigos** e *cada um deles* recebeu pelo menos **10 citações**.
>
> Isso ajuda nosso algoritmo a valorizar a **consistência** da carreira, evitando que um autor com apenas um único "artigo viral" (mas baixa produção geral) distorça o ranking.

## Estrutura do Projeto

```bash
paper_scraper/
├── articles_pdf/       # Diretório onde os PDFs baixados são salvos
├── modules/            # Módulos com a lógica de negócio (conexão, rede, scraping)
├── init_db.py          # Script para inicializar as tabelas no banco
├── main.py             # Script principal de execução do scraper
├── docker-compose.yaml # Definição do serviço de Banco de Dados
└── .env                # Variáveis de ambiente (não versionado)
```

## Pré-requisitos

Antes de começar, garanta que você tenha os seguintes softwares instalados na sua máquina:

* **Python 3.12+**
* **Docker** & **Docker Compose**
* **Cliente SQL** (Recomendado: [DBeaver](https://dbeaver.io/) ou [DataGrip]) para visualizar os dados.

## Configuração do Ambiente

### 1. Crie e Ative um Ambiente Virtual

É uma boa prática isolar as dependências do projeto.

```bash
# Crie o ambiente virtual na pasta raíz do projeto (scinewsAI/)
python -m venv .venv

# Ative o ambiente (Linux/macOS)
source .venv/bin/activate

# Entre no diretório do scraper
cd paper_scraper/
```

### 2. Instale as Dependências

Com o ambiente virtual ativado, instale as bibliotecas Python necessárias.

```bash
pip install -r requirements.txt
```

### 3. Configure as Variáveis de Ambiente

As credenciais do banco de dados são gerenciadas através de um arquivo `.env`.

Primeiro, copie o arquivo de exemplo:

```bash
cp .env.example .env
```

Agora, abra o arquivo .env recém-criado e preencha as variáveis.

#### Exemplo de preenchimento do `.env`:

```Ini
# Variáveis para o Docker Compose configurar o container
POSTGRES_USER=docker
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_DB=scinews_db

# String de conexão que o script Python usará para se conectar ao banco
# ATENÇÃO: Os valores devem ser os mesmos definidos acima.
# Use 'localhost' como host, pois a porta do container será mapeada para sua máquina.
DATABASE_URL="postgresql+psycopg2://docker:mysecretpassword@localhost:5432/scinews_db"

# Chave de API Externa (Semantic Scholar)
S2_API_KEY="sua_chave_de_api_do_semantic_scholar"
```

> [!TIP]
> **Recomendação sobre a API Key**: A `S2_API_KEY` é opcional; o sistema funcionará sem ela. No entanto, ela é altamente recomendada para evitar bloqueios por limite de requisições (rate limiting) e garantir uma coleta de dados mais rápida e estável junto ao Semantic Scholar.
> Você pode solicitar uma chave gratuita no site oficial deles.

## Como Rodar

Siga estes passos na ordem para executar o projeto.

### Passo 1: Iniciar o Banco de Dados

Este comando irá subir o container do PostgreSQL definido no `docker-compose.yaml`.

```bash
docker compose up -d
```

Você pode verificar se o container está rodando com `docker compose ps`.

### Passo 2: Inicializar as Tabelas

Com o banco de dados no ar, execute o script `init_db.py` para criar a tabela `articles` e qualquer outra estrutura necessária.

```bash
python init_db.py
```

*Você só precisa rodar este comando na primeira vez que configurar o ambiente ou se apagar os dados do banco.*

### Passo 3: Executar o Scraper de Artigos

Execute o script principal. Ele utilizará as configurações definidas em `modules/config.py` e a lógica em `modules/arxiv_source.py` para buscar e salvar os artigos.

```bash
python main.py
```

O script exibirá o progresso no terminal. Para parar a execução de forma segura, pressione `Ctrl+C` uma vez e aguarde a finalização da tarefa atual.

## Como Visualizar os Dados (DBeaver/Cliente SQL)

1. Abra o **DBeaver** (ou seu cliente preferido).

2. Crie uma **Nova Conexão** do tipo **PostgreSQL**.

3. Preencha os dados conforme seu arquivo `.env`:

    - **Host**: `localhost`

    - **Port**: `5432`

    - **Database**: `scinews_db` (ou o valor de `POSTGRES_DB`)

    - **Username**: `docker` (ou o valor de `POSTGRES_USER`)

    - **Password**: `mysecretpassword` (ou o valor de `POSTGRES_PASSWORD`)

4. Clique em "Test Connection" e depois em "Finish".

## Para Parar

Para parar o container do banco de dados, utilize o seguinte comando:

```bash
docker compose down
```

*Os dados persistem no volume `postgres_data` mesmo após desligar o container.*
