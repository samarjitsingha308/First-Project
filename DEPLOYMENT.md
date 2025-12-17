# Deployment Guide

## Table of Contents
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
  - [Heroku](#heroku)
  - [AWS](#aws)
  - [Google Cloud Platform](#google-cloud-platform)
  - [Azure](#azure)
- [Production Considerations](#production-considerations)

## Local Development

### Quick Start
```bash
# Automated setup
./setup.sh

# Start both services
./start.sh
```

### Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Docker Deployment

### Development with Docker

```bash
# Build and start
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild specific service
docker-compose up --build backend
```

### Production Docker Setup

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: docker/Dockerfile.backend
    restart: always
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
    volumes:
      - ./models:/app/models:ro
    command: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000

  frontend:
    build:
      context: .
      dockerfile: docker/Dockerfile.frontend.prod
    restart: always
    ports:
      - "80:80"
    depends_on:
      - backend

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - frontend
      - backend
```

Create `docker/Dockerfile.frontend.prod`:

```dockerfile
FROM node:18-alpine as builder

WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Cloud Deployment

### Heroku

#### Backend Deployment

1. **Prepare files:**

Create `Procfile` in backend directory:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

Create `runtime.txt`:
```
python-3.10.12
```

2. **Deploy:**
```bash
# Login to Heroku
heroku login

# Create app
heroku create student-risk-api

# Add buildpack
heroku buildpacks:set heroku/python

# Deploy
git subtree push --prefix backend heroku main

# Or use Heroku Git
cd backend
git init
heroku git:remote -a student-risk-api
git add .
git commit -m "Initial commit"
git push heroku main
```

3. **Configure:**
```bash
# Set environment variables
heroku config:set PYTHONUNBUFFERED=1

# View logs
heroku logs --tail
```

#### Frontend Deployment (Vercel/Netlify)

**Vercel:**
```bash
cd frontend
npm install -g vercel
vercel

# Configure build settings:
# Build Command: npm run build
# Output Directory: dist
# Install Command: npm install
```

**Netlify:**
```bash
cd frontend
npm install -g netlify-cli
netlify deploy

# Configure:
# Build command: npm run build
# Publish directory: dist
```

Update frontend `.env`:
```
VITE_API_URL=https://your-heroku-app.herokuapp.com
```

### AWS

#### Using Elastic Beanstalk

**Backend:**
```bash
# Install EB CLI
pip install awsebcli

# Initialize
cd backend
eb init -p python-3.10 student-risk-api

# Create environment
eb create student-risk-production

# Deploy
eb deploy

# Open app
eb open
```

**Frontend (S3 + CloudFront):**
```bash
cd frontend
npm run build

# Upload to S3
aws s3 sync dist/ s3://your-bucket-name --delete

# Create CloudFront distribution
aws cloudfront create-distribution \
  --origin-domain-name your-bucket-name.s3.amazonaws.com
```

#### Using ECS (Docker)

1. **Push images to ECR:**
```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  123456789.dkr.ecr.us-east-1.amazonaws.com

# Build and push backend
docker build -t student-risk-backend -f docker/Dockerfile.backend .
docker tag student-risk-backend:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/student-risk-backend:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/student-risk-backend:latest

# Build and push frontend
docker build -t student-risk-frontend -f docker/Dockerfile.frontend .
docker tag student-risk-frontend:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/student-risk-frontend:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/student-risk-frontend:latest
```

2. **Create ECS task definition and service** (use AWS Console or CLI)

### Google Cloud Platform

#### Using Cloud Run

**Backend:**
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/student-risk-backend backend/

gcloud run deploy student-risk-backend \
  --image gcr.io/PROJECT_ID/student-risk-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**Frontend (Firebase Hosting):**
```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize
cd frontend
firebase init hosting

# Build and deploy
npm run build
firebase deploy --only hosting
```

#### Using GKE (Kubernetes)

```bash
# Create cluster
gcloud container clusters create student-risk-cluster \
  --num-nodes=3 \
  --region=us-central1

# Get credentials
gcloud container clusters get-credentials student-risk-cluster \
  --region=us-central1

# Apply Kubernetes configs
kubectl apply -f k8s/
```

### Azure

#### Using App Service

**Backend:**
```bash
# Login
az login

# Create resource group
az group create --name StudentRiskRG --location eastus

# Create app service plan
az appservice plan create \
  --name StudentRiskPlan \
  --resource-group StudentRiskRG \
  --sku B1 \
  --is-linux

# Create web app
az webapp create \
  --resource-group StudentRiskRG \
  --plan StudentRiskPlan \
  --name student-risk-api \
  --runtime "PYTHON:3.10"

# Deploy
cd backend
az webapp up --name student-risk-api --resource-group StudentRiskRG
```

**Frontend (Static Web Apps):**
```bash
# Create static web app
az staticwebapp create \
  --name student-risk-frontend \
  --resource-group StudentRiskRG \
  --source https://github.com/youruser/yourrepo \
  --location eastus \
  --branch main \
  --app-location "/frontend" \
  --output-location "dist"
```

## Production Considerations

### Security

1. **CORS Configuration:**
```python
# backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

2. **Environment Variables:**
```bash
# Never commit sensitive data
# Use environment variables for:
# - Database credentials
# - API keys
# - Secret keys
```

3. **HTTPS:**
- Use SSL certificates (Let's Encrypt, AWS ACM, etc.)
- Redirect HTTP to HTTPS
- Enable HSTS headers

4. **Rate Limiting:**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/predict")
@limiter.limit("100/hour")
async def predict_risk(request: Request, payload: StudentFeatures):
    # ...
```

### Performance

1. **Caching:**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def load_model():
    return joblib.load(MODEL_PATH)
```

2. **Database:**
- Use PostgreSQL/MySQL for production
- Store predictions for analytics
- Implement connection pooling

3. **Load Balancing:**
- Use multiple worker processes
- Implement health checks
- Use load balancers (ALB, NLB, etc.)

4. **CDN:**
- Serve frontend static assets via CDN
- Enable gzip/brotli compression

### Monitoring

1. **Logging:**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

2. **Application Monitoring:**
- Use Sentry for error tracking
- Use New Relic/DataDog for APM
- Set up alerts for errors

3. **Health Checks:**
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "timestamp": datetime.now().isoformat()
    }
```

### Scaling

1. **Horizontal Scaling:**
- Use auto-scaling groups
- Implement session-less design
- Use external model storage

2. **Model Serving:**
- Consider TensorFlow Serving or TorchServe for high-throughput
- Use model versioning
- Implement A/B testing

3. **Database Optimization:**
- Use read replicas
- Implement caching (Redis)
- Optimize queries

### Backup & Recovery

1. **Model Backup:**
```bash
# Automated backup script
#!/bin/bash
aws s3 sync models/ s3://your-bucket/models-backup/$(date +%Y%m%d)/
```

2. **Database Backup:**
- Automated daily backups
- Point-in-time recovery
- Cross-region replication

### CI/CD

**GitHub Actions Example:**

`.github/workflows/deploy.yml`:
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          cd backend
          pip install -r requirements.txt
          pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to production
        run: |
          # Your deployment commands
```

## Troubleshooting

### Common Issues

1. **Model not loading:**
   - Ensure model.pkl exists in models/
   - Check file permissions
   - Verify model is trained correctly

2. **CORS errors:**
   - Update CORS origins in backend
   - Check API URL in frontend .env

3. **Port conflicts:**
   - Change ports in configuration
   - Kill existing processes

4. **Memory issues:**
   - Increase container memory limits
   - Optimize model size
   - Use model compression

### Debug Commands

```bash
# Check backend health
curl http://localhost:8000/health

# Test prediction
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"data": {...}}'

# View backend logs
docker-compose logs -f backend

# Check frontend build
cd frontend && npm run build

# Test production build
cd frontend && npm run preview
```
