import { useState, useEffect } from 'react';
import { Layout } from '@/components/layout/Layout';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { toast } from '@/hooks/use-toast';
import { topicsApi, usersApi } from '@/lib/apiService';
import { Topic, ProfileType } from '@/types';
import { 
  User, 
  GraduationCap, 
  Briefcase, 
  Heart, 
  Save,
  Bell,
  Check,
  X,
  Loader2
} from 'lucide-react';

const profileTypes: { value: ProfileType; label: string; description: string; icon: React.ElementType }[] = [
  {
    value: 'student',
    label: 'Student',
    description: 'Learning and exploring the field',
    icon: GraduationCap,
  },
  {
    value: 'educator',
    label: 'Educator',
    description: 'Teaching and sharing knowledge',
    icon: Briefcase,
  },
  {
    value: 'enthusiast',
    label: 'Enthusiast',
    description: 'Curious about technology',
    icon: Heart,
  },
];

export default function Profile() {
  const { user, setUser } = useAuth();
  const [name, setName] = useState(user?.name || '');
  const [profileType, setProfileType] = useState<ProfileType>(user?.profile_type || 'student');
  const [isSaving, setIsSaving] = useState(false);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loadingTopics, setLoadingTopics] = useState(true);
  const [togglingTopics, setTogglingTopics] = useState<Set<string>>(new Set());

  const subscribedTopics = user?.subscribed_topics || [];
  const subscribedTopicObjects = topics.filter(t => subscribedTopics.includes(t.id));

  useEffect(() => {
    const loadTopics = async () => {
      try {
        setLoadingTopics(true);
        const data = await topicsApi.getAll();
        setTopics(data);
      } catch (err) {
        console.error('Error loading topics:', err);
        toast({
          title: 'Erro',
          description: 'Falha ao carregar tópicos.',
          variant: 'destructive',
        });
      } finally {
        setLoadingTopics(false);
      }
    };

    loadTopics();
  }, []);

  const handleSave = async () => {
    setIsSaving(true);
    try {
      await usersApi.update(user?.id || '', { name, profile_type: profileType });
      setUser({ ...user!, name, profile_type: profileType });
      toast({
        title: 'Perfil atualizado',
        description: 'Suas alterações foram salvas.',
      });
    } catch (err) {
      console.error('Error updating profile:', err);
      toast({
        title: 'Erro',
        description: 'Falha ao atualizar perfil.',
        variant: 'destructive',
      });
    } finally {
      setIsSaving(false);
    }
  };

  const handleTopicToggle = async (topicId: string, topicName: string) => {
    const isSubscribed = subscribedTopics.includes(topicId);
    
    try {
      setTogglingTopics((prev) => new Set(prev).add(topicId));
      
      let updatedUser;
      if (isSubscribed) {
        updatedUser = await usersApi.unsubscribeTopic(topicId);
        toast({
          title: 'Desinscrito!',
          description: `Você se desinscreveu de ${topicName}`,
        });
      } else {
        updatedUser = await usersApi.subscribeTopic(topicId);
        toast({
          title: 'Inscrito!',
          description: `Você agora receberá atualizações sobre ${topicName}`,
        });
      }
      
      setUser(updatedUser);
    } catch (err: any) {
      console.error('Error toggling topic subscription:', err);
      
      // If already subscribed error, just update the user state
      if (err?.response?.status === 400 && err?.response?.data?.detail === "Already subscribed to this topic") {
        try {
          const currentUser = await usersApi.getCurrentUser();
          setUser(currentUser);
          toast({
            title: 'Já inscrito',
            description: 'Você já está inscrito neste tópico.',
          });
        } catch (refreshErr) {
          console.error('Error refreshing user:', refreshErr);
        }
      } else {
        toast({
          title: 'Erro',
          description: 'Falha ao atualizar inscrição.',
          variant: 'destructive',
        });
      }
    } finally {
      setTogglingTopics((prev) => {
        const updated = new Set(prev);
        updated.delete(topicId);
        return updated;
      });
    }
  };

  return (
    <Layout>
      <div className="container py-8 lg:py-12">
        {/* Header */}
        <div className="flex items-center gap-3 mb-8">
          <div className="w-12 h-12 rounded-full bg-accent/10 flex items-center justify-center">
            <User className="h-6 w-6 text-accent" />
          </div>
          <div>
            <h1 className="font-serif text-2xl font-bold text-foreground">
              Configurações de Perfil
            </h1>
            <p className="text-muted-foreground">
              Gerencie sua conta e preferências
            </p>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Left Column - Profile Form */}
          <div>
            {/* Profile Form */}
            <div className="scholarly-card p-6">
            <h2 className="font-serif text-lg font-semibold mb-6">
              Informações Pessoais
            </h2>

            <div className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="name">Nome de Exibição</Label>
                <Input
                  id="name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Seu nome"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  value={user?.email || ''}
                  disabled
                  className="bg-muted"
                />
                <p className="text-xs text-muted-foreground">
                  O e-mail não pôde ser alterado
                </p>
              </div>

              <div className="space-y-3">
                <Label>Tipo de Perfil</Label>
                <p className="text-sm text-muted-foreground">
                  O tipo de perfil ajuda a personalizar o conteúdo de acordo com seu nível de expertise.
                </p>
                <RadioGroup
                  value={profileType}
                  onValueChange={(value: ProfileType) => setProfileType(value)}
                  className="grid grid-cols-1 gap-3"
                >
                  {profileTypes.map((type) => (
                    <label
                      key={type.value}
                      className={`flex items-center gap-4 p-4 rounded-lg border cursor-pointer transition-colors ${
                        profileType === type.value
                          ? 'border-accent bg-accent/5'
                          : 'border-border hover:border-muted-foreground/30'
                      }`}
                    >
                      <RadioGroupItem value={type.value} id={`profile-${type.value}`} />
                      <type.icon className="h-5 w-5 text-muted-foreground" />
                      <div>
                        <div className="font-medium">{type.label}</div>
                        <div className="text-sm text-muted-foreground">
                          {type.description}
                        </div>
                      </div>
                    </label>
                  ))}
                </RadioGroup>
              </div>

              <Button
                variant="scholarly"
                onClick={handleSave}
                disabled={isSaving}
              >
                <Save className="h-4 w-4 mr-2" />
                {isSaving ? 'Salvando...' : 'Salvar Alterações'}
              </Button>
            </div>
            </div>
          </div>

          {/* Right Column - Topic Subscriptions */}
          <div>
            {/* Topic Subscriptions */}
            <div className="scholarly-card p-6">
            <div className="flex items-center gap-2 mb-6">
              <Bell className="h-5 w-5 text-accent" />
              <h2 className="font-serif text-lg font-semibold">
                Seus Tópicos Inscritos
              </h2>
            </div>
            <p className="text-sm text-muted-foreground mb-6">
              Tópicos nos quais você está inscrito. Você receberá newsletters semanais
              sobre esses tópicos.
            </p>

            {loadingTopics ? (
              <div className="flex justify-center py-8">
                <Loader2 className="h-6 w-6 animate-spin text-accent" />
              </div>
            ) : subscribedTopicObjects.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-muted-foreground mb-4">
                  Você não está inscrito em nenhum tópico ainda.
                </p>
                <Button variant="scholarly" asChild>
                  <a href="/topics">Explorar Tópicos</a>
                </Button>
              </div>
            ) : (
              <div className="space-y-2">
                {subscribedTopicObjects.map((topic) => {
                  const isToggling = togglingTopics.has(topic.id);
                  return (
                    <button
                      key={topic.id}
                      onClick={() => handleTopicToggle(topic.id, topic.name)}
                      disabled={isToggling}
                      className={`w-full flex items-center justify-between p-4 rounded-lg border transition-colors text-left disabled:opacity-50 ${
                        'border-accent bg-accent/5'
                      }`}
                    >
                      <div>
                        <div className="font-medium text-sm">{topic.name}</div>
                      </div>
                      <div
                        className={`w-6 h-6 rounded-full flex items-center justify-center ${
                          isToggling ? '' : 'bg-accent text-accent-foreground'
                        }`}
                      >
                        {isToggling ? (
                          <Loader2 className="h-3 w-3 animate-spin" />
                        ) : (
                          <X className="h-3 w-3" />
                        )}
                      </div>
                    </button>
                  );
                })}
              </div>
            )}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
