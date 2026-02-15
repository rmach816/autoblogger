import React, { useState, useEffect } from 'react';
import { getArticle, type Article } from '../services/apiService';
import { X, Calendar, FileText, Tag, Hash } from 'lucide-react';

interface ArticleViewerProps {
  articleId: string;
  onClose: () => void;
}

export const ArticleViewer: React.FC<ArticleViewerProps> = ({ articleId, onClose }) => {
  const [article, setArticle] = useState<Article | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchArticle = async () => {
      try {
        const result = await getArticle(articleId);
        if (result.success && result.data) {
          setArticle(result.data.article);
        } else {
          setError(result.error || 'Failed to load article');
        }
      } catch (err) {
        setError('Failed to connect to the server');
      } finally {
        setLoading(false);
      }
    };

    fetchArticle();
  }, [articleId]);

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-8 max-w-md mx-4">
          <div className="flex items-center justify-center mb-4">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
          <p className="text-center text-gray-600">Loading article...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-8 max-w-md mx-4">
          <div className="text-red-600 text-center">
            <div className="w-16 h-16 mx-auto mb-4 bg-red-100 rounded-full flex items-center justify-center">
              <X className="w-8 h-8" />
            </div>
            <p className="text-lg font-semibold mb-2">Error</p>
            <p className="mb-4">{error}</p>
            <button
              onClick={onClose}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors duration-200"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!article) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-6xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-gray-200 p-6 flex justify-between items-start">
          <div className="flex-1 pr-4">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{article.title}</h1>
            <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600">
              <div className="flex items-center">
                <Tag className="w-4 h-4 mr-1" />
                {article.topic}
              </div>
              <div className="flex items-center">
                <FileText className="w-4 h-4 mr-1" />
                {article.wordCount} words
              </div>
              <div className="flex items-center">
                <Calendar className="w-4 h-4 mr-1" />
                {new Date(article.createdAt).toLocaleDateString()}
              </div>
              <div className="flex items-center">
                <Hash className="w-4 h-4 mr-1" />
                {article.articleType}
              </div>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-3xl font-bold p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            X
          </button>
        </div>
        
        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6">
          {article.keywords && (
            <div className="bg-gray-50 p-4 rounded-lg mb-6">
              <h3 className="font-semibold text-gray-700 mb-2">Keywords:</h3>
              <p className="text-gray-600">{article.keywords}</p>
            </div>
          )}
          
          <div 
            className="prose prose-lg max-w-none prose-headings:text-gray-900 prose-p:text-gray-700 prose-strong:text-gray-900"
            dangerouslySetInnerHTML={{ 
              __html: (article.content ?? '').replace(/\n/g, '<br>') 
            }}
          />
        </div>
      </div>
    </div>
  );
};
