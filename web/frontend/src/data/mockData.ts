import { Article, Topic } from '@/types';

export const TOPICS: Topic[] = [
  {
    id: 'ai-ml',
    name: 'Inteligência Artificial e Aprendizado de Máquina',
    description: 'Aprendizado profundo, redes neurais e sistemas inteligentes',
    slug: 'artificial-intelligence',
    article_count: 142,
  },
  {
    id: 'nlp',
    name: 'Processamento de Linguagem Natural',
    description: 'Modelos de linguagem, análise de texto e linguística computacional',
    slug: 'nlp',
    article_count: 89,
  },
  {
    id: 'cv',
    name: 'Visão Computacional',
    description: 'Reconhecimento de imagens, detecção de objetos e computação visual',
    slug: 'computer-vision',
    article_count: 67,
  },
  {
    id: 'distributed',
    name: 'Sistemas Distribuídos',
    description: 'Computação em nuvem, processamento paralelo e arquiteturas escaláveis',
    slug: 'distributed-systems',
    article_count: 45,
  },
  {
    id: 'security',
    name: 'Cibersegurança',
    description: 'Criptografia, segurança de redes e privacidade',
    slug: 'cybersecurity',
    article_count: 78,
  },
  {
    id: 'hci',
    name: 'Interação Humano-Computador',
    description: 'Experiência do usuário, acessibilidade e design de interfaces',
    slug: 'hci',
    article_count: 34,
  },
  {
    id: 'algorithms',
    name: 'Algoritmos e Estruturas de Dados',
    description: 'Complexidade computacional, otimização e design de algoritmos',
    slug: 'algorithms',
    article_count: 56,
  },
  {
    id: 'quantum',
    name: 'Computação Quântica',
    description: 'Algoritmos quânticos, informação quântica e hardware quântico',
    slug: 'quantum-computing',
    article_count: 28,
  },
];

