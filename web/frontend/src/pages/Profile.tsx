import { useState } from 'react';
import { Layout } from '@/components/layout/Layout';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { toast } from '@/hooks/use-toast';
import { TOPICS } from '@/data/mockData';
import { ProfileType } from '@/types';
import { 
  User, 
  GraduationCap, 
  Briefcase, 
  Heart, 
  Save,
  Bell,
  Check,
  X
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
  const { user, updateProfile, subscribeToTopic, unsubscribeFromTopic } = useAuth();
  const [name, setName] = useState(user?.name || '');
  const [profileType, setProfileType] = useState<ProfileType>(user?.profile_type || 'student');
  const [isSaving, setIsSaving] = useState(false);

  const subscribedTopics = user?.subscribed_topics || [];

  const handleSave = async () => {
    setIsSaving(true);
    await new Promise((resolve) => setTimeout(resolve, 500));
    updateProfile({ name, profile_type: profileType });
    toast({
      title: 'Perfil atualizado',
      description: 'Suas alterações foram salvas.',
    });
    setIsSaving(false);
  };

  const handleTopicToggle = (topicId: string) => {
    if (subscribedTopics.includes(topicId)) {
      unsubscribeFromTopic(topicId);
    } else {
      subscribeToTopic(topicId);
    }
  };

  return (
    <Layout>
      <div className="container py-8 lg:py-12">
        <div className="max-w-2xl">
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

          {/* Profile Form */}
          <div className="scholarly-card p-6 mb-8">
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

          {/* Topic Subscriptions */}
          <div className="scholarly-card p-6">
            <div className="flex items-center gap-2 mb-6">
              <Bell className="h-5 w-5 text-accent" />
              <h2 className="font-serif text-lg font-semibold">
                Inscrições em Tópicos
              </h2>
            </div>
            <p className="text-sm text-muted-foreground mb-6">
              Gerencie suas inscrições em tópicos. Você receberá newsletters semanais
              sobre esses tópicos.
            </p>

            <div className="space-y-2">
              {TOPICS.map((topic) => {
                const isSubscribed = subscribedTopics.includes(topic.id);
                return (
                  <button
                    key={topic.id}
                    onClick={() => handleTopicToggle(topic.id)}
                    className={`w-full flex items-center justify-between p-4 rounded-lg border transition-colors text-left ${
                      isSubscribed
                        ? 'border-accent bg-accent/5'
                        : 'border-border hover:border-muted-foreground/30'
                    }`}
                  >
                    <div>
                      <div className="font-medium text-sm">{topic.name}</div>
                      <div className="text-xs text-muted-foreground">
                        {topic.article_count} artigos
                      </div>
                    </div>
                    <div
                      className={`w-6 h-6 rounded-full flex items-center justify-center ${
                        isSubscribed
                          ? 'bg-accent text-accent-foreground'
                          : 'bg-muted text-muted-foreground'
                      }`}
                    >
                      {isSubscribed ? (
                        <Check className="h-3 w-3" />
                      ) : (
                        <X className="h-3 w-3" />
                      )}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
