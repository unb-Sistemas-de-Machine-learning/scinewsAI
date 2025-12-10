-- SciNewsAI Database Initialization

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create profile type enum
CREATE TYPE profile_type AS ENUM ('STUDENT', 'EDUCATOR', 'ENTHUSIAST');

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    profile_type profile_type DEFAULT 'STUDENT',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

-- Topics table
CREATE TABLE IF NOT EXISTS topics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL UNIQUE,
    slug VARCHAR(255) NOT NULL UNIQUE,
    description TEXT
);

CREATE INDEX idx_topics_slug ON topics(slug);

-- Articles table (matches user's schema)
CREATE TABLE IF NOT EXISTS articles (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    authors TEXT[],
    publication_date DATE,
    abstract TEXT,
    keywords TEXT[],
    full_text TEXT,
    source_url TEXT,
    original_pdf_path TEXT,
    processing_status VARCHAR(50) DEFAULT 'pending',
    simplified_text TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    relevance_score FLOAT DEFAULT 0.0
);

CREATE INDEX idx_articles_status ON articles(processing_status);
CREATE INDEX idx_articles_date ON articles(publication_date DESC);

-- Subscriptions table (user-topic relationship)
CREATE TABLE IF NOT EXISTS subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, topic_id)
);

CREATE INDEX idx_subscriptions_user ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_topic ON subscriptions(topic_id);

-- Likes table (user-article relationship for likes/favorites)
CREATE TABLE IF NOT EXISTS likes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    article_id TEXT NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, article_id)
);

CREATE INDEX idx_likes_user ON likes(user_id);
CREATE INDEX idx_likes_article ON likes(article_id);
CREATE INDEX idx_likes_created ON likes(created_at DESC);

-- Insert default topics based on ArXiv CS Categories
INSERT INTO topics (name, slug, description) VALUES
    ('Inteligência Artificial', 'artificial-intelligence', 'IA, sistemas inteligentes e raciocínio automático'),
    ('Aprendizado de Máquina', 'machine-learning', 'Aprendizado de máquina, redes neurais e deep learning'),
    ('Visão Computacional e Reconhecimento de Padrões', 'computer-vision', 'Visão computacional, detecção de objetos e reconhecimento de padrões'),
    ('Processamento de Linguagem Natural', 'nlp', 'Processamento de linguagem natural, análise de texto e modelos de linguagem'),
    ('Robótica', 'robotics', 'Robótica, automação e sistemas robóticos'),
    ('Computação Distribuída', 'distributed-computing', 'Computação distribuída, paralela e em cluster'),
    ('Criptografia e Segurança', 'cybersecurity', 'Criptografia, segurança de redes e privacidade de dados'),
    ('Bancos de Dados', 'databases', 'Sistemas de banco de dados, consultas e armazenamento'),
    ('Engenharia de Software', 'software-engineering', 'Engenharia de software, desenvolvimento e arquitetura'),
    ('Linguagens de Programação', 'programming-languages', 'Linguagens de programação, compiladores e interpretadores'),
    ('Interação Humano-Computador', 'hci', 'Interação humano-computador, UX e design de interfaces'),
    ('Computação Gráfica', 'graphics', 'Computação gráfica, visualização e renderização'),
    ('Estruturas de Dados e Algoritmos', 'algorithms', 'Estruturas de dados, algoritmos e análise de complexidade'),
    ('Recuperação de Informação', 'information-retrieval', 'Recuperação de informação, busca e indexação'),
    ('Sistemas Operacionais', 'operating-systems', 'Sistemas operacionais, kernel e gerenciamento de recursos'),
    ('Redes e Arquitetura de Internet', 'networking', 'Redes de computadores, protocolos e arquitetura de internet'),
    ('Computação Neural e Evolutiva', 'neural-computing', 'Computação neural, algoritmos genéticos e evolução'),
    ('Linguagens Formais e Teoria de Autômatos', 'formal-languages', 'Linguagens formais, autômatos e teoria computacional'),
    ('Teoria da Informação', 'information-theory', 'Teoria da informação, codificação e compressão'),
    ('Lógica em Ciência da Computação', 'logic', 'Lógica computacional, verificação formal e especificação'),
    ('Complexidade Computacional', 'complexity', 'Complexidade computacional, P vs NP e problemas intratáveis'),
    ('Bancos de Dados', 'databases', 'Bancos de dados, consultas otimizadas e indexação'),
    ('Redes Sociais e de Informação', 'social-networks', 'Redes sociais, análise de grafos e difusão de informação'),
    ('Sistemas e Controle', 'systems-control', 'Sistemas de controle, automação e engenharia de sistemas'),
    ('Geometria Computacional', 'computational-geometry', 'Geometria computacional e algoritmos geométricos'),
    ('Multimídia', 'multimedia', 'Processamento multimídia, áudio, vídeo e animação'),
    ('Bibliotecas Digitais', 'digital-libraries', 'Bibliotecas digitais, catalogação e preservação de conteúdo'),
    ('Arquitetura de Hardware', 'hardware-architecture', 'Arquitetura de hardware, processadores e computadores'),
    ('Desempenho', 'performance', 'Otimização de performance, benchmarking e análise de desempenho'),
    ('Tecnologias Emergentes', 'emerging-technologies', 'Tecnologias emergentes como computação quântica e IA explícita')
