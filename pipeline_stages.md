# CI/CD Pipeline Basics - DecodeLabs DevOps Project 3

## 1. What is CI/CD?

| Term | Full Form | Description |
|------|-----------|-------------|
| CI | Continuous Integration | Automatically build and test code every time a developer pushes changes |
| CD | Continuous Deployment | Automatically deploy the code to production after it passes all tests |
| CD | Continuous Delivery | Automatically prepare code for deployment, but require manual approval to deploy |

---

## 2. CI/CD Pipeline Stages

| Stage | Description | Tools |
|-------|-------------|-------|
| **Source** | Code is stored in version control (GitHub) | Git, GitHub |
| **Build** | Code is compiled or packaged | Docker, Maven, npm |
| **Test** | Automated tests are run | JUnit, PyTest, Selenium |
| **Deploy** | Code is deployed to servers | Kubernetes, AWS, Heroku |
| **Monitor** | Application is monitored for issues | Prometheus, Grafana |

---

## 3. CI/CD Pipeline Flow

---

### 📁 File: `github_actions.yml`

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        if [ -f requirements.txt ]; then
          pip install -r requirements.txt
        else
          echo "No requirements.txt found"
        fi
    
    - name: Run tests
      run: |
        if [ -f test.py ]; then
          python test.py
        else
          echo "No test file found"
        fi
    
    - name: Build
      run: |
        echo "✅ Build completed successfully!"
        echo "Build time: $(date)"
    
    - name: Display system info
      run: |
        echo "Python version: $(python --version)"
        echo "Current directory: $(pwd)"
        echo "Files in repository:"
        ls -la