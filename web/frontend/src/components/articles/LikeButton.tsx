import { useState, useEffect } from 'react';
import { Heart } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { likesApi } from '@/lib/apiService';
import { toast } from '@/hooks/use-toast';

interface LikeButtonProps {
  articleId: string;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'default' | 'outline' | 'ghost';
}

export function LikeButton({ articleId, size = 'md', variant = 'outline' }: LikeButtonProps) {
  const [isLiked, setIsLiked] = useState(false);
  const [likeCount, setLikeCount] = useState(0);
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);

  // Load initial like status
  useEffect(() => {
    loadLikeStatus();
  }, [articleId]);

  const loadLikeStatus = async () => {
    try {
      setInitialLoading(true);
      const data = await likesApi.getStatus(articleId);
      setIsLiked(data.is_liked);
      setLikeCount(data.like_count);
    } catch (error) {
      console.error('Error loading like status:', error);
      // Try to load public count if not authenticated
      try {
        const data = await likesApi.getCount(articleId);
        setLikeCount(data.like_count);
      } catch (err) {
        console.error('Error loading like count:', err);
      }
    } finally {
      setInitialLoading(false);
    }
  };

  const handleToggleLike = async () => {
    if (initialLoading) return;

    try {
      setLoading(true);
      if (isLiked) {
        await likesApi.unlike(articleId);
        setIsLiked(false);
        setLikeCount((prev) => Math.max(0, prev - 1));
        toast({
          title: 'Sucesso',
          description: 'Você removeu a curtida',
        });
      } else {
        await likesApi.like(articleId);
        setIsLiked(true);
        setLikeCount((prev) => prev + 1);
        toast({
          title: 'Sucesso',
          description: 'Você curtiu este artigo!',
        });
      }
    } catch (error: any) {
      console.error('Error toggling like:', error);
      
      if (error.response?.status === 401) {
        toast({
          title: 'Autenticação necessária',
          description: 'Você precisa estar logado para curtir artigos',
          variant: 'destructive',
        });
      } else if (error.response?.status === 400) {
        // Already liked
        if (!isLiked) {
          setIsLiked(true);
          setLikeCount((prev) => prev + 1);
        }
      } else {
        toast({
          title: 'Erro',
          description: 'Falha ao processar curtida',
          variant: 'destructive',
        });
      }
    } finally {
      setLoading(false);
    }
  };

  const sizeClasses = {
    sm: 'h-8 px-2 text-sm gap-1',
    md: 'h-10 px-3 gap-2',
    lg: 'h-12 px-4 gap-2',
  };

  const iconSize = {
    sm: 16,
    md: 18,
    lg: 20,
  };

  return (
    <Button
      onClick={handleToggleLike}
      disabled={loading || initialLoading}
      variant={variant}
      className={`${sizeClasses[size]} ${
        isLiked
          ? 'text-red-500 border-red-500 hover:bg-red-50 dark:hover:bg-red-950'
          : ''
      }`}
    >
      <Heart
        size={iconSize[size]}
        fill={isLiked ? 'currentColor' : 'none'}
      />
      <span className="font-medium">{likeCount}</span>
    </Button>
  );
}
