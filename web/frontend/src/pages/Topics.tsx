import { Layout } from '@/components/layout/Layout';
import { useAuth } from '@/contexts/AuthContext';
import { TOPICS } from '@/data/mockData';
import { Check, Plus, BookMarked } from 'lucide-react';
import { toast } from '@/hooks/use-toast';

export default function Topics() {
  const { user, subscribeToTopic, unsubscribeFromTopic } = useAuth();
  const subscribedTopics = user?.subscribed_topics || [];

  const handleToggle = (topicId: string, topicName: string) => {
    const isSubscribed = subscribedTopics.includes(topicId);
    if (isSubscribed) {
      unsubscribeFromTopic(topicId);
      toast({
        title: 'Desinscrito!',
        description: `Você se desinscreveu de ${topicName}`,
      });
    } else {
      subscribeToTopic(topicId);
      toast({
        title: 'Inscrito!',
        description: `Você agora receberá atualizações sobre ${topicName}`,
      });
    }
  };

  return (
    <Layout>
      <div className="container py-8 lg:py-12">
        {/* Header */}
        <div className="max-w-2xl mb-12">
          <div className="flex items-center gap-3 mb-4">
            <BookMarked className="h-8 w-8 text-accent" />
            <h1 className="font-serif text-3xl md:text-4xl font-bold text-foreground">
              Tópicos de Pesquisa
            </h1>
          </div>
          <p className="text-muted-foreground text-lg">
            Inscreva-se nos tópicos do seu interesse. Você receberá recomendações personalizadas 
            de artigos e atualizações semanais por newsletter com base em suas seleções.
          </p>
        </div>

        {/* Subscribed Count */}
        <div className="mb-8 p-4 bg-accent/10 rounded-lg inline-flex items-center gap-3">
          <Check className="h-5 w-5 text-accent" />
            <span className="text-sm font-medium">
            Inscrito em {subscribedTopics.length} tópico{subscribedTopics.length !== 1 ? 's' : ''}
            </span>
        </div>

        {/* Topics Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {TOPICS.map((topic) => {
            const isSubscribed = subscribedTopics.includes(topic.id);
            return (
              <button
                key={topic.id}
                onClick={() => handleToggle(topic.id, topic.name)}
                className={`scholarly-card p-6 text-left transition-all ${
                  isSubscribed ? 'ring-2 ring-accent bg-accent/5' : ''
                }`}
              >
                <div className="flex items-start justify-between mb-3">
                  <h3 className="font-serif text-lg font-semibold text-foreground pr-4">
                    {topic.name}
                  </h3>
                  <div
                    className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center transition-colors ${
                      isSubscribed
                        ? 'bg-accent text-accent-foreground'
                        : 'bg-secondary text-muted-foreground'
                    }`}
                  >
                    {isSubscribed ? (
                      <Check className="h-4 w-4" />
                    ) : (
                      <Plus className="h-4 w-4" />
                    )}
                  </div>
                </div>
                <p className="text-sm text-muted-foreground mb-4">
                  {topic.description}
                </p>
                <div className="text-xs text-muted-foreground">
                  {topic.article_count} artigos
                </div>
              </button>
            );
          })}
        </div>
      </div>
    </Layout>
  );
}
