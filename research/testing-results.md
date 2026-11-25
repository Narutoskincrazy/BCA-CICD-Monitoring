# Project Testing Results

## 1. Testing Environment

- Project: BCA CI/CD Monitoring System
- Testing Date: 25 November 2026
- Operating Environment: Linux (WSL Ubuntu)
- Python Version: 3.14.4
- Pytest Version: 9.2.0
- Docker Image: bca-cicd-monitoring:v5

## 2. Application Health Check

The application was started using its Docker container.

- Container Name: bca-cicd-app
- Container Status: Running
- Port Mapping: 5000:5001
- Health Endpoint: /health
- Observed Application Status: healthy

The health API returned the application name, status, and timestamp.

## 3. Automated Testing Results

Five automated test cases were executed using Pytest.

| Test Case | Result |
|---|---|
| Home page test | PASSED |
| Health check test | PASSED |
| Deployment record test | PASSED |
| Invalid deployment data test | PASSED |
| Deployment comparison API test | PASSED |

## 4. Test Summary

- Total Test Cases: 5
- Passed: 5
- Failed: 0
- Execution Time: 0.25 seconds
- Pass Rate: 100%

## 5. Interpretation

All five automated test cases passed successfully. The results indicate that the tested dashboard, health endpoint, deployment record functionality, input validation, and deployment comparison API behaved as expected during this test execution.

These results represent the observed outcome of this particular test run.
