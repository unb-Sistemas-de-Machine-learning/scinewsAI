import { Link } from 'react-router-dom';
import { BookOpen } from 'lucide-react';

export function Footer() {
  return (
    <footer className="border-t border-border bg-secondary/30">
      <div className="container py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="md:col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <BookOpen className="h-6 w-6 text-accent" />
              <span className="font-serif text-xl font-semibold">SciNewsAI</span>
            </div>
            <p className="text-muted-foreground text-sm max-w-md">
              Simplificando pesquisas de ponta em ciência da computação para todos. 
              Mantenha-se informado com resumos de artigos gerados por IA entregues na sua caixa de entrada.
            </p>
          </div>

          {/* Links */}
          <div>
            <h4 className="font-serif font-semibold mb-4">Plataforma</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><Link to="/dashboard" className="hover:text-foreground transition-colors">Buscar Artigos</Link></li>
              <li><Link to="/topics" className="hover:text-foreground transition-colors">Tópicos</Link></li>
              <li><Link to="/auth?mode=signup" className="hover:text-foreground transition-colors">Inscrever-se</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="font-serif font-semibold mb-4">Recursos</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><a href="https://arxiv.org" target="_blank" rel="noopener noreferrer" className="hover:text-foreground transition-colors">arXiv</a></li>
              <li><Link to="/about" className="hover:text-foreground transition-colors">Sobre</Link></li>
              <li><Link to="/contact" className="hover:text-foreground transition-colors">Contato</Link></li>
            </ul>
          </div>
        </div>

        <div className="border-t border-border mt-8 pt-8 text-center text-sm text-muted-foreground">
          <p>&copy; {new Date().getFullYear()} SciNewsAI. Tornando a pesquisa acessível.</p>
        </div>
      </div>
    </footer>
  );
}
