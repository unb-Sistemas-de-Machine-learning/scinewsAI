import { useState, useMemo } from 'react';
import { Layout } from '@/components/layout/Layout';
import { ArticleCard } from '@/components/articles/ArticleCard';
import { SearchBar } from '@/components/search/SearchBar';
import { TopicBadge } from '@/components/topics/TopicBadge';
import { useAuth } from '@/contexts/AuthContext';
import { MOCK_ARTICLES, TOPICS } from '@/data/mockData';
import { Button } from '@/components/ui/button';
import { Link } from 'react-router-dom';
import { BookOpen, Compass, Bell } from 'lucide-react';

export default function Dashboard() {
  const { user, subscribeToTopic, unsubscribeFromTopic } = useAuth();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTopicFilter, setSelectedTopicFilter] = useState<string | null>(null);

  const subscribedTopics = user?.subscribed_topics || [];

  const filteredArticles = useMemo(() => {
    let articles = MOCK_ARTICLES;

    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      articles = articles.filter(
        (article) =>
          article.title.toLowerCase().includes(query) ||
          article.abstract.toLowerCase().includes(query) ||
          article.authors.some((author) =>
            author.toLowerCase().includes(query)
          ) ||
          article.keywords.some((keyword) =>
            keyword.toLowerCase().includes(query)
          )
      );
    }

    if (selectedTopicFilter) {
      // Mock filter - in real app, articles would have topic IDs
      articles = articles.filter((article) =>
        article.keywords.some((k) => k.toLowerCase().includes(selectedTopicFilter.toLowerCase()))
      );
    }

    return articles;
  }, [searchQuery, selectedTopicFilter]);

  const hasSubscriptions = subscribedTopics.length > 0;

  return (
    <Layout>
      <div className="container py-8 lg:py-12">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="font-serif text-3xl md:text-4xl font-bold text-foreground mb-2">
            Bem-vindo, {user?.name}
          </h1>
          <p className="text-muted-foreground">
            Descubra as últimas pesquisas em ciência da computação, simplificadas para você.
          </p>
        </div>

        {/* Search and Filters */}
        <div className="mb-8 space-y-4">
          <SearchBar
            onSearch={setSearchQuery}
            placeholder="Busque artigos por título, autor ou palavra-chave..."
          />

          {/* Topic Filter */}
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setSelectedTopicFilter(null)}
              className={`topic-badge ${!selectedTopicFilter ? 'subscribed' : ''}`}
            >
              Todos os tópicos
            </button>
            {TOPICS.slice(0, 5).map((topic) => (
              <button
                key={topic.id}
                onClick={() => setSelectedTopicFilter(topic.slug)}
                className={`topic-badge ${selectedTopicFilter === topic.slug ? 'subscribed' : ''}`}
              >
                {topic.name}
              </button>
            ))}
          </div>
        </div>

        {/* Subscribed Topics Section */}
        {hasSubscriptions && (
          <div className="mb-8 p-6 bg-secondary/50 rounded-lg border border-border">
            <div className="flex items-center gap-2 mb-4">
              <Bell className="h-5 w-5 text-accent" />
              <h2 className="font-serif text-lg font-semibold">Suas Inscrições</h2>
            </div>
            <div className="flex flex-wrap gap-2">
              {subscribedTopics.map((topicId) => {
                const topic = TOPICS.find((t) => t.id === topicId);
                return topic ? (
                  <TopicBadge
                    key={topic.id}
                    name={topic.name}
                    isSubscribed={true}
                    onToggle={() => unsubscribeFromTopic(topic.id)}
                  />
                ) : null;
              })}
            </div>
          </div>
        )}

        {/* Empty State */}
        {!hasSubscriptions && (
          <div className="mb-8 p-8 bg-secondary/30 rounded-lg border border-border text-center">
            <Compass className="h-12 w-12 text-accent mx-auto mb-4" />
            <h2 className="font-serif text-xl font-semibold mb-2">
              Explore Tópicos de Pesquisa
            </h2>
            <p className="text-muted-foreground mb-6 max-w-md mx-auto">
              Inscreva-se nos tópicos do seu interesse para receber recomendações personalizadas de artigos
              e atualizações semanais do boletim informativo.
            </p>
            <Button variant="scholarly" asChild>
              <Link to="/topics">
                Navegar por Tópicos
              </Link>
            </Button>
          </div>
        )}

        {/* Articles Grid */}
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="font-serif text-2xl font-semibold flex items-center gap-2">
              <BookOpen className="h-6 w-6 text-accent" />
              Últimos Artigos
            </h2>
            <span className="text-sm text-muted-foreground">
              {filteredArticles.length} artigo{filteredArticles.length !== 1 ? 's' : ''}
            </span>
          </div>

          {filteredArticles.length > 0 ? (
            <div className="grid md:grid-cols-2 gap-6">
              {filteredArticles.map((article) => (
                <ArticleCard key={article.id} article={article} />
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-muted-foreground">
                Nenhum artigo encontrado correspondente à sua pesquisa.
              </p>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}
