# Design and Implementation of a CI/CD-Based Deployment Monitoring and Failure Analysis System

## 1. Project Overview

The BCA CI/CD Monitoring System is a Python Flask-based web application designed to record deployment activities, monitor deployment status, analyze failures, and compare manual and automated deployment processes.

The project demonstrates how DevOps tools and automation can improve application testing and deployment verification.

## 2. Objectives

- Develop a web-based deployment monitoring dashboard.
- Store deployment records using SQLite.
- Track successful and failed deployments.
- Analyze recorded deployment failures.
- Compare manual and automated deployment durations.
- Automate application testing using Pytest.
- Build a Docker image for application packaging.
- Implement a GitHub Actions CI pipeline.
- Verify application health using an API endpoint.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application programming |
| Flask | Web framework |
| HTML/CSS | Dashboard interface |
| SQLite | Database |
| Docker | Application containerization |
| Git and GitHub | Version control |
| GitHub Actions | CI automation |
| Pytest | Automated testing |
| Linux (Ubuntu/WSL) | Development environment |

## 4. System Features

- Deployment history dashboard
- Success and failure statistics
- Deployment record management
- Failure analysis API
- Manual vs automated deployment comparison
- Application health-check API
- Automated test execution
- Docker image creation
- CI pipeline health verification

## 5. Project Structure

```text
BCA-CICD-Project/
├── .github/
│   └── workflows/
│       └── cicd.yml
├── app/
│   ├── app.py
│   └── templates/
│       └── index.html
├── data/
│   └── deployments.db
├── tests/
│   └── test_app.py
├── .dockerignore
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

## 6. Installation and Setup

Clone the repository:

```bash
git clone https://github.com/Narutoskincrazy/BCA-CICD-Monitoring.git
cd BCA-CICD-Monitoring
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app/app.py
```

Open the application:

http://localhost:5001

## 7. Automated Testing

Run the test suite:

```bash
python -m pytest -v
```

The tests verify the home page, health endpoint, deployment record storage, invalid input handling, and deployment comparison API.

## 8. Docker Setup

Build the Docker image:

```bash
docker build -t bca-cicd-monitoring:v1 .
```

Run the container:

```bash
docker run -d \
  --name bca-cicd-app \
  -p 5000:5001 \
  -v "$(pwd)/data:/app/data" \
  bca-cicd-monitoring:v1
```

Open:

http://localhost:5000

Check application health:

```bash
curl http://localhost:5000/health
```

## 9. CI Pipeline

The GitHub Actions workflow performs the following operations:

1. Checks out the repository code.
2. Sets up Python.
3. Installs project dependencies.
4. Executes automated tests.
5. Builds the Docker image.
6. Starts a temporary application container on the GitHub-hosted runner.
7. Checks the application health endpoint.
8. Removes the temporary test container.

This workflow verifies the application build and health. It does not perform production deployment to a remote server.

## 10. API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Display dashboard |
| `/health` | GET | Check application health |
| `/record` | POST | Save a deployment record |
| `/api/deployments` | GET | Retrieve deployment records |
| `/api/failure-analysis` | GET | Retrieve failure analysis |
| `/api/deployment-comparison` | GET | Compare deployment types |

## 11. Future Enhancements

- Integration with GitHub API for workflow information.
- Remote server deployment automation.
- Email notifications for deployment failures.
- Advanced deployment analytics.
- User authentication and access control.

## 12. Conclusion

This project demonstrates the practical use of Python, Flask, SQLite, Docker, Pytest, Git, and GitHub Actions in a DevOps-oriented application.

It provides a foundation for deployment monitoring, failure analysis, automated testing, and CI pipeline verification.
