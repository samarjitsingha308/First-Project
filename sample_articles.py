"""
Sample script to populate the search engine with example articles
Run this after starting the server to add some test data
"""

import requests
import json

API_BASE = "http://localhost:8000"

sample_articles = [
    {
        "title": "Introduction to Machine Learning",
        "content": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It focuses on developing computer programs that can access data and use it to learn for themselves. The process of learning begins with observations or data, such as examples, direct experience, or instruction, to look for patterns in data and make better decisions in the future.",
        "author": "Dr. Sarah Johnson",
        "tags": ["AI", "machine learning", "technology", "education"]
    },
    {
        "title": "Healthy Eating Habits for Busy Professionals",
        "content": "Maintaining a healthy diet while managing a busy professional life can be challenging. Start by meal prepping on weekends, keeping healthy snacks at your desk, and staying hydrated throughout the day. Choose whole grains, lean proteins, and plenty of fruits and vegetables. Avoid skipping meals and try to eat at regular intervals to maintain your energy levels and metabolism.",
        "author": "Emily Chen",
        "tags": ["health", "nutrition", "lifestyle", "wellness"]
    },
    {
        "title": "Getting Started with Web Development",
        "content": "Web development is an exciting field that combines creativity with technical skills. Begin your journey by learning HTML for structure, CSS for styling, and JavaScript for interactivity. Modern web development also involves frameworks like React, Vue, or Angular. Understanding responsive design principles and accessibility standards is crucial for creating websites that work well across all devices and for all users.",
        "author": "Alex Martinez",
        "tags": ["web development", "programming", "HTML", "CSS", "JavaScript"]
    },
    {
        "title": "The Benefits of Meditation and Mindfulness",
        "content": "Meditation and mindfulness practices have been shown to reduce stress, improve focus, and enhance overall well-being. Regular meditation can help lower blood pressure, reduce anxiety, and improve sleep quality. Start with just 5-10 minutes per day, focusing on your breath and being present in the moment. Apps and guided meditations can help beginners establish a consistent practice.",
        "author": "Dr. Michael Thompson",
        "tags": ["mental health", "mindfulness", "meditation", "wellness"]
    },
    {
        "title": "Understanding Climate Change and Its Impact",
        "content": "Climate change refers to long-term shifts in global temperatures and weather patterns. While climate change is a natural phenomenon, scientific evidence shows that human activities, particularly the burning of fossil fuels, have accelerated these changes dramatically since the industrial revolution. The impacts include rising sea levels, extreme weather events, and disruptions to ecosystems. Taking action through renewable energy adoption, sustainable practices, and policy changes is crucial for our planet's future.",
        "author": "Dr. Jennifer Lee",
        "tags": ["environment", "climate change", "sustainability", "science"]
    },
    {
        "title": "Python Programming for Data Science",
        "content": "Python has become the dominant language for data science due to its simplicity and powerful libraries. Key libraries include NumPy for numerical computing, Pandas for data manipulation, Matplotlib and Seaborn for visualization, and Scikit-learn for machine learning. Learning Python for data science opens doors to careers in analytics, artificial intelligence, and business intelligence. Start with basic Python syntax, then progress to data structures and algorithms before diving into specialized libraries.",
        "author": "Robert Kim",
        "tags": ["Python", "data science", "programming", "analytics"]
    },
    {
        "title": "Travel Tips for Budget-Conscious Explorers",
        "content": "Traveling doesn't have to break the bank. Book flights in advance and be flexible with dates to find the best deals. Consider staying in hostels, using Airbnb, or even house-sitting. Cook your own meals occasionally and take advantage of free walking tours. Use public transportation instead of taxis, and look for city passes that offer discounts on attractions. Research free activities and local festivals that happen during your visit.",
        "author": "Maria Rodriguez",
        "tags": ["travel", "budget", "adventure", "tips"]
    },
    {
        "title": "The Future of Renewable Energy",
        "content": "Renewable energy sources like solar, wind, and hydroelectric power are rapidly becoming more efficient and cost-effective. Solar panel technology has improved dramatically, making it accessible for residential use. Wind farms are generating significant portions of electricity in many countries. Energy storage solutions, particularly battery technology, are addressing the intermittency challenges of renewables. The transition to renewable energy is essential for reducing carbon emissions and combating climate change.",
        "author": "David Wilson",
        "tags": ["renewable energy", "sustainability", "solar", "environment"]
    },
    {
        "title": "Effective Communication Skills in the Workplace",
        "content": "Strong communication skills are essential for professional success. Practice active listening by giving full attention to speakers and asking clarifying questions. Be clear and concise in your messages, whether written or verbal. Adapt your communication style to your audience and use appropriate channels for different types of messages. Non-verbal communication, including body language and tone, is just as important as words. Regular feedback and open dialogue foster better team collaboration.",
        "author": "Lisa Anderson",
        "tags": ["communication", "workplace", "professional development", "soft skills"]
    },
    {
        "title": "Understanding Blockchain Technology",
        "content": "Blockchain is a decentralized, distributed ledger technology that records transactions across multiple computers. Each block contains a cryptographic hash of the previous block, timestamp, and transaction data. This makes the blockchain resistant to modification and provides transparency. While Bitcoin made blockchain famous, the technology has applications beyond cryptocurrency, including supply chain management, smart contracts, and secure voting systems. Understanding blockchain is increasingly important in the digital economy.",
        "author": "Thomas Brown",
        "tags": ["blockchain", "cryptocurrency", "technology", "innovation"]
    }
]

def create_articles():
    """Create sample articles via API"""
    print("🚀 Creating sample articles...")
    print(f"Connecting to {API_BASE}")
    print()
    
    created_count = 0
    failed_count = 0
    
    for i, article in enumerate(sample_articles, 1):
        try:
            response = requests.post(
                f"{API_BASE}/api/articles",
                json=article,
                timeout=30
            )
            
            if response.status_code == 200:
                created_count += 1
                print(f"✅ [{i}/{len(sample_articles)}] Created: {article['title']}")
            else:
                failed_count += 1
                print(f"❌ [{i}/{len(sample_articles)}] Failed: {article['title']} - {response.status_code}")
        
        except requests.exceptions.ConnectionError:
            print("❌ Could not connect to the server. Make sure the server is running on http://localhost:8000")
            print("   Start the server with: python app.py")
            return
        except Exception as e:
            failed_count += 1
            print(f"❌ [{i}/{len(sample_articles)}] Error: {article['title']} - {str(e)}")
    
    print()
    print(f"📊 Summary: {created_count} created, {failed_count} failed")
    print()
    print("🎉 Done! You can now search these articles at http://localhost:8000")

if __name__ == "__main__":
    create_articles()
