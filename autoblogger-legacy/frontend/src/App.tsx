import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Article {
  id: string;
  title: string;
  content: string;
  slug: string;
  articleType: string;
  wordCount: number;
  createdAt: string;
}

const App: React.FC = () => {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    topic: '',
    keywords: '',
    wordCount: 1200,
    articleType: 'custom'
  });

  const [imagePrompt, setImagePrompt] = useState('');
  const [imageStyle, setImageStyle] = useState('professional');

  // Fetch articles on component mount
  useEffect(() => {
    fetchArticles();
  }, []);

  const fetchArticles = async () => {
    try {
      const response = await axios.get('http://localhost:5001/api/articles');
      setArticles(response.data);
    } catch (error) {
      console.error('Error fetching articles:', error);
    }
  };

  const generateArticle = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await axios.post('http://localhost:5001/api/generate-article', {
        topic: formData.topic,
        keywords: formData.keywords.split(',').map(k => k.trim()),
        wordCount: formData.wordCount,
        articleType: formData.articleType
      });
      
      console.log('Article generated:', response.data);
      fetchArticles(); // Refresh articles list
      setFormData({ topic: '', keywords: '', wordCount: 1200, articleType: 'custom' });
    } catch (error) {
      console.error('Error generating article:', error);
    } finally {
      setLoading(false);
    }
  };

  const generateImage = async () => {
    try {
      const response = await axios.post('http://localhost:5001/api/generate-image', {
        prompt: imagePrompt,
        style: imageStyle
      });
      
      console.log('Image generated:', response.data);
    } catch (error) {
      console.error('Error generating image:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            AutoBlogger
          </h1>
          <p className="text-xl text-gray-600">
            AI-Powered Blog Content Generation
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Article Generation Form */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-semibold mb-4">Generate Article</h2>
            <form onSubmit={generateArticle} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Topic
                </label>
                <input
                  type="text"
                  value={formData.topic}
                  onChange={(e) => setFormData({...formData, topic: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter article topic..."
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Keywords (comma-separated)
                </label>
                <input
                  type="text"
                  value={formData.keywords}
                  onChange={(e) => setFormData({...formData, keywords: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="keyword1, keyword2, keyword3"
                />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Word Count
                  </label>
                  <input
                    type="number"
                    value={formData.wordCount}
                    onChange={(e) => setFormData({...formData, wordCount: parseInt(e.target.value)})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    min="300"
                    max="2000"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Article Type
                  </label>
                  <select
                    value={formData.articleType}
                    onChange={(e) => setFormData({...formData, articleType: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="custom">Custom</option>
                    <option value="quick">Quick Action</option>
                  </select>
                </div>
              </div>
              
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
              >
                {loading ? 'Generating...' : 'Generate Article'}
              </button>
            </form>
          </div>

          {/* Image Generation */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-semibold mb-4">Generate Image</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Image Prompt
                </label>
                <input
                  type="text"
                  value={imagePrompt}
                  onChange={(e) => setImagePrompt(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Describe the image you want..."
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Style
                </label>
                <select
                  value={imageStyle}
                  onChange={(e) => setImageStyle(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="professional">Professional</option>
                  <option value="business">Business</option>
                  <option value="technology">Technology</option>
                  <option value="security">Security</option>
                  <option value="networking">Networking</option>
                </select>
              </div>
              
              <button
                onClick={generateImage}
                className="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                Generate Image
              </button>
            </div>
          </div>
        </div>

        {/* Articles List */}
        <div className="mt-8">
          <h2 className="text-2xl font-semibold mb-4">Generated Articles ({articles.length})</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {articles.map((article) => (
              <div key={article.id} className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold mb-2">{article.title}</h3>
                <div className="text-sm text-gray-600 mb-2">
                  <span className="inline-block bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs mr-2">
                    {article.articleType}
                  </span>
                  <span className="text-gray-500">{article.wordCount} words</span>
                </div>
                <p className="text-gray-700 text-sm mb-4 line-clamp-3">
                  {article.content.substring(0, 150)}...
                </p>
                <div className="text-xs text-gray-500">
                  Created: {new Date(article.createdAt).toLocaleDateString()}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;

