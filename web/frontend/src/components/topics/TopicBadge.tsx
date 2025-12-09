import { cn } from '@/lib/utils';
import { Check, Plus } from 'lucide-react';

interface TopicBadgeProps {
  name: string;
  isSubscribed: boolean;
  onToggle: () => void;
  showIcon?: boolean;
}

export function TopicBadge({ name, isSubscribed, onToggle, showIcon = true }: TopicBadgeProps) {
  return (
    <button
      onClick={onToggle}
      className={cn(
        'topic-badge',
        isSubscribed && 'subscribed'
      )}
    >
      {showIcon && (
        isSubscribed ? (
          <Check className="h-3 w-3 mr-1" />
        ) : (
          <Plus className="h-3 w-3 mr-1" />
        )
      )}
      {name}
    </button>
  );
}
