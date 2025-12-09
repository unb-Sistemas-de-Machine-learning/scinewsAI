export interface Article {
  id: string;
  title: string;
  authors: string[];
  publication_date: string;
  abstract: string;
  keywords: string[];
  full_text?: string;
  source_url: string;
  original_pdf_path?: string;
  processing_status: 'pending' | 'processing' | 'completed' | 'failed';
  simplified_text?: string;
  created_at: string;
}

export interface User {
  id: string;
  email: string;
  name: string;
  profile_type: 'student' | 'educator' | 'enthusiast';
  subscribed_topics: string[];
  created_at: string;
}

export interface Topic {
  id: string;
  name: string;
  description: string;
  slug: string;
  article_count: number;
}

export type ProfileType = 'student' | 'educator' | 'enthusiast';
