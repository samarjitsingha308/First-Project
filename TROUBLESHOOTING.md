# Troubleshooting Guide

## Common Issues and Solutions

### Issue 1: `venv/bin/activate: No such file or directory`

**Problem**: The virtual environment hasn't been created yet.

**Solution**:
```bash
cd /workspace/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python train_model.py
```

Or run the automated setup:
```bash
./setup.sh
```

---

### Issue 2: `node_modules not found`

**Problem**: Frontend dependencies not installed.

**Solution**:
```bash
cd /workspace/frontend
npm install
```

---

### Issue 3: Manual Startup (If scripts don't work)

**Option A: Using Two Terminals**

Terminal 1 - Backend:
```bash
cd /workspace/backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2 - Frontend:
```bash
cd /workspace/frontend
npm run dev
```

**Option B: Using the manual script**
```bash
./start-manual.sh
```

This will show you the exact commands to run.

---

### Issue 4: Port Already in Use

**Error**: `Address already in use`

**Solution**:

Find and kill the process:
```bash
# For port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# For port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

Or use different ports:
```bash
# Backend on port 8001
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8001

# Frontend on port 3001
cd frontend
npm run dev -- --port 3001
```

---

### Issue 5: Model Not Found

**Error**: `Failed to load model bundle`

**Solution**:
```bash
cd /workspace/backend
source venv/bin/activate
python train_model.py
```

This will train the model and save it to `/workspace/models/model.pkl`

---

### Issue 6: API Connection Failed (Frontend)

**Problem**: Frontend can't connect to backend.

**Check**:
1. Is backend running? Visit http://localhost:8000/health
2. Check `.env` file in frontend:
   ```bash
   cat /workspace/frontend/.env
   # Should contain: VITE_API_URL=http://localhost:8000
   ```

**Solution**:
```bash
# Create/update .env file
echo "VITE_API_URL=http://localhost:8000" > /workspace/frontend/.env

# Restart frontend
cd /workspace/frontend
npm run dev
```

---

### Issue 7: Permission Denied on Scripts

**Error**: `Permission denied: ./setup.sh`

**Solution**:
```bash
chmod +x /workspace/setup.sh
chmod +x /workspace/start.sh
chmod +x /workspace/start-manual.sh
```

---

### Issue 8: Python Module Not Found

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
cd /workspace/backend
source venv/bin/activate
pip install -r requirements.txt
```

---

### Issue 9: `apt install` Fails (Setup Script)

**Problem**: Need sudo permissions.

**Solution**: Run setup commands manually with sudo:
```bash
sudo apt update
sudo apt install -y python3-venv python3-pip

cd /workspace/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python train_model.py

cd /workspace/frontend
npm install
```

---

### Issue 10: CORS Error in Browser

**Error**: `Access to XMLHttpRequest has been blocked by CORS policy`

**Solution**: The backend is already configured for CORS. Make sure:
1. Backend is running on port 8000
2. Frontend `.env` has correct API URL
3. Clear browser cache and reload

If still having issues, verify backend CORS settings in `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Should allow all origins in development
    ...
)
```

---

## Step-by-Step Manual Setup

If all else fails, here's the complete manual setup:

### 1. Setup Backend

```bash
# Go to backend directory
cd /workspace/backend

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Train model
python train_model.py

# Test backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

Visit http://localhost:8000/docs to verify backend works.

### 2. Setup Frontend

Open a new terminal:

```bash
# Go to frontend directory
cd /workspace/frontend

# Create .env file
echo "VITE_API_URL=http://localhost:8000" > .env

# Install dependencies
npm install

# Start dev server
npm run dev
```

Visit http://localhost:3000 to see the UI.

---

## Testing Checklist

After setup, verify everything works:

- [ ] Backend health check: `curl http://localhost:8000/health`
- [ ] Model info: `curl http://localhost:8000/model/info`
- [ ] Frontend loads: http://localhost:3000
- [ ] API connection indicator is green
- [ ] Can load sample data
- [ ] Can make prediction
- [ ] Results display correctly

---

## Getting More Help

### Check Logs

**Backend logs**:
- Look at terminal where backend is running
- Check for Python errors or import issues

**Frontend logs**:
- Look at terminal where frontend is running
- Check browser console (F12) for JavaScript errors

### Verify Installation

**Python packages**:
```bash
cd /workspace/backend
source venv/bin/activate
pip list | grep -E "fastapi|uvicorn|scikit-learn|shap"
```

**Node packages**:
```bash
cd /workspace/frontend
npm list --depth=0 | grep -E "react|vite|axios"
```

### Clean Start

If everything is broken, clean and restart:

```bash
# Clean backend
cd /workspace/backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python train_model.py

# Clean frontend
cd /workspace/frontend
rm -rf node_modules package-lock.json
npm install

# Restart everything
cd /workspace
./start.sh
```

---

## Quick Reference

### Essential Commands

```bash
# Start backend only
cd /workspace/backend && source venv/bin/activate && uvicorn main:app --reload

# Start frontend only
cd /workspace/frontend && npm run dev

# Train model
cd /workspace/backend && source venv/bin/activate && python train_model.py

# Test API
curl http://localhost:8000/health
python /workspace/test_api.py

# Check if ports are in use
lsof -i :8000  # Backend
lsof -i :3000  # Frontend
```

### File Locations

- Backend code: `/workspace/backend/`
- Frontend code: `/workspace/frontend/`
- Model file: `/workspace/models/model.pkl`
- Training data: `/workspace/data/student_data.csv`
- Documentation: `/workspace/*.md`

---

## Still Having Issues?

1. Check the main README.md for detailed setup instructions
2. Review QUICKSTART.md for simplified setup
3. Try the manual setup steps above
4. Check that all prerequisites are installed (Python 3.8+, Node 16+)
5. Make sure you have sufficient disk space and permissions

---

**Most Common Solution**: Just run the setup script!

```bash
cd /workspace
chmod +x setup.sh
./setup.sh
```

This handles 95% of setup issues automatically.
