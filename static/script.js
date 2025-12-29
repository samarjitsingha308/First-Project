// API Base URL
const API_BASE = '';

// Tab Management
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(`${tabName}-tab`).classList.add('active');
    event.target.classList.add('active');
    
    // Load data if needed
    if (tabName === 'browse') {
        loadAllArticles();
    }
}

// Loading Overlay
function showLoading() {
    document.getElementById('loading-overlay').classList.add('active');
}

function hideLoading() {
    document.getElementById('loading-overlay').classList.remove('active');
}

// Search Articles
async function searchArticles() {
    const query = document.getElementById('search-input').value.trim();
    const topK = parseInt(document.getElementById('top-k').value);
    const mode = document.getElementById('search-mode').value;
    const semanticWeight = parseInt(document.getElementById('semantic-weight').value) / 100;
    const resultsDiv = document.getElementById('search-results');
    
    if (!query) {
        resultsDiv.innerHTML = '<p class="error-message">Please enter a search query</p>';
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/api/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                query, 
                top_k: topK,
                mode: mode,
                semantic_weight: semanticWeight
            })
        });
        
        if (!response.ok) {
            throw new Error('Search failed');
        }
        
        const results = await response.json();
        displaySearchResults(results, mode);
    } catch (error) {
        resultsDiv.innerHTML = `<p class="error-message">Error: ${error.message}</p>`;
    } finally {
        hideLoading();
    }
}

// Display Search Results
function displaySearchResults(results, mode) {
    const resultsDiv = document.getElementById('search-results');
    
    if (results.length === 0) {
        resultsDiv.innerHTML = `
            <div class="empty-state">
                <h3>No results found</h3>
                <p>Try different keywords or create a new article</p>
            </div>
        `;
        return;
    }
    
    resultsDiv.innerHTML = results.map(article => {
        // Generate score badges based on mode
        let scoreHTML = '';
        
        if (mode === 'hybrid') {
            scoreHTML = `
                <div class="score-badges">
                    <div class="similarity-score hybrid">
                        ${(article.similarity_score * 100).toFixed(1)}% Overall
                    </div>
                    <div class="score-detail semantic">
                        🧠 ${(article.semantic_score * 100).toFixed(1)}%
                    </div>
                    <div class="score-detail keyword">
                        🔑 ${(article.keyword_score * 100).toFixed(1)}%
                    </div>
                </div>
            `;
        } else if (mode === 'semantic') {
            scoreHTML = `
                <div class="score-badges">
                    <div class="similarity-score semantic">
                        🧠 ${(article.semantic_score * 100).toFixed(1)}% Semantic
                    </div>
                </div>
            `;
        } else {
            scoreHTML = `
                <div class="score-badges">
                    <div class="similarity-score keyword">
                        🔑 ${(article.keyword_score * 100).toFixed(1)}% Keyword
                    </div>
                </div>
            `;
        }
        
        // Add keyword match indicator if there's direct keyword match
        let keywordMatchBadge = '';
        if (article.keyword_match_ratio > 0) {
            keywordMatchBadge = `
                <span class="keyword-match-badge" title="Direct keyword matches found">
                    ✓ ${Math.round(article.keyword_match_ratio * 100)}% keywords matched
                </span>
            `;
        }
        
        return `
            <div class="article-card">
                <div class="article-header">
                    <div>
                        <h3 class="article-title">${escapeHtml(article.title)}</h3>
                        <p class="article-meta">
                            By ${escapeHtml(article.author)} • ${formatDate(article.created_at)}
                        </p>
                        ${keywordMatchBadge}
                    </div>
                    ${scoreHTML}
                </div>
                <p class="article-content">${escapeHtml(truncate(article.content, 300))}</p>
                ${article.tags.length > 0 ? `
                    <div class="article-tags">
                        ${article.tags.map(tag => `<span class="tag">${escapeHtml(tag)}</span>`).join('')}
                    </div>
                ` : ''}
            </div>
        `;
    }).join('');
}