ON CONFLICT (slug) DO NOTHING;

-- Inserir artigos de exemplo
INSERT INTO articles (id, title, authors, publication_date, abstract, keywords, source_url, processing_status, simplified_text) VALUES
    ('arxiv-2401-00001', 
     'Atenção é Tudo que Você Precisa: Uma Revisão Abrangente das Arquiteturas Transformer',
     ARRAY['Maria Santos', 'John Chen', 'Ahmed Hassan'],
     '2024-01-15',
     'Este artigo fornece uma revisão abrangente das arquiteturas transformer e sua evolução desde o artigo original "Attention Is All You Need". Analisamos os componentes-chave que tornam os transformers eficazes e discutimos avanços recentes em mecanismos de atenção eficientes.',
     ARRAY['transformers', 'atenção', 'aprendizado profundo', 'redes neurais'],
     'https://arxiv.org/abs/2401.00001',
     'translated',
     '## Sobre o que é este artigo?

Este artigo analisa profundamente as **arquiteturas transformer** — a tecnologia por trás de sistemas modernos de IA como ChatGPT e BERT.

## A Inovação Principal: Atenção

A ideia principal por trás dos transformers é algo chamado **atenção**. Imagine ler uma frase e entender a que "ele" se refere anteriormente no texto. Os transformers fazem isso automaticamente e de forma muito eficiente.

## Por que Isso Importa?

Antes dos transformers, os sistemas de IA processavam texto palavra por palavra. Os transformers podem olhar para frases inteiras de uma só vez, entendendo relações entre todas as palavras simultaneamente.

## Principais Descobertas

1. **Eficiência**: Modelos transformer mais novos estão ficando mais rápidos
2. **Escalabilidade**: Funcionam bem para frases únicas ou milhões de documentos
3. **Versatilidade**: A mesma arquitetura funciona para texto, imagens e música'),
    
    ('arxiv-2401-00002',
     'Aprendizado Federado em Escala: Aprendizado de Máquina com Preservação de Privacidade para Saúde',
     ARRAY['Elena Rodriguez', 'Michael Zhang', 'Sarah Johnson'],
     '2024-01-18',
     'Apresentamos uma nova abordagem para aprendizado federado que permite que múltiplas instituições de saúde treinem colaborativamente modelos de aprendizado de máquina sem compartilhar dados sensíveis de pacientes.',
     ARRAY['aprendizado federado', 'privacidade', 'saúde', 'aprendizado de máquina'],
     'https://arxiv.org/abs/2401.00002',
     'translated',
     '## Sobre o que é este artigo?

Esta pesquisa introduz uma nova forma de treinar sistemas de IA em saúde mantendo os dados dos pacientes completamente privados através do **aprendizado federado**.

## O Problema

Hospitais possuem dados médicos valiosos que poderiam ajudar a treinar IA, mas compartilhar dados de pacientes levanta sérias preocupações de privacidade.

## A Solução

Em vez de trazer todos os dados para um único lugar, esta abordagem leva o treinamento de IA para onde os dados já estão:

1. Cada hospital treina um modelo local de IA com seus próprios dados
2. Apenas os padrões aprendidos (não os dados reais) são compartilhados
3. Esses padrões são combinados para criar um modelo global

## Principais Benefícios

- **Privacidade**: Dados dos pacientes nunca saem do hospital
- **Conformidade**: Atende às regulamentações de privacidade em saúde
- **Precisão**: O modelo combinado é tão bom quanto se todos os dados fossem compartilhados')
ON CONFLICT (id) DO NOTHING;

-- Função para atualizar o timestamp updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para a tabela users
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
