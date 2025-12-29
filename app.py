"""
BERT-powered Search Engine Backend
Provides API endpoints for article creation and semantic search
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import json
import os
from datetime import datetime
from search_engine import BERTSearchEngine

app = FastAPI(title="BERT Search Engine")

# Initialize the search engine
search_engine = BERTSearchEngine()

# Data models
class Article(BaseModel):
    title: str
    content: str
    author: Optional[str] = "Anonymous"
    tags: Optional[List[str]] = []

class SearchQuery(BaseModel):
    query: str
    top_k: Optional[int] = 5
    mode: Optional[str] = "hybrid"  # "semantic", "keyword", or "hybrid"
    semantic_weight: Optional[float] = 0.7  # Weight for semantic in hybrid mode

class ContentSnippet(BaseModel):
    start: int
    end: int
    text: str

class ArticleResponse(BaseModel):
    id: str
    title: str
    content: str
    author: str
    tags: List[str]
    created_at: str
    similarity_score: Optional[float] = None
    semantic_score: Optional[float] = None
    keyword_score: Optional[float] = None
    keyword_match_ratio: Optional[float] = None
    matched_keywords: Optional[List[str]] = []
    content_snippets: Optional[List[ContentSnippet]] = []
    title_has_keywords: Optional[bool] = False

# Storage file
ARTICLES_FILE = "articles.json"

def load_articles():
    """Load articles from JSON file"""
    if os.path.exists(ARTICLES_FILE):
        with open(ARTICLES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_articles(articles):
    """Save articles to JSON file"""
    with open(ARTICLES_FILE, 'w') as f:
        json.dump(articles, f, indent=2)

@app.on_event("startup")
async def startup_event():
    """Initialize search engine with existing articles"""
    articles = load_articles()
    if articles:
        search_engine.index_articles(articles)
        print(f"Loaded {len(articles)} articles into search engine")

@app.get("/")
async def root():
    """Serve the main HTML page"""
    return FileResponse("static/index.html")

@app.post("/api/articles", response_model=ArticleResponse)
async def create_article(article: Article):
    """Create a new article and add it to the search index"""
    articles = load_articles()
    
    # Create new article with metadata
    new_article = {
        "id": str(len(articles) + 1),
        "title": article.title,
        "content": article.content,
        "author": article.author,
        "tags": article.tags,
        "created_at": datetime.now().isoformat()
    }
    
    articles.append(new_article)
    save_articles(articles)
    
    # Add to search index
    search_engine.add_article(new_article)
    
    return ArticleResponse(**new_article)

@app.get("/api/articles", response_model=List[ArticleResponse])
async def get_all_articles():
    """Get all articles"""
    articles = load_articles()
    return [ArticleResponse(**article) for article in articles]

@app.get("/api/articles/{article_id}", response_model=ArticleResponse)
async def get_article(article_id: str):
    """Get a specific article by ID"""
    articles = load_articles()
    for article in articles:
        if article["id"] == article_id:
            return ArticleResponse(**article)
    raise HTTPException(status_code=404, detail="Article not found")

@app.post("/api/search", response_model=List[ArticleResponse])
async def search_articles(query: SearchQuery):
    """Search articles using hybrid search (semantic + keyword matching)"""
    if not query.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    # Validate mode
    if query.mode not in ["semantic", "keyword", "hybrid"]:
        raise HTTPException(status_code=400, detail="Mode must be 'semantic', 'keyword', or 'hybrid'")
    
    # Validate semantic_weight
    if not 0 <= query.semantic_weight <= 1:
        raise HTTPException(status_code=400, detail="semantic_weight must be between 0 and 1")
    
    results = search_engine.search(
        query.query, 
        top_k=query.top_k,
        mode=query.mode,
        semantic_weight=query.semantic_weight
    )
    
    return [
        ArticleResponse(
            id=result["id"],
            title=result["title"],
            content=result["content"],
            author=result["author"],
            tags=result["tags"],
            created_at=result["created_at"],
            similarity_score=result.get("similarity_score"),
            semantic_score=result.get("semantic_score"),
            keyword_score=result.get("keyword_score"),
            keyword_match_ratio=result.get("keyword_match_ratio"),
            matched_keywords=result.get("matched_keywords", []),
            content_snippets=[ContentSnippet(**snippet) for snippet in result.get("content_snippets", [])],
            title_has_keywords=result.get("title_has_keywords", False)
        )
        for result in results
    ]

@app.delete("/api/articles/{article_id}")
async def delete_article(article_id: str):
    """Delete an article"""
    articles = load_articles()
    articles = [a for a in articles if a["id"] != article_id]
    save_articles(articles)
    
    # Rebuild search index
    search_engine.index_articles(articles)
    
    return {"message": "Article deleted successfully"}

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
