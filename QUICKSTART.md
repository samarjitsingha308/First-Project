# 🚀 Quick Start Guide

Get your BERT search engine running in 3 simple steps!

## Step 1: Install Dependencies

```bash
pip3 install -r requirements.txt
```

**Note**: The first time you run the application, it will download the BERT model (~80MB). This is a one-time download and will be cached for future use.

## Step 2: Start the Server

### Option A: Using the start script (Linux/Mac)
```bash
./start.sh
```

### Option B: Using Python directly
```bash
python3 app.py
```

### Option C: Using Uvicorn (with auto-reload for development)
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Step 3: Open in Browser

Navigate to: **http://localhost:8000**

## 🎯 Next Steps

### Add Sample Data (Optional)

To quickly test the search functionality, add sample articles:

1. Make sure the server is running (Step 2)
2. Open a new terminal
3. Run:
```bash
python3 sample_articles.py
```

This will add 10 sample articles covering various topics like AI, health, web development, and more!

### Try These Searches

After adding sample data, try these semantic search queries:

- "artificial intelligence" → Find ML and AI articles
- "staying healthy" → Find nutrition and wellness articles
- "building websites" → Find web development content
- "stress relief" → Find meditation and mindfulness articles
- "sustainable energy" → Find environmental and renewable energy articles

## 📱 Using the Application

### Creating Articles

1. Click **"Create Article"** tab
2. Fill in the form (Title and Content are required)
3. Click **"Create Article"** button
4. Your article is now searchable!

### Searching Articles

1. Go to **"Search Articles"** tab
2. Enter your search query (keywords or natural language)
3. Select number of results (5, 10, 15, or 20)
4. Click **"Search"** button
5. Results show similarity scores (higher = better match)

### Browsing All Articles

1. Click **"Browse All"** tab
2. View all articles
3. Delete articles if needed

## 🔧 Troubleshooting

### Port Already in Use

If port 8000 is already in use:
```bash
uvicorn app:app --port 8080
```
Then open: http://localhost:8080

### Dependencies Installation Failed

Make sure you have Python 3.8 or higher:
```bash
python3 --version
```

Upgrade pip:
```bash
pip3 install --upgrade pip
```

### BERT Model Download Issues

If the model download fails:
1. Check your internet connection
2. Try running again (downloads will resume)
3. Or manually specify a different model in `search_engine.py`

## 💡 Tips

- **Search is semantic**: "AI" will match "artificial intelligence" and "machine learning"
- **Use natural language**: "How to build a website" works better than just "website"
- **Tags improve search**: Add relevant tags when creating articles
- **Similarity scores**: 70%+ is usually a good match

## 🎉 You're All Set!

Enjoy your BERT-powered search engine! For more details, check the main [README.md](README.md).
