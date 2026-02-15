import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import axios from 'axios';
import { 
  Home, 
  FileText, 
  Settings, 
  Plus, 
  Zap, 
  Eye, 
  Trash2,
  Calendar,
  Hash,
  Target
} from 'lucide-react';

// API Configuration
const API_BASE = 'http://localhost:5001/api';

// Custom Hook for API calls
const useAPI = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const apiCall = async (method, url, data = null) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios({
        method,
        url: `${API_BASE}${url}`,
        data,
        headers: {
          'Content-Type': 'application/json',
        },
      });
      return response.data;
    } catch (err) {
      setError(err.response?.data?.error || err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { apiCall, loading, error };
};

// Dashboard Component
const Dashboard = () => {
  const [articles, setArticles] = useState([]);
  const [stats, setStats] = useState({ total: 0, custom: 0, quick: 0 });
  const { apiCall, loading, error } = useAPI();

  useEffect(() => {
    fetchArticles();
  }, []);

  const fetchArticles = async () => {
    try {
      const data = await apiCall('GET', '/articles?limit=10');
      setArticles(data.articles);
      
      // Calculate stats
      const total = data.articles.length;
      const custom = data.articles.filter(a => a.articleType === 'custom').length;
      const quick = data.articles.filter(a => a.articleType === 'quick').length;
      setStats({ total, custom, quick });
    } catch (err) {
      console.error('Failed to fetch articles:', err);
    }
  };

  return (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">AutoBlogger Dashboard</h1>
        <p className="text-gray-600">AI-powered blog automation for Houston technology companies</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-md border">
          <div className="flex items-center">
            <FileText className="h-8 w-8 text-blue-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Articles</p>
              <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md border">
          <div className="flex items-center">
            <Plus className="h-8 w-8 text-green-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Custom Articles</p>
              <p className="text-2xl font-bold text-gray-900">{stats.custom}</p>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md border">
          <div className="flex items-center">
            <Zap className="h-8 w-8 text-purple-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Quick Articles</p>
              <p className="text-2xl font-bold text-gray-900">{stats.quick}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Articles */}
      <div className="bg-white rounded-lg shadow-md border">
        <div className="px-6 py-4 border-b">
          <h2 className="text-xl font-semibold text-gray-900">Recent Articles</h2>
        </div>
        <div className="divide-y">
          {articles.map((article) => (
            <div key={article.id} className="px-6 py-4 hover:bg-gray-50">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <h3 className="text-lg font-medium text-gray-900">{article.title}</h3>
                  <div className="mt-1 flex items-center space-x-4 text-sm text-gray-500">
                    <span className="flex items-center">
                      <Hash className="h-4 w-4 mr-1" />
                      {article.wordCount} words
                    </span>
                    <span className="flex items-center">
                      <Calendar className="h-4 w-4 mr-1" />
                      {new Date(article.createdAt).toLocaleDateString()}
                    </span>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      article.articleType === 'custom' 
                        ? 'bg-blue-100 text-blue-800' 
                        : 'bg-purple-100 text-purple-800'
                    }`}>
                      {article.articleType}
                    </span>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <Link
                    to={`/articles/${article.slug}`}
                    className="p-2 text-gray-400 hover:text-blue-600"
                  >
                    <Eye className="h-4 w-4" />
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// Custom Generator Component
const CustomGenerator = () => {
  const [formData, setFormData] = useState({
    topic: '',
    keywords: '',
    wordCount: 1200,
    articleType: 'custom'
  });
  const [generating, setGenerating] = useState(false);
  const [result, setResult] = useState(null);
  const { apiCall, loading, error } = useAPI();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setGenerating(true);
    setResult(null);

    try {
      const data = await apiCall('POST', '/generate-article', formData);
      setResult(data);
      // Reset form
      setFormData({
        topic: '',
        keywords: '',
        wordCount: 1200,
        articleType: 'custom'
      });
    } catch (err) {
      console.error('Failed to generate article:', err);
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Custom Article Generator</h1>
        <p className="text-gray-600">Generate personalized articles for your Houston technology business</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Form */}
        <div className="bg-white rounded-lg shadow-md border p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Article Configuration</h2>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Article Topic *
              </label>
              <input
                type="text"
                required
                value={formData.topic}
                onChange={(e) => setFormData({...formData, topic: e.target.value})}
                placeholder="e.g., Smart Home Security Systems for Houston Homes"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Keywords (comma-separated)
              </label>
              <input
                type="text"
                value={formData.keywords}
                onChange={(e) => setFormData({...formData, keywords: e.target.value})}
                placeholder="smart home, automation, Houston, security"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Word Count
              </label>
              <select
                value={formData.wordCount}
                onChange={(e) => setFormData({...formData, wordCount: parseInt(e.target.value)})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value={800}>800 words (Quick read)</option>
                <option value={1200}>1200 words (Standard)</option>
                <option value={1500}>1500 words (Comprehensive)</option>
                <option value={2000}>2000 words (In-depth)</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={generating || loading}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {generating ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Generating Article...
                </>
              ) : (
                <>
                  <Plus className="h-4 w-4 mr-2" />
                  Generate Custom Article
                </>
              )}
            </button>
          </form>

          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-md">
              <p className="text-red-800">{error}</p>
            </div>
          )}
        </div>

        {/* Results */}
        <div className="bg-white rounded-lg shadow-md border p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Generation Results</h2>
          
          {result ? (
            <div className="space-y-4">
              <div className="p-4 bg-green-50 border border-green-200 rounded-md">
                <h3 className="font-medium text-green-800">Article Generated Successfully!</h3>
                <p className="text-green-700 mt-1">{result.article.title}</p>
              </div>
              
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-600">Word Count:</span>
                  <span className="font-medium">{result.article.wordCount}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Created:</span>
                  <span className="font-medium">{new Date(result.article.createdAt).toLocaleString()}</span>
                </div>
              </div>

              <div className="pt-4">
                <Link
                  to={`/articles/${result.article.slug}`}
                  className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  <Eye className="h-4 w-4 mr-2" />
                  View Article
                </Link>
              </div>
            </div>
          ) : (
            <div className="text-center text-gray-500 py-8">
              <FileText className="h-12 w-12 mx-auto mb-4 text-gray-300" />
              <p>Generate an article to see results here</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// Quick Actions Component
const QuickActions = () => {
  const [generating, setGenerating] = useState(false);
  const [results, setResults] = useState([]);
  const { apiCall, loading, error } = useAPI();

  const quickTopics = [
    {
      title: "Smart Home Automation Solutions",
      keywords: "smart home, automation, Houston, voice control, energy efficiency",
      wordCount: 1200
    },
    {
      title: "Professional Home Theater Installation",
      keywords: "home theater, AV installation, Houston, 4K, surround sound",
      wordCount: 1000
    },
    {
      title: "Business Networking Solutions",
      keywords: "business networking, WiFi, LAN, Houston, corporate solutions",
      wordCount: 1100
    },
    {
      title: "Smart Security Systems",
      keywords: "home security, surveillance, Houston, smart cameras, protection",
      wordCount: 1000
    },
    {
      title: "Lighting Control Systems",
      keywords: "smart lighting, LED, dimming, Houston, energy efficient",
      wordCount: 900
    }
  ];

  const generateQuickArticle = async (topic) => {
    setGenerating(true);
    try {
      const data = await apiCall('POST', '/generate-article', {
        topic: topic.title,
        keywords: topic.keywords,
        wordCount: topic.wordCount,
        articleType: 'quick'
      });
      setResults(prev => [data.article, ...prev]);
    } catch (err) {
      console.error('Failed to generate quick article:', err);
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Quick Actions</h1>
        <p className="text-gray-600">Generate articles instantly with pre-configured topics</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {quickTopics.map((topic, index) => (
          <div key={index} className="bg-white rounded-lg shadow-md border p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">{topic.title}</h3>
            <p className="text-sm text-gray-600 mb-4">{topic.keywords}</p>
            <button
              onClick={() => generateQuickArticle(topic)}
              disabled={generating}
              className="w-full bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {generating ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Generating...
                </>
              ) : (
                <>
                  <Zap className="h-4 w-4 mr-2" />
                  Generate Article
                </>
              )}
            </button>
          </div>
        ))}
      </div>

      {/* Results */}
      {results.length > 0 && (
        <div className="bg-white rounded-lg shadow-md border">
          <div className="px-6 py-4 border-b">
            <h2 className="text-xl font-semibold text-gray-900">Generated Articles</h2>
          </div>
          <div className="divide-y">
            {results.map((article) => (
              <div key={article.id} className="px-6 py-4">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <h3 className="text-lg font-medium text-gray-900">{article.title}</h3>
                    <div className="mt-1 flex items-center space-x-4 text-sm text-gray-500">
                      <span>{article.wordCount} words</span>
                      <span>{new Date(article.createdAt).toLocaleString()}</span>
                    </div>
                  </div>
                  <Link
                    to={`/articles/${article.slug}`}
                    className="p-2 text-gray-400 hover:text-blue-600"
                  >
                    <Eye className="h-4 w-4" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// Article Viewer Component
const ArticleViewer = ({ match }) => {
  const [article, setArticle] = useState(null);
  const [loading, setLoading] = useState(true);
  const { apiCall, error } = useAPI();

  useEffect(() => {
    fetchArticle();
  }, [match.params.slug]);

  const fetchArticle = async () => {
    try {
      const data = await apiCall('GET', `/articles/${match.params.slug}`);
      setArticle(data.article);
    } catch (err) {
      console.error('Failed to fetch article:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-3/4 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2 mb-8"></div>
          <div className="space-y-4">
            <div className="h-4 bg-gray-200 rounded"></div>
            <div className="h-4 bg-gray-200 rounded w-5/6"></div>
            <div className="h-4 bg-gray-200 rounded w-4/6"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error || !article) {
    return (
      <div className="p-6">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Article Not Found</h1>
          <p className="text-gray-600 mb-6">The article you're looking for doesn't exist.</p>
          <Link
            to="/"
            className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            <Home className="h-4 w-4 mr-2" />
            Back to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="mb-8">
        <Link
          to="/"
          className="inline-flex items-center text-blue-600 hover:text-blue-800 mb-4"
        >
          <Home className="h-4 w-4 mr-2" />
          Back to Dashboard
        </Link>
        <h1 className="text-3xl font-bold text-gray-900 mb-4">{article.title}</h1>
        <div className="flex items-center space-x-4 text-sm text-gray-500">
          <span>{article.wordCount} words</span>
          <span>{new Date(article.createdAt).toLocaleDateString()}</span>
          <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
            {article.articleType}
          </span>
        </div>
      </div>

      <div className="prose prose-lg max-w-none">
        <div dangerouslySetInnerHTML={{ __html: article.content.replace(/\n/g, '<br>') }} />
      </div>
    </div>
  );
};

// Main App Component
const App = () => {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {/* Navigation */}
        <nav className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <Link to="/" className="flex items-center">
                  <FileText className="h-8 w-8 text-blue-600" />
                  <span className="ml-2 text-xl font-bold text-gray-900">AutoBlogger</span>
                </Link>
              </div>
              <div className="flex items-center space-x-4">
                <Link
                  to="/"
                  className="flex items-center px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900"
                >
                  <Home className="h-4 w-4 mr-2" />
                  Dashboard
                </Link>
                <Link
                  to="/custom"
                  className="flex items-center px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900"
                >
                  <Plus className="h-4 w-4 mr-2" />
                  Custom Generator
                </Link>
                <Link
                  to="/quick"
                  className="flex items-center px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900"
                >
                  <Zap className="h-4 w-4 mr-2" />
                  Quick Actions
                </Link>
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/custom" element={<CustomGenerator />} />
            <Route path="/quick" element={<QuickActions />} />
            <Route path="/articles/:slug" element={<ArticleViewer match={{ params: { slug: window.location.pathname.split('/').pop() } }} />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App;

