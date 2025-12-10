import { useParams, Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { Layout } from '@/components/layout/Layout';
import { articlesApi } from '@/lib/apiService';
import { Article as ArticleType } from '@/types';
import { Button } from '@/components/ui/button';
import { LikeButton } from '@/components/articles/LikeButton';
import { 
  ArrowLeft, 
  Calendar, 
  Users, 
  ExternalLink, 
  Tag,
  Share2,
  Bookmark,
  Loader2
} from 'lucide-react';
import { format } from 'date-fns';
import { toast } from '@/hooks/use-toast';

export default function Article() {
  const { id } = useParams<{ id: string }>();
  const [article, setArticle] = useState<ArticleType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadArticle = async () => {
      if (!id) return;
      
      try {
        setLoading(true);
        const data = await articlesApi.getById(id);
        setArticle(data);
        setError(null);
      } catch (err) {
        console.error('Error loading article:', err);
        setError('Erro ao carregar artigo. Tente novamente.');
        toast({
          title: 'Erro',
          description: 'Falha ao carregar artigo.',
          variant: 'destructive',
        });
      } finally {
        setLoading(false);
      }
    };

    loadArticle();
  }, [id]);

  if (loading) {
    return (
      <Layout>
        <div className="container py-16 flex justify-center">
          <Loader2 className="h-8 w-8 animate-spin text-accent" />
        </div>
      </Layout>
    );
  }

  if (error || !article) {
    return (
      <Layout>
        <div className="container py-16 text-center">
          <h1 className="font-serif text-2xl font-bold mb-4">Artigo não encontrado</h1>
          <p className="text-muted-foreground mb-8">
            {error || 'O artigo que você está procurando não existe.'}
          </p>
          <Button variant="scholarly" asChild>
            <Link to="/dashboard">Voltar para artigos</Link>
          </Button>
        </div>
      </Layout>
    );
  }

  const handleShare = async () => {
    try {
      await navigator.share({
        title: article.title,
        url: window.location.href,
      });
    } catch {
      navigator.clipboard.writeText(window.location.href);
      toast({
        title: 'Link copiado!',
        description: 'O link do artigo foi copiado para a área de transferência.',
      });
    }
  };

  const handleBookmark = () => {
    toast({
      title: 'Artigo salvo!',
      description: 'Este artigo foi adicionado à sua lista de leitura.',
    });
  };

  return (
    <Layout>
      <article className="container py-8 lg:py-12">
        {/* Botão Voltar */}
        <Link
          to="/dashboard"
          className="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground mb-8 transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          Voltar para artigos
        </Link>

        {/* Cabeçalho do Artigo */}
        <header className="max-w-3xl mb-12">
          <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground mb-4">
            <span className="flex items-center gap-1">
              <Calendar className="h-4 w-4" />
              {format(new Date(article.publication_date), 'dd/MM/yyyy')}
            </span>
            <span className="flex items-center gap-1">
              <Users className="h-4 w-4" />
              {article.authors.length} autor{article.authors.length !== 1 ? 'es' : ''}
            </span>
          </div>

          <h1 className="font-serif text-3xl md:text-4xl lg:text-5xl font-bold text-foreground mb-6 text-balance">
            {article.title}
          </h1>

          <div className="flex flex-wrap gap-2 mb-6">
            {article.keywords.map((keyword) => (
              <span
                key={keyword}
                className="inline-flex items-center gap-1 px-3 py-1 bg-secondary text-secondary-foreground rounded-full text-sm"
              >
                <Tag className="h-3 w-3" />
                {keyword}
              </span>
            ))}
          </div>

          <div className="mb-6">
            <h3 className="text-sm font-medium text-muted-foreground mb-2">Autores</h3>
            <p className="text-foreground">{article.authors.join(', ')}</p>
          </div>

          <div className="flex flex-wrap gap-4">
            <LikeButton articleId={article.id} size="md" />
            <Button variant="outline" size="sm" onClick={handleShare}>
              <Share2 className="h-4 w-4 mr-2" />
              Compartilhar
            </Button>
            <Button variant="outline" size="sm" onClick={handleBookmark}>
              <Bookmark className="h-4 w-4 mr-2" />
              Salvar
            </Button>
            <Button variant="accent" size="sm" asChild>
              <a href={article.source_url} target="_blank" rel="noopener noreferrer">
                <ExternalLink className="h-4 w-4 mr-2" />
                Ver original no arXiv
              </a>
            </Button>
          </div>
        </header>

        {/* Abstrato Original */}
        <section className="max-w-3xl mb-12 p-6 bg-secondary/30 rounded-lg border border-border">
          <h2 className="font-serif text-lg font-semibold mb-3 text-muted-foreground">
            Abstrato Original
          </h2>
          <p className="text-foreground/80 italic leading-relaxed">
            {article.abstract}
          </p>
        </section>

        {/* Versão Simplificada */}
        {article.simplified_text && (
          <section className="max-w-3xl">
            <div className="flex items-center gap-2 mb-6">
              <div className="h-1 w-12 bg-accent rounded" />
              <h2 className="font-serif text-2xl font-semibold text-foreground">
                Explicação Simplificada
              </h2>
            </div>
            <div className="article-prose prose prose-lg max-w-none text-foreground">
              {article.simplified_text.split('\n').map((paragraph, index) => {
                if (paragraph.startsWith('## ')) {
                  return (
                    <h2 key={index} className="font-serif text-xl font-semibold mt-8 mb-4 text-foreground">
                      {paragraph.replace('## ', '')}
                    </h2>
                  );
                }
                if (paragraph.startsWith('**') && paragraph.endsWith('**')) {
                  return (
                    <p key={index} className="font-semibold text-foreground">
                      {paragraph.replace(/\*\*/g, '')}
                    </p>
                  );
                }
                if (paragraph.startsWith('- ')) {
                  return (
                    <li key={index} className="ml-4 text-foreground/90">
                      {paragraph.replace('- ', '')}
                    </li>
                  );
                }
                if (paragraph.match(/^\d+\./)) {
                  return (
                    <li key={index} className="ml-4 list-decimal text-foreground/90">
                      {paragraph.replace(/^\d+\.\s*/, '')}
                    </li>
                  );
                }
                if (paragraph.trim()) {
                  // Handle inline bold text
                  const parts = paragraph.split(/(\*\*[^*]+\*\*)/);
                  return (
                    <p key={index} className="text-foreground/90">
                      {parts.map((part, i) => {
                        if (part.startsWith('**') && part.endsWith('**')) {
                          return (
                            <strong key={i} className="text-foreground font-semibold">
                              {part.replace(/\*\*/g, '')}
                            </strong>
                          );
                        }
                        return part;
                      })}
                    </p>
                  );
                }
                return null;
              })}
            </div>
          </section>
        )}

        {/* Navegação */}
        <div className="max-w-3xl mt-12 pt-8 border-t border-border">
          <Button variant="outline" asChild>
            <Link to="/dashboard">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Voltar para artigos
            </Link>
          </Button>
        </div>
      </article>
    </Layout>
  );
}
