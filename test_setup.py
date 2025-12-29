"""
Quick test script to verify the setup is correct
Run this before starting the server
"""

import sys

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = {
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'sentence_transformers': 'Sentence Transformers',
        'torch': 'PyTorch',
        'sklearn': 'Scikit-learn',
        'numpy': 'NumPy',
        'pydantic': 'Pydantic'
    }
    
    all_installed = True
    print("\n📦 Checking dependencies...")
    
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - Not installed")
            all_installed = False
    
    return all_installed

def check_files():
    """Check if all required files exist"""
    import os
    
    required_files = [
        'app.py',
        'search_engine.py',
        'requirements.txt',
        'static/index.html',
        'static/styles.css',
        'static/script.js'
    ]
    
    print("\n📁 Checking files...")
    all_exist = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - Missing")
            all_exist = False
    
    return all_exist

def test_imports():
    """Test if our modules can be imported"""
    print("\n🔧 Testing module imports...")
    
    try:
        from search_engine import BERTSearchEngine
        print("✅ search_engine.py imports successfully")
    except Exception as e:
        print(f"❌ search_engine.py import failed: {e}")
        return False
    
    try:
        import app
        print("✅ app.py imports successfully")
    except Exception as e:
        print(f"❌ app.py import failed: {e}")
        return False
    
    return True

def main():
    """Run all checks"""
    print("🔍 BERT Search Engine Setup Validation")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version()),
        ("Files", check_files()),
        ("Dependencies", check_dependencies()),
        ("Module Imports", test_imports())
    ]
    
    print("\n" + "=" * 50)
    print("📊 Summary:")
    print("=" * 50)
    
    all_passed = all(result for _, result in checks)
    
    for check_name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {check_name}")
    
    print("=" * 50)
    
    if all_passed:
        print("\n🎉 All checks passed! You're ready to start the server.")
        print("\nRun: python app.py")
        print("Or:  ./start.sh")
        print("\nThen open: http://localhost:8000")
    else:
        print("\n⚠️  Some checks failed. Please install missing dependencies:")
        print("\n    pip install -r requirements.txt")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