export const MOCK_ARTICLES: Article[] = [
  {
    id: 'arxiv-2401-00001',
    title: 'Atenção é Tudo que Você Precisa: Uma Revisão Abrangente das Arquiteturas Transformer',
    authors: ['Maria Santos', 'John Chen', 'Ahmed Hassan'],
    publication_date: '2024-01-15',
    abstract: 'Este artigo fornece uma revisão abrangente das arquiteturas transformer e sua evolução desde o artigo original "Attention Is All You Need". Analisamos os componentes-chave que tornam os transformers eficazes e discutimos avanços recentes em mecanismos de atenção eficientes.',
    keywords: ['transformers', 'atenção', 'aprendizado profundo', 'redes neurais'],
    source_url: 'https://arxiv.org/abs/2401.00001',
    processing_status: 'completed',
    simplified_text: `
## Sobre o que é este artigo?

Este artigo analisa profundamente as **arquiteturas transformer** — a tecnologia por trás de sistemas de IA modernos como ChatGPT e BERT. Pense nos transformers como uma nova maneira dos computadores entenderem e processarem informações, especialmente texto.

## A Inovação Principal: Atenção

A ideia principal por trás dos transformers é algo chamado **atenção**. Imagine ler uma frase: "O gato sentou no tapete porque estava cansado." Para entender a que "estava" se refere, você precisa prestar atenção em "gato" anteriormente na frase. Os transformers fazem isso automaticamente e de forma muito eficiente.

## Por Que Isso Importa?

Antes dos transformers, sistemas de IA processavam texto palavra por palavra, como ler um livro uma letra por vez. Os transformers podem olhar para sentenças ou parágrafos inteiros de uma vez, entendendo relações entre todas as palavras simultaneamente.

## Principais Descobertas

1. **Eficiência**: Os modelos transformer mais novos estão se tornando mais rápidos e usam menos poder computacional
2. **Escalabilidade**: Eles funcionam bem seja processando uma única frase ou milhões de documentos
3. **Versatilidade**: A mesma arquitetura básica funciona para texto, imagens e até música

## O Que Vem a Seguir?

Pesquisadores estão trabalhando para tornar os transformers ainda mais eficientes, potencialmente permitindo que sistemas de IA poderosos rodem em smartphones e outros dispositivos pequenos.
    `,
    created_at: '2024-01-15T10:30:00Z',
  },
  {
    id: 'arxiv-2401-00002',
    title: 'Aprendizado Federado em Escala: Aprendizado de Máquina com Preservação de Privacidade para Saúde',
    authors: ['Elena Rodriguez', 'Michael Zhang', 'Sarah Johnson'],
    publication_date: '2024-01-18',
    abstract: 'Apresentamos uma abordagem inovadora para aprendizado federado que permite que múltiplas instituições de saúde treinem colaborativamente modelos de aprendizado de máquina sem compartilhar dados sensíveis de pacientes. Nosso método alcança precisão de ponta enquanto mantém garantias rigorosas de privacidade.',
    keywords: ['aprendizado federado', 'privacidade', 'saúde', 'aprendizado de máquina'],
    source_url: 'https://arxiv.org/abs/2401.00002',
    processing_status: 'completed',
    simplified_text: `
## Sobre o que é este artigo?

Esta pesquisa introduz uma nova maneira de treinar sistemas de IA na área da saúde mantendo os dados dos pacientes completamente privados. Isso se chama **aprendizado federado**.

## O Problema

Hospitais têm dados médicos valiosos que poderiam ajudar a treinar IA para detectar doenças mais cedo e melhorar tratamentos. Mas compartilhar dados de pacientes entre hospitais levanta sérias preocupações de privacidade e questões legais.

## A Solução: Aprendizado Federado

Em vez de trazer todos os dados para um único lugar, essa abordagem leva o treinamento de IA para onde os dados já estão:

1. Cada hospital treina um modelo de IA local com seus próprios dados
2. Apenas os padrões aprendidos (não os dados reais) são compartilhados
3. Esses padrões são combinados para criar um modelo global
4. O processo se repete até que a IA se torne altamente precisa

## Principais Benefícios

- **Privacidade**: Os dados dos pacientes nunca saem do hospital
- **Conformidade**: Atende aos regulamentos de privacidade em saúde
- **Precisão**: O modelo combinado é tão bom quanto se todos os dados fossem compartilhados

## Impacto no Mundo Real

Esta tecnologia poderia ajudar a detectar doenças mais cedo, prever resultados de pacientes e personalizar tratamentos — tudo sem comprometer a privacidade dos pacientes.
    `,
    created_at: '2024-01-18T14:20:00Z',
  },
  {
    id: 'arxiv-2401-00003',
    title: 'Correção de Erros Quânticos em Computadores Quânticos de Escala Intermediária Ruidosa',
    authors: ['David Lee', 'Anna Petrova', 'James Wilson'],
    publication_date: '2024-01-20',
    abstract: 'Demonstramos um esquema prático de correção de erros quânticos que funciona em dispositivos NISQ atuais. Nossa abordagem reduz as taxas de erro em uma ordem de magnitude enquanto requer menos qubits físicos do que métodos anteriores.',
    keywords: ['computação quântica', 'correção de erros', 'NISQ', 'qubits'],
    source_url: 'https://arxiv.org/abs/2401.00003',
    processing_status: 'completed',
    simplified_text: `
## Sobre o que é este artigo?

Computadores quânticos têm um grande problema: eles cometem erros. Este artigo apresenta uma nova maneira de **corrigir erros em computadores quânticos** sem precisar de muitos recursos extras.

## Entendendo Computadores Quânticos

Diferente de computadores normais que usam bits (0s e 1s), computadores quânticos usam **qubits** que podem ser 0, 1, ou ambos ao mesmo tempo. Isso lhes dá um poder incredível, mas também os torna muito frágeis.

## O Desafio

Informação quântica é facilmente perturbada por:
- Mudanças de temperatura
- Interferência eletromagnética
- Até raios cósmicos!

Essas perturbações causam erros nos cálculos.

## A Nova Abordagem

Os pesquisadores desenvolveram uma maneira inteligente de detectar e corrigir esses erros:

1. **Redundância**: Armazena informação quântica em múltiplos qubits
2. **Detecção de Erros**: Verifica continuamente por inconsistências
3. **Correção**: Corrige erros antes que causem problemas

## Por Que Isso Importa

Isso nos aproxima de **computadores quânticos práticos** que poderiam:
- Quebrar criptografia atual (exigindo novas medidas de segurança)
- Descobrir novos medicamentos mais rapidamente
- Resolver problemas de modelagem climática
- Otimizar logística complexa

## Conclusão

Estamos um passo mais perto de computadores quânticos confiáveis que podem resolver problemas além do alcance dos supercomputadores de hoje.
    `,
    created_at: '2024-01-20T09:15:00Z',
  },
  {
    id: 'arxiv-2401-00004',
    title: 'Busca de Arquitetura Neural para Computação de Borda: Modelos Eficientes para Dispositivos IoT',
    authors: ['Lisa Wang', 'Robert Taylor', 'Yuki Tanaka'],
    publication_date: '2024-01-22',
    abstract: 'Este artigo introduz um método automatizado para projetar redes neurais otimizadas para dispositivos de borda com recursos limitados. Nossa abordagem gera modelos que são 10x menores e 5x mais rápidos do que arquiteturas padrão, mantendo precisão comparável.',
    keywords: ['busca de arquitetura neural', 'computação de borda', 'IoT', 'compressão de modelo'],
    source_url: 'https://arxiv.org/abs/2401.00004',
    processing_status: 'completed',
    simplified_text: `
## Sobre o que é este artigo?

Esta pesquisa apresenta uma maneira de projetar automaticamente modelos de IA que podem rodar em dispositivos pequenos como smartwatches, câmeras de segurança e sensores — dispositivos com memória e poder de processamento limitados.

## O Desafio

A maioria dos modelos de IA poderosos são projetados para rodar em computadores massivos em data centers. Mas cada vez mais queremos IA em todos os lugares:
- Dispositivos domésticos inteligentes
- Monitores de saúde vestíveis
- Sensores industriais
- Drones agrícolas

## A Solução: Design Automatizado

Em vez de humanos projetarem manualmente modelos de IA menores, os pesquisadores criaram um sistema que:

1. **Explora**: Testa milhares de possíveis designs de modelo
2. **Avalia**: Mede velocidade, tamanho e precisão
3. **Otimiza**: Encontra o melhor equilíbrio para dispositivos específicos

## Resultados

Os modelos projetados automaticamente são:
- **10x menores**: Cabem na memória limitada do dispositivo
- **5x mais rápidos**: Respondem em tempo real
- **Quase tão precisos**: Apenas pequenas compensações de qualidade

## Aplicações Práticas

- **Saúde**: Monitoramento cardíaco contínuo no seu smartwatch
- **Agricultura**: Drones que detectam doenças em plantas
- **Segurança**: Câmeras que reconhecem rostos localmente (mais privado)
- **Indústria**: Sensores que preveem falhas de equipamentos

Isso traz capacidades de IA para dispositivos onde não era possível antes.
    `,
    created_at: '2024-01-22T16:45:00Z',
  },
];
