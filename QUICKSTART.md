# Quick Start Guide

Get the Student Risk Prediction System up and running in minutes!

## Prerequisites Check

Before starting, ensure you have:
- [ ] Python 3.8+ installed (`python3 --version`)
- [ ] Node.js 16+ installed (`node --version`)
- [ ] pip installed (`pip --version`)
- [ ] npm installed (`npm --version`)

## Option 1: Automated Setup (Recommended) ⚡

```bash
# 1. Make setup script executable
chmod +x setup.sh start.sh

# 2. Run automated setup (installs dependencies and trains model)
./setup.sh

# 3. Start the application
./start.sh
```

That's it! The application will be running at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Option 2: Manual Setup 🛠️

### Step 1: Setup Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Train the model
python train_model.py
```

### Step 2: Setup Frontend

```bash
cd frontend

# Copy environment file
cp .env.example .env

# Install dependencies
npm install
```

### Step 3: Start Services

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Option 3: Docker Setup 🐳

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d

# Stop services
docker-compose down
```

## First Steps After Setup

### 1. Test the Backend API

```bash
# Health check
curl http://localhost:8000/health

# Model info
curl http://localhost:8000/model/info
```

### 2. Open the Frontend

Navigate to http://localhost:3000 in your browser.

### 3. Try a Prediction

1. Click "Load High-Risk Sample" or "Load Low-Risk Sample"
2. Adjust the sliders as needed
3. Click "Predict Risk"
4. View the results with SHAP explanations

## Using the UI

### Input Form

The form is organized into four groups:

1. **Academic Performance**
   - GPA, Attendance Rate, Failed Courses, Credit Hours

2. **Engagement**
   - Library Visits, Tutoring Sessions, Office Hours, Club Participation

3. **Demographics & Background**
   - Age, First Generation, Financial Aid, Work Hours

4. **Support Services**
   - Counseling Visits, Health Center Visits, Advisor Meetings, Study Groups

### Sample Data

Use the preset buttons:
- **Load High-Risk Sample**: Student with multiple risk factors
- **Load Low-Risk Sample**: Well-performing student
- **Reset to Default**: Average student profile

### Understanding Results

After prediction, you'll see:

1. **Risk Assessment**
   - Risk Band (Low/Medium/High)
   - Dropout Probability (0-100%)
   - Prediction (Retained/Dropout)

2. **Top Risk Drivers (SHAP Values)**
   - Features that most influence the prediction
   - Positive values = increase dropout risk
   - Negative values = decrease dropout risk

3. **Recommended Actions**
   - Specific interventions based on risk factors

4. **Additional Information**
   - Risk band explanations
   - SHAP methodology

## API Usage Examples

### Python

```python
import requests

response = requests.post('http://localhost:8000/predict', json={
    "data": {
        "gpa": 3.5,
        "attendance_rate": 0.90,
        "failed_courses": 0,
        # ... other features
    }
})

print(response.json())
```

### cURL

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "gpa": 3.5,
      "attendance_rate": 0.90,
      "failed_courses": 0
    }
  }'
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

const result = await axios.post('http://localhost:8000/predict', {
  data: {
    gpa: 3.5,
    attendance_rate: 0.90,
    failed_courses: 0,
    // ... other features
  }
});

console.log(result.data);
```

## Troubleshooting

### Backend won't start

**Problem**: "Model not found" error
```bash
# Solution: Train the model
cd backend
source venv/bin/activate
python train_model.py
```

**Problem**: Import errors
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt
```

### Frontend won't start

**Problem**: Module not found
```bash
# Solution: Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Problem**: Can't connect to API
```bash
# Solution: Check backend is running and update .env
echo "VITE_API_URL=http://localhost:8000" > .env
```

### Port conflicts

**Problem**: Port already in use

```bash
# Find process using port 8000
lsof -i :8000
# Kill the process
kill -9 <PID>

# Or use different ports:
# Backend: uvicorn main:app --port 8001
# Frontend: npm run dev -- --port 3001
```

### CORS errors

**Problem**: CORS policy blocking requests

Update `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update if using different port
    ...
)
```

## Next Steps

- 📖 Read the full [README.md](README.md) for detailed information
- 🔧 Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- 📡 See [API_EXAMPLES.md](API_EXAMPLES.md) for more API usage examples
- 🐛 Run tests: `python test_api.py` (after starting backend)

## Getting Help

If you encounter issues:

1. Check the logs for error messages
2. Verify all prerequisites are installed
3. Ensure ports 3000 and 8000 are available
4. Try the automated setup script: `./setup.sh`
5. Check the troubleshooting section above

## Feature Highlights

✨ **What makes this system special:**

- 🤖 **AI-Powered**: Random Forest classifier with 85%+ accuracy
- 🔍 **Explainable**: SHAP values show exactly why predictions are made
- 🎨 **Beautiful UI**: Modern, responsive design with smooth animations
- ⚡ **Fast**: Real-time predictions in milliseconds
- 📊 **Comprehensive**: 16 features covering academic, social, and demographic factors
- 🔄 **Flexible**: RESTful API for easy integration
- 🐳 **Docker Ready**: Containerized deployment option
- 📈 **Scalable**: Built for production use

Enjoy using the Student Risk Prediction System! 🎓
