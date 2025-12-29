# 🔧 Troubleshooting Guide

Common issues and solutions for the BERT Search Engine

## Installation Issues

### Problem: `pip install` fails

**Solution 1**: Upgrade pip
```bash
pip3 install --upgrade pip
```

**Solution 2**: Use virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
pip3 install -r requirements.txt
```

**Solution 3**: Install system dependencies (Linux)
```bash
sudo apt-get update
sudo apt-get install python3-dev build-essential
```

### Problem: PyTorch installation fails

**Solution**: Install PyTorch separately with CPU version
```bash
pip3 install torch --index-url https://download.pytorch.org/whl/cpu
pip3 install -r requirements.txt
```

### Problem: "No module named 'sentence_transformers'"

**Solution**: Install directly
```bash
pip3 install sentence-transformers
```

## Runtime Issues

### Problem: "Port 8000 is already in use"

**Solution 1**: Kill the process using the port
```bash
# Find process ID
lsof -i :8000
# Kill it
kill -9 <PID>
```

**Solution 2**: Use a different port
```bash
uvicorn app:app --port 8080
```

### Problem: BERT model download fails

**Symptoms**: 
- Connection errors
- Partial downloads
- "Model not found" errors

**Solutions**:

1. **Check internet connection**
   ```bash
   ping huggingface.co
   ```

2. **Manual model download**
   ```python
   from sentence_transformers import SentenceTransformer
   model = SentenceTransformer('all-MiniLM-L6-v2')
   ```

3. **Try different model**
   Edit `search_engine.py`:
   ```python
   model = SentenceTransformer('paraphrase-MiniLM-L3-v2')  # Smaller
   ```

4. **Set cache directory**
   ```bash
   export SENTENCE_TRANSFORMERS_HOME=/your/path/
   ```

### Problem: Server starts but can't access in browser

**Check 1**: Verify server is running
```bash
curl http://localhost:8000
```

**Check 2**: Check firewall settings
```bash
# Linux
sudo ufw status
sudo ufw allow 8000

# Or use 0.0.0.0 to bind all interfaces
uvicorn app:app --host 0.0.0.0 --port 8000
```

**Check 3**: Try 127.0.0.1 instead of localhost
```
http://127.0.0.1:8000
```

### Problem: "articles.json not found" or permission errors

**Solution 1**: Check permissions
```bash
ls -la articles.json
chmod 644 articles.json
```

**Solution 2**: Delete and recreate
```bash
rm articles.json
# Restart server, it will recreate
```

**Solution 3**: Specify absolute path in app.py
```python
ARTICLES_FILE = "/absolute/path/to/articles.json"
```

## Search Issues

### Problem: Search returns no results

**Possible Causes**:
1. No articles indexed
2. Query too specific
3. Model not loaded

**Solutions**:

1. **Check article count**
   - Go to "Browse All" tab
   - Or check `articles.json`

2. **Create test articles**
   ```bash
   python3 sample_articles.py
   ```

3. **Try broader queries**
   - Instead of "specific technical term"
   - Try "general concept"

4. **Check server logs**
   ```bash
   # Look for errors in terminal
   ```

### Problem: Search results seem random/irrelevant

**Possible Causes**:
1. Very short article content
2. Query doesn't match article topics
3. Model needs time to load

**Solutions**:

1. **Ensure articles have substantial content**
   - At least 50-100 words
   - Include relevant keywords

2. **Use descriptive tags**
   - Add tags when creating articles
   - Tags are included in search

3. **Wait for model to fully load**
   - First search may be slow
   - Subsequent searches are faster

### Problem: Low similarity scores (< 50%)

**This is normal!**
- Similarity scores of 30-50% can still be relevant
- BERT compares semantic meaning, not just keywords
- Lower scores = less similar content

**Tips**:
- Scores > 70%: Highly relevant
- Scores 50-70%: Relevant
- Scores 30-50%: Somewhat relevant
- Scores < 30%: Not very relevant

## Performance Issues

### Problem: First search is very slow

**This is expected!**
- BERT model loads on first use
- Can take 10-30 seconds
- Subsequent searches are fast (< 1 second)

**Solution**: Preload model
```python
# Add to app.py startup event
@app.on_event("startup")
async def startup_event():
    # Warm up the model
    search_engine.model.encode(["test"])