// Create Article
async function createArticle(event) {
    event.preventDefault();
    
    const title = document.getElementById('title').value.trim();
    const content = document.getElementById('content').value.trim();
    const author = document.getElementById('author').value.trim() || 'Anonymous';
    const tagsInput = document.getElementById('tags').value.trim();
    const tags = tagsInput ? tagsInput.split(',').map(tag => tag.trim()).filter(tag => tag) : [];
    
    const messageDiv = document.getElementById('create-message');
    
    if (!title || !content) {
        messageDiv.innerHTML = '<p class="error-message">Title and content are required</p>';
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/api/articles`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title, content, author, tags })
        });
        
        if (!response.ok) {
            throw new Error('Failed to create article');
        }
        
        const article = await response.json();
        
        messageDiv.innerHTML = '<p class="success-message">Article created successfully!</p>';
        document.getElementById('article-form').reset();
        
        // Auto-hide success message after 3 seconds
        setTimeout(() => {
            messageDiv.innerHTML = '';
        }, 3000);
        
    } catch (error) {
        messageDiv.innerHTML = `<p class="error-message">Error: ${error.message}</p>`;
    } finally {
        hideLoading();
    }
}

// Load All Articles
async function loadAllArticles() {
    const articlesDiv = document.getElementById('all-articles');
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/api/articles`);
        
        if (!response.ok) {
            throw new Error('Failed to load articles');
        }
        
        const articles = await response.json();
        displayAllArticles(articles);
    } catch (error) {
        articlesDiv.innerHTML = `<p class="error-message">Error: ${error.message}</p>`;
    } finally {
        hideLoading();
    }
}

// Display All Articles
function displayAllArticles(articles) {
    const articlesDiv = document.getElementById('all-articles');
    
    if (articles.length === 0) {
        articlesDiv.innerHTML = `
            <div class="empty-state">
                <h3>No articles yet</h3>
                <p>Create your first article to get started</p>
            </div>
        `;
        return;
    }
    
    articlesDiv.innerHTML = articles.map(article => `
        <div class="article-card">
            <div class="article-header">
                <div>
                    <h3 class="article-title">${escapeHtml(article.title)}</h3>
                    <p class="article-meta">
                        By ${escapeHtml(article.author)} • ${formatDate(article.created_at)}
                    </p>
                </div>
                <button class="delete-btn" onclick="deleteArticle('${article.id}')">Delete</button>
            </div>
            <p class="article-content">${escapeHtml(article.content)}</p>
            ${article.tags.length > 0 ? `
                <div class="article-tags">
                    ${article.tags.map(tag => `<span class="tag">${escapeHtml(tag)}</span>`).join('')}
                </div>
            ` : ''}
        </div>
    `).join('');
}

// Delete Article
async function deleteArticle(articleId) {
    if (!confirm('Are you sure you want to delete this article?')) {
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/api/articles/${articleId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete article');
        }
        
        // Reload articles
        loadAllArticles();
    } catch (error) {
        alert(`Error: ${error.message}`);
    } finally {
        hideLoading();
    }
}

// Utility Functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function truncate(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Initialize page
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                searchArticles();
            }
        });
    }
    
    // Handle search mode change
    const searchMode = document.getElementById('search-mode');
    const weightLabel = document.getElementById('weight-label');
    
    if (searchMode && weightLabel) {
        searchMode.addEventListener('change', () => {
            // Show/hide weight slider based on mode
            if (searchMode.value === 'hybrid') {
                weightLabel.style.display = 'block';
            } else {
                weightLabel.style.display = 'none';
            }
        });
    }
    
    // Handle weight slider
    const weightSlider = document.getElementById('semantic-weight');
    const weightValue = document.getElementById('weight-value');
    
    if (weightSlider && weightValue) {
        weightSlider.addEventListener('input', () => {
            weightValue.textContent = weightSlider.value + '%';
        });
    }
});
