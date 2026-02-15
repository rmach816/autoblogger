"""
Content generator for AutoBlogger.

Handles AI-powered article generation using various providers
(Gemini, Groq, or mock for testing).
"""

import asyncio
import os
import uuid
from datetime import datetime
from typing import List, Optional

from models import Article, BlogConfig, GenerationError, APIError, RateLimitError
from utils.logger import LogContext, get_logger
from utils.retry import retry, get_rate_limiter

logger = get_logger(__name__)


class BaseAIProvider:
    """Base class for AI providers."""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = get_logger(f"ai.{name}")
    
    async def generate_content(self, prompt: str) -> str:
        """Generate content from prompt."""
        raise NotImplementedError


class RealAIProvider(BaseAIProvider):
    """Real AI provider using OpenAI API for production content generation."""
    
    def __init__(self):
        super().__init__("openai")
        self.rate_limiter = get_rate_limiter("openai")
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            self.logger.warning("OPENAI_API_KEY not found, using enhanced fallback content")
    
    async def generate_content(self, prompt: str) -> str:
        """
        Generate real content using OpenAI API.
        
        Args:
            prompt: Generation prompt
            
        Returns:
            Generated content from OpenAI
        """
        # If no API key, use enhanced fallback content
        if not self.api_key:
            self.logger.info("Using enhanced fallback content (no API key)")
            return self._generate_enhanced_fallback_content(prompt)
        
        try:
            # Import OpenAI
            import openai
            
            # Configure OpenAI client
            client = openai.AsyncOpenAI(api_key=self.api_key)
            
            # Generate content using OpenAI
            response = await client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional content writer specializing in creating high-quality, SEO-optimized blog articles. Generate comprehensive, well-structured content that provides real value to readers."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=4000,
                temperature=0.7,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            content = response.choices[0].message.content
            self.logger.info(f"Generated real content using OpenAI GPT-4")
            return content
            
        except Exception as e:
            self.logger.error(f"OpenAI API error: {str(e)}")
            # Fallback to enhanced mock content
            return self._generate_enhanced_fallback_content(prompt)
    
    def _generate_enhanced_fallback_content(self, prompt: str) -> str:
        """Generate enhanced fallback content when OpenAI is unavailable."""
        self.logger.info(f"=== ENHANCED FALLBACK CONTENT DEBUG ===")
        self.logger.info(f"Prompt received: {prompt[:200]}...")
        
        # Extract topic from prompt
        topic = self._extract_topic_from_prompt(prompt)
        self.logger.info(f"Extracted topic: '{topic}'")
        
        # Create a proper title based on topic
        title = self._create_title_from_topic(topic)
        self.logger.info(f"Generated title: '{title}'")
        
        # Generate enhanced content based on topic
        if "automation" in topic.lower():
            self.logger.info("Using automation content")
            content = self._generate_automation_content()
        elif "theater" in topic.lower():
            self.logger.info("Using theater content")
            content = self._generate_theater_content()
        elif "security" in topic.lower():
            self.logger.info("Using security content")
            content = self._generate_security_content()
        elif "gardening" in topic.lower():
            self.logger.info("Using gardening content")
            content = self._generate_gardening_content()
        elif "networking" in topic.lower():
            self.logger.info("Using networking content")
            content = self._generate_networking_content()
        elif "lighting" in topic.lower():
            self.logger.info("Using lighting content")
            content = self._generate_lighting_content()
        elif "commercial" in topic.lower() and "av" in topic.lower():
            self.logger.info("Using commercial av content")
            content = self._generate_commercial_av_content()
        else:
            self.logger.info("Using default content")
            content = self._generate_default_content(topic)
        
        result = f"# {title}\n\n{content}"
        self.logger.info(f"Final result length: {len(result)} characters")
        return result
    
    def _generate_mock_content(self, topic: str) -> str:
        """Generate mock content based on topic."""
        self.logger.info(f"Generating content for topic: {topic}")
        
        # Create a proper title based on topic
        title = self._create_title_from_topic(topic)
        
        # Generate content based on topic
        if "automation" in topic.lower():
            content = self._generate_automation_content()
        elif "theater" in topic.lower():
            content = self._generate_theater_content()
        elif "security" in topic.lower():
            content = self._generate_security_content()
        elif "gardening" in topic.lower():
            content = self._generate_gardening_content()
        elif "networking" in topic.lower():
            content = self._generate_networking_content()
        elif "lighting" in topic.lower():
            content = self._generate_lighting_content()
        elif "commercial" in topic.lower() and "av" in topic.lower():
            content = self._generate_commercial_av_content()
        else:
            content = self._generate_default_content(topic)
        
        return f"# {title}\n\n{content}"
    
    def _generate_networking_content(self) -> str:
        """Generate networking solutions content."""
        return """Transform your Houston business with professional networking solutions that deliver reliable, high-speed connectivity. Modern business networking systems provide the foundation for productivity, collaboration, and growth in today's digital economy.

## Why Professional Networking Solutions Matter for Houston Businesses

Houston's diverse business landscape and growing tech sector make professional networking essential for competitive advantage. These advanced systems provide:

- **Reliable Connectivity**: High-speed internet and network infrastructure
- **Scalable Solutions**: Networks that grow with your business
- **Security Integration**: Advanced firewall and security protocols
- **Managed Services**: Professional monitoring and maintenance

## Essential Business Networking Components

### Wireless Network Infrastructure
Modern WiFi systems provide seamless connectivity:
- Enterprise-grade access points
- Mesh network coverage
- Guest network isolation
- Bandwidth management and QoS

### Wired Network Solutions
Reliable wired connections for critical systems:
- Cat6 and Cat6a cabling
- Network switches and routers
- Power over Ethernet (PoE)
- Structured cabling systems

### Network Security
Comprehensive security for business networks:
- Firewall configuration and management
- VPN access for remote workers
- Network monitoring and intrusion detection
- Regular security audits and updates

### Managed Network Services
Professional network management includes:
- 24/7 network monitoring
- Proactive maintenance and updates
- Performance optimization
- Technical support and troubleshooting

## Professional Installation Benefits

Working with certified networking professionals ensures:
- Proper network design and planning
- Quality equipment selection and installation
- Network optimization for your specific needs
- Ongoing support and maintenance

## Houston-Specific Considerations

Houston's business environment requires special considerations:
- High humidity protection for equipment
- Power conditioning for stable operation
- Scalable solutions for growing businesses
- Integration with existing IT infrastructure

## Creating Your Business Network

Professional networking installation transforms your Houston business with reliable, secure connectivity. With expert design, installation, and ongoing support, these systems deliver the foundation for business success.

The investment in professional networking technology pays dividends through improved productivity, enhanced security, and scalable growth. For Houston businesses, these systems represent the backbone of modern operations.

## Ready to Get Started?

**Executive Technology Group** is your trusted partner for technology solutions in Houston and surrounding areas. We specialize in:

- **Smart Home Automation** - Seamless integration and control
- **Home Theater & AV Systems** - Premium entertainment experiences
- **Networking Solutions** - Reliable, high-speed connectivity
- **Security & Surveillance** - Advanced protection systems
- **Lighting Control** - Energy-efficient, automated lighting

### Why Choose Executive Technology Group?
- ✅ **20+ Years Experience** - Proven expertise in technology integration
- ✅ **Certified Installers** - Thoroughly trained and certified team
- ✅ **Quality & Reliability** - Dependable, high-quality services
- ✅ **Veteran Owned & Operated** - Trusted by Houston businesses and homeowners

### Ready to Get Started?
**Call us today for a free consultation:** [(281) 826-1880](tel:281-826-1880)
**Visit our website:** [www.executivetechnologygroup.com](https://www.executivetechnologygroup.com/)

*Serving Houston & surrounding areas with professional technology solutions that just work.*"""
    
    def _generate_lighting_content(self) -> str:
        """Generate smart lighting content."""
        return """Transform your Houston home with intelligent lighting control systems that enhance comfort, efficiency, and ambiance. Modern smart lighting solutions provide unprecedented control and energy savings while creating the perfect atmosphere for every occasion.

## Why Smart Lighting Control Matters for Houston Homes

Houston's diverse neighborhoods and growing focus on energy efficiency make smart lighting control essential for modern living. These advanced systems provide:

- **Energy Efficiency**: Automated lighting reduces energy consumption and costs
- **Convenience**: Voice and app control from anywhere
- **Security**: Automated lighting for security and peace of mind
- **Ambiance**: Perfect lighting for every mood and occasion

## Essential Smart Lighting Components

### LED Lighting Systems
Energy-efficient LED solutions provide:
- Dimmable LED bulbs and fixtures
- Color-changing RGB lighting
- Energy-efficient operation
- Long-lasting performance

### Smart Controls
Intelligent lighting control systems include:
- Smart switches and dimmers
- Motion sensors and occupancy detection
- Voice control integration
- Mobile app control

### Automated Lighting
Programmed lighting for convenience and security:
- Scheduled lighting routines
- Sunrise/sunset automation
- Vacation mode lighting
- Security lighting activation

### Scene Control
Pre-programmed lighting scenes for:
- Entertainment and movie nights
- Reading and work activities
- Relaxation and ambiance
- Party and celebration modes

## Professional Installation Benefits

Working with certified lighting professionals ensures:
- Proper system design and component selection
- Professional wiring and installation
- Integration with existing home systems
- Programming and user training

## Houston-Specific Considerations

Houston's climate and architecture require special considerations:
- Humidity protection for electronic components
- Power conditioning for stable operation
- Integration with HVAC systems
- Hurricane-resistant installations

## Creating Your Smart Lighting Experience

Professional smart lighting installation transforms your Houston home into an intelligent, energy-efficient living space. With expert design, installation, and ongoing support, these systems deliver unparalleled convenience and efficiency.

The investment in smart lighting technology pays dividends through energy savings, enhanced comfort, and increased home value. For Houston homeowners, these systems represent the future of modern living.

## Ready to Get Started?

**Executive Technology Group** is your trusted partner for technology solutions in Houston and surrounding areas. We specialize in:

- **Smart Home Automation** - Seamless integration and control
- **Home Theater & AV Systems** - Premium entertainment experiences
- **Networking Solutions** - Reliable, high-speed connectivity
- **Security & Surveillance** - Advanced protection systems
- **Lighting Control** - Energy-efficient, automated lighting

### Why Choose Executive Technology Group?
- ✅ **20+ Years Experience** - Proven expertise in technology integration
- ✅ **Certified Installers** - Thoroughly trained and certified team
- ✅ **Quality & Reliability** - Dependable, high-quality services
- ✅ **Veteran Owned & Operated** - Trusted by Houston businesses and homeowners

### Ready to Get Started?
**Call us today for a free consultation:** [(281) 826-1880](tel:281-826-1880)
**Visit our website:** [www.executivetechnologygroup.com](https://www.executivetechnologygroup.com/)

*Serving Houston & surrounding areas with professional technology solutions that just work.*"""
    
    def _generate_commercial_av_content(self) -> str:
        """Generate commercial AV content."""
        return """Enhance your Houston business with professional commercial AV systems that improve communication, collaboration, and presentation capabilities. Modern commercial AV solutions provide the technology foundation for successful meetings, presentations, and business operations.

## Why Commercial AV Systems Matter for Houston Businesses

Houston's dynamic business environment and growing tech sector make professional commercial AV systems essential for competitive advantage. These advanced systems provide:

- **Enhanced Communication**: Crystal-clear audio and video for meetings
- **Professional Presentations**: High-quality display and sound systems
- **Collaboration Tools**: Interactive whiteboards and video conferencing
- **Scalable Solutions**: Systems that grow with your business

## Essential Commercial AV Components

### Conference Room Systems
Professional meeting room solutions include:
- High-definition displays and projectors
- Professional audio systems
- Video conferencing equipment
- Interactive whiteboards and displays

### Presentation Systems
Advanced presentation technology provides:
- 4K and 8K display capabilities
- Wireless presentation systems
- Document cameras and visualizers
- Professional audio reinforcement

### Video Conferencing
Integrated video conferencing solutions:
- High-definition cameras and microphones
- Professional lighting systems
- Acoustic treatment for optimal sound
- Integration with popular platforms

### Digital Signage
Dynamic digital signage systems:
- High-resolution displays
- Content management systems
- Remote content updates
- Multi-zone display capabilities

## Professional Installation Benefits

Working with certified AV professionals ensures:
- Proper system design and component selection
- Professional installation and configuration
- Integration with existing IT infrastructure
- User training and ongoing support

## Houston-Specific Considerations

Houston's business environment requires special considerations:
- Climate control for equipment protection
- Power conditioning for stable operation
- Scalable solutions for growing businesses
- Integration with existing systems

## Creating Your Business AV Experience

Professional commercial AV installation transforms your Houston business with advanced communication and presentation capabilities. With expert design, installation, and ongoing support, these systems deliver the technology foundation for business success.

The investment in professional commercial AV technology pays dividends through improved communication, enhanced presentations, and increased productivity. For Houston businesses, these systems represent the competitive edge in today's digital economy.

## Ready to Get Started?

**Executive Technology Group** is your trusted partner for technology solutions in Houston and surrounding areas. We specialize in:

- **Smart Home Automation** - Seamless integration and control
- **Home Theater & AV Systems** - Premium entertainment experiences
- **Networking Solutions** - Reliable, high-speed connectivity
- **Security & Surveillance** - Advanced protection systems
- **Lighting Control** - Energy-efficient, automated lighting

### Why Choose Executive Technology Group?
- ✅ **20+ Years Experience** - Proven expertise in technology integration
- ✅ **Certified Installers** - Thoroughly trained and certified team
- ✅ **Quality & Reliability** - Dependable, high-quality services
- ✅ **Veteran Owned & Operated** - Trusted by Houston businesses and homeowners

### Ready to Get Started?
**Call us today for a free consultation:** [(281) 826-1880](tel:281-826-1880)
**Visit our website:** [www.executivetechnologygroup.com](https://www.executivetechnologygroup.com/)

*Serving Houston & surrounding areas with professional technology solutions that just work.*"""
    
    def _create_title_from_topic(self, topic: str) -> str:
        """Create a proper title from the topic."""
        if "automation" in topic.lower():
            return "Smart Home Automation Solutions for Houston Families"
        elif "theater" in topic.lower():
            return "Premium Home Theater Installation in Houston"
        elif "security" in topic.lower():
            return "Smart Home Security Systems for Houston Homes"
        elif "gardening" in topic.lower():
            return "Sustainable Gardening Solutions for Houston"
        elif "networking" in topic.lower():
            return "Professional Business Networking Solutions for Houston Companies"
        elif "lighting" in topic.lower():
            return "Smart Lighting Control Systems for Houston Homes"
        elif "commercial" in topic.lower() and "av" in topic.lower():
            return "Commercial AV Systems for Houston Businesses"
        else:
            return f"Professional {topic.title()} Services in Houston"
    
    def _generate_automation_content(self) -> str:
        """Generate smart home automation content."""
        return """Transform your Houston home into a smart, connected living space with professional home automation solutions. Modern smart home automation systems provide unprecedented convenience, energy efficiency, and peace of mind for Houston families.

## Why Smart Home Automation Matters for Houston Families

Houston's diverse neighborhoods and growing tech-savvy population make smart home automation essential for modern family living. These advanced systems provide:

- **Voice Control**: Control your home with simple voice commands
- **Energy Efficiency**: Automated systems reduce energy consumption and costs
- **Family Convenience**: Control multiple systems from one interface
- **Security Integration**: Connect with security and surveillance systems
- **Customization**: Tailored solutions for your family's specific needs

## Essential Smart Home Automation Components

### Voice Control Systems
Modern voice assistants provide hands-free control:
- Amazon Alexa and Google Assistant integration
- Whole-home voice control capabilities
- Custom voice commands for family routines
- Multi-room audio and announcements

### Smart Lighting Control
Automated lighting systems enhance comfort and efficiency:
- Dimmer controls and color-changing bulbs
- Motion-activated lighting
- Scheduled lighting for security
- Energy-efficient LED integration

### Climate Control Automation
Smart thermostats optimize comfort and energy usage:
- Programmable temperature schedules
- Remote access and control
- Energy usage monitoring
- Integration with HVAC systems

### Security and Monitoring
Comprehensive security integration:
- Door and window sensors
- Motion detection systems
- Camera integration and monitoring
- Mobile app notifications

## Professional Installation Benefits

Working with certified automation professionals ensures:
- Proper system design and component selection
- Seamless integration of all systems
- Professional wiring and setup
- Family training and ongoing support

## Houston-Specific Considerations

Houston's climate and architecture require special considerations:
- Humidity control for equipment protection
- Power conditioning for stable operation
- Integration with existing home systems
- Local code compliance and permits

## Creating Your Smart Home Experience

Professional home automation installation transforms your Houston home into a smart, connected living space. With expert design, installation, and ongoing support, these systems deliver unparalleled convenience and efficiency.

The investment in smart home automation technology pays dividends through enhanced comfort, energy savings, increased home value, and years of convenience. For Houston families, these systems represent the future of modern living.

## Ready to Get Started?

**Executive Technology Group** is your trusted partner for technology solutions in Houston and surrounding areas. We specialize in:

- **Smart Home Automation** - Seamless integration and control
- **Home Theater & AV Systems** - Premium entertainment experiences
- **Networking Solutions** - Reliable, high-speed connectivity
- **Security & Surveillance** - Advanced protection systems
- **Lighting Control** - Energy-efficient, automated lighting

### Why Choose Executive Technology Group?
- ✅ **20+ Years Experience** - Proven expertise in technology integration
- ✅ **Certified Installers** - Thoroughly trained and certified team
- ✅ **Quality & Reliability** - Dependable, high-quality services
- ✅ **Veteran Owned & Operated** - Trusted by Houston businesses and homeowners

### Ready to Get Started?
**Call us today for a free consultation:** [(281) 826-1880](tel:281-826-1880)
**Visit our website:** [www.executivetechnologygroup.com](https://www.executivetechnologygroup.com/)

*Serving Houston & surrounding areas with professional technology solutions that just work.*"""
    
    def _generate_theater_content(self) -> str:
        """Generate home theater content."""
        return """Transform your Houston home into a premium entertainment destination with professional home theater installation. Modern home theater systems deliver cinematic experiences that rival commercial theaters, bringing the magic of the big screen directly to your living space.

## Why Professional Home Theater Installation Matters

Houston's diverse entertainment scene and growing tech-savvy population make professional home theater installation essential for creating the ultimate entertainment experience. These advanced systems provide:

- **Immersive Audio**: Surround sound that puts you in the action
- **Crystal Clear Video**: 4K and 8K projection for stunning visuals
- **Smart Integration**: Seamless control of all entertainment systems
- **Professional Design**: Custom solutions tailored to your space

## Essential Home Theater Components

### 4K and 8K Projectors
Modern projectors deliver stunning visual experiences:
- Ultra-high definition 4K and 8K resolution
- HDR support for enhanced color and contrast
- Laser projection for long-lasting performance
- Smart connectivity for streaming services

### Surround Sound Systems
Immersive audio systems create cinematic experiences:
- Dolby Atmos and DTS:X support
- Multiple speaker configurations
- Wireless subwoofer options
- Room calibration for optimal sound

### Acoustic Treatment
Professional acoustic design ensures optimal sound quality:
- Sound-absorbing panels and bass traps
- Room acoustics analysis and treatment
- Noise isolation for external disturbances
- Custom acoustic solutions

## Professional Installation Benefits

Working with certified AV professionals ensures:
- Proper system design and component selection
- Optimal speaker and projector placement
- Professional wiring and cable management
- Integration with smart home systems

## Houston-Specific Considerations

Houston's climate and architecture require special considerations:
- Humidity control for equipment protection
- Power conditioning for stable operation
- Room design for optimal acoustics
- Integration with existing home systems

## Creating Your Ultimate Entertainment Experience

Professional home theater installation transforms your Houston home into a premium entertainment destination. With expert design, installation, and ongoing support, these systems deliver unparalleled entertainment experiences.

The investment in professional home theater technology pays dividends through enhanced entertainment value, increased home value, and years of enjoyment. For Houston homeowners and entertainment enthusiasts, these systems represent the ultimate in home entertainment.

## Ready to Get Started?

**Executive Technology Group** is your trusted partner for technology solutions in Houston and surrounding areas. We specialize in:

- **Smart Home Automation** - Seamless integration and control
- **Home Theater & AV Systems** - Premium entertainment experiences
- **Networking Solutions** - Reliable, high-speed connectivity
- **Security & Surveillance** - Advanced protection systems
- **Lighting Control** - Energy-efficient, automated lighting

### Why Choose Executive Technology Group?
- ✅ **20+ Years Experience** - Proven expertise in technology integration
- ✅ **Certified Installers** - Thoroughly trained and certified team
- ✅ **Quality & Reliability** - Dependable, high-quality services
- ✅ **Veteran Owned & Operated** - Trusted by Houston businesses and homeowners

### Ready to Get Started?
**Call us today for a free consultation:** [(281) 826-1880](tel:281-826-1880)
**Visit our website:** [www.executivetechnologygroup.com](https://www.executivetechnologygroup.com/)

*Serving Houston & surrounding areas with professional technology solutions that just work.*"""
    
    def _generate_security_content(self) -> str:
        """Generate smart home security content."""
        return """Protect your Houston home with advanced smart home security systems. Modern security technology provides comprehensive protection while offering the convenience and control you need for peace of mind.

## Why Smart Home Security Matters for Houston Homes

Houston's diverse neighborhoods and growing population make smart home security essential for protecting your family and property. These advanced systems provide:

- **24/7 Monitoring**: Continuous protection day and night
- **Remote Access**: Control and monitor from anywhere
- **Smart Integration**: Connect with other home automation systems
- **Professional Installation**: Expert setup and ongoing support

## Essential Smart Security Components

### Wireless Security Cameras
Modern wireless cameras provide high-definition video monitoring with night vision capabilities. These systems offer:
- Weather-resistant outdoor cameras
- Indoor monitoring with privacy controls
- Mobile app access for real-time viewing
- Cloud storage for video recordings

### Smart Door Locks
Advanced smart locks offer keyless entry and remote access:
- Keypad and biometric access options
- Remote locking/unlocking capabilities
- Activity logs and user management
- Integration with home automation systems

### Motion Sensors and Alarms
Comprehensive motion detection systems include:
- Pet-friendly motion sensors
- Glass break detectors
- Door and window sensors
- Siren and notification systems

## Professional Installation Benefits

Working with certified security professionals ensures:
- Proper system design and component selection
- Optimal camera and sensor placement
- Professional wiring and setup
- Integration with existing home systems

## Houston-Specific Considerations

Houston's climate and architecture require special considerations:
- Weather-resistant equipment for outdoor use
- Power backup systems for reliability
- Local code compliance
- Integration with existing home systems

## Protecting Your Houston Home

Smart home security systems provide comprehensive protection for your Houston home while offering the convenience and control you need. With professional installation and ongoing support, these systems deliver peace of mind and enhanced security.

The investment in smart security technology pays dividends through improved safety, convenience, and potentially reduced insurance costs. For Houston homeowners and business owners, these systems represent a smart choice for modern living.

## Ready to Get Started?

**Executive Technology Group** is your trusted partner for technology solutions in Houston and surrounding areas. We specialize in:

- **Smart Home Automation** - Seamless integration and control
- **Home Theater & AV Systems** - Premium entertainment experiences
- **Networking Solutions** - Reliable, high-speed connectivity
- **Security & Surveillance** - Advanced protection systems
- **Lighting Control** - Energy-efficient, automated lighting

### Why Choose Executive Technology Group?
- ✅ **20+ Years Experience** - Proven expertise in technology integration
- ✅ **Certified Installers** - Thoroughly trained and certified team
- ✅ **Quality & Reliability** - Dependable, high-quality services
- ✅ **Veteran Owned & Operated** - Trusted by Houston businesses and homeowners

### Ready to Get Started?
**Call us today for a free consultation:** [(281) 826-1880](tel:281-826-1880)
**Visit our website:** [www.executivetechnologygroup.com](https://www.executivetechnologygroup.com/)

*Serving Houston & surrounding areas with professional technology solutions that just work.*"""
    
    def _generate_gardening_content(self) -> str:
        """Generate sustainable gardening content."""
        return """Create a beautiful, sustainable garden in Houston with eco-friendly gardening techniques. Sustainable gardening practices help protect the environment while creating beautiful, productive gardens that thrive in Houston's unique climate.

## Why Sustainable Gardening Matters in Houston

Houston's diverse climate and growing environmental awareness make sustainable gardening essential for creating beautiful, productive gardens. These eco-friendly practices provide:

- **Environmental Protection**: Reduce chemical use and water consumption
- **Cost Savings**: Lower water bills and reduced need for fertilizers
- **Health Benefits**: Chemical-free produce and cleaner air
- **Biodiversity**: Support local wildlife and beneficial insects

## Essential Sustainable Gardening Techniques

### Water Conservation
Efficient water use is crucial for sustainable gardening:
- Drip irrigation systems
- Rainwater harvesting
- Mulching to retain moisture
- Drought-resistant plant selection

### Organic Soil Management
Healthy soil is the foundation of sustainable gardening:
- Composting kitchen and garden waste
- Natural soil amendments
- Crop rotation for soil health
- Cover cropping for soil improvement

### Natural Pest Control
Eco-friendly pest management techniques:
- Beneficial insect habitats
- Companion planting strategies
- Natural pest deterrents
- Integrated pest management

### Native Plant Landscaping
Houston-native plants provide numerous benefits:
- Reduced water requirements
- Natural pest resistance
- Wildlife habitat creation
- Low maintenance requirements

## Professional Garden Design Benefits

Working with certified landscape professionals ensures:
- Proper plant selection for Houston's climate
- Efficient irrigation system design
- Sustainable landscape planning
- Ongoing maintenance and support

## Houston-Specific Considerations

Houston's climate and soil conditions require special considerations:
- Heat and humidity management
- Soil improvement for clay conditions
- Seasonal planting schedules
- Hurricane-resistant garden design

## Creating Your Sustainable Garden

Professional sustainable garden design transforms your Houston property into a beautiful, eco-friendly landscape. With expert planning, installation, and ongoing support, these gardens provide years of beauty and environmental benefits.

The investment in sustainable gardening practices pays dividends through reduced maintenance costs, environmental benefits, and increased property value. For Houston homeowners, these gardens represent the future of responsible landscaping.

## Ready to Get Started?

**Executive Technology Group** is your trusted partner for technology solutions in Houston and surrounding areas. We specialize in:

- **Smart Home Automation** - Seamless integration and control
- **Home Theater & AV Systems** - Premium entertainment experiences
- **Networking Solutions** - Reliable, high-speed connectivity
- **Security & Surveillance** - Advanced protection systems
- **Lighting Control** - Energy-efficient, automated lighting

### Why Choose Executive Technology Group?
- ✅ **20+ Years Experience** - Proven expertise in technology integration
- ✅ **Certified Installers** - Thoroughly trained and certified team
- ✅ **Quality & Reliability** - Dependable, high-quality services
- ✅ **Veteran Owned & Operated** - Trusted by Houston businesses and homeowners

### Ready to Get Started?
**Call us today for a free consultation:** [(281) 826-1880](tel:281-826-1880)
**Visit our website:** [www.executivetechnologygroup.com](https://www.executivetechnologygroup.com/)

*Serving Houston & surrounding areas with professional technology solutions that just work.*"""
    
    def _generate_default_content(self, topic: str) -> str:
        """Generate default content for unknown topics."""
        return f"""Welcome to our comprehensive guide on {topic}. This detailed resource provides valuable insights and practical information for Houston-area residents and business owners.

## What You'll Learn

This guide covers essential information about {topic}, including:

- Key concepts and principles
- Practical applications and benefits
- Professional implementation strategies
- Houston-specific considerations

## Key Components and Features

### Core Technology
Understanding the fundamental technology behind these systems is essential for making informed decisions.

### Professional Benefits
Working with certified professionals ensures proper implementation and ongoing support.

### Local Considerations
Houston's unique environment requires special considerations for optimal results.

## Ready to Get Started?

**Executive Technology Group** is your trusted partner for technology solutions in Houston and surrounding areas. We specialize in:

- **Smart Home Automation** - Seamless integration and control
- **Home Theater & AV Systems** - Premium entertainment experiences
- **Networking Solutions** - Reliable, high-speed connectivity
- **Security & Surveillance** - Advanced protection systems
- **Lighting Control** - Energy-efficient, automated lighting

### Why Choose Executive Technology Group?
- ✅ **20+ Years Experience** - Proven expertise in technology integration
- ✅ **Certified Installers** - Thoroughly trained and certified team
- ✅ **Quality & Reliability** - Dependable, high-quality services
- ✅ **Veteran Owned & Operated** - Trusted by Houston businesses and homeowners

### Ready to Get Started?
**Call us today for a free consultation:** [(281) 826-1880](tel:281-826-1880)
**Visit our website:** [www.executivetechnologygroup.com](https://www.executivetechnologygroup.com/)

*Serving Houston & surrounding areas with professional technology solutions that just work.*"""
    
    def _generate_mock_content_old(self, topic: str) -> str:
        """Generate mock content based on topic."""
        content_templates = {
            "sustainable gardening": """
# The Complete Guide to Sustainable Gardening

Sustainable gardening is more than just a trend—it's a way of life that benefits both you and the environment. In this comprehensive guide, we'll explore the essential practices that will transform your garden into an eco-friendly haven.

## Why Sustainable Gardening Matters

Sustainable gardening focuses on working with nature rather than against it. By implementing these practices, you'll:

- Reduce your environmental footprint
- Create a healthier ecosystem in your backyard
- Save money on water and fertilizers
- Grow healthier, more nutritious food

## Essential Sustainable Practices

### 1. Composting: Nature's Recycling System

Composting is the cornerstone of sustainable gardening. Start with kitchen scraps, yard waste, and organic materials. A well-maintained compost pile will provide nutrient-rich soil amendments while reducing waste.

**Getting Started:**
- Choose a location with good drainage
- Layer green and brown materials
- Turn regularly for faster decomposition
- Keep the pile moist but not wet

### 2. Water Conservation Techniques

Water is a precious resource, and sustainable gardens use it wisely:

- Install rain barrels to collect runoff
- Use drip irrigation systems
- Mulch heavily to retain moisture
- Choose drought-resistant plants

### 3. Natural Pest Management

Instead of reaching for chemical pesticides, try these natural alternatives:

- Companion planting to deter pests
- Beneficial insects like ladybugs and lacewings
- Physical barriers and traps
- Healthy soil that supports strong plants

## Building Your Sustainable Garden

Start small and expand gradually. Focus on these key areas:

1. **Soil Health**: Test your soil and amend as needed
2. **Plant Selection**: Choose native and adapted varieties
3. **Water Management**: Implement efficient irrigation
4. **Wildlife Support**: Create habitats for beneficial creatures

## The Long-Term Benefits

Sustainable gardening isn't just about today—it's about creating a legacy. Your efforts will:

- Improve soil health over time
- Support local wildlife
- Reduce chemical dependency
- Create a beautiful, productive space

## Getting Started Today

Begin with one sustainable practice this season. Whether it's starting a compost pile, installing a rain barrel, or choosing native plants, every step makes a difference.

Remember, sustainable gardening is a journey, not a destination. Each season brings new opportunities to learn and improve your practices.

Your garden can be a powerful force for environmental good. Start today, and watch as your sustainable practices create a thriving ecosystem right in your backyard.
""",
            
            "technology": """
# The Future of Technology: Trends That Will Shape Tomorrow

Technology continues to evolve at an unprecedented pace, bringing new opportunities and challenges. In this article, we'll explore the key trends that are shaping the future of technology and how they'll impact our daily lives.

## Artificial Intelligence: Beyond the Hype

Artificial Intelligence has moved from science fiction to everyday reality. Today's AI systems are:

- More accessible than ever before
- Integrated into business processes
- Helping solve complex problems
- Learning and adapting continuously

The key to successful AI implementation lies in understanding its capabilities and limitations. Organizations that embrace AI thoughtfully will gain significant competitive advantages.

## The Internet of Things Revolution

Connected devices are transforming how we interact with our environment. Smart homes, connected cars, and industrial IoT systems are creating new possibilities for:

- Automation and efficiency
- Data collection and analysis
- Remote monitoring and control
- Predictive maintenance

## Cloud Computing: The Foundation of Modern Tech

Cloud computing has become the backbone of modern technology infrastructure. Its benefits include:

- Scalability and flexibility
- Cost-effective resource management
- Global accessibility
- Enhanced security and reliability

## Emerging Technologies to Watch

Several technologies are poised to make significant impacts:

### Quantum Computing
While still in development, quantum computing promises to solve problems that are currently impossible for classical computers.

### Blockchain and Web3
Decentralized technologies are creating new paradigms for digital interactions and ownership.

### Augmented and Virtual Reality
AR and VR are moving beyond gaming into practical applications in education, healthcare, and business.

## The Human Element

As technology advances, the human element becomes even more important. Skills like:

- Critical thinking
- Creativity
- Emotional intelligence
- Adaptability

These will remain valuable regardless of technological changes.

## Preparing for the Future

To thrive in this technological landscape, individuals and organizations should:

- Stay informed about emerging trends
- Invest in continuous learning
- Embrace change and innovation
- Focus on human-centered design

## Conclusion

The future of technology is bright, but it requires thoughtful navigation. By understanding these trends and preparing accordingly, we can harness technology's power to create a better world.

The key is to remain curious, adaptable, and focused on using technology to solve real problems and improve human experiences.
""",
            
            "business": """
# Building a Successful Business in the Digital Age

Starting and growing a business has never been more accessible, thanks to digital tools and platforms. However, success requires more than just having a great idea—it demands strategic thinking, execution, and adaptation.

## The Foundation of Business Success

Every successful business is built on solid fundamentals:

### Clear Value Proposition
Your business must solve a real problem for a specific audience. Ask yourself:
- What problem does my product or service solve?
- Who is my target customer?
- Why would they choose me over competitors?

### Market Research and Validation
Before investing heavily, validate your idea:
- Survey potential customers
- Test your concept with a minimum viable product
- Analyze your competition
- Understand market size and trends

## Digital Marketing Strategies

In today's connected world, digital marketing is essential:

### Content Marketing
Create valuable content that attracts and engages your audience:
- Blog posts and articles
- Social media content
- Videos and podcasts
- Email newsletters

### Search Engine Optimization (SEO)
Make sure your business can be found online:
- Keyword research and optimization
- Local SEO for location-based businesses
- Technical SEO for website performance
- Link building and authority development

### Social Media Marketing
Build relationships with your audience:
- Choose the right platforms for your business
- Create consistent, valuable content
- Engage with your community
- Use paid advertising strategically

## Financial Management

Sound financial practices are crucial for business success:

### Budgeting and Forecasting
- Create realistic financial projections
- Monitor cash flow carefully
- Plan for seasonal variations
- Set aside emergency funds

### Pricing Strategy
- Understand your costs and margins
- Research competitor pricing
- Test different price points
- Consider value-based pricing

## Building Your Team

As your business grows, you'll need to build a team:

### Hiring the Right People
- Define clear job descriptions
- Look for cultural fit as well as skills
- Use multiple interview methods
- Check references thoroughly

### Creating a Positive Culture
- Define your company values
- Communicate expectations clearly
- Provide growth opportunities
- Recognize and reward good work

## Technology and Automation

Leverage technology to improve efficiency:

### Essential Business Tools
- Customer relationship management (CRM)
- Project management software
- Accounting and bookkeeping tools
- Communication platforms

### Automation Opportunities
- Email marketing automation
- Social media scheduling
- Customer service chatbots
- Inventory management

## Scaling Your Business

Growth requires careful planning:

### Systems and Processes
- Document your procedures
- Create training materials
- Implement quality controls
- Plan for increased volume

### Strategic Partnerships
- Identify complementary businesses
- Develop mutually beneficial relationships
- Consider joint ventures
- Explore licensing opportunities

## Measuring Success

Track the right metrics to guide your decisions:

### Key Performance Indicators (KPIs)
- Revenue and profit margins
- Customer acquisition cost
- Customer lifetime value
- Website traffic and conversion rates

### Regular Review and Adjustment
- Monthly financial reviews
- Quarterly strategy sessions
- Annual planning meetings
- Continuous improvement processes

## The Path Forward

Building a successful business is a marathon, not a sprint. Focus on:

- Delivering consistent value to customers
- Building strong relationships
- Adapting to market changes
- Maintaining financial discipline
- Investing in your team and systems

Success comes from persistence, learning, and the willingness to adapt. Start with a solid foundation, and build systematically toward your goals.

Remember, every successful business started with a single step. Take that step today, and keep moving forward.
"""
        }
        
        return content_templates.get(topic, content_templates["technology"])
    
    def _extract_topic_from_prompt(self, prompt: str) -> str:
        """Extract the main topic from the prompt using intelligent keyword matching."""
        prompt_lower = prompt.lower()
        
        # Debug logging
        self.logger.info(f"Extracting topic from prompt: {prompt[:200]}...")
        self.logger.info(f"Full prompt for debugging: {prompt}")
        
        # Extract the actual topic from the prompt structure
        # Look for "Create a comprehensive article about: {topic}"
        if "create a comprehensive article about:" in prompt_lower:
            topic_start = prompt_lower.find("create a comprehensive article about:") + len("create a comprehensive article about:")
            topic_end = prompt_lower.find("\n", topic_start)
            if topic_end == -1:
                topic_end = len(prompt_lower)
            
            actual_topic = prompt_lower[topic_start:topic_end].strip()
            self.logger.info(f"Extracted actual topic: '{actual_topic}'")
            
            # Now check the actual topic for keywords
            # Check for networking FIRST (most specific)
            if "networking" in actual_topic:
                self.logger.info("Detected networking solutions topic")
                return "networking solutions"
            elif "automation" in actual_topic or "smart home" in actual_topic:
                self.logger.info("Detected automation topic")
                return "home automation"
            elif "theater" in actual_topic or "av" in actual_topic or "installation" in actual_topic:
                self.logger.info("Detected home theater topic")
                return "home theater"
            elif "security" in actual_topic or "surveillance" in actual_topic:
                self.logger.info("Detected smart home security topic")
                return "smart home security"
            elif "gardening" in actual_topic or "sustainable" in actual_topic:
                self.logger.info("Detected sustainable gardening topic")
                return "sustainable gardening"
            elif "lighting" in actual_topic or "led" in actual_topic:
                self.logger.info("Detected lighting control topic")
                return "lighting control"
            elif "commercial" in actual_topic and "av" in actual_topic:
                self.logger.info("Detected commercial AV topic")
                return "commercial av"
            elif "business" in actual_topic:
                self.logger.info("Detected business topic - defaulting to networking")
                return "networking solutions"
            else:
                self.logger.info(f"No specific topic detected in '{actual_topic}', using default")
                return "technology"
        
        # Fallback to old logic if prompt structure is different
        self.logger.info("Prompt structure not recognized, using fallback logic")
        return "technology"
    
    def _generate_dynamic_content(self, prompt: str, topic: str) -> str:
        """Generate dynamic content that matches the actual prompt."""
        # Extract key information from the prompt
        word_count = self._extract_word_count(prompt)
        keywords = self._extract_keywords(prompt)
        tone = self._extract_tone(prompt)
        
        # Generate a title based on the actual topic
        title = self._generate_title_from_topic(topic)
        
        # Generate content structure
        content = f"# {title}\n\n"
        
        # Add introduction based on topic
        content += self._generate_introduction(topic, keywords)
        
        # Add main sections
        content += self._generate_main_sections(topic, keywords)
        
        # Add conclusion
        content += self._generate_conclusion(topic)
        
        # Add CTA if present in prompt
        if "cta" in prompt.lower() or "call-to-action" in prompt.lower():
            content += self._generate_cta()
        
        return content
    
    def _extract_word_count(self, prompt: str) -> int:
        """Extract word count from prompt."""
        import re
        word_count_match = re.search(r'(\d+)\s*words?', prompt.lower())
        if word_count_match:
            return int(word_count_match.group(1))
        return 1200  # Default
    
    def _extract_keywords(self, prompt: str) -> list:
        """Extract keywords from prompt."""
        import re
        keywords_match = re.search(r'keywords?.*?:\s*([^\n]+)', prompt.lower())
        if keywords_match:
            return [k.strip() for k in keywords_match.group(1).split(',')]
        return []
    
    def _extract_tone(self, prompt: str) -> str:
        """Extract tone from prompt."""
        prompt_lower = prompt.lower()
        if 'professional' in prompt_lower:
            return 'professional'
        elif 'friendly' in prompt_lower:
            return 'friendly'
        elif 'authoritative' in prompt_lower:
            return 'authoritative'
        elif 'conversational' in prompt_lower:
            return 'conversational'
        elif 'technical' in prompt_lower:
            return 'technical'
        return 'professional'
    
    def _generate_title_from_topic(self, topic: str) -> str:
        """Generate a title based on the topic."""
        if isinstance(topic, list):
            topic = ' '.join(topic)
        
        # Create a proper title
        if "smart home security" in topic.lower():
            return "Smart Home Security Systems for Houston Homes"
        elif "automation" in topic.lower():
            return "Smart Home Automation Solutions for Houston Families"
        elif "networking" in topic.lower():
            return "Professional Networking Solutions for Houston Businesses"
        elif "theater" in topic.lower():
            return "Premium Home Theater Installation in Houston"
        elif "lighting" in topic.lower():
            return "Smart Lighting Control Systems for Houston Homes"
        else:
            # Use the topic as title, properly formatted
            return topic.title()
    
    def _generate_introduction(self, topic: str, keywords: list) -> str:
        """Generate introduction based on topic."""
        if "smart home security" in topic.lower():
            return """In today's connected world, protecting your Houston home with smart security systems has never been more important. Modern smart home security solutions offer comprehensive protection while providing convenience and peace of mind for homeowners and business owners throughout the Houston area.

## Why Smart Home Security Matters in Houston

Houston's diverse neighborhoods and growing population make smart security systems essential for protecting your most valuable assets. These advanced systems provide:

- **24/7 Monitoring**: Continuous protection even when you're away
- **Remote Access**: Control and monitor your system from anywhere
- **Integration**: Seamless connection with other smart home devices
- **Professional Installation**: Expert setup by certified technicians

"""
        elif "theater" in topic.lower():
            return """Transform your Houston home into a premium entertainment destination with professional home theater installation. Modern home theater systems deliver cinematic experiences that rival commercial theaters, bringing the magic of the big screen directly to your living space.

## Why Professional Home Theater Installation Matters

Houston's diverse entertainment scene and growing tech-savvy population make professional home theater installation essential for creating the ultimate entertainment experience. These advanced systems provide:

- **Immersive Audio**: Surround sound that puts you in the action
- **Crystal Clear Video**: 4K and 8K projection for stunning visuals
- **Smart Integration**: Seamless control of all entertainment systems
- **Professional Design**: Custom solutions tailored to your space

"""
        elif "automation" in topic.lower():
            return """Transform your Houston home into a smart, connected living space with professional home automation solutions. Modern smart home automation systems provide unprecedented convenience, energy efficiency, and peace of mind for Houston families.

## Why Smart Home Automation Matters for Houston Families

Houston's diverse neighborhoods and growing tech-savvy population make smart home automation essential for modern family living. These advanced systems provide:

- **Voice Control**: Control your home with simple voice commands
- **Energy Efficiency**: Automated systems reduce energy consumption and costs
- **Family Convenience**: Control multiple systems from one interface
- **Security Integration**: Connect with security and surveillance systems
- **Customization**: Tailored solutions for your family's specific needs

"""
        else:
            return f"""Welcome to our comprehensive guide on {topic}. This detailed resource provides valuable insights and practical information for Houston-area residents and business owners.

## What You'll Learn

In this guide, we'll cover:

- Essential concepts and best practices
- Practical implementation strategies
- Professional recommendations
- Local considerations for Houston area

"""

    def _generate_main_sections(self, topic: str, keywords: list) -> str:
        """Generate main content sections."""
        if "smart home security" in topic.lower():
            return """## Essential Smart Security Components

### Wireless Security Cameras
Modern wireless cameras provide high-definition video monitoring with night vision capabilities. These systems offer:
- Weather-resistant outdoor cameras
- Indoor monitoring with privacy controls
- Mobile app access for real-time viewing
- Cloud storage for video recordings

### Smart Door Locks
Advanced smart locks offer keyless entry and remote access:
- Keypad and biometric access options
- Remote locking/unlocking capabilities
- Activity logs and user management
- Integration with home automation systems

### Motion Sensors and Alarms
Comprehensive motion detection systems include:
- Pet-friendly motion sensors
- Glass break detectors
- Door and window sensors
- Siren and notification systems

## Professional Installation Benefits

Working with certified professionals ensures:
- Proper system design and placement
- Reliable connectivity and performance
- Integration with existing systems
- Ongoing support and maintenance

## Houston-Specific Considerations

Houston's climate and architecture require special considerations:
- Weather-resistant equipment for humidity and storms
- Power backup systems for reliability
- Local code compliance
- Integration with existing home systems

"""
        elif "automation" in topic.lower():
            return """## Essential Smart Home Automation Components

### Voice Control Systems
Modern voice assistants provide hands-free control:
- Amazon Alexa and Google Assistant integration
- Whole-home voice control capabilities
- Custom voice commands for family routines
- Multi-room audio and announcements

### Smart Lighting Control
Automated lighting systems enhance comfort and efficiency:
- Dimmer controls and color-changing bulbs
- Motion-activated lighting
- Scheduled lighting for security
- Energy-efficient LED integration

### Climate Control Automation
Smart thermostats optimize comfort and energy usage:
- Programmable temperature schedules
- Remote access and control
- Energy usage monitoring
- Integration with HVAC systems

### Security and Monitoring
Comprehensive security integration:
- Door and window sensors
- Motion detection systems
- Camera integration and monitoring
- Mobile app notifications

## Professional Installation Benefits

Working with certified automation professionals ensures:
- Proper system design and component selection
- Seamless integration of all systems
- Professional wiring and setup
- Family training and ongoing support

## Houston-Specific Considerations

Houston's climate and architecture require special considerations:
- Humidity control for equipment protection
- Power conditioning for stable operation
- Integration with existing home systems
- Local code compliance and permits

"""
        elif "theater" in topic.lower():
            return """## Essential Home Theater Components

### 4K and 8K Projectors
Modern projectors deliver stunning visual experiences:
- Ultra-high definition 4K and 8K resolution
- HDR support for enhanced color and contrast
- Laser projection for long-lasting performance
- Smart connectivity for streaming services

### Surround Sound Systems
Immersive audio systems create cinematic experiences:
- Dolby Atmos and DTS:X support
- Multiple speaker configurations
- Wireless subwoofer options
- Room calibration for optimal sound

### Acoustic Treatment
Professional acoustic design ensures optimal sound quality:
- Sound-absorbing panels and bass traps
- Room acoustics analysis and treatment
- Noise isolation for external disturbances
- Custom acoustic solutions

## Professional Installation Benefits

Working with certified AV professionals ensures:
- Proper system design and component selection
- Optimal speaker and projector placement
- Professional wiring and cable management
- Integration with smart home systems

## Houston-Specific Considerations

Houston's climate and architecture require special considerations:
- Humidity control for equipment protection
- Power conditioning for stable operation
- Room design for optimal acoustics
- Integration with existing home systems

"""
        else:
            return """## Key Components and Features

### Core Technology
Understanding the fundamental technology behind these systems is essential for making informed decisions.

### Implementation Strategies
Professional implementation ensures optimal performance and reliability.

### Maintenance and Support
Ongoing support and maintenance are crucial for long-term success.

## Professional Services

Working with experienced professionals provides:
- Expert consultation and design
- Professional installation and setup
- Training and support
- Ongoing maintenance and updates

"""

    def _generate_conclusion(self, topic: str) -> str:
        """Generate conclusion based on topic."""
        if "smart home security" in topic.lower():
            return """## Protecting Your Houston Home

Smart home security systems provide comprehensive protection for your Houston home while offering the convenience and control you need. With professional installation and ongoing support, these systems deliver peace of mind and enhanced security.

The investment in smart security technology pays dividends through improved safety, convenience, and potentially reduced insurance costs. For Houston homeowners and business owners, these systems represent a smart choice for modern living.

"""
        elif "automation" in topic.lower():
            return """## Creating Your Smart Home Experience

Professional home automation installation transforms your Houston home into a smart, connected living space. With expert design, installation, and ongoing support, these systems deliver unparalleled convenience and efficiency.

The investment in smart home automation technology pays dividends through enhanced comfort, energy savings, increased home value, and years of convenience. For Houston families, these systems represent the future of modern living.

"""
        elif "theater" in topic.lower():
            return """## Creating Your Ultimate Entertainment Experience

Professional home theater installation transforms your Houston home into a premium entertainment destination. With expert design, installation, and ongoing support, these systems deliver unparalleled entertainment experiences.

The investment in professional home theater technology pays dividends through enhanced entertainment value, increased home value, and years of enjoyment. For Houston homeowners and entertainment enthusiasts, these systems represent the ultimate in home entertainment.

"""
        else:
            return f"""## Moving Forward with {topic}

This comprehensive approach to {topic} provides the foundation for success. Professional implementation and ongoing support ensure optimal results for Houston-area residents and businesses.

The investment in quality solutions pays dividends through improved performance, reliability, and long-term value. For Houston residents and business owners, these systems represent a smart choice for modern living.

"""

    def _generate_cta(self) -> str:
        """Generate call-to-action section."""
        return """## Ready to Get Started?

**Executive Technology Group** is your trusted partner for technology solutions in Houston and surrounding areas. We specialize in:

- **Smart Home Automation** - Seamless integration and control
- **Home Theater & AV Systems** - Premium entertainment experiences  
- **Networking Solutions** - Reliable, high-speed connectivity
- **Security & Surveillance** - Advanced protection systems
- **Lighting Control** - Energy-efficient, automated lighting

### Why Choose Executive Technology Group?

- ✅ **20+ Years Experience** - Proven expertise in technology integration
- ✅ **Certified Installers** - Thoroughly trained and certified team
- ✅ **Quality & Reliability** - Dependable, high-quality services
- ✅ **Veteran Owned & Operated** - Trusted by Houston businesses and homeowners

### Ready to Get Started?

**Call us today for a free consultation:** [(281) 826-1880](tel:281-826-1880)

**Visit our website:** [www.executivetechnologygroup.com](https://www.executivetechnologygroup.com/)

*Serving Houston & surrounding areas with professional technology solutions that just work.*

"""


