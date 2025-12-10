import { Link } from 'react-router-dom';
import { Layout } from '@/components/layout/Layout';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/contexts/AuthContext';
import { 
  BookOpen, 
  Sparkles, 
  Mail, 
  Users, 
  ArrowRight,
  Zap,
  Shield,
  Clock
} from 'lucide-react';

const features = [
  {
    icon: Sparkles,
    title: 'Conteúdo Simplificado por IA',
    description: 'Artigos complexos transformados em resumos acessíveis e fáceis de entender, adaptados ao seu nível de conhecimento.',
  },
  {
    icon: Clock,
    title: 'Atualizações Semanais',
    description: 'Mantenha-se atualizado com a coleta automatizada das últimas pesquisas em ciência da computação do arXiv.',
  },
  {
    icon: Mail,
    title: 'Newsletter Personalizada',
    description: 'Receba resumos de artigos selecionados diretamente na sua caixa de entrada com base em seus interesses.',
  },
  {
    icon: Users,
    title: 'Experiência Personalizada',
    description: 'Seja você um estudante, educador ou entusiasta, o conteúdo se adapta ao seu perfil.',
  },
];

// const stats = [
//   { value: '1,000+', label: 'Artigos Simplificados' },
//   { value: '50+', label: 'Tópicos de Pesquisa' },
//   { value: '10K+', label: 'Leitores Ativos' },
// ];

export default function Index() {
  const { isAuthenticated } = useAuth();

  return (
    <Layout>
      {/* Hero Section */}
      <section className="relative py-20 lg:py-32 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-secondary/50 to-transparent" />
        <div className="container relative">
          <div className="max-w-3xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-accent/10 text-accent text-sm font-medium mb-8 animate-fade-in">
              <Zap className="h-4 w-4" />
              Simplificação de Pesquisa com IA
            </div>
            
            <h1 className="font-serif text-4xl md:text-5xl lg:text-6xl font-bold text-foreground mb-6 animate-slide-up text-balance">
              Pesquisa de Ponta,{' '}
              <span className="text-accent">Feita Simples</span>
            </h1>
            
            <p className="text-lg md:text-xl text-muted-foreground mb-10 max-w-2xl mx-auto animate-slide-up" style={{ animationDelay: '0.1s' }}>
              SciNewsAI transforma artigos complexos de ciência da computação do arXiv em 
              resumos acessíveis. Mantenha-se informado sem o jargão acadêmico.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center animate-slide-up" style={{ animationDelay: '0.2s' }}>
              <Button variant="hero" asChild>
                <Link to="/auth?mode=signup">
                  Comece a Ler Gratuitamente
                  <ArrowRight className="h-5 w-5 ml-2" />
                </Link>
              </Button>
              <Button variant="hero-outline" asChild>
                <Link to="/auth?mode=login">
                  Entrar
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      {/* <section className="py-12 border-y border-border bg-card">
        <div className="container">
          <div className="grid grid-cols-3 gap-8 max-w-2xl mx-auto">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="font-serif text-2xl md:text-3xl font-bold text-foreground">
                  {stat.value}
                </div>
                <div className="text-sm text-muted-foreground mt-1">
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section> */}

      {/* Features Section */}
      <section className="py-20 lg:py-5">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="font-serif text-3xl md:text-4xl font-bold text-foreground mb-4">
              Como o SciNewsAI funciona
            </h2>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              Tornamos o estado da arte acessível a todos, 
              independentemente de seu background técnico.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div 
                key={index} 
                className="scholarly-card p-6 text-center"
              >
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-accent/10 text-accent mb-4">
                  <feature.icon className="h-6 w-6" />
                </div>
                <h3 className="font-serif text-lg font-semibold text-foreground mb-2">
                  {feature.title}
                </h3>
                <p className="text-sm text-muted-foreground">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-secondary/30">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <h2 className="font-serif text-3xl md:text-4xl font-bold text-foreground mb-12 text-center">
              Comece em Quatro Simples Passos
            </h2>

            <div className="space-y-8">
              {[
                {
                  step: '01',
                  title: 'Crie Seu Perfil',
                  description: 'Escolha seu nível de especialização — Estudante, Educador ou Entusiasta — e selecione os tópicos que lhe interessam.',
                },
                {
                  step: '02',
                  title: 'Navegue e Assine',
                  description: 'Explore nossa coleção selecionada de artigos simplificados ou assine tópicos de pesquisa específicos.',
                },
                {
                  step: '03',
                  title: 'Leia e Aprenda',
                  description: 'Desfrute de resumos simplificados por IA que correspondem ao seu nível de conhecimento, com links para os artigos originais.',
                },
                {
                  step: '04',
                  title: 'Mantenha-se Atualizado',
                  description: 'Receba newsletters semanais com as pesquisas mais recentes em suas áreas de interesse.',
                },
              ].map((item, index) => (
                <div key={index} className="flex gap-6 items-start">
                  <div className="flex-shrink-0 w-12 h-12 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-serif font-bold">
                    {item.step}
                  </div>
                  <div>
                    <h3 className="font-serif text-xl font-semibold text-foreground mb-2">
                      {item.title}
                    </h3>
                    <p className="text-muted-foreground">
                      {item.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 lg:py-28">
        <div className="container">
          <div className="max-w-3xl mx-auto text-center scholarly-card p-12">
            <BookOpen className="h-12 w-12 text-accent mx-auto mb-6" />
            <h2 className="font-serif text-3xl md:text-4xl font-bold text-foreground mb-4">
              Pronto para Explorar a Pesquisa?
            </h2>
            <p className="text-muted-foreground text-lg mb-8 max-w-xl mx-auto">
              Junte-se a milhares de mentes curiosas que se mantêm à frente com 
              os resumos simplificados de pesquisa do SciNewsAI.
            </p>
            <Button variant="hero" asChild>
              <Link to="/auth?mode=signup">
                Crie uma Conta Gratuita
                <ArrowRight className="h-5 w-5 ml-2" />
              </Link>
            </Button>
          </div>
        </div>
      </section>
    </Layout>
  );
}
