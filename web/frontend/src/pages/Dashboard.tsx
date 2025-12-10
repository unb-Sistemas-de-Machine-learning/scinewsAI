import { useState, useEffect } from 'react';
import { Layout } from '@/components/layout/Layout';
import { ArticleCard } from '@/components/articles/ArticleCard';
import { SearchBar } from '@/components/search/SearchBar';
import { TopicBadge } from '@/components/topics/TopicBadge';
import { useAuth } from '@/contexts/AuthContext';
import { articlesApi, topicsApi, usersApi } from '@/lib/apiService';
import { Article, Topic } from '@/types';
import { Button } from '@/components/ui/button';
import { Link } from 'react-router-dom';
import { BookOpen, Compass, Bell, Loader2 } from 'lucide-react';
import { toast } from '@/hooks/use-toast';

export default function Dashboard() {
  const { user, setUser } = useAuth();
  const [articles, setArticles] = useState<Article[]>([]);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [filteredArticles, setFilteredArticles] = useState<Article[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTopicFilter, setSelectedTopicFilter] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const subscribedTopics = user?.subscribed_topics || [];

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        setError(null);
        const [articlesData, topicsData] = await Promise.all([
          articlesApi.getAll({ page: 1, page_size: 50 }),
          topicsApi.getAll(),
        ]);
        
        // Handle articles response - could be { articles: [], total, page, page_size } or array
        const articlesList = articlesData.articles || articlesData.items || articlesData || [];
        setArticles(Array.isArray(articlesList) ? articlesList : []);
        setTopics(Array.isArray(topicsData) ? topicsData : []);
      } catch (err: any) {
        console.error('Error loading data:', err);
        
        // Check if it's an auth error
        if (err?.response?.status === 401) {
          setError('Sua sessão expirou. Por favor, faça login novamente.');
        } else {
          setError('Erro ao carregar artigos. Tente novamente.');
        }
        
        toast({
          title: 'Erro',
          description: 'Falha ao carregar dados.',
          variant: 'destructive',
        });
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  useEffect(() => {
    let filtered = Array.isArray(articles) ? articles : [];

    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(
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
      // Find the topic object to get its description for better matching
      const selectedTopic = topics.find(t => t.slug === selectedTopicFilter);
      if (selectedTopic) {
        filtered = filtered.filter((article) => {
          // Match by topic name in keywords or description similarity
          const topicNameLower = selectedTopic.name.toLowerCase();
          const topicDescLower = selectedTopic.description?.toLowerCase() || '';
          
          return (
            article.keywords.some((k) => 
              k.toLowerCase().includes(selectedTopic.name.toLowerCase()) ||
              topicNameLower.includes(k.toLowerCase())
            ) ||
            article.title.toLowerCase().includes(topicNameLower) ||
            article.abstract.toLowerCase().includes(topicNameLower)
          );
        });
      }
    }

    setFilteredArticles(filtered);
  }, [searchQuery, selectedTopicFilter, articles, topics]);

  const handleSubscribeTopic = async (topicId: string) => {
    try {
      const updatedUser = await usersApi.subscribeTopic(topicId);
      setUser(updatedUser);
      toast({
        title: 'Inscrito!',
        description: 'Você agora receberá atualizações sobre este tópico.',
      });
    } catch (err: any) {
      console.error('Error subscribing to topic:', err);
      
      // Check if already subscribed
      if (err?.response?.status === 400) {
        toast({
          title: 'Já inscrito',
          description: 'Você já está inscrito neste tópico.',
          variant: 'destructive',
        });
      } else {
        const errorMsg = err?.response?.data?.detail || err?.message || 'Falha ao se inscrever no tópico.';
        toast({
          title: 'Erro',
          description: errorMsg,
          variant: 'destructive',
        });
      }
    }
  };

  const handleUnsubscribeTopic = async (topicId: string) => {
    try {
      const updatedUser = await usersApi.unsubscribeTopic(topicId);
      setUser(updatedUser);
      toast({
        title: 'Desinscrito!',
        description: 'Você não receberá mais atualizações sobre este tópico.',
      });
    } catch (err: any) {
      console.error('Error unsubscribing from topic:', err);
      const errorMsg = err?.response?.data?.detail || err?.message || 'Falha ao se desinscrever do tópico.';
      toast({
        title: 'Erro',
        description: errorMsg,
        variant: 'destructive',
      });
    }
  };

  const hasSubscriptions = subscribedTopics.length > 0;

  return (
    <Layout>
      <div className="container py-8 lg:py-12">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="font-serif text-3xl md:text-4xl font-bold text-foreground mb-2">
            Bem-vindo, {user?.name || 'Visitante'}
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
          <div className="space-y-3">
            {/* Separator Line */}
            <div className="flex items-center gap-3 pt-2">
              <div className="flex-1 h-0.5 bg-gradient-to-r from-accent to-transparent"></div>
              <span className="text-sm font-semibold text-accent whitespace-nowrap">Filtrar por Tópico</span>
              <div className="flex-1 h-0.5 bg-gradient-to-l from-accent to-transparent"></div>
            </div>
            
            <button
              onClick={() => setSelectedTopicFilter(null)}
              className={`topic-badge w-full ${!selectedTopicFilter ? 'subscribed' : ''}`}
            >
              Todos os tópicos
            </button>
            <div className="flex flex-wrap gap-2">
              {topics.map((topic) => (
                <button
                  key={topic.id}
                  onClick={() => setSelectedTopicFilter(topic.slug)}
                  className={`topic-badge ${selectedTopicFilter === topic.slug ? 'subscribed' : ''}`}
                  title={topic.description}
                >
                  {topic.name}
                </button>
              ))}
            </div>
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
                const topic = topics.find((t) => t.id === topicId);
                return topic ? (
                  <TopicBadge
                    key={topic.id}
                    name={topic.name}
                    isSubscribed={true}
                    onToggle={() => handleUnsubscribeTopic(topic.id)}
                  />
                ) : null;
              })}
            </div>
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
              {loading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                `${filteredArticles.length} artigo${filteredArticles.length !== 1 ? 's' : ''}`
              )}
            </span>
          </div>

          {loading ? (
            <div className="flex justify-center py-12">
              <Loader2 className="h-8 w-8 animate-spin text-accent" />
            </div>
          ) : error ? (
            <div className="text-center py-12">
              <p className="text-destructive">{error}</p>
            </div>
          ) : filteredArticles.length > 0 ? (
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
