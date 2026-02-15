import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001/api';
const HEALTH_URL = `${API_BASE_URL}`.replace(/\/api\/?$/, '') + '/health';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds for AI generation
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface ArticleFormData {
  topic: string;
  keywords: string[];
  wordCount: number;
  articleType: 'custom' | 'quick';
}

export interface Article {
  id: string;
  title: string;
  content?: string;
  excerpt?: string;
  slug: string;
  topic: string;
  keywords: string;
  wordCount: number;
  articleType: string;
  status: string;
  createdAt: string;
  publishedAt: string;
  images?: any[];
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

const getErrorMessage = (error: unknown): string => {
  if (axios.isAxiosError(error)) {
    const data = error.response?.data as any;
    return data?.error || data?.message || error.message;
  }
  return error instanceof Error ? error.message : 'Request failed';
};

export const generateArticle = async (formData: ArticleFormData): Promise<ApiResponse<{ article: Partial<Article> }>> => {
  try {
    const response = await api.post('/generate-article', formData);
    return response.data;
  } catch (error) {
    console.error('Error generating article:', error);
    return {
      success: false,
      error: getErrorMessage(error)
    };
  }
};

export const getArticle = async (id: string): Promise<ApiResponse<{ article: Article }>> => {
  try {
    const response = await api.get(`/articles/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching article:', error);
    return {
      success: false,
      error: getErrorMessage(error)
    };
  }
};

export const getArticles = async (type?: string, limit = 20, offset = 0): Promise<ApiResponse<{ articles: Article[] }>> => {
  try {
    const params = new URLSearchParams();
    if (type) params.append('type', type);
    params.append('limit', limit.toString());
    params.append('offset', offset.toString());
    
    const response = await api.get(`/articles?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching articles:', error);
    return {
      success: false,
      error: getErrorMessage(error)
    };
  }
};

export const generateImage = async (prompt: string): Promise<ApiResponse<{ imageUrl: string }>> => {
  try {
    const response = await api.post('/generate-image', { prompt });
    return response.data;
  } catch (error) {
    console.error('Error generating image:', error);
    return {
      success: false,
      error: getErrorMessage(error)
    };
  }
};

export const checkHealth = async (): Promise<ApiResponse<{ status: string; version: string }>> => {
  try {
    const response = await axios.get(HEALTH_URL);
    return response.data;
  } catch (error) {
    console.error('Error checking health:', error);
    return {
      success: false,
      error: getErrorMessage(error)
    };
  }
};
