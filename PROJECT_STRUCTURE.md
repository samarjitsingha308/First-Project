# 📋 Project Structure

Complete overview of the BERT Search Engine project structure and components.

## 📁 Directory Structure

```
workspace/
├── app.py                  # Main FastAPI application
├── search_engine.py        # BERT search engine implementation
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
│
├── start.sh               # Quick start script (Linux/Mac)
├── sample_articles.py     # Script to populate sample data
├── test_setup.py          # Setup validation script
│
├── README.md              # Main documentation
├── QUICKSTART.md          # Quick start guide
├── PROJECT_STRUCTURE.md   # This file
│
├── static/                # Frontend files
│   ├── index.html         # Main UI page
│   ├── styles.css         # Styling
│   └── script.js          # Frontend logic
│
└── articles.json          # Created automatically (data storage)
```

## 🔧 Core Components

### 1. Backend (`app.py`)

**Purpose**: Main API server using FastAPI

**Key Features**:
- RESTful API endpoints
- Article CRUD operations
- Search endpoint with BERT integration
- Static file serving
- JSON-based persistent storage

**API Endpoints**:
```
GET  /                      → Serve frontend
POST /api/articles          → Create article
GET  /api/articles          → Get all articles
GET  /api/articles/{id}     → Get specific article
DELETE /api/articles/{id}   → Delete article
POST /api/search            → Search articles
```

**Data Models**:
- `Article`: For creating articles (title, content, author, tags)
- `SearchQuery`: For search requests (query, top_k)
- `ArticleResponse`: For API responses (includes similarity_score)

### 2. Search Engine (`search_engine.py`)

**Purpose**: BERT-powered semantic search implementation

**Key Features**:
- Uses Sentence Transformers library
- Default model: `all-MiniLM-L6-v2` (fast, 80MB)
- Cosine similarity for ranking
- In-memory vector storage
- Supports batch indexing

**Main Methods**:
```python
BERTSearchEngine(model_name)  # Initialize with model
add_article(article)          # Add single article to index
index_articles(articles)      # Batch index articles
search(query, top_k)          # Semantic search
get_stats()                   # Get statistics
```

**How It Works**:
1. Articles → BERT → Embeddings (384-dimensional vectors)
2. Query → BERT → Query embedding
3. Cosine similarity between query and all articles
4. Return top-k most similar articles with scores

### 3. Frontend (`static/`)

#### `index.html`
- Three-tab interface (Search, Create, Browse)
- Responsive design
- Form validation
- Loading states

#### `styles.css`
- Modern gradient theme (purple/blue)
- Card-based layout
- Hover effects and transitions
- Mobile-responsive
- ~300 lines of clean CSS

#### `script.js`
- Tab switching
- API communication (fetch)
- Dynamic result rendering
- Error handling
- XSS prevention (HTML escaping)

## 🔄 Data Flow

### Creating an Article

```
User fills form → Frontend validates
    ↓
POST /api/articles
    ↓
app.py receives data
    ↓
Save to articles.json
    ↓
Add to search_engine index
    ↓
Return success to frontend
```

### Searching Articles

```
User enters query → Frontend sends request
    ↓
POST /api/search
    ↓
search_engine.search(query)
    ↓
BERT encodes query
    ↓
Calculate cosine similarity with all articles
    ↓
Sort by similarity, return top-k
    ↓
Frontend displays results with scores
```

## 🗄️ Data Storage

### `articles.json`

**Format**:
```json
[
  {
    "id": "1",
    "title": "Article Title",
    "content": "Article content...",
    "author": "Author Name",
    "tags": ["tag1", "tag2"],
    "created_at": "2025-12-29T12:00:00"
  }
]
```

**Location**: Root directory (created automatically)

**Persistence**: 
- Written on every article creation/deletion
- Loaded on server startup
- Embeddings regenerated on startup (not persisted)

## 📦 Dependencies

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.109.0 | Web framework |
| uvicorn | 0.27.0 | ASGI server |
| sentence-transformers | 2.3.1 | BERT models |
| torch | 2.1.2 | Deep learning |
| numpy | 1.26.3 | Numerical operations |
| scikit-learn | 1.4.0 | Similarity calculations |
| pydantic | 2.5.3 | Data validation |

