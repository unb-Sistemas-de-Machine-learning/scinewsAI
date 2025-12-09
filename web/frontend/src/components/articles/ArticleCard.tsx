import { Link } from 'react-router-dom';
import { Article } from '@/types';
import { Calendar, Users, ArrowRight } from 'lucide-react';
import { format } from 'date-fns';

interface ArticleCardProps {
  article: Article;
}

export function ArticleCard({ article }: ArticleCardProps) {
  return (
    <Link to={`/article/${article.id}`} className="block">
      <article className="scholarly-card p-6 h-full flex flex-col">
        <div className="flex-1">
          <div className="flex items-center gap-4 text-sm text-muted-foreground mb-3">
            <span className="flex items-center gap-1">
              <Calendar className="h-4 w-4" />
                {format(new Date(article.publication_date), 'dd/MM/yyyy')}
            </span>
            <span className="flex items-center gap-1">
              <Users className="h-4 w-4" />
              {article.authors.length} autor{article.authors.length !== 1 ? 'es' : ''}
            </span>
          </div>

          <h3 className="font-serif text-lg font-semibold text-foreground mb-2 line-clamp-2 group-hover:text-accent transition-colors">
            {article.title}
          </h3>

          <p className="text-sm text-muted-foreground mb-3">
            {article.authors.slice(0, 3).join(', ')}
            {article.authors.length > 3 && ` +${article.authors.length - 3} more`}
          </p>

          <p className="text-sm text-muted-foreground line-clamp-3">
            {article.abstract}
          </p>
        </div>

        <div className="flex items-center gap-2 mt-4 pt-4 border-t border-border text-accent font-medium text-sm">
          Leia a versão simplificada
          <ArrowRight className="h-4 w-4" />
        </div>
      </article>
    </Link>
  );
}
