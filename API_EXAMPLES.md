# API Usage Examples

## Using cURL

### Health Check
```bash
curl http://localhost:8000/health
```

### Get Model Information
```bash
curl http://localhost:8000/model/info
```

### Single Prediction - Low Risk Student
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "gpa": 3.7,
      "attendance_rate": 0.95,
      "failed_courses": 0,
      "credit_hours": 16,
      "library_visits": 15,
      "tutoring_sessions": 5,
      "office_hours_visits": 4,
      "club_participation": 2,
      "age": 19,
      "first_generation": 0,
      "financial_aid": 0,
      "work_hours_per_week": 10,
      "counseling_visits": 2,
      "health_center_visits": 1,
      "advisor_meetings": 3,
      "study_group_participation": 1
    }
  }'
```

### Single Prediction - High Risk Student
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "gpa": 2.0,
      "attendance_rate": 0.65,
      "failed_courses": 3,
      "credit_hours": 12,
      "library_visits": 2,
      "tutoring_sessions": 0,
      "office_hours_visits": 0,
      "club_participation": 0,
      "age": 22,
      "first_generation": 1,
      "financial_aid": 1,
      "work_hours_per_week": 30,
      "counseling_visits": 0,
      "health_center_visits": 1,
      "advisor_meetings": 1,
      "study_group_participation": 0
    }
  }'
```

### Get Top Risk Drivers
```bash
curl -X POST http://localhost:8000/explanations/top-drivers \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "gpa": 2.5,
      "attendance_rate": 0.75,
      "failed_courses": 2,
      "credit_hours": 14,
      "library_visits": 5,
      "tutoring_sessions": 1,
      "office_hours_visits": 1,
      "club_participation": 1,
      "age": 20,
      "first_generation": 1,
      "financial_aid": 1,
      "work_hours_per_week": 20,
      "counseling_visits": 1,
      "health_center_visits": 2,
      "advisor_meetings": 2,
      "study_group_participation": 0
    }
  }'
```

### Risk Band Assessment
```bash
curl -X POST http://localhost:8000/risk/band \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "gpa": 3.0,
      "attendance_rate": 0.80,
      "failed_courses": 1,
      "credit_hours": 15,
      "library_visits": 8,
      "tutoring_sessions": 2,
      "office_hours_visits": 2,
      "club_participation": 1,
      "age": 20,
      "first_generation": 0,
      "financial_aid": 1,
      "work_hours_per_week": 15,
      "counseling_visits": 1,
      "health_center_visits": 1,
      "advisor_meetings": 2,
      "study_group_participation": 1
    }
  }'
```

### Batch Prediction
```bash
# First, create a sample CSV file
cat > students.csv << EOF
gpa,attendance_rate,failed_courses,credit_hours,library_visits,tutoring_sessions,office_hours_visits,club_participation,age,first_generation,financial_aid,work_hours_per_week,counseling_visits,health_center_visits,advisor_meetings,study_group_participation
3.7,0.95,0,16,15,5,4,2,19,0,0,10,2,1,3,1
2.0,0.65,3,12,2,0,0,0,22,1,1,30,0,1,1,0
3.0,0.80,1,15,8,2,2,1,20,0,1,15,1,1,2,1
EOF

# Upload and predict
curl -X POST http://localhost:8000/batch/predict \
  -F "file=@students.csv"
```

## Using Python

### Install requests library
```bash
pip install requests
```

### Python Script
```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Health check
response = requests.get(f"{BASE_URL}/health")
print("Health:", response.json())

# Model info
response = requests.get(f"{BASE_URL}/model/info")
print("Model Info:", json.dumps(response.json(), indent=2))

# Prediction
student_data = {
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
}

response = requests.post(f"{BASE_URL}/predict", json=student_data)
result = response.json()

print("\nPrediction Result:")
print(f"  Prediction: {result['prediction']}")
print(f"  Dropout Probability: {result['dropout_probability']:.2%}")
print(f"  Risk Band: {result['risk_band']}")

if 'top_risk_drivers' in result:
    print("\n  Top Risk Drivers:")
    for feature, value in result['top_risk_drivers'].items():
        direction = "↑" if value > 0 else "↓"
        print(f"    {direction} {feature}: {value:.4f}")
```

## Using JavaScript/Node.js

### Install axios
```bash
npm install axios
```

### JavaScript Script
```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000';

async function predictStudentRisk() {
  try {
    // Health check
    const health = await axios.get(`${BASE_URL}/health`);
    console.log('Health:', health.data);

    // Prediction
    const studentData = {
      data: {
        gpa: 3.5,
        attendance_rate: 0.90,
        failed_courses: 0,
        credit_hours: 15,
        library_visits: 10,
        tutoring_sessions: 3,
        office_hours_visits: 2,
        club_participation: 1,
        age: 20,
        first_generation: 0,
        financial_aid: 1,
        work_hours_per_week: 12,
        counseling_visits: 1,
        health_center_visits: 1,
        advisor_meetings: 2,
        study_group_participation: 1
      }
    };

    const prediction = await axios.post(`${BASE_URL}/predict`, studentData);
    const result = prediction.data;

    console.log('\nPrediction Result:');
    console.log(`  Prediction: ${result.prediction}`);
    console.log(`  Dropout Probability: ${(result.dropout_probability * 100).toFixed(2)}%`);
    console.log(`  Risk Band: ${result.risk_band}`);

    if (result.top_risk_drivers) {
      console.log('\n  Top Risk Drivers:');
      Object.entries(result.top_risk_drivers).forEach(([feature, value]) => {
        const direction = value > 0 ? '↑' : '↓';
        console.log(`    ${direction} ${feature}: ${value.toFixed(4)}`);
      });
    }
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

predictStudentRisk();
```

## Response Examples

### Successful Prediction Response
```json
{
  "prediction": "Retained",
  "dropout_probability": 0.1234,
  "risk_band": "Low",
  "top_risk_drivers": {
    "gpa": -0.2341,
    "attendance_rate": -0.1567,
    "failed_courses": 0.0234,
    "library_visits": -0.0987,
    "work_hours_per_week": 0.0654
  },
  "all_shap_values": {
    "gpa": -0.2341,
    "attendance_rate": -0.1567,
    ...
  }
}
```

### Error Response
```json
{
  "detail": "Missing feature: gpa"
}
```

### Batch Prediction Response
```json
{
  "count": 3,
  "results": [
    {
      "row": 0,
      "dropout_probability": 0.1234,
      "risk_band": "Low"
    },
    {
      "row": 1,
      "dropout_probability": 0.8765,
      "risk_band": "High"
    },
    {
      "row": 2,
      "dropout_probability": 0.4567,
      "risk_band": "Medium"
    }
  ]
}
```

## Testing Tips

1. **Use the Interactive Docs**: Visit http://localhost:8000/docs for an interactive API explorer
2. **Check Health First**: Always verify the API is running with `/health`
3. **Verify Model Info**: Use `/model/info` to see which features are required
4. **Test with Samples**: Use the provided high-risk and low-risk examples
5. **Monitor Logs**: Watch the backend logs for detailed error messages