### Installation

```bash
pip3 install -r requirements.txt
```

**Note**: First run downloads BERT model (~80MB) from HuggingFace.

## 🚀 Startup Process

1. **Server Start**:
   ```bash
   python3 app.py
   ```

2. **Initialization**:
   - Load FastAPI application
   - Import search_engine module
   - Load articles.json (if exists)
   - Initialize BERT model (first time: download)
   - Index all existing articles
   - Start Uvicorn server on port 8000

3. **Ready State**:
   - API endpoints available
   - Frontend accessible at http://localhost:8000
   - Search engine ready for queries

## 🧪 Testing & Validation

### `test_setup.py`

**Purpose**: Validate environment before running

**Checks**:
- Python version (3.8+)
- Required files exist
- Dependencies installed
- Modules can be imported

**Usage**:
```bash
python3 test_setup.py
```

### `sample_articles.py`

**Purpose**: Populate with test data

**Contents**: 10 diverse articles covering:
- Technology (AI, Web Dev, Blockchain)
- Health (Nutrition, Meditation)
- Environment (Climate, Renewable Energy)
- Lifestyle (Travel, Communication)

**Usage**:
```bash
python3 sample_articles.py
```

## 🎨 UI Features

### Search Tab
- Text input with Enter key support
- Results selector (5/10/15/20)
- Similarity score badges
- Article cards with metadata
- Truncated content preview

### Create Tab
- Required fields: Title, Content
- Optional: Author, Tags
- Success/error messages
- Form reset on success

### Browse Tab
- List all articles
- Delete functionality
- Refresh button
- Empty state message

## 🔐 Security Considerations

### Current Implementation
- XSS prevention (HTML escaping)
- Input validation (Pydantic)
- No SQL injection risk (JSON storage)

### Production Recommendations
- Add authentication/authorization
- Rate limiting
- Input sanitization
- CORS configuration
- HTTPS/SSL
- Database with proper security

## ⚡ Performance

### Current Setup
- In-memory search (fast)
- Single-threaded (good for demo)
- No caching
- Simple JSON storage

### Optimization Ideas
- Add embedding caching
- Use vector database (FAISS, Pinecone)
- Implement pagination
- Add Redis for caching
- Async database operations
- Load balancing for production

## 🛠️ Customization

### Change BERT Model

Edit `search_engine.py`:
```python
search_engine = BERTSearchEngine(model_name="all-mpnet-base-v2")
```

### Change Port

Edit `app.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8080)
```

### Modify UI Theme

Edit `static/styles.css`:
```css
background: linear-gradient(135deg, #your-color 0%, #your-color2 100%);
```

### Add Fields to Articles

1. Update `Article` model in `app.py`
2. Update form in `static/index.html`
3. Update display logic in `static/script.js`

## 📊 Project Statistics

- **Total Files**: 12
- **Lines of Code**: ~1,200
- **Languages**: Python, JavaScript, HTML, CSS
- **API Endpoints**: 6
- **BERT Model Size**: 80MB
- **Embedding Dimension**: 384

## 🎯 Key Design Decisions

1. **Sentence Transformers**: Pre-trained models for quick setup
2. **JSON Storage**: Simple, no external database needed
3. **FastAPI**: Modern, fast, automatic API docs
4. **Vanilla JS**: No framework dependencies, lightweight
5. **In-Memory Search**: Fast, suitable for moderate data sizes
6. **All-MiniLM-L6-v2**: Best balance of speed and quality

## 🔄 Future Enhancements

Potential improvements:
- [ ] User authentication
- [ ] Article categories
- [ ] Advanced filters
- [ ] Export/import functionality
- [ ] Search history
- [ ] Article versioning
- [ ] Multi-language support
- [ ] API documentation UI (Swagger)
- [ ] Unit tests
- [ ] Docker containerization

---

For quick start instructions, see [QUICKSTART.md](QUICKSTART.md)

For detailed documentation, see [README.md](README.md)
