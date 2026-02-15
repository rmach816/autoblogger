const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const path = require('path');
require('dotenv').config();

const { PrismaClient } = require('@prisma/client');
// Using Google Gemini API instead of OpenAI
const { GoogleGenerativeAI } = require('@google/generative-ai');

const app = express();
const prisma = new PrismaClient();

// Fallback content generation function
function generateFallbackContent(topic, keywords, wordCount) {
  const templates = {
    'automation': {
      title: 'Smart Home Automation Solutions for Houston Families',
      content: `# Smart Home Automation Solutions for Houston Families

Transform your Houston home into a smart, connected living space with professional home automation solutions. Modern smart home automation systems provide unprecedented convenience, energy efficiency, and peace of mind for Houston families.

## Why Smart Home Automation Matters for Houston Families

Houston's diverse neighborhoods and growing tech-savvy population make smart home automation essential for modern family living. These advanced systems provide:

- **Voice Control**: Control your home with simple voice commands
- **Energy Efficiency**: Automated systems reduce energy consumption and costs
- **Security Integration**: Seamless connection with security systems
- **Remote Access**: Monitor and control your home from anywhere
- **Customization**: Tailored solutions for your family's needs

## Popular Automation Features in Houston Homes

### Lighting Control
Smart lighting systems allow you to:
- Schedule lights to turn on/off automatically
- Adjust brightness and color temperature
- Control lights remotely via smartphone
- Integrate with security systems

### Climate Control
Smart thermostats provide:
- Learning capabilities that adapt to your schedule
- Energy usage monitoring and optimization
- Remote temperature control
- Integration with weather data

### Security Integration
Connect your automation system with:
- Smart door locks and garage door openers
- Security cameras and motion sensors
- Alarm systems and monitoring services
- Video doorbells and intercom systems

## Professional Installation in Houston

Executive Technology Group specializes in custom home automation solutions for Houston families. Our certified technicians ensure:

- Proper system design and planning
- Professional installation and configuration
- Comprehensive testing and training
- Ongoing support and maintenance

## Getting Started with Home Automation

Ready to transform your Houston home? Contact Executive Technology Group at (281) 826-1880 for a free consultation. We'll help you design the perfect automation solution for your family's needs and budget.

**Schedule a Free Consultation Today** - Let us show you how smart home automation can enhance your Houston lifestyle.`
    },
    'networking': {
      title: 'Professional Business Networking Solutions for Houston Companies',
      content: `# Professional Business Networking Solutions for Houston Companies

Houston's thriving business environment demands reliable, high-performance networking solutions. Executive Technology Group provides comprehensive business networking services that keep Houston companies connected, secure, and productive.

## Why Professional Networking Matters for Houston Businesses

In today's digital economy, your network infrastructure is the backbone of your business operations. Professional networking solutions provide:

- **Reliability**: 99.9% uptime for critical business operations
- **Security**: Advanced protection against cyber threats
- **Scalability**: Solutions that grow with your business
- **Performance**: High-speed connectivity for all devices
- **Support**: Professional maintenance and troubleshooting

## Business Networking Services in Houston

### WiFi Network Design and Installation
- Enterprise-grade wireless access points
- Seamless roaming and coverage
- Guest network management
- Bandwidth optimization

### Wired Network Infrastructure
- Cat6 and fiber optic cabling
- Network switches and routers
- Structured cabling systems
- Network monitoring and management

### Security and Compliance
- Firewall configuration and management
- VPN setup and maintenance
- Network security audits
- Compliance with industry standards

## Managed Network Services

Executive Technology Group offers comprehensive managed network services including:

- 24/7 network monitoring
- Proactive maintenance and updates
- Security patch management
- Performance optimization
- Help desk support

## Choosing the Right Networking Solution

Every Houston business has unique networking requirements. Our team works with you to:

- Assess your current infrastructure
- Identify performance bottlenecks
- Design scalable solutions
- Implement best practices
- Provide ongoing support

## Professional Installation and Support

Our certified network engineers ensure:

- Proper network design and planning
- Professional installation and configuration
- Comprehensive testing and documentation
- Staff training and support
- Ongoing maintenance and optimization

## Get Started Today

Ready to upgrade your business networking? Contact Executive Technology Group at (281) 826-1880 for a free network assessment. We'll help you design the perfect networking solution for your Houston business.

**Schedule a Free Consultation Today** - Let us show you how professional networking can transform your business operations.`
    },
    'security': {
      title: 'Smart Home Security Systems for Houston Homes',
      content: `# Smart Home Security Systems for Houston Homes

Protect your Houston home and family with advanced smart security systems. Executive Technology Group provides comprehensive security solutions that integrate seamlessly with your smart home automation.

## Why Smart Security Matters for Houston Homes

Houston's diverse neighborhoods require sophisticated security solutions that provide:

- **24/7 Monitoring**: Continuous surveillance and alert systems
- **Remote Access**: Monitor your home from anywhere
- **Smart Integration**: Seamless connection with automation systems
- **Professional Installation**: Certified technicians ensure proper setup
- **Local Support**: Houston-based service and maintenance

## Smart Security Features

### Video Surveillance
- High-definition security cameras
- Night vision and motion detection
- Cloud storage and remote viewing
- Mobile app integration

### Access Control
- Smart door locks and keypads
- Garage door automation
- Visitor management systems
- Keyless entry options

### Alarm Systems
- Professional monitoring services
- Glass break detection
- Motion sensors and door contacts
- Panic buttons and emergency response

## Integration with Home Automation

Smart security systems work seamlessly with:

- Lighting control and automation
- Climate control systems
- Entertainment systems
- Voice control integration

## Professional Installation and Support

Executive Technology Group provides:

- Custom security system design
- Professional installation and configuration
- Staff training and user guides
- 24/7 monitoring services
- Ongoing maintenance and support

## Getting Started

Ready to secure your Houston home? Contact Executive Technology Group at (281) 826-1880 for a free security assessment. We'll help you design the perfect security solution for your family's needs.

**Schedule a Free Consultation Today** - Protect what matters most with professional smart security systems.`
    }
  };

  // Determine content type based on topic keywords
  let contentType = 'automation';
  const keywordsStr = Array.isArray(keywords) ? keywords.join(' ') : (keywords || '');
  if (keywordsStr.toLowerCase().includes('networking')) {
    contentType = 'networking';
  } else if (keywordsStr.toLowerCase().includes('security')) {
    contentType = 'security';
  }

  const template = templates[contentType] || templates['automation'];
  return `# ${template.title}\n\n${template.content}`;
}

