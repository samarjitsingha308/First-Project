"""
Hybrid Search Engine
Combines BERT semantic search with keyword matching for comprehensive results
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Dict, Any
import re

class BERTSearchEngine:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the Hybrid Search Engine
        
        Args:
            model_name: Name of the sentence-transformer model to use
                       'all-MiniLM-L6-v2' is lightweight and fast (80MB)
        """
        print(f"Loading BERT model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        self.articles = []
        self.embeddings = None
        
        # TF-IDF for keyword matching
        self.tfidf_vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words='english',
            max_features=5000
        )
        self.tfidf_matrix = None
        self.searchable_texts = []
        
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
        self.searchable_texts.append(searchable_text)
        
        # Add BERT embedding
        new_embedding = self.model.encode([searchable_text])
        if self.embeddings is None:
            self.embeddings = new_embedding
        else:
            self.embeddings = np.vstack([self.embeddings, new_embedding])
        
        # Rebuild TF-IDF matrix
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.searchable_texts)
    
    def index_articles(self, articles: List[Dict[str, Any]]):
        """
        Index multiple articles for search
        
        Args:
            articles: List of article dictionaries
        """
        if not articles:
            self.articles = []
            self.embeddings = None
            self.tfidf_matrix = None
            self.searchable_texts = []
            return
        
        print(f"Indexing {len(articles)} articles...")
        self.articles = articles
        
        # Create searchable text for each article
        self.searchable_texts = [self._create_searchable_text(article) for article in articles]
        
        # Generate BERT embeddings
        self.embeddings = self.model.encode(self.searchable_texts, show_progress_bar=True)
        
        # Generate TF-IDF matrix for keyword matching
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.searchable_texts)
        
        print(f"Indexing complete! {len(articles)} articles ready for hybrid search.")
    
    def _keyword_search(self, query: str) -> np.ndarray:
        """
        Perform keyword-based search using TF-IDF
        
        Args:
            query: Search query string
        
        Returns:
            Array of keyword similarity scores
        """
        query_vector = self.tfidf_vectorizer.transform([query])
        keyword_scores = cosine_similarity(query_vector, self.tfidf_matrix)[0]
        return keyword_scores
    
    def _simple_keyword_match(self, query: str, text: str) -> float:
        """
        Simple keyword matching score (case-insensitive, exact word matches)
        
        Args:
            query: Search query
            text: Text to search in
        
        Returns:
            Score between 0 and 1
        """
        query_words = set(re.findall(r'\w+', query.lower()))
        text_words = set(re.findall(r'\w+', text.lower()))
        
        if not query_words:
            return 0.0
        
        matches = query_words.intersection(text_words)
        return len(matches) / len(query_words)
    
    def _find_matched_keywords(self, query: str, text: str) -> list:
        """
        Find which keywords from the query are present in the text
        
        Args:
            query: Search query
            text: Text to search in
        
        Returns:
            List of matched keywords
        """
        query_words = set(re.findall(r'\w+', query.lower()))
        text_words = set(re.findall(r'\w+', text.lower()))
        
        matches = query_words.intersection(text_words)
        return sorted(list(matches))
    
    def search(self, query: str, top_k: int = 5, mode: str = "hybrid", 
               semantic_weight: float = 0.7) -> List[Dict[str, Any]]:
        """
        Search articles using hybrid approach (semantic + keyword matching)
        
        Args:
            query: Search query string
            top_k: Number of top results to return
            mode: Search mode - "semantic", "keyword", or "hybrid" (default)
            semantic_weight: Weight for semantic score in hybrid mode (0-1)
                           keyword_weight = 1 - semantic_weight
        
        Returns:
            List of articles with scores
        """
        if not self.articles or self.embeddings is None:
            return []
        
        keyword_weight = 1 - semantic_weight
        
        # Get semantic scores
        query_embedding = self.model.encode([query])
        semantic_scores = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get keyword scores
        keyword_scores = self._keyword_search(query)
        
        # Combine scores based on mode
        if mode == "semantic":
            final_scores = semantic_scores
        elif mode == "keyword":
            final_scores = keyword_scores
        else:  # hybrid
            final_scores = (semantic_weight * semantic_scores + 
                          keyword_weight * keyword_scores)
        
        # Get top k results
        top_indices = np.argsort(final_scores)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            article = self.articles[idx].copy()
            article["similarity_score"] = float(final_scores[idx])
            article["semantic_score"] = float(semantic_scores[idx])
            article["keyword_score"] = float(keyword_scores[idx])
            
            # Add simple keyword match info
            searchable_text = self.searchable_texts[idx]
            article["keyword_match_ratio"] = self._simple_keyword_match(query, searchable_text)
            
            # Find matched keywords for highlighting
            article["matched_keywords"] = self._find_matched_keywords(query, searchable_text)
            
            results.append(article)
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get search engine statistics"""
        return {
            "total_articles": len(self.articles),
            "model_name": self.model.get_sentence_embedding_dimension(),
            "embedding_dimension": self.model.get_sentence_embedding_dimension()
        }
