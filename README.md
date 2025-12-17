# 🎓 Student Risk Prediction System

An AI-powered early warning system for student retention using Machine Learning and SHAP (SHapley Additive exPlanations) for interpretable predictions.

## 🌟 Features

- **Real-time Risk Prediction**: Predict student dropout risk based on multiple factors
- **Interpretable AI**: SHAP values explain which factors contribute most to the prediction
- **Beautiful UI**: Modern, responsive React frontend with intuitive visualizations
- **RESTful API**: FastAPI backend with automatic documentation
- **Risk Banding**: Categorizes students into Low/Medium/High risk groups
- **Actionable Insights**: Provides recommended interventions based on risk factors
- **Batch Processing**: Support for bulk predictions via CSV upload

## 📋 Table of Contents

- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Manual Setup](#manual-setup)
- [Docker Deployment](#docker-deployment)
- [API Documentation](#api-documentation)
- [Model Details](#model-details)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         React Frontend (Vite)          │
│  • Student Input Form                  │
│  • Results Visualization                │
│  • SHAP Explanations                    │
└──────────────┬──────────────────────────┘
               │ HTTP/REST API
┌──────────────▼──────────────────────────┐
│        FastAPI Backend                  │
│  • /predict - Single prediction         │
│  • /batch/predict - Bulk predictions    │
│  • /explanations/top-drivers            │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│       ML Model Bundle (.pkl)            │
│  • Random Forest Classifier             │
│  • StandardScaler                       │
│  • SHAP Explainer                       │
└─────────────────────────────────────────┘
```

## 🔧 Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 16+** (for frontend)
- **pip** (Python package manager)
- **npm** (Node package manager)
- **Docker** (optional, for containerized deployment)

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd workspace

# Make setup script executable
chmod +x setup.sh

# Run setup script (installs dependencies and trains model)
./setup.sh

# Start the application
chmod +x start.sh
./start.sh
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Docker Deployment

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d

# Stop services
docker-compose down
```

## 📝 Manual Setup

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Train the model (generates synthetic data)
python train_model.py

# Start the API server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Copy environment file
cp .env.example .env

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at http://localhost:3000

## 📚 API Documentation

### Main Endpoints

#### Health Check
```bash
GET /health
```

#### Single Prediction
```bash
POST /predict
Content-Type: application/json

{
  "data": {
    "gpa": 3.5,
    "attendance_rate": 0.9,
    "failed_courses": 0,
    "credit_hours": 15,
    ...
  }
}
```

Response:
```json
{
  "prediction": "Retained",
  "dropout_probability": 0.1234,
  "risk_band": "Low",
  "top_risk_drivers": {
    "gpa": -0.234,
    "attendance_rate": -0.156,
    ...
  }
}
```

#### Top Risk Drivers
```bash
POST /explanations/top-drivers
```

#### Batch Prediction
```bash
POST /batch/predict
Content-Type: multipart/form-data

file: student_data.csv
```

#### Model Information
```bash
GET /model/info
```

### Interactive API Documentation

Visit http://localhost:8000/docs for the full interactive Swagger UI documentation.

## 🤖 Model Details

### Features (16 total)

The model uses the following features to predict dropout risk:

**Academic Performance**
- GPA (0.0 - 4.0)
- Attendance Rate (0.0 - 1.0)
- Failed Courses (0 - 10)
- Credit Hours (3 - 21)

**Engagement**
- Library Visits
- Tutoring Sessions
- Office Hours Visits
- Club Participation

**Demographics & Background**
- Age
- First Generation Status (0/1)
- Financial Aid Status (0/1)
- Work Hours per Week

**Support Services**
- Counseling Visits
- Health Center Visits
- Advisor Meetings
- Study Group Participation (0/1)

### Model Architecture

- **Algorithm**: Random Forest Classifier
- **Trees**: 100
- **Max Depth**: 10
- **Feature Scaling**: StandardScaler
- **Explainability**: SHAP (SHapley Additive exPlanations)

### Risk Bands

- **Low Risk** (0-30%): Minimal intervention needed
- **Medium Risk** (30-60%): Monitor and support recommended
- **High Risk** (60-100%): Immediate intervention required

### Model Performance

The model is trained on synthetic data with the following characteristics:
- 1000 samples (training + test)
- 80/20 train-test split
- Stratified sampling
- ~30% dropout rate

Typical performance metrics:
- ROC AUC: ~0.85-0.90
- Precision: ~0.75-0.80
- Recall: ~0.70-0.80

## 📁 Project Structure

```
workspace/
├── backend/                    # FastAPI backend
│   ├── main.py                # API endpoints
│   ├── train_model.py         # Model training script
│   └── requirements.txt       # Python dependencies
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── PredictionForm.tsx
│   │   │   └── ResultsDisplay.tsx
│   │   ├── services/          # API service
│   │   │   └── api.ts
│   │   ├── types/             # TypeScript types
│   │   ├── App.tsx            # Main app component
│   │   └── main.tsx           # Entry point
│   ├── package.json
│   └── vite.config.ts
├── models/                     # Trained models
│   └── model.pkl              # Model bundle
├── data/                       # Training data
│   └── student_data.csv       # Generated dataset
├── docker/                     # Docker configurations
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
├── docker-compose.yml          # Multi-container setup
├── setup.sh                    # Setup script
├── start.sh                    # Start script
└── README.md                   # This file
```

## 🎨 UI Features

### Input Form
- Organized feature groups
- Slider inputs with real-time value display
- Sample data presets (high-risk and low-risk)
- Input validation
- Responsive design

### Results Display
- Risk assessment with color-coded visualization
- Probability gauge
- Top 5 risk drivers with SHAP values
- Visual indicators for increasing/decreasing factors
- Actionable recommendations
- Educational information about risk bands

## 🔬 Training Your Own Model

The included training script generates synthetic data. To use your own data:

1. Prepare a CSV file with the required features
2. Modify `train_model.py` to load your data:

```python
# Replace the generate_student_data() call with:
df = pd.read_csv('your_data.csv')
```

3. Run the training script:

```bash
python backend/train_model.py
```

## 🛠️ Development

### Backend Development

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend
npm run dev
```

### Building for Production

#### Frontend
```bash
cd frontend
npm run build
npm run preview  # Preview production build
```

#### Backend
```bash
# Use gunicorn for production
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

## 🧪 Testing

### Test API Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Model info
curl http://localhost:8000/model/info

# Prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"data": {"gpa": 3.5, "attendance_rate": 0.9, ...}}'
```

## 🔐 Security Considerations

For production deployment:

1. **CORS**: Update `allow_origins` in `main.py` to specify your frontend domain
2. **Environment Variables**: Use environment variables for sensitive configuration
3. **HTTPS**: Enable HTTPS for both frontend and backend
4. **Authentication**: Add authentication/authorization if needed
5. **Rate Limiting**: Implement rate limiting for API endpoints
6. **Input Validation**: Additional validation for production data

## 🚀 Deployment

### Heroku

Backend:
```bash
# Add Procfile
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

Frontend (Vercel/Netlify):
```bash
npm run build
# Deploy dist/ folder
```

### AWS/GCP/Azure

Use the provided Dockerfiles to deploy as containerized applications on your preferred cloud platform.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- React and Vite for the frontend tools
- SHAP for interpretable machine learning
- scikit-learn for machine learning tools

## 📞 Support

For issues, questions, or suggestions, please open an issue in the repository.

---

**Built with ❤️ for Education and Student Success**