```

### Problem: Server uses too much memory

**Cause**: BERT model is loaded in memory

**Solutions**:

1. **Use smaller model**
   ```python
   model = SentenceTransformer('all-MiniLM-L6-v2')  # 80MB
   # Instead of
   model = SentenceTransformer('all-mpnet-base-v2')  # 420MB
   ```

2. **Limit article count**
   - Archive old articles
   - Implement pagination

3. **Use quantized model** (advanced)
   ```python
   model = SentenceTransformer('all-MiniLM-L6-v2')
   model.half()  # Use FP16
   ```

### Problem: Search gets slower over time

**Cause**: Many articles indexed

**Solutions**:

1. **Implement pagination**
   - Only show top-k results
   - Default is already 5

2. **Use vector database**
   - FAISS, Pinecone, or Weaviate
   - Much faster for large datasets

3. **Add caching**
   - Cache frequent queries
   - Use Redis

## Frontend Issues

### Problem: Forms don't submit

**Check 1**: Browser console for errors
- Right-click → Inspect → Console

**Check 2**: Verify API connection
```javascript
// Check in browser console
fetch('/api/articles')
  .then(r => r.json())
  .then(console.log)
```

**Check 3**: CORS issues (if accessing from different domain)
```python
# Add to app.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Problem: Styles not loading

**Check 1**: Verify file exists
```bash
ls static/styles.css
```

**Check 2**: Check browser console for 404s

**Check 3**: Clear browser cache
- Ctrl+Shift+R (hard refresh)
- Or Ctrl+Shift+Delete (clear cache)

**Check 4**: Check static mount in app.py
```python
app.mount("/static", StaticFiles(directory="static"), name="static")
```

### Problem: JavaScript errors

**Common causes**:
1. API endpoint changes
2. Response format changes
3. Browser compatibility

**Solution**: Check browser console
- Look for specific error messages
- Check network tab for failed requests

## Data Issues

### Problem: Articles lost after restart

**Cause**: `articles.json` deleted or corrupted

**Solutions**:

1. **Check if file exists**
   ```bash
   ls -la articles.json
   ```

2. **Restore from backup** (if available)

3. **Recreate sample data**
   ```bash
   python3 sample_articles.py
   ```

### Problem: Can't delete articles

**Check 1**: Verify file permissions
```bash
chmod 644 articles.json
```

**Check 2**: Check server logs for errors

**Check 3**: Try via API directly
```bash
curl -X DELETE http://localhost:8000/api/articles/1
```

## Environment-Specific Issues

### Windows-Specific

**Problem**: `start.sh` doesn't work
- Solution: Use `python3 app.py` directly or create `start.bat`

**Problem**: File path issues
- Solution: Use forward slashes `/` or raw strings `r"path"`

### Linux-Specific

**Problem**: Permission denied
- Solution: `chmod +x start.sh`

**Problem**: Missing system packages
- Solution: `sudo apt-get install python3-pip python3-dev`

### Mac-Specific

**Problem**: SSL certificate errors
- Solution: `/Applications/Python\ 3.x/Install\ Certificates.command`

**Problem**: Homebrew Python conflicts
- Solution: Use `python3` explicitly, not `python`

## Getting Help

If you still have issues:

1. **Check server logs**
   - Terminal output shows errors
   - Look for stack traces

2. **Enable debug mode**
   ```python
   # In app.py
   uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
   ```

3. **Test individual components**
   ```bash
   python3 test_setup.py
   ```

4. **Verify Python version**
   ```bash
   python3 --version  # Should be 3.8+
   ```

5. **Check disk space**
   ```bash
   df -h
   ```

6. **Reinstall dependencies**
   ```bash
   pip3 install -r requirements.txt --force-reinstall
   ```

## Quick Diagnostics

Run these commands to gather diagnostic info:

```bash
# System info
python3 --version
pip3 --version
which python3

# Dependencies
pip3 list | grep -E "fastapi|uvicorn|sentence|torch|sklearn"

# Files
ls -la static/
cat articles.json

# Ports
netstat -an | grep 8000
# or
lsof -i :8000

# Test imports
python3 -c "import fastapi, uvicorn, sentence_transformers; print('OK')"
```

## Still Need Help?

Create an issue with:
- Python version
- Operating system
- Error message (full stack trace)
- Steps to reproduce
- Output of quick diagnostics above

---

**Most common fix**: Reinstall dependencies in a clean environment!

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 app.py
```