class GeminiAIProvider(BaseAIProvider):
    """Google Gemini AI provider."""
    
    def __init__(self, api_key: str):
        super().__init__("gemini")
        self.api_key = api_key
        self.rate_limiter = get_rate_limiter("gemini")
    
    async def generate_content(self, prompt: str) -> str:
        """
        Generate content using Google Gemini API.
        
        Args:
            prompt: Generation prompt
            
        Returns:
            Generated content
        """
        # This would integrate with the actual Gemini API
        # For now, we'll use the mock provider
        mock_provider = MockAIProvider()
        return await mock_provider.generate_content(prompt)


class ContentGenerator:
    """Main content generation orchestrator."""
    
    def __init__(self, ai_provider: BaseAIProvider):
        """
        Initialize content generator.
        
        Args:
            ai_provider: AI provider instance
        """
        self.ai_provider = ai_provider
        self.logger = get_logger("content_generator")
        self.generated_titles = set()  # Track generated titles to avoid duplicates
    
    async def generate_article(self, blog_config: BlogConfig) -> Article:
        """
        Generate a complete article for a blog.
        
        Args:
            blog_config: Blog configuration
            
        Returns:
            Generated article
        """
        with LogContext(self.logger, "generate_article", 
                       blog_id=blog_config.id, niche=blog_config.niche):
            
            try:
                # Generate article ID
                article_id = f"art_{uuid.uuid4().hex[:8]}"
                
                # Create generation prompt
                prompt = self._create_prompt(blog_config)
                
                # Generate content
                content = await self._generate_content_with_retry(prompt)
                
                # Extract title and meta description
                title = self._extract_title(content)
                
                # Check for duplicate titles and add variation if needed
                original_title = title
                counter = 1
                while title in self.generated_titles:
                    title = f"{original_title} - Part {counter}"
                    counter += 1
                    if counter > 10:  # Prevent infinite loop
                        title = f"{original_title} - {datetime.now().strftime('%Y%m%d')}"
                        break
                
                # Add to generated titles set
                self.generated_titles.add(title)
                
                meta_description = self._generate_meta_description(content, blog_config)
                
                # Create article
                article = Article(
                    id=article_id,
                    title=title,
                    content=content,
                    meta_description=meta_description,
                    keywords=blog_config.keywords,
                    word_count=len(content.split()),
                    blog_id=blog_config.id,
                    created_at=datetime.now()
                )
                
                self.logger.info(f"Generated article: {title}")
                return article
                
            except Exception as e:
                self.logger.error(f"Failed to generate article: {e}")
                raise GenerationError(f"Content generation failed: {e}")
    
    async def generate_article_with_prompt(self, blog_config: BlogConfig, custom_prompt: str) -> Article:
        """
        Generate a complete article with a custom prompt.
        
        Args:
            blog_config: Blog configuration
            custom_prompt: Custom generation prompt
            
        Returns:
            Generated article
        """
        with LogContext(self.logger, "generate_article_with_prompt", 
                       blog_id=blog_config.id, niche=blog_config.niche):
            
            try:
                # Generate article ID
                article_id = f"art_{uuid.uuid4().hex[:8]}"
                
                # Add dynamic variation to the custom prompt
                enhanced_prompt = self._add_dynamic_variation_to_prompt(custom_prompt)
                
                # Generate content with enhanced prompt
                content = await self._generate_content_with_retry(enhanced_prompt)
                
                # Extract title and meta description
                title = self._extract_title(content)
                
                # Check for duplicate titles and add variation if needed
                original_title = title
                counter = 1
                while title in self.generated_titles:
                    title = f"{original_title} - Part {counter}"
                    counter += 1
                    if counter > 10:  # Prevent infinite loop
                        title = f"{original_title} - {datetime.now().strftime('%Y%m%d')}"
                        break
                
                # Add to generated titles set
                self.generated_titles.add(title)
                
                meta_description = self._generate_meta_description(content, blog_config)
                
                # Create article
                article = Article(
                    id=article_id,
                    title=title,
                    content=content,
                    meta_description=meta_description,
                    keywords=blog_config.keywords,
                    word_count=len(content.split()),
                    blog_id=blog_config.id,
                    created_at=datetime.now()
                )
                
                self.logger.info(f"Generated custom article: {title}")
                return article
                
            except Exception as e:
                self.logger.error(f"Failed to generate custom article: {e}")
                raise GenerationError(f"Custom content generation failed: {e}")
    
    def _create_prompt(self, blog_config: BlogConfig) -> str:
        """Create generation prompt from blog configuration with dynamic variation."""
        import random
        from datetime import datetime
        
        # Add dynamic elements to prevent duplicate content
        current_time = datetime.now()
        time_variations = [
            f"in {current_time.year}",
            f"for {current_time.strftime('%B %Y')}",
            f"in the current market",
            f"for today's {blog_config.target_audience}",
            f"in the modern era"
        ]
        
        angle_variations = [
            "comprehensive guide",
            "detailed analysis", 
            "practical tips and insights",
            "expert recommendations",
            "step-by-step approach",
            "in-depth exploration",
            "professional advice",
            "industry best practices"
        ]
        
        focus_variations = [
            "focusing on practical applications",
            "emphasizing real-world benefits",
            "highlighting key advantages",
            "covering essential aspects",
            "providing actionable insights",
            "addressing common challenges",
            "offering expert solutions",
            "delivering valuable information"
        ]
        
        # Randomly select variations
        time_context = random.choice(time_variations)
        article_angle = random.choice(angle_variations)
        focus_approach = random.choice(focus_variations)
        
        # Add topic-specific variations
        topic_variations = self._get_topic_variations(blog_config.niche)
        specific_topic = random.choice(topic_variations)
        
        # Add seasonal/trending context
        seasonal_contexts = [
            "current trends and developments",
            "emerging technologies and solutions", 
            "latest industry insights",
            "modern approaches and techniques",
            "contemporary best practices",
            "cutting-edge strategies",
            "innovative solutions",
            "advanced methodologies"
        ]
        
        trending_context = random.choice(seasonal_contexts)
        
        prompt = f"""
Write a {article_angle} about {specific_topic} {time_context}.

Target audience: {blog_config.target_audience}
Tone: {blog_config.tone}
Word count: approximately {blog_config.word_count} words
Keywords to include: {', '.join(blog_config.keywords)}

The article should be:
- Well-structured with clear headings
- Informative and engaging
- SEO-friendly with natural keyword integration
- Practical and actionable
- Original and valuable content
- {focus_approach}
- Covering {trending_context}

Format the article with proper headings (H2, H3) and include:
- An engaging introduction that hooks the reader
- Main content sections with subheadings
- Practical tips or actionable advice
- Real-world examples and case studies
- A compelling conclusion with clear next steps

Make this article unique and valuable by:
- Including specific examples relevant to {blog_config.target_audience}
- Providing actionable insights they can implement immediately
- Addressing common pain points and challenges
- Offering expert-level advice and recommendations

Do not include any meta information or instructions in the output - just the article content.
"""
        return prompt.strip()
    
    def _get_topic_variations(self, niche: str) -> list:
        """Get topic variations based on the niche."""
        variations = {
            "smart home technology and automation": [
                "smart home security systems",
                "home automation for energy efficiency", 
                "voice-controlled smart devices",
                "smart lighting solutions",
                "home theater automation",
                "smart home networking",
                "commercial AV integration",
                "smart home maintenance",
                "home automation ROI",
                "smart home troubleshooting"
            ],
            "sustainable gardening": [
                "eco-friendly gardening techniques",
                "organic pest control methods",
                "water-efficient gardening",
                "composting for beginners",
                "native plant landscaping",
                "seasonal garden planning",
                "sustainable soil management",
                "greenhouse gardening tips",
                "pollinator-friendly gardens",
                "urban gardening solutions"
            ]
        }
        
        # Default variations if niche not found
        default_variations = [
            f"advanced {niche} techniques",
            f"beginner-friendly {niche}",
            f"{niche} best practices",
            f"common {niche} mistakes",
            f"{niche} troubleshooting",
            f"professional {niche} services",
            f"{niche} cost analysis",
            f"{niche} maintenance tips"
        ]
        
        return variations.get(niche.lower(), default_variations)
    
    def _add_dynamic_variation_to_prompt(self, custom_prompt: str) -> str:
        """Add dynamic variation to a custom prompt to prevent duplicate content."""
        import random
        from datetime import datetime
        
        # Add dynamic elements to prevent duplicate content
        current_time = datetime.now()
        time_variations = [
            f"in {current_time.year}",
            f"for {current_time.strftime('%B %Y')}",
            f"in the current market",
            f"for today's customers",
            f"in the modern era"
        ]
        
        angle_variations = [
            "comprehensive guide",
            "detailed analysis", 
            "practical tips and insights",
            "expert recommendations",
            "step-by-step approach",
            "in-depth exploration",
            "professional advice",
            "industry best practices"
        ]
        
        focus_variations = [
            "focusing on practical applications",
            "emphasizing real-world benefits",
            "highlighting key advantages",
            "covering essential aspects",
            "providing actionable insights",
            "addressing common challenges",
            "offering expert solutions",
            "delivering valuable information"
        ]
        
        # Randomly select variations
        time_context = random.choice(time_variations)
        article_angle = random.choice(angle_variations)
        focus_approach = random.choice(focus_variations)
        
        # Add seasonal/trending context
        seasonal_contexts = [
            "current trends and developments",
            "emerging technologies and solutions", 
            "latest industry insights",
            "modern approaches and techniques",
            "contemporary best practices",
            "cutting-edge strategies",
            "innovative solutions",
            "advanced methodologies"
        ]
        
        trending_context = random.choice(seasonal_contexts)
        
        # Enhance the custom prompt with dynamic elements
        enhanced_prompt = f"""
{custom_prompt}

IMPORTANT: Make this article unique and fresh by:
- {focus_approach}
- Covering {trending_context}
- Writing as a {article_angle} {time_context}
- Including specific examples and real-world applications
- Providing actionable insights readers can implement immediately
- Addressing current market conditions and trends
- Offering expert-level advice and recommendations

Ensure the content is original, valuable, and different from any previous articles.
"""
        return enhanced_prompt.strip()
    
    def clear_generated_titles(self):
        """Clear the generated titles set (useful for testing or reset)."""
        self.generated_titles.clear()
        self.logger.info("Cleared generated titles cache")
    
    @retry(max_attempts=3, on_exceptions=(APIError, RateLimitError))
    async def _generate_content_with_retry(self, prompt: str) -> str:
        """Generate content with retry logic."""
        # Apply rate limiting
        await self.ai_provider.rate_limiter.acquire()
        
        # Generate content
        content = await self.ai_provider.generate_content(prompt)
        
        if not content or len(content.strip()) < 100:
            raise GenerationError("Generated content is too short or empty")
        
        return content
    
    def _extract_title(self, content: str) -> str:
        """Extract title from content (first H1 or first line)."""
        lines = content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                return line[2:].strip()
            elif line and not line.startswith('#'):
                # Use first non-empty line as title
                return line[:100]  # Limit length
        
        return "Generated Article"
    
    def _generate_meta_description(self, content: str, blog_config: BlogConfig) -> str:
        """Generate meta description from content."""
        # Extract first paragraph or create from content
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        if paragraphs:
            first_para = paragraphs[0]
            # Remove markdown formatting
            first_para = first_para.replace('**', '').replace('*', '')
            # Limit to 160 characters
            if len(first_para) > 160:
                first_para = first_para[:157] + "..."
            return first_para
        
        # Fallback description
        return f"Learn about {blog_config.niche} for {blog_config.target_audience}. " \
               f"Comprehensive guide with practical tips and insights."


def create_ai_provider(provider_name: str, api_key: Optional[str] = None) -> BaseAIProvider:
    """
    Create AI provider instance.
    
    Args:
        provider_name: Name of the provider (real, mock, gemini, groq)
        api_key: API key for the provider
        
    Returns:
        AI provider instance
    """
    if provider_name == "real":
        return RealAIProvider()
    elif provider_name == "mock":
        return MockAIProvider()
    elif provider_name == "gemini":
        if not api_key:
            raise ValueError("API key required for Gemini provider")
        return GeminiAIProvider(api_key)
    else:
        raise ValueError(f"Unknown AI provider: {provider_name}")
