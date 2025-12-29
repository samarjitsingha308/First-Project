# 🚀 Deployment Guide

How to deploy the BERT Search Engine to various platforms

## 📦 Pre-Deployment Checklist

- [ ] Test locally with `python3 app.py`
- [ ] Verify all dependencies in `requirements.txt`
- [ ] Test with sample data
- [ ] Check browser console for errors
- [ ] Verify API endpoints work
- [ ] Test on target Python version
- [ ] Review security settings

## 🐳 Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 8000

# Download BERT model during build
RUN python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Run application
CMD ["python3", "app.py"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  bert-search:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./articles.json:/app/articles.json
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
```

### Build and Run

```bash
# Build
docker build -t bert-search-engine .

# Run
docker run -p 8000:8000 -v $(pwd)/articles.json:/app/articles.json bert-search-engine

# Or with docker-compose
docker-compose up -d
```

## ☁️ Cloud Platform Deployment

### Heroku

1. **Create Procfile**
```
web: uvicorn app:app --host 0.0.0.0 --port $PORT
```

2. **Create runtime.txt**
```
python-3.11.7
```

3. **Deploy**
```bash
heroku create your-app-name
git push heroku main
heroku open
```

### Google Cloud Platform (Cloud Run)

1. **Create cloudbuild.yaml**
```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/bert-search', '.']
images:
  - 'gcr.io/$PROJECT_ID/bert-search'
```

2. **Deploy**
```bash
gcloud builds submit --config cloudbuild.yaml
gcloud run deploy bert-search \
  --image gcr.io/$PROJECT_ID/bert-search \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### AWS (Elastic Beanstalk)

1. **Install EB CLI**
```bash
pip install awsebcli
```

2. **Initialize**
```bash
eb init -p python-3.11 bert-search
```

3. **Create environment**
```bash
eb create bert-search-env
```

4. **Deploy**
```bash
eb deploy
```

### DigitalOcean App Platform

1. **Create app.yaml**
```yaml
name: bert-search-engine
services:
  - name: web
    github:
      repo: your-username/your-repo
      branch: main
    build_command: pip install -r requirements.txt
    run_command: python3 app.py
    envs:
      - key: PORT
        value: "8000"
    http_port: 8000
```

2. Deploy via DigitalOcean dashboard or CLI

## 🖥️ VPS/Server Deployment

### Using Nginx + Gunicorn

1. **Install Nginx**
```bash
sudo apt update
sudo apt install nginx python3-pip python3-venv
```

2. **Setup Application**
```bash
cd /var/www/
git clone your-repo bert-search
cd bert-search
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

3. **Create systemd service** (`/etc/systemd/system/bert-search.service`)
```ini
[Unit]
Description=BERT Search Engine
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/bert-search
Environment="PATH=/var/www/bert-search/venv/bin"
ExecStart=/var/www/bert-search/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app --bind 127.0.0.1:8000

[Install]
WantedBy=multi-user.target
```

4. **Configure Nginx** (`/etc/nginx/sites-available/bert-search`)
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /var/www/bert-search/static;
    }
}
```

5. **Enable and start**
```bash
sudo systemctl enable bert-search
sudo systemctl start bert-search
sudo ln -s /etc/nginx/sites-available/bert-search /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 🔐 Production Configuration

### Environment Variables

Create `.env` file:
```bash
# Server
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Storage
ARTICLES_FILE=/path/to/articles.json

# BERT Model
MODEL_NAME=all-MiniLM-L6-v2
MODEL_CACHE_DIR=/path/to/cache

# Security
ALLOWED_HOSTS=your-domain.com
SECRET_KEY=your-secret-key
```

### Update app.py for production

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
DEBUG = os.getenv("DEBUG", "False") == "True"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
ARTICLES_FILE = os.getenv("ARTICLES_FILE", "articles.json")

# Run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level="info" if not DEBUG else "debug"
    )
```

### Security Best Practices

1. **HTTPS/SSL**
```bash
# Using Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

2. **CORS Configuration**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)
```

3. **Rate Limiting**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/search")
@limiter.limit("10/minute")
async def search_articles(request: Request, query: SearchQuery):
    # ...
```

4. **API Key Authentication** (optional)
```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

@app.post("/api/articles", dependencies=[Security(verify_api_key)])
async def create_article(article: Article):
    # ...
```

## 📊 Monitoring & Logging

### Application Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### Health Check Endpoint

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "articles_count": len(search_engine.articles),
        "model_loaded": search_engine.embeddings is not None
    }
```

### Monitoring Tools

- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **Sentry**: Error tracking
- **New Relic**: Application monitoring
- **CloudWatch**: AWS monitoring

## 🗄️ Database Migration

For production, consider using a proper database:

### PostgreSQL Setup

```python
from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String, default="Anonymous")
    created_at = Column(DateTime)

Base.metadata.create_all(bind=engine)
```

## 🔄 CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python3 test_setup.py
    
    - name: Deploy to server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /var/www/bert-search
          git pull
          source venv/bin/activate
          pip install -r requirements.txt
          sudo systemctl restart bert-search
```

## 📈 Scaling Strategies

### Horizontal Scaling

1. **Load Balancer**: Distribute traffic across multiple instances
2. **Shared Storage**: Use S3/GCS for articles.json
3. **Vector Database**: Migrate to FAISS/Pinecone for embeddings
4. **Caching**: Add Redis for frequent queries

### Vertical Scaling

1. **More RAM**: Load more articles
2. **Better CPU**: Faster BERT inference
3. **GPU**: Use GPU-accelerated inference (optional)

### Performance Optimization

```python
# Pre-compute embeddings
@app.on_event("startup")
async def warmup():
    # Preload model
    search_engine.model.encode(["warmup query"])

# Add caching
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_search(query: str, top_k: int):
    return search_engine.search(query, top_k)
```

## 🎯 Post-Deployment

### Checklist

- [ ] Verify application is accessible
- [ ] Test search functionality
- [ ] Test article creation
- [ ] Check logs for errors
- [ ] Verify SSL certificate
- [ ] Test from different devices
- [ ] Monitor resource usage
- [ ] Set up backups
- [ ] Configure alerts
- [ ] Document deployment process

### Backup Strategy

```bash
# Backup articles.json
crontab -e
# Add: 0 2 * * * cp /var/www/bert-search/articles.json /backups/articles-$(date +\%Y\%m\%d).json

# Or use cloud storage
aws s3 sync /var/www/bert-search/articles.json s3://your-bucket/backups/
```

## 🆘 Rollback Plan

```bash
# Keep previous version
git tag v1.0.0
git push origin v1.0.0

# If needed to rollback
git checkout v1.0.0
sudo systemctl restart bert-search
```

---

Choose the deployment method that best fits your needs and infrastructure!
