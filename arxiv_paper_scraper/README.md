# ArXiv Paper Scraper

Este diretório contém os scripts responsáveis por buscar, processar e armazenar artigos científicos da plataforma arXiv em um banco de dados PostgreSQL.

## Pré-requisitos

Antes de começar, garanta que você tenha os seguintes softwares instalados na sua máquina:
* Python 3.12+
* Docker
* Docker Compose

## Configuração do Ambiente

Vamos configurar o ambiente passo a passo.

### 1. Crie e Ative um Ambiente Virtual

É uma boa prática isolar as dependências do projeto.

```bash
# Crie o ambiente virtual na pasta raíz do projeto (scinewsAI/)
python -m venv .venv

# Ative o ambiente (Linux/macOS)
source .venv/bin/activate

# Entre no diretório do scraper
cd arxiv_paper_scraper/
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
```

## Como Rodar

Siga estes passos na ordem para executar o projeto.

### Passo 1: Iniciar o Banco de Dados

Este comando irá baixar a imagem do PostgreSQL (se necessário) e iniciar o container do banco de dados em segundo plano.

```bash
docker compose up -d
```

Você pode verificar se o container está rodando com `docker compose ps`.

### Passo 2: Inicializar as Tabelas no Banco

Com o banco de dados no ar, execute o script `db.py` para criar a tabela `articles` e qualquer outra estrutura necessária.

```bash
python db.py
```

*Você só precisa rodar este comando na primeira vez que configurar o ambiente ou se apagar os dados do banco.*

### Passo 3: Executar o Scraper de Artigos

Agora, execute o script principal para buscar 20 artigos da última semana no arXiv, processá-los e salvá-los no banco de dados.

*Caso queira aumentar ou diminuir o número de papers a serem buscados, altere o valor de `max_results` na linha **81** de `fetch_articles.py`*

```bash
python fetch_articles.py
```

O script exibirá o progresso no terminal. Para parar a execução de forma segura, pressione `Ctrl+C` uma vez e aguarde a finalização da tarefa atual.

## Como Visualizar as Tabelas

### 1. Acesse o pgAdmin:

Abra seu navegador e acesse: `http://localhost:5050`.

### 2. Faça Login no pgAdmin:

Use as credenciais que definimos no arquivo `docker-compose.yaml`:
- **Email**: admin@scinews.com
- **Senha**: admin

### 3. Conecte ao Banco de Dados:

Esta é a parte mais importante. Dentro da interface do pgAdmin, você precisará adicionar um novo servidor para se conectar ao seu banco de dados PostgreSQL.

- Clique com o botão direito em "Servers" -> "Register" -> "Server...".

- Na aba **"General"**, dê um nome para a sua conexão, por exemplo, "SciNews Articles".

- Vá para a aba **"Connection"** e preencha com os seguintes dados:

    - **Host name/address**: `db` (Este é o nome do serviço do banco no `docker-compose.yaml`).

    - **Port**: `5432`

    - **Maintenance database**: Use o nome do seu banco (`POSTGRES_DB`) definido no seu arquivo `.env`.

    - **Username**: Use o nome do seu usuário (`POSTGRES_USER`) definido no seu arquivo `.env`.

    - **Password**: Use a sua senha (`POSTGRES_PASSWORD`) definida no seu arquivo `.env`.

- Clique em "Save".

## Para Parar

Para parar o container do banco de dados, utilize o seguinte comando:

```bash
docker compose down
```

Este comando para e remove o container, mas seus dados continuarão salvos no volume do Docker, prontos para a próxima vez que você iniciar o serviço com `docker compose up -d`.