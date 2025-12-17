# Usage Guide - Student Risk Prediction System

## Table of Contents
1. [Getting Started](#getting-started)
2. [Using the Web Interface](#using-the-web-interface)
3. [Using the API](#using-the-api)
4. [Understanding the Results](#understanding-the-results)
5. [Best Practices](#best-practices)
6. [Advanced Usage](#advanced-usage)

## Getting Started

### Starting the Application

**Option 1: Quick Start**
```bash
./start.sh
```

**Option 2: Manual Start**

Terminal 1 - Backend:
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

### Accessing the Application

- **Frontend**: Open http://localhost:3000 in your browser
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Alternative API Docs**: http://localhost:8000/redoc (ReDoc)

## Using the Web Interface

### 1. Main Dashboard

When you first load the application, you'll see:
- **Header**: Application title and API connection status
- **Input Form**: Interactive form with student features
- **Footer**: System information

### 2. Entering Student Data

#### Method 1: Using Sample Data (Recommended for First Use)

Click one of the sample buttons:
- **Load High-Risk Sample**: Pre-fills data for a student at high risk
  - Low GPA (2.0)
  - Poor attendance (65%)
  - Multiple failed courses (3)
  - High work hours (30/week)
  
- **Load Low-Risk Sample**: Pre-fills data for a successful student
  - High GPA (3.7)
  - Excellent attendance (95%)
  - No failed courses
  - Good engagement with campus resources

#### Method 2: Manual Entry

The form is organized into four sections:

**Academic Performance**
- **GPA**: Move slider between 0.0-4.0
  - 0.0-2.0: Poor
  - 2.0-3.0: Average
  - 3.0-4.0: Good to Excellent

- **Attendance Rate**: 0-100%
  - Below 70%: Concerning
  - 70-85%: Average
  - Above 85%: Good

- **Failed Courses**: Number of failed courses (0-10)
  - 0-1: Normal
  - 2-3: Warning sign
  - 4+: High risk

- **Credit Hours**: Current course load (3-21)
  - 12-15: Standard full-time
  - Below 12: Part-time
  - Above 18: Heavy load

**Engagement**
- **Library Visits**: Monthly visits (0-50)
- **Tutoring Sessions**: Per semester (0-20)
- **Office Hours Visits**: Per semester (0-20)
- **Club Participation**: Number of clubs (0-5)

**Demographics & Background**
- **Age**: Student age (17-30)
- **First Generation**: Yes (1) or No (0)
- **Financial Aid**: Receiving aid? Yes (1) or No (0)
- **Work Hours/Week**: 0-40 hours

**Support Services**
- **Counseling Visits**: Per semester (0-20)
- **Health Center Visits**: Per semester (0-20)
- **Advisor Meetings**: Per semester (0-20)
- **Study Group Participation**: Yes (1) or No (0)

### 3. Getting a Prediction

1. Fill in all student data (or use a sample)
2. Click the **"🎯 Predict Risk"** button
3. Wait for the prediction (usually < 1 second)
4. View comprehensive results

### 4. Understanding the Results

#### Risk Assessment Card

**Risk Band Display**:
- **🟢 Low Risk** (Green)
  - Dropout probability: 0-30%
  - Message: "Student is performing well with minimal dropout risk"
  - Action: Maintain current support level

- **🟡 Medium Risk** (Orange)
  - Dropout probability: 30-60%
  - Message: "Student shows some warning signs"
  - Action: Early intervention recommended

- **🔴 High Risk** (Red)
  - Dropout probability: 60-100%
  - Message: "Student is at high risk"
  - Action: Immediate intervention required

**Probability Gauge**:
- Visual bar showing exact dropout probability
- Percentage displayed prominently
- Color-coded to match risk band

**Prediction Outcome**:
- **Retained**: Model predicts student will continue
- **Dropout**: Model predicts student will leave

#### Top Risk Drivers (SHAP Values)

**What are SHAP Values?**
SHAP (SHapley Additive exPlanations) values show how much each feature contributes to the prediction.

**How to Read Them**:
- **Positive Value** (Red, ↑): Feature INCREASES dropout risk
  - Example: `failed_courses: +0.2341` means having failed courses pushes the prediction toward dropout

- **Negative Value** (Green, ↓): Feature DECREASES dropout risk
  - Example: `gpa: -0.2341` means higher GPA pushes the prediction toward retention

**Top 5 Drivers**:
The system shows the 5 most influential features for this specific student:
1. Ranked by importance (#1 is most influential)
2. Feature name in plain English
3. Direction indicator (↑ increasing or ↓ decreasing)
4. Actual SHAP value (magnitude shows strength)
5. Visual bar (longer = stronger influence)

**Example Interpretation**:
```
#1 ↑ Failed Courses: +0.2341 (increasing)
   → Having failed courses is the strongest factor pushing toward dropout

#2 ↓ GPA: -0.1567 (decreasing)  
   → Good GPA is helping reduce dropout risk

#3 ↑ Work Hours Per Week: +0.0987 (increasing)
   → High work hours are contributing to dropout risk
```

#### Recommended Actions

Based on the risk level and top drivers, the system suggests:

**For High/Medium Risk**:
- Specific interventions targeting the risk factors
- Academic support recommendations
- Counseling or advising referrals
- Resource connections

**For Low Risk**:
- Maintenance strategies
- Periodic check-ins
- Continued engagement encouragement

#### Additional Information

- **Risk Bands**: Explanation of each risk level
- **SHAP Methodology**: How the explanations work
- **Next Steps**: How to use the information

### 5. Taking Action on Results

**Immediate Actions**:
1. **High Risk**: Contact student immediately for intervention meeting
2. **Medium Risk**: Schedule check-in within 1-2 weeks
3. **Low Risk**: Continue normal support schedule

**Using the Insights**:
1. Focus interventions on top risk drivers
2. Address multiple factors simultaneously
3. Track progress with periodic re-predictions
4. Document interventions and outcomes

### 6. Resetting or New Prediction

- Click **"← Back to Form"** button
- Modify values as needed
- Click **"Predict Risk"** again for new prediction

## Using the API

### Interactive Documentation

Visit http://localhost:8000/docs for interactive API documentation where you can:
- See all available endpoints
- Test API calls directly in browser
- View request/response schemas
- Download OpenAPI specification

### Common API Workflows

#### 1. Check System Health
```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "ok",
  "model_loaded": true,
  "features_count": 16
}
```

#### 2. Get Model Information
```bash
curl http://localhost:8000/model/info
```

Use this to see which features are required for prediction.

#### 3. Single Student Prediction
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "gpa": 3.5,
      "attendance_rate": 0.90,
      "failed_courses": 0,
      "credit_hours": 15,
      "library_visits": 10,
      "tutoring_sessions": 3,
      "office_hours_visits": 2,
      "club_participation": 1,
      "age": 20,
      "first_generation": 0,
      "financial_aid": 1,
      "work_hours_per_week": 12,
      "counseling_visits": 1,
      "health_center_visits": 1,
      "advisor_meetings": 2,
      "study_group_participation": 1
    }
  }'
```

#### 4. Batch Predictions from CSV
```bash
# Create CSV file
cat > students.csv << EOF
gpa,attendance_rate,failed_courses,credit_hours,...
3.7,0.95,0,16,...
2.0,0.65,3,12,...
EOF

# Upload and predict
curl -X POST http://localhost:8000/batch/predict \
  -F "file=@students.csv"
```

#### 5. Integration Examples

**Python Script**:
```python
import requests
import pandas as pd

# Load student data
df = pd.read_csv('students.csv')

# Predict for each student
results = []
for _, row in df.iterrows():
    response = requests.post('http://localhost:8000/predict', 
                           json={'data': row.to_dict()})
    results.append(response.json())

# Save results
pd.DataFrame(results).to_csv('predictions.csv')
```

**JavaScript/Node.js**:
```javascript
const axios = require('axios');

async function predictRisk(studentData) {
  const response = await axios.post('http://localhost:8000/predict', {
    data: studentData
  });
  return response.data;
}

// Use in your application
const result = await predictRisk({
  gpa: 3.5,
  attendance_rate: 0.90,
  // ... other features
});

console.log(`Risk: ${result.risk_band}, Probability: ${result.dropout_probability}`);
```

## Best Practices

### Data Quality
1. **Complete Data**: Ensure all 16 features are provided
2. **Accurate Values**: Use actual measured values, not estimates
3. **Consistent Units**: Follow the specified ranges
4. **Recent Data**: Use current semester data for best accuracy

### Prediction Frequency
- **High Risk Students**: Re-predict weekly or bi-weekly
- **Medium Risk Students**: Re-predict monthly
- **Low Risk Students**: Re-predict each semester

### Interpretation
1. **Don't rely on single prediction**: Consider trends over time
2. **Context matters**: Combine predictions with human judgment
3. **Focus on top drivers**: Address the most influential factors
4. **Multiple interventions**: Tackle several risk factors simultaneously

### Privacy & Ethics
1. **Data Privacy**: Protect student information
2. **Informed Consent**: Students should know they're being assessed
3. **Human Oversight**: Use as decision support, not sole decision maker
4. **Bias Awareness**: Monitor for potential model biases
5. **Right to Explanation**: Provide SHAP explanations to students

## Advanced Usage

### Custom Thresholds

Adjust risk band thresholds in API calls:
```bash
curl -X POST http://localhost:8000/risk/band \
  -H "Content-Type: application/json" \
  -d '{
    "data": {...},
    "low": 0.25,
    "medium": 0.65
  }'
```

### Batch Processing

For large student populations:
1. Export student data to CSV with all 16 features
2. Use `/batch/predict` endpoint
3. Process results in your SIS or data warehouse
4. Generate intervention lists by risk band

### Integration with SIS

Example integration pattern:
```python
# 1. Query student data from SIS
students = query_sis_database()

# 2. Transform to required format
features = transform_to_model_features(students)

# 3. Get predictions
predictions = batch_predict(features)

# 4. Update SIS with risk flags
update_sis_risk_flags(predictions)

# 5. Generate intervention reports
generate_advisor_reports(predictions)
```

### Monitoring & Alerting

Set up automated alerts:
```python
# Daily batch prediction
results = predict_all_students()

# Alert for high-risk students
high_risk = [s for s in results if s['risk_band'] == 'High']

if high_risk:
    send_alert_to_advisors(high_risk)
```

### Model Retraining

Periodically retrain with actual outcome data:
```bash
cd backend
source venv/bin/activate

# Prepare your data with actual outcomes
# Update train_model.py to use your data

python train_model.py
```

## Troubleshooting

### Common Issues

**"Model not loaded" error**:
```bash
cd backend
source venv/bin/activate
python train_model.py
```

**API connection failed**:
- Verify backend is running: `curl http://localhost:8000/health`
- Check frontend .env: `VITE_API_URL=http://localhost:8000`
- Verify no firewall blocking

**Incorrect predictions**:
- Verify all 16 features are provided
- Check value ranges are correct
- Ensure model is trained

**SHAP values missing**:
- SHAP explainer may not be loaded
- Retrain model to ensure explainer is included

## Getting Help

- **Documentation**: See README.md for detailed information
- **API Docs**: http://localhost:8000/docs for API reference
- **Examples**: See API_EXAMPLES.md for code samples
- **Deployment**: See DEPLOYMENT.md for production setup

## Tips for Success

1. **Start with samples**: Use the preset data to understand the system
2. **Focus on patterns**: Look for common risk factors across students
3. **Track interventions**: Document what works
4. **Regular monitoring**: Don't wait until problems are severe
5. **Holistic approach**: Consider all aspects of student success

---

**Remember**: This is a decision support tool. Always combine AI predictions with human judgment and institutional knowledge.
