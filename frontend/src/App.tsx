import { useState, useEffect } from 'react';
import { ArticleGenerator } from './components/ArticleGenerator';
import { ArticleList } from './components/ArticleList';
import { ArticleViewer } from './components/ArticleViewer';
import { checkHealth } from './services/apiService';
import { Sparkles, FileText, AlertCircle, CheckCircle } from 'lucide-react';

type Tab = 'generate' | 'articles';

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('generate');
  const [selectedArticleId, setSelectedArticleId] = useState<string | null>(null);
  const [serverStatus, setServerStatus] = useState<'checking' | 'online' | 'offline'>('checking');

  useEffect(() => {
    const checkServerHealth = async () => {
      try {
        const result = await checkHealth();
        setServerStatus(result.success ? 'online' : 'offline');
      } catch {
        setServerStatus('offline');
      }
    };

    checkServerHealth();
  }, []);

  const handleViewArticle = (articleId: string) => {
    setSelectedArticleId(articleId);
  };

  const handleCloseArticle = () => {
    setSelectedArticleId(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <Sparkles className="w-8 h-8 text-blue-600 mr-3" />
              <h1 className="text-2xl font-bold text-gray-900">AutoBlogger</h1>
            </div>
            
            <div className="flex items-center space-x-4">
              {/* Server Status */}
              <div className="flex items-center">
                {serverStatus === 'checking' && (
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                )}
                {serverStatus === 'online' && (
                  <div className="flex items-center text-green-600">
                    <CheckCircle className="w-4 h-4 mr-1" />
                    <span className="text-sm">Online</span>
                  </div>
                )}
                {serverStatus === 'offline' && (
                  <div className="flex items-center text-red-600">
                    <AlertCircle className="w-4 h-4 mr-1" />
                    <span className="text-sm">Offline</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            <button
              onClick={() => setActiveTab('generate')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'generate'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <Sparkles className="w-4 h-4 inline mr-2" />
              Generate Article
            </button>
            <button
              onClick={() => setActiveTab('articles')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'articles'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <FileText className="w-4 h-4 inline mr-2" />
              My Articles
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {serverStatus === 'offline' && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center">
              <AlertCircle className="w-5 h-5 text-red-600 mr-2" />
              <p className="text-red-800">
                Server is offline. Please make sure the backend server is running on port 5001.
              </p>
            </div>
          </div>
        )}

        {activeTab === 'generate' && <ArticleGenerator />}
        {activeTab === 'articles' && <ArticleList onViewArticle={handleViewArticle} />}
      </main>

      {/* Article Viewer Modal */}
      {selectedArticleId && (
        <ArticleViewer
          articleId={selectedArticleId}
          onClose={handleCloseArticle}
        />
      )}

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-500">
            <p>&copy; 2025 AutoBlogger. AI-Powered Content Generation.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;