"""
BERT-based Semantic Search Engine
Uses sentence transformers to create embeddings and perform similarity search
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any

class BERTSearchEngine:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the BERT search engine
        
        Args:
            model_name: Name of the sentence-transformer model to use
                       'all-MiniLM-L6-v2' is lightweight and fast (80MB)
        """
        print(f"Loading BERT model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        self.articles = []
        self.embeddings = None
        print("BERT model loaded successfully!")
    
    def _create_searchable_text(self, article: Dict[str, Any]) -> str:
        """Combine article fields into searchable text"""
        text_parts = [
            article.get("title", ""),
            article.get("content", ""),
            " ".join(article.get("tags", []))
        ]
        return " ".join(filter(None, text_parts))
    
    def add_article(self, article: Dict[str, Any]):
        """Add a single article to the search index"""
        self.articles.append(article)
        searchable_text = self._create_searchable_text(article)
        new_embedding = self.model.encode([searchable_text])
        
        if self.embeddings is None:
            self.embeddings = new_embedding
        else:
            self.embeddings = np.vstack([self.embeddings, new_embedding])
    
    def index_articles(self, articles: List[Dict[str, Any]]):
        """
        Index multiple articles for search
        
        Args:
            articles: List of article dictionaries
        """
        if not articles:
            self.articles = []
            self.embeddings = None
            return
        
        print(f"Indexing {len(articles)} articles...")
        self.articles = articles
        
        # Create searchable text for each article
        searchable_texts = [self._create_searchable_text(article) for article in articles]
        
        # Generate embeddings
        self.embeddings = self.model.encode(searchable_texts, show_progress_bar=True)
        print(f"Indexing complete! {len(articles)} articles ready for search.")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search articles using semantic similarity
        
        Args:
            query: Search query string
            top_k: Number of top results to return
        
        Returns:
            List of articles with similarity scores
        """
        if not self.articles or self.embeddings is None:
            return []
        
        # Encode the query
        query_embedding = self.model.encode([query])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get top k results
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            article = self.articles[idx].copy()
            article["similarity_score"] = float(similarities[idx])
            results.append(article)
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get search engine statistics"""
        return {
            "total_articles": len(self.articles),
            "model_name": self.model.get_sentence_embedding_dimension(),
            "embedding_dimension": self.model.get_sentence_embedding_dimension()
        }
