# System Architecture

## 1. CI Pipeline Architecture

```mermaid
flowchart TD
    A[Developer] --> B[GitHub Repository]
    B --> C[GitHub Actions]
    C --> D[Python Setup]
    D --> E[Install Dependencies]
    E --> F[Pytest Automated Tests]
    F --> G[Docker Image Build]
    G --> H[Start Temporary Container]
    H --> I[Health API Check]
    I --> J[Cleanup Container]
```
## 2. Application Architecture

```mermaid
flowchart TD
    A[User Browser] --> B[Flask Web Application]
    B --> C[Dashboard]
    B --> D[Health API]
    B --> E[Deployment APIs]
    E --> F[SQLite Database]
    C --> F
```

## 3. Architecture Explanation

The developer pushes application code to the GitHub repository. GitHub Actions automatically starts the CI workflow.

The workflow installs dependencies, executes automated tests, builds a Docker image, starts a temporary container, and verifies application health.

The Flask application provides a dashboard and API endpoints. SQLite stores deployment records used for deployment history, statistics, and failure analysis.

The GitHub Actions container is a temporary test environment. It is not a production deployment to a remote server.
