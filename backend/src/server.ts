import express from 'express';
import 'dotenv/config';
import { ArticleController } from './controllers/articleController';
import { securityHeaders, corsConfig, rateLimiter, apiRateLimiter } from './middleware/security';
import { requestLogger, devLogger } from './middleware/logging';

const app = express();
const PORT = process.env['PORT'] || 5001;

// Middleware
app.use(securityHeaders);
app.use(corsConfig);
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Logging
if (process.env['NODE_ENV'] === 'development') {
  app.use(devLogger);
} else {
  app.use(requestLogger);
}

// Rate limiting
app.use(rateLimiter);

// Initialize controllers
const articleController = new ArticleController();

// Health check endpoint
app.get('/health', (_req, res) => {
  res.json({
    success: true,
    data: {
      status: 'healthy',
      service: 'AutoBlogger API',
      version: '2.0.0',
      timestamp: new Date().toISOString(),
      uptime: process.uptime()
    }
  });
});

// API routes
app.use('/api', apiRateLimiter);

// Article generation endpoint
app.post('/api/generate-article', (req, res) => {
  articleController.generateArticle(req, res);
});

// Get single article endpoint
app.get('/api/articles/:id', (req, res) => {
  articleController.getArticle(req, res);
});

// Get articles endpoint
app.get('/api/articles', (req, res) => {
  articleController.getArticles(req, res);
});

// Image generation endpoint (placeholder)
app.post('/api/generate-image', (_req, res) => {
  res.json({
    success: true,
    data: {
      imageUrl: 'https://via.placeholder.com/800x400/007bff/ffffff?text=AutoBlogger+Image'
    },
    message: 'Image generation feature coming soon'
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    success: false,
    error: 'Route not found',
    message: `Cannot ${req.method} ${req.originalUrl}`
  });
});

// Error handling middleware
app.use((err: Error, _req: express.Request, res: express.Response, _next: express.NextFunction) => {
  console.error('Unhandled error:', err);
  res.status(500).json({
    success: false,
    error: 'Internal server error',
    message: process.env['NODE_ENV'] === 'development' ? err.message : 'Something went wrong'
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 AutoBlogger API Server v2.0.0 running on port ${PORT}`);
  console.log(`📊 Health check: http://localhost:${PORT}/health`);
  console.log(`🔗 API Base: http://localhost:${PORT}/api`);
  console.log(`🌍 Environment: ${process.env['NODE_ENV'] || 'development'}`);
});

export default app;
