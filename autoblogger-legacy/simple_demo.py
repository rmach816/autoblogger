#!/usr/bin/env python3
"""
Simple AutoBlogger Demo
Works without complex dependencies
"""

import os
import json
from datetime import datetime

def create_sample_article():
    """Create a sample article to demonstrate the system"""
    
    article = {
        "title": "The Future of Sustainable Gardening: 10 Eco-Friendly Tips for Urban Gardeners",
        "content": """
        <h1>The Future of Sustainable Gardening: 10 Eco-Friendly Tips for Urban Gardeners</h1>
        
        <p>As urban populations continue to grow, sustainable gardening practices have become more important than ever. Urban gardeners are leading the charge in creating environmentally friendly spaces that not only beautify our cities but also contribute to a healthier planet.</p>
        
        <h2>Why Sustainable Gardening Matters</h2>
        <p>Sustainable gardening goes beyond just growing plants. It's about creating ecosystems that support local wildlife, reduce waste, and minimize environmental impact. For urban gardeners, this means working with limited space while maximizing positive environmental outcomes.</p>
        
        <h2>10 Essential Tips for Sustainable Urban Gardening</h2>
        
        <h3>1. Choose Native Plants</h3>
        <p>Native plants are adapted to your local climate and require less water, fertilizer, and maintenance. They also provide essential habitat for local wildlife.</p>
        
        <h3>2. Compost Your Kitchen Scraps</h3>
        <p>Turn your food waste into nutrient-rich compost. This reduces landfill waste and provides free fertilizer for your plants.</p>
        
        <h3>3. Collect Rainwater</h3>
        <p>Install rain barrels to collect and store rainwater for irrigation. This reduces your water bill and conserves precious resources.</p>
        
        <h3>4. Use Organic Pest Control</h3>
        <p>Avoid chemical pesticides and instead use natural methods like companion planting, beneficial insects, and organic sprays.</p>
        
        <h3>5. Practice Crop Rotation</h3>
        <p>Even in small spaces, rotating your crops helps prevent soil depletion and reduces pest problems.</p>
        
        <h3>6. Mulch Your Beds</h3>
        <p>Mulching helps retain moisture, suppress weeds, and gradually improves soil quality as it decomposes.</p>
        
        <h3>7. Choose Drought-Tolerant Varieties</h3>
        <p>Select plants that are naturally adapted to dry conditions to reduce water usage.</p>
        
        <h3>8. Create Wildlife Habitats</h3>
        <p>Include plants that provide food and shelter for birds, bees, and other beneficial wildlife.</p>
        
        <h3>9. Use Vertical Growing</h3>
        <p>Maximize your space by growing vertically with trellises, hanging baskets, and wall-mounted planters.</p>
        
        <h3>10. Share Your Knowledge</h3>
        <p>Connect with other urban gardeners to share seeds, knowledge, and resources. Community gardens are excellent places to start.</p>
        
        <h2>Getting Started</h2>
        <p>Starting a sustainable urban garden doesn't require a large space or expensive equipment. Begin with a few containers on your balcony or a small plot in a community garden. Focus on learning about your local climate and soil conditions, then gradually expand your garden as you gain experience.</p>
        
        <h2>Conclusion</h2>
        <p>Sustainable urban gardening is not just a trend—it's a necessity for our planet's future. By implementing these practices, urban gardeners can create beautiful, productive spaces that benefit both people and the environment. Start small, be patient, and remember that every sustainable choice you make contributes to a healthier planet.</p>
        """,
        "meta_description": "Discover 10 essential tips for sustainable urban gardening. Learn how to create eco-friendly gardens that benefit both you and the environment.",
        "keywords": ["sustainable gardening", "urban gardening", "eco-friendly", "environmental", "green living"],
        "author": "AutoBlogger AI",
        "published_date": datetime.now().isoformat(),
        "word_count": 850,
        "reading_time": "4 minutes"
    }
    
    return article

def save_article(article, format="html"):
    """Save article to file"""
    
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = "".join(c for c in article["title"] if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_title = safe_title.replace(' ', '_')[:50]
    filename = f"{timestamp}_{safe_title}"
    
    if format == "html":
        # Create HTML file
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']}</title>
    <meta name="description" content="{article['meta_description']}">
    <meta name="keywords" content="{', '.join(article['keywords'])}">
    <meta name="author" content="{article['author']}">
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        h3 {{ color: #7f8c8d; }}
        .meta {{ background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .meta p {{ margin: 5px 0; }}
    </style>
</head>
<body>
    <article>
        {article['content']}
        
        <div class="meta">
            <p><strong>Author:</strong> {article['author']}</p>
            <p><strong>Published:</strong> {article['published_date']}</p>
            <p><strong>Word Count:</strong> {article['word_count']}</p>
            <p><strong>Reading Time:</strong> {article['reading_time']}</p>
            <p><strong>Keywords:</strong> {', '.join(article['keywords'])}</p>
        </div>
    </article>
</body>
</html>
        """
        
        filepath = f"output/{filename}.html"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath
    
    elif format == "json":
        # Create JSON file
        filepath = f"output/{filename}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(article, f, indent=2, ensure_ascii=False)
        
        return filepath

def main():
    """Main demo function"""
    
    print("AutoBlogger Demo")
    print("=" * 50)
    
    # Create sample article
    print("Generating sample article...")
    article = create_sample_article()
    
    # Save as HTML
    print("Saving as HTML...")
    html_file = save_article(article, "html")
    print(f"HTML saved to: {html_file}")
    
    # Save as JSON
    print("Saving as JSON...")
    json_file = save_article(article, "json")
    print(f"JSON saved to: {json_file}")
    
    print("\nDemo complete!")
    print(f"Article: {article['title']}")
    print(f"Word count: {article['word_count']}")
    print(f"Reading time: {article['reading_time']}")
    
    print("\nNext steps:")
    print("1. Open the HTML file in your browser to see the article")
    print("2. Check the JSON file to see the structured data")
    print("3. This demonstrates the core functionality of AutoBlogger")
    print("4. With your Gemini API key, we can generate real AI content!")

if __name__ == "__main__":
    main()