// Image generation function
async function generateImage(prompt, style) {
  try {
    // For now, return placeholder images based on style
    const placeholderImages = {
      'professional': 'https://images.unsplash.com/photo-1551434678-e076c223a692?w=800&h=600&fit=crop',
      'business': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=600&fit=crop',
      'technology': 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800&h=600&fit=crop',
      'security': 'https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=800&h=600&fit=crop',
      'networking': 'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&h=600&fit=crop'
    };
    
    return placeholderImages[style] || placeholderImages['professional'];
  } catch (error) {
    console.error('Image generation error:', error);
    return 'https://images.unsplash.com/photo-1551434678-e076c223a692?w=800&h=600&fit=crop';
  }
}

// Initialize Gemini AI
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || 'your-gemini-api-key-here');

// Middleware
app.use(helmet({
  contentSecurityPolicy: false
}));
app.use(cors({
  origin: process.env.CORS_ORIGIN || 'http://localhost:3000',
  credentials: true
}));
app.use(morgan('combined'));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    service: 'autoblogger',
    version: '2.0.0'
  });
});

// Image generation endpoint
app.post('/api/generate-image', async (req, res) => {
  const { prompt, style = 'professional' } = req.body;

  if (!prompt) {
    return res.status(400).json({ error: 'Prompt is required' });
  }

  try {
    // Generate image using Gemini Vision or fallback to placeholder
    const imageUrl = await generateImage(prompt, style);
    
    res.status(201).json({
      imageUrl,
      prompt,
      style,
      generatedAt: new Date().toISOString()
    });
  } catch (error) {
    console.error('Error generating image:', error);
    res.status(500).json({ error: 'Failed to generate image', details: error.message });
  }
});

