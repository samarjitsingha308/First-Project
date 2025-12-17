#!/usr/bin/env python3
"""
Quick test script for Student Risk Prediction API
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✓ Health check: {response.json()}")
        return True
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False

def test_model_info():
    """Test model info endpoint"""
    print("\nTesting /model/info endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/model/info")
        info = response.json()
        print(f"✓ Model type: {info['model_type']}")
        print(f"✓ Features: {info['feature_count']}")
        return True
    except Exception as e:
        print(f"✗ Model info failed: {e}")
        return False

def test_prediction():
    """Test prediction endpoint"""
    print("\nTesting /predict endpoint...")
    
    # High-risk student
    high_risk_student = {
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
            "study_group_participation": 0,
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=high_risk_student)
        result = response.json()
        
        print(f"✓ Prediction: {result['prediction']}")
        print(f"✓ Dropout Probability: {result['dropout_probability']:.2%}")
        print(f"✓ Risk Band: {result['risk_band']}")
        
        if 'top_risk_drivers' in result:
            print("✓ Top Risk Drivers:")
            for feature, value in list(result['top_risk_drivers'].items())[:3]:
                direction = "↑" if value > 0 else "↓"
                print(f"    {direction} {feature}: {value:.4f}")
        
        return True
    except Exception as e:
        print(f"✗ Prediction failed: {e}")
        return False

def test_low_risk_prediction():
    """Test prediction with low-risk student"""
    print("\nTesting low-risk student prediction...")
    
    low_risk_student = {
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
            "study_group_participation": 1,
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=low_risk_student)
        result = response.json()
        
        print(f"✓ Prediction: {result['prediction']}")
        print(f"✓ Dropout Probability: {result['dropout_probability']:.2%}")
        print(f"✓ Risk Band: {result['risk_band']}")
        
        return True
    except Exception as e:
        print(f"✗ Prediction failed: {e}")
        return False

def main():
    print("="*60)
    print("Student Risk Prediction API - Test Script")
    print("="*60)
    print(f"\nTesting API at: {BASE_URL}")
    print("Make sure the backend is running before executing this test.")
    print("="*60)
    
    tests = [
        test_health,
        test_model_info,
        test_prediction,
        test_low_risk_prediction
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed!")
        sys.exit(0)
    else:
        print("✗ Some tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
