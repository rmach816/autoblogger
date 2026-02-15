import { GoogleGenerativeAI } from '@google/generative-ai';

export interface ArticleGenerationResult {
  title: string;
  content: string;
}

export class AIService {
  private genAI: GoogleGenerativeAI | null;
  // private fallbackContent: Map<string, string> = new Map();

  constructor() {
    const apiKey = process.env['GEMINI_API_KEY'];
    if (!apiKey) {
      // Allow the API to run without external AI credentials (dev/offline mode).
      // Article generation will fall back to deterministic template content.
      this.genAI = null;
      return;
    }
    this.genAI = new GoogleGenerativeAI(apiKey);
  }

  async generateArticle(topic: string, keywords: string[], wordCount: number): Promise<ArticleGenerationResult> {
    const prompt = this.buildPrompt(topic, keywords, wordCount);
    
    try {
      if (!this.genAI) {
        return this.generateFallbackContent(topic, keywords, wordCount);
      }
      const model = this.genAI.getGenerativeModel({ model: 'gemini-1.5-flash' });
      const result = await model.generateContent(prompt);
      const response = await result.response;
      const content = response.text();
      
      return this.parseContent(content, topic);
    } catch (error) {
      console.error('AI generation failed:', error);
      return this.generateFallbackContent(topic, keywords, wordCount);
    }
  }

  private buildPrompt(topic: string, keywords: string[], wordCount: number): string {
    return `Create a comprehensive, SEO-optimized article about: ${topic}

Target audience: General audience interested in ${topic}
Word count: ${wordCount} words
Keywords to include: ${keywords.join(', ')}

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
  }

  private parseContent(content: string, topic: string): ArticleGenerationResult {
    const titleMatch = content.match(/^#\s+(.+)$/m);
    const title = titleMatch?.[1] || topic;
    
    return { title, content };
  }

  private generateFallbackContent(topic: string, keywords: string[], wordCount: number): ArticleGenerationResult {
    // Generate unique fallback content based on topic
    const title = this.generateUniqueTitle(topic);
    const content = this.generateUniqueContent(topic, keywords, wordCount);
    
    return { title, content };
  }

  private generateUniqueTitle(topic: string): string {
    const variations = [
      `The Complete Guide to ${topic}`,
      `${topic}: Everything You Need to Know`,
      `Understanding ${topic} in 2026`,
      `${topic}: A Comprehensive Overview`,
      `Mastering ${topic}: Expert Insights`
    ];
    
    const randomIndex = Math.floor(Math.random() * variations.length);
    return variations[randomIndex] || topic;
  }

  private generateUniqueContent(topic: string, _keywords: string[], _wordCount: number): string {
    // const timestamp = Date.now();
    const sections = [
      `# ${topic}\n\n`,
      `## Introduction\n\n`,
      `In this comprehensive guide, we'll explore ${topic} and its impact on modern society. This topic has gained significant attention in recent years, and understanding its nuances is crucial for anyone looking to stay informed.\n\n`,
      `## Key Concepts\n\n`,
      `### What is ${topic}?\n\n`,
      `${topic} represents a fundamental shift in how we approach complex problems. It combines traditional methodologies with innovative approaches to create solutions that are both effective and sustainable.\n\n`,
      `### Why ${topic} Matters\n\n`,
      `The importance of ${topic} cannot be overstated. It provides:\n\n`,
      `- **Innovation**: New ways of thinking and problem-solving\n`,
      `- **Efficiency**: Streamlined processes and improved outcomes\n`,
      `- **Scalability**: Solutions that grow with your needs\n`,
      `- **Sustainability**: Long-term benefits and positive impact\n\n`,
      `## Best Practices\n\n`,
      `When implementing ${topic}, consider these proven strategies:\n\n`,
      `1. **Start Small**: Begin with pilot projects to test concepts\n`,
      `2. **Measure Impact**: Track metrics and adjust approaches\n`,
      `3. **Stay Updated**: Keep abreast of latest developments\n`,
      `4. **Collaborate**: Work with experts and stakeholders\n\n`,
      `## Conclusion\n\n`,
      `${topic} represents an exciting opportunity for growth and innovation. By understanding its principles and implementing best practices, you can unlock its full potential and achieve remarkable results.\n\n`,
      `*This article was generated on ${new Date().toISOString()} and focuses specifically on ${topic}.*\n\n`
    ];
    
    return sections.join('');
  }
}
