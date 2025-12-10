import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Layout } from '@/components/layout/Layout';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { toast } from '@/hooks/use-toast';
import { BookOpen, GraduationCap, Briefcase, Heart, ArrowLeft } from 'lucide-react';
import { ProfileType } from '@/types';
import { z } from 'zod';

const loginSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(1, 'Password is required'),
});

const signupSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string(),
  profileType: z.enum(['student', 'educator', 'enthusiast']),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
});

const profileTypes: { value: ProfileType; label: string; description: string; icon: React.ElementType }[] = [
  {
    value: 'student',
    label: 'Estudante',
    description: 'Aprendendo e explorando o campo',
    icon: GraduationCap,
  },
  {
    value: 'educator',
    label: 'Educador',
    description: 'Ensinando e compartilhando conhecimento',
    icon: Briefcase,
  },
  {
    value: 'enthusiast',
    label: 'Entusiasta',
    description: 'Curioso sobre tecnologia',
    icon: Heart,
  },
];

export default function Auth() {
  const [searchParams] = useSearchParams();
  const mode = searchParams.get('mode') || 'login';
  const [isLogin, setIsLogin] = useState(mode === 'login');
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});
  
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    profileType: 'student' as ProfileType,
  });

  const { login, signup, isAuthenticated, isLoading: authLoading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    setIsLogin(mode === 'login');
  }, [mode]);

  // Redirect to dashboard if already authenticated
  useEffect(() => {
    if (isAuthenticated && !authLoading) {
      navigate('/dashboard', { replace: true });
    }
  }, [isAuthenticated, authLoading, navigate]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    // Clear error when user starts typing
    if (errors[e.target.name]) {
      setErrors({ ...errors, [e.target.name]: '' });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});
    setIsLoading(true);

    try {
      if (isLogin) {
        const validation = loginSchema.safeParse(formData);
        if (!validation.success) {
          const fieldErrors: Record<string, string> = {};
          validation.error.errors.forEach((err) => {
            if (err.path[0]) {
              fieldErrors[err.path[0] as string] = err.message;
            }
          });
          setErrors(fieldErrors);
          setIsLoading(false);
          return;
        }

        const result = await login(formData.email, formData.password);
        if (result.success) {
          toast({
            title: 'Bem-vindo!',
            description: 'Você entrou com sucesso!.',
          });
          navigate('/dashboard');
        } else {
          toast({
            title: 'Falha no login',
            description: result.error || 'Por favor, verifique suas credenciais.',
            variant: 'destructive',
          });
        }
      } else {
        const validation = signupSchema.safeParse(formData);
        if (!validation.success) {
          const fieldErrors: Record<string, string> = {};
          validation.error.errors.forEach((err) => {
            if (err.path[0]) {
              fieldErrors[err.path[0] as string] = err.message;
            }
          });
          setErrors(fieldErrors);
          setIsLoading(false);
          return;
        }

        const result = await signup(
          formData.email,
          formData.password,
          formData.name,
          formData.profileType
        );
        if (result.success) {
          toast({
            title: 'Conta criada!',
            description: 'Bem-vindo ao SciNewsAI.',
          });
          navigate('/dashboard');
        } else {
          toast({
            title: 'Falha no cadastro',
            description: result.error || 'Por favor, tente novamente.',
            variant: 'destructive',
          });
        }
      }
    } catch (error) {
      toast({
        title: 'Erro!',
        description: 'Ocorreu um erro inesperado.',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Layout showFooter={false}>
      <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center py-12 px-4">
        <div className="w-full max-w-md">
          <div className="text-center mb-8">
            <Link to="/" className="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground mb-6">
              <ArrowLeft className="h-4 w-4" />
              Voltar
            </Link>
            <div className="flex items-center justify-center gap-2 mb-4">
              <BookOpen className="h-8 w-8 text-accent" />
              <span className="font-serif text-2xl font-bold">SciNewsAI</span>
            </div>
            <h1 className="font-serif text-2xl font-bold text-foreground">
              {isLogin ? 'Bem-vindo!' : 'Crie sua conta'}
            </h1>
            <p className="text-muted-foreground mt-2">
              {isLogin
                ? 'Faça login para acessar seu feed de pesquisas personalizado'
                : 'Explore diversas pesquisas simplificadas!'}
            </p>
          </div>

          <div className="scholarly-card p-8">
            <form onSubmit={handleSubmit} className="space-y-6">
              {!isLogin && (
                <div className="space-y-2">
                  <Label htmlFor="name">Nome Completo</Label>
                  <Input
                    id="name"
                    name="name"
                    placeholder="Seu nome"
                    value={formData.name}
                    onChange={handleChange}
                  />
                  {errors.name && (
                    <p className="text-sm text-destructive">{errors.name}</p>
                  )}
                </div>
              )}

              <div className="space-y-2">
                <Label htmlFor="email">E-mail</Label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  placeholder="exemplo@email.com"
                  value={formData.email}
                  onChange={handleChange}
                />
                {errors.email && (
                  <p className="text-sm text-destructive">{errors.email}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="password">Senha</Label>
                <Input
                  id="password"
                  name="password"
                  type="password"
                  placeholder="••••••••"
                  value={formData.password}
                  onChange={handleChange}
                />
                {errors.password && (
                  <p className="text-sm text-destructive">{errors.password}</p>
                )}
              </div>

              {!isLogin && (
                <>
                  <div className="space-y-2">
                    <Label htmlFor="confirmPassword">Confirmar Senha</Label>
                    <Input
                      id="confirmPassword"
                      name="confirmPassword"
                      type="password"
                      placeholder="••••••••"
                      value={formData.confirmPassword}
                      onChange={handleChange}
                    />
                    {errors.confirmPassword && (
                      <p className="text-sm text-destructive">{errors.confirmPassword}</p>
                    )}
                  </div>

                  <div className="space-y-3">
                    <Label>Eu sou um...</Label>
                    <RadioGroup
                      value={formData.profileType}
                      onValueChange={(value: ProfileType) =>
                        setFormData({ ...formData, profileType: value })
                      }
                      className="grid grid-cols-1 gap-3"
                    >
                      {profileTypes.map((type) => (
                        <label
                          key={type.value}
                          className={`flex items-center gap-4 p-4 rounded-lg border cursor-pointer transition-colors ${
                            formData.profileType === type.value
                              ? 'border-accent bg-accent/5'
                              : 'border-border hover:border-muted-foreground/30'
                          }`}
                        >
                          <RadioGroupItem value={type.value} id={type.value} />
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
                </>
              )}

              <Button
                type="submit"
                variant="scholarly"
                className="w-full"
                disabled={isLoading}
              >
                {isLoading
                  ? 'Por favor, aguarde...'
                  : isLogin
                  ? 'Entrar'
                  : 'Criar Conta'}
              </Button>
            </form>

            <div className="mt-6 text-center text-sm text-muted-foreground">
              {isLogin ? (
                <>
                  Não tem uma conta?{' '}
                  <Link
                    to="/auth?mode=signup"
                    className="text-accent hover:underline font-medium"
                  >
                    Criar Conta
                  </Link>
                </>
              ) : (
                <>
                  Já tem uma conta?{' '}
                  <Link
                    to="/auth?mode=login"
                    className="text-accent hover:underline font-medium"
                  >
                    Entrar
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