// Generate article endpoint
app.post('/api/generate-article', async (req, res) => {
  try {
    const { topic, keywords, wordCount = 1200, articleType = 'custom' } = req.body;

    if (!topic) {
      return res.status(400).json({ error: 'Topic is required' });
    }

    // Generate content using OpenAI
    const prompt = `Create a comprehensive, SEO-optimized article about: ${topic}

Target audience: General audience interested in ${topic}
Word count: ${wordCount} words
Keywords to include: ${keywords || 'technology, innovation, solutions'}

Requirements:
- Include headings and subheadings
- Use bullet points and numbered lists where appropriate
- Add callout boxes for important information
- Include relevant statistics and examples
- Write in a professional, authoritative tone
- Include a compelling call-to-action
- Optimize for SEO with natural keyword integration
- Make the content unique and specific to the topic: ${topic}

Format the response as markdown with proper heading structure.`;

    let content;
    
    try {
      const model = genAI.getGenerativeModel({ model: 'gemini-1.5-flash' });
      const result = await model.generateContent(prompt);
      content = result.response.text();
    } catch (error) {
      console.log('Gemini API error, using fallback content generation:', error.message);
      content = generateFallbackContent(topic, keywords, wordCount);
    }
    
    // Extract title from content (first line after #)
    const titleMatch = content.match(/^#\s+(.+)$/m);
    const title = titleMatch ? titleMatch[1] : topic;
    
    // Create unique slug with timestamp
    const timestamp = Date.now();
    const baseSlug = title.toLowerCase()
      .replace(/[^a-z0-9\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .trim('-');
    const slug = `${baseSlug}-${timestamp}`;

    // Calculate word count
    const actualWordCount = content.split(/\s+/).length;

    // Save to database
    const article = await prisma.article.create({
      data: {
        title,
        content,
        slug,
        topic,
        keywords: Array.isArray(keywords) ? keywords.join(', ') : (keywords || ''),
        wordCount: actualWordCount,
        articleType,
        status: 'published',
        publishedAt: new Date()
      }
    });

    res.json({
      success: true,
      article: {
        id: article.id,
        title: article.title,
        slug: article.slug,
        wordCount: article.wordCount,
        createdAt: article.createdAt
      }
    });

  } catch (error) {
    console.error('Error generating article:', error);
    res.status(500).json({ 
      error: 'Failed to generate article',
      details: error.message 
    });
  }
});

// Get single article endpoint
app.get('/api/articles/:id', async (req, res) => {
  try {
    const { id } = req.params;
    
    const article = await prisma.article.findUnique({
      where: { id },
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

    if (!article) {
      return res.status(404).json({ error: 'Article not found' });
    }

    res.json({ article });
  } catch (error) {
    console.error('Error fetching article:', error);
    res.status(500).json({ error: 'Failed to fetch article' });
  }
});

// Get articles endpoint
app.get('/api/articles', async (req, res) => {
  try {
    const { type, limit = 20, offset = 0 } = req.query;
    
    const where = type ? { articleType: type } : {};
    
    const articles = await prisma.article.findMany({
      where,
      orderBy: { createdAt: 'desc' },
      take: parseInt(limit),
      skip: parseInt(offset),
      select: {
        id: true,
        title: true,
        slug: true,
        topic: true,
        wordCount: true,
        articleType: true,
        status: true,
        createdAt: true,
        publishedAt: true
      }
    });

    res.json({ articles });
  } catch (error) {
    console.error('Error fetching articles:', error);
    res.status(500).json({ error: 'Failed to fetch articles' });
  }
});

// Get single article endpoint
app.get('/api/articles/:slug', async (req, res) => {
  try {
    const { slug } = req.params;
    
    const article = await prisma.article.findUnique({
      where: { slug },
      include: {
        imagesList: true
      }
    });

    if (!article) {
      return res.status(404).json({ error: 'Article not found' });
    }

    res.json({ article });
  } catch (error) {
    console.error('Error fetching article:', error);
    res.status(500).json({ error: 'Failed to fetch article' });
  }
});

// Delete article endpoint
app.delete('/api/articles/:id', async (req, res) => {
  try {
    const { id } = req.params;
    
    await prisma.article.delete({
      where: { id }
    });

    res.json({ success: true });
  } catch (error) {
    console.error('Error deleting article:', error);
    res.status(500).json({ error: 'Failed to delete article' });
  }
});

// Serve static files
app.use(express.static('public'));

// Serve the main UI
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

const PORT = process.env.PORT || 5001;

app.listen(PORT, () => {
  console.log(`🚀 AutoBlogger API Server running on port ${PORT}`);
  console.log(`📊 Health check: http://localhost:${PORT}/health`);
  console.log(`🔗 API Base: http://localhost:${PORT}/api`);
});

// Graceful shutdown
process.on('SIGINT', async () => {
  console.log('\n🛑 Shutting down server...');
  await prisma.$disconnect();
  process.exit(0);
});

module.exports = app;
