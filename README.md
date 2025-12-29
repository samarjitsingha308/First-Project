# 🔍 BERT-Powered Search Engine

A modern, intelligent search engine that uses BERT (Bidirectional Encoder Representations from Transformers) for semantic search capabilities. Create, store, and search through articles using natural language understanding.

## ✨ Features

- **🔀 Hybrid Search**: Combines BERT semantic search with TF-IDF keyword matching for best results
- **🧠 BERT Semantic Search**: Understands meaning and context, not just exact words
- **🔑 Keyword Matching**: Traditional TF-IDF search for exact keyword matches
- **⚖️ Adjustable Balance**: Control the weight between semantic and keyword matching
- **📝 Article Creation**: Easy-to-use interface for creating and managing articles
- **🎯 Multiple Score Types**: See semantic, keyword, and combined similarity scores
- **🏷️ Tag Support**: Organize articles with tags for better categorization
- **💨 Fast & Efficient**: Optimized with the lightweight `all-MiniLM-L6-v2` model
- **🎨 Modern UI**: Beautiful, responsive interface built with vanilla JavaScript
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository** (if not already done):
```bash
git clone <repository-url>
cd workspace
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

This will install:
- FastAPI (web framework)
- Uvicorn (ASGI server)
- sentence-transformers (BERT models)
- PyTorch (deep learning framework)
- scikit-learn (similarity calculations)
- And other required packages

### Running the Application

1. **Start the server**:
```bash
python app.py
```

Or alternatively:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

2. **Open your browser** and navigate to:
```
http://localhost:8000
```

The first time you run the application, it will download the BERT model (~80MB). This is a one-time download.

## 📖 Usage

### Creating Articles

1. Click on the **"Create Article"** tab
2. Fill in the form:
   - **Title** (required): The title of your article
   - **Author** (optional): Your name (defaults to "Anonymous")
   - **Tags** (optional): Comma-separated tags (e.g., "AI, machine learning, technology")
   - **Content** (required): The main body of your article
3. Click **"Create Article"**

### Searching Articles

1. Go to the **"Search Articles"** tab
2. Enter your search query (keywords or natural language phrases)
3. Choose how many results to display (5, 10, 15, or 20)
4. Click **"Search"**

The search engine will:
- Understand the semantic meaning of your query
- Find articles with similar content
- Display results ranked by similarity score

### Browsing All Articles

1. Click on the **"Browse All"** tab
2. View all articles in your repository
3. Delete articles if needed

## 🏗️ Architecture

### Backend (`app.py`)
- Built with FastAPI for high-performance async operations
- RESTful API endpoints for CRUD operations
- JSON-based storage for simplicity

### Search Engine (`search_engine.py`)
- Uses `sentence-transformers` library
- Model: `all-MiniLM-L6-v2` (384-dimensional embeddings)
- Cosine similarity for ranking results
- In-memory vector storage for fast searches

### Frontend
- **HTML** (`static/index.html`): Structure
- **CSS** (`static/styles.css`): Modern, gradient-based styling
- **JavaScript** (`static/script.js`): Dynamic interactions and API calls

## 🔌 API Endpoints

### Articles

- `POST /api/articles` - Create a new article
- `GET /api/articles` - Get all articles
- `GET /api/articles/{id}` - Get a specific article
- `DELETE /api/articles/{id}` - Delete an article

### Search

- `POST /api/search` - Search articles
  ```json
  {
    "query": "machine learning algorithms",
    "top_k": 5
  }
  ```

## 🎯 How Hybrid Search Works

### Three Search Modes

1. **Hybrid Mode (Default)** - Best of both worlds
   - Combines BERT semantic understanding with TF-IDF keyword matching
   - Adjustable weight slider (default: 70% semantic, 30% keyword)
   - Finds both conceptually similar AND exact keyword matches

2. **Semantic Mode** - AI-powered understanding
   - Pure BERT embeddings
   - Understands synonyms and related concepts
   - "AI" matches "machine learning", "neural networks"

3. **Keyword Mode** - Traditional search
   - TF-IDF based keyword matching
   - Best for exact term searches
   - Fast and precise for specific words

### How It Works

**Semantic Search (BERT)**:
1. Articles converted to 384-dimensional vectors
2. Query converted to same vector space
3. Cosine similarity measures semantic closeness

**Keyword Search (TF-IDF)**:
1. Articles analyzed for term frequency
2. Query terms weighted by importance
3. TF-IDF scores measure keyword relevance

**Hybrid Search**:
- Combines both scores with adjustable weighting
- Default: 70% semantic + 30% keyword
- Customizable via UI slider

## 📊 Example Queries

Try these to see semantic search in action:

- **Query**: "artificial intelligence" → Matches: "machine learning", "neural networks", "AI"
- **Query**: "healthy eating" → Matches: "nutrition", "diet tips", "food health"
- **Query**: "web development" → Matches: "frontend coding", "HTML CSS JavaScript", "building websites"

## 🛠️ Customization

### Change BERT Model

Edit `search_engine.py` and modify the model name:

```python
search_engine = BERTSearchEngine(model_name="paraphrase-MiniLM-L6-v2")
```

Popular alternatives:
- `all-MiniLM-L6-v2` (default, fast, 80MB)
- `paraphrase-MiniLM-L6-v2` (optimized for paraphrase detection)
- `all-mpnet-base-v2` (higher quality, slower, 420MB)

### Adjust UI Theme

Edit `static/styles.css` to change colors, gradients, and styling.

## 📝 Data Storage

Articles are stored in `articles.json` in the root directory. This file is created automatically when you create your first article.

**Note**: The vector embeddings are regenerated on each startup for simplicity. For production use, consider persisting embeddings to disk.

## 🚀 Deployment Tips

For production deployment:

1. Use a proper database (PostgreSQL, MongoDB)
2. Add vector database (Pinecone, Weaviate, or FAISS)
3. Implement user authentication
4. Add rate limiting
5. Use environment variables for configuration
6. Deploy with Docker or cloud platforms (AWS, GCP, Azure)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [Sentence Transformers](https://www.sbert.net/) - For the BERT models
- [FastAPI](https://fastapi.tiangolo.com/) - For the web framework
- [Hugging Face](https://huggingface.co/) - For the transformer models

---

**Built with ❤️ using BERT and FastAPI**
