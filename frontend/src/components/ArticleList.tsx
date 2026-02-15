import React, { useState, useEffect } from 'react';
import { getArticles, type Article } from '../services/apiService';
import { Eye, Calendar, FileText, Tag, Hash, RefreshCw } from 'lucide-react';

interface ArticleListProps {
  onViewArticle: (articleId: string) => void;
}

export const ArticleList: React.FC<ArticleListProps> = ({ onViewArticle }) => {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<string>('all');

  const fetchArticles = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await getArticles(filter === 'all' ? undefined : filter);
      if (result.success && result.data) {
        setArticles(result.data.articles);
      } else {
        setError(result.error || 'Failed to load articles');
      }
    } catch (err) {
      setError('Failed to connect to the server');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchArticles();
  }, [filter]);

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto bg-white rounded-lg shadow-lg p-6 border border-gray-200">
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p className="ml-4 text-gray-600">Loading articles...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-6xl mx-auto bg-white rounded-lg shadow-lg p-6 border border-gray-200">
        <div className="text-center py-12">
          <div className="w-16 h-16 mx-auto mb-4 bg-red-100 rounded-full flex items-center justify-center">
            <RefreshCw className="w-8 h-8 text-red-600" />
          </div>
          <p className="text-red-600 text-lg font-semibold mb-4">Error Loading Articles</p>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={fetchArticles}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors duration-200"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-lg p-6 border border-gray-200 mb-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Your Articles</h2>
            <p className="text-gray-600">
              {articles.length} article{articles.length !== 1 ? 's' : ''} generated
            </p>
          </div>
          
          <div className="mt-4 sm:mt-0">
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              className="w-full sm:w-auto px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-colors duration-200"
            >
              <option value="all">All Articles</option>
              <option value="custom">Custom Articles</option>
              <option value="quick">Quick Actions</option>
            </select>
          </div>
        </div>
      </div>

      {/* Articles Grid */}
      {articles.length === 0 ? (
        <div className="bg-white rounded-lg shadow-lg p-6 border border-gray-200 text-center py-12">
          <FileText className="w-16 h-16 mx-auto mb-4 text-gray-400" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No Articles Yet</h3>
          <p className="text-gray-600 mb-6">
            Generate your first article to get started!
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {articles.map((article) => (
            <div key={article.id} className="bg-white rounded-lg shadow-lg p-6 border border-gray-200 hover:shadow-xl transition-shadow duration-200">
              <div className="mb-4">
                <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
                  {article.title}
                </h3>
                <p className="text-gray-600 text-sm line-clamp-3">
                  {(article.excerpt || article.content?.slice(0, 150) || '').trim()}...
                </p>
              </div>
              
              <div className="space-y-2 mb-4">
                <div className="flex items-center text-sm text-gray-500">
                  <Tag className="w-4 h-4 mr-2" />
                  {article.topic}
                </div>
                <div className="flex items-center text-sm text-gray-500">
                  <FileText className="w-4 h-4 mr-2" />
                  {article.wordCount} words
                </div>
                <div className="flex items-center text-sm text-gray-500">
                  <Calendar className="w-4 h-4 mr-2" />
                  {new Date(article.createdAt).toLocaleDateString()}
                </div>
                <div className="flex items-center text-sm text-gray-500">
                  <Hash className="w-4 h-4 mr-2" />
                  {article.articleType}
                </div>
              </div>
              
              <button
                onClick={() => onViewArticle(article.id)}
                className="w-full bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors duration-200 flex items-center justify-center"
              >
                <Eye className="w-4 h-4 mr-2" />
                View Article
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
