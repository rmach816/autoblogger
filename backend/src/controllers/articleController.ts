import { Request, Response } from 'express';
import { AIService } from '../services/aiService';
import { PrismaClient } from '@prisma/client';

export class ArticleController {
  private prisma: PrismaClient;
  private aiService: AIService;

  constructor() {
    this.prisma = new PrismaClient();
    this.aiService = new AIService();
  }

  async generateArticle(req: Request, res: Response): Promise<void> {
    try {
      const { topic, keywords, wordCount, articleType } = req.body;

      if (!topic) {
        res.status(400).json({ success: false, error: 'Topic is required' });
        return;
      }

      // Generate unique content using real AI
      const { title, content } = await this.aiService.generateArticle(
        topic, 
        keywords || [], 
        wordCount || 800
      );

      // Create unique slug with timestamp
      const timestamp = Date.now();
      const slug = `${title.toLowerCase()
        .replace(/[^a-z0-9\s-]/g, '')
        .replace(/\s+/g, '-')
        .replace(/-+/g, '-')
        .replace(/^-+|-+$/g, '')}-${timestamp}`;

      // Save to database
      const article = await this.prisma.article.create({
        data: {
          title,
          content,
          slug,
          topic,
          keywords: Array.isArray(keywords) ? keywords.join(', ') : (keywords || ''),
          wordCount: content.split(/\s+/).length,
          articleType: articleType || 'custom',
          status: 'published',
          publishedAt: new Date()
        }
      });

      res.json({
        success: true,
        data: {
          article: {
            id: article.id,
            title: article.title,
            slug: article.slug,
            wordCount: article.wordCount,
            createdAt: article.createdAt
          }
        },
        message: 'Article generated'
      });
    } catch (error) {
      console.error('Error generating article:', error);
      res.status(500).json({ 
        success: false,
        error: 'Failed to generate article',
        message: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  }

  async getArticle(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      
      const article = await this.prisma.article.findUnique({
        where: { id: id as string },
        include: { imagesList: true }
      });

      if (!article) {
        res.status(404).json({ success: false, error: 'Article not found' });
        return;
      }

      res.json({ 
        success: true,
        data: {
          article: {
            id: article.id,
            title: article.title,
            content: article.content,
            slug: article.slug,
            topic: article.topic,
            keywords: article.keywords,
            wordCount: article.wordCount,
            articleType: article.articleType,
            status: article.status,
            createdAt: article.createdAt,
            publishedAt: article.publishedAt,
            images: article.imagesList || []
          }
        }
      });
    } catch (error) {
      console.error('Error fetching article:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch article' });
    }
  }

  async getArticles(req: Request, res: Response): Promise<void> {
    try {
      const { type, limit = 20, offset = 0 } = req.query;
      
      const where = type ? { articleType: type as string } : {};
      const take = Math.max(1, Math.min(100, Number(limit) || 20));
      const skip = Math.max(0, Number(offset) || 0);
      
      const articlesRaw = await this.prisma.article.findMany({
        where,
        orderBy: { createdAt: 'desc' },
        take,
        skip,
        select: {
          id: true,
          title: true,
          content: true,
          slug: true,
          topic: true,
          keywords: true,
          wordCount: true,
          articleType: true,
          status: true,
          createdAt: true,
          publishedAt: true
        }
      });

      const articles = articlesRaw.map((a) => ({
        id: a.id,
        title: a.title,
        slug: a.slug,
        topic: a.topic,
        keywords: a.keywords,
        wordCount: a.wordCount,
        articleType: a.articleType,
        status: a.status,
        createdAt: a.createdAt,
        publishedAt: a.publishedAt,
        excerpt: a.content.slice(0, 200)
      }));

      res.json({ 
        success: true,
        data: { articles }
      });
    } catch (error) {
      console.error('Error fetching articles:', error);
      res.status(500).json({ success: false, error: 'Failed to fetch articles' });
    }
  }
}
