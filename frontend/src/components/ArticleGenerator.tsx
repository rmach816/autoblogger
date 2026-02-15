import React, { useState } from 'react';
import { generateArticle, type ArticleFormData } from '../services/apiService';
import { Loader2, Sparkles, FileText, Zap } from 'lucide-react';

export const ArticleGenerator: React.FC = () => {
  const [formData, setFormData] = useState<ArticleFormData>({
    topic: '',
    keywords: [],
    wordCount: 800,
    articleType: 'custom'
  });
  const [isGenerating, setIsGenerating] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsGenerating(true);
    setMessage(null);

    try {
      const keywords = formData.keywords.join(',').split(',').map((k: string) => k.trim()).filter((k: string) => k);
      const result = await generateArticle({
        ...formData,
        keywords
      });

      if (result.success) {
        setMessage({ 
          type: 'success', 
          text: `Article "${result.data?.article.title}" generated successfully!` 
        });
        setFormData({ topic: '', keywords: [], wordCount: 800, articleType: 'custom' });
      } else {
        setMessage({ type: 'error', text: result.error || 'Failed to generate article' });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to connect to the server' });
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg p-6 border border-gray-200">
      <div className="text-center mb-8">
        <div className="flex items-center justify-center mb-4">
          <Sparkles className="w-8 h-8 text-blue-600 mr-3" />
          <h2 className="text-3xl font-bold text-gray-900">Generate Your Next Blog Article</h2>
        </div>
        <p className="text-gray-600 text-lg">
          Create unique, SEO-optimized content with AI-powered generation
        </p>
      </div>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Article Topic *
          </label>
          <input
            type="text"
            value={formData.topic}
            onChange={(e) => setFormData({ ...formData, topic: e.target.value })}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-colors duration-200"
            placeholder="e.g., The Future of AI in Healthcare"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Keywords (comma-separated)
          </label>
          <input
            type="text"
            value={formData.keywords.join(', ')}
            onChange={(e) => setFormData({ ...formData, keywords: e.target.value.split(',').map(k => k.trim()) })}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-colors duration-200"
            placeholder="e.g., AI, healthcare, innovation, technology"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Word Count
          </label>
          <select
            value={formData.wordCount}
            onChange={(e) => setFormData({ ...formData, wordCount: parseInt(e.target.value) })}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-colors duration-200"
          >
            <option value={500}>500 words (Quick read)</option>
            <option value={800}>800 words (Standard)</option>
            <option value={1200}>1200 words (Comprehensive)</option>
            <option value={1500}>1500 words (In-depth)</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-4">Article Type</label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <label             className={`p-6 border-2 rounded-lg cursor-pointer transition-all duration-200 ${
              formData.articleType === 'custom' 
                ? 'border-blue-500 bg-blue-50 shadow-md' 
                : 'border-gray-200 hover:border-gray-300'
            }`}>
              <input
                type="radio"
                name="articleType"
                value="custom"
                checked={formData.articleType === 'custom'}
                onChange={(e) => setFormData({ ...formData, articleType: e.target.value as 'custom' | 'quick' })}
                className="sr-only"
              />
              <div className="text-center">
                <FileText className="w-8 h-8 mx-auto mb-3 text-blue-600" />
                <h3 className="font-semibold text-lg mb-2">Custom Article</h3>
                <p className="text-sm text-gray-600">Tailored to your specific topic and requirements</p>
              </div>
            </label>
            
            <label             className={`p-6 border-2 rounded-lg cursor-pointer transition-all duration-200 ${
              formData.articleType === 'quick' 
                ? 'border-blue-500 bg-blue-50 shadow-md' 
                : 'border-gray-200 hover:border-gray-300'
            }`}>
              <input
                type="radio"
                name="articleType"
                value="quick"
                checked={formData.articleType === 'quick'}
                onChange={(e) => setFormData({ ...formData, articleType: e.target.value as 'custom' | 'quick' })}
                className="sr-only"
              />
              <div className="text-center">
                <Zap className="w-8 h-8 mx-auto mb-3 text-blue-600" />
                <h3 className="font-semibold text-lg mb-2">Quick Action</h3>
                <p className="text-sm text-gray-600">Fast, actionable content for immediate use</p>
              </div>
            </label>
          </div>
        </div>

        <button
          type="submit"
          disabled={isGenerating}
          className="w-full bg-blue-600 text-white px-6 py-4 rounded-lg font-semibold hover:bg-blue-700 transition-colors duration-200 text-lg disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center"
        >
          {isGenerating ? (
            <>
              <Loader2 className="w-5 h-5 mr-2 animate-spin" />
              Generating Article...
            </>
          ) : (
            <>
              <Sparkles className="w-5 h-5 mr-2" />
              Generate Article
            </>
          )}
        </button>

        {message && (
          <div className={`p-4 rounded-lg ${
            message.type === 'success' 
              ? 'bg-green-100 text-green-800 border border-green-200' 
              : 'bg-red-100 text-red-800 border border-red-200'
          }`}>
            {message.text}
          </div>
        )}
      </form>
    </div>
  );
};
