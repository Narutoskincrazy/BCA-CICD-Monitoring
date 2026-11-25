# Deployment Experiment Results

Date: 25 November 2026
Project: CI/CD-Based Deployment Monitoring and Failure Analysis System

## Experiment 1: Automated CI Pipeline

- Platform: GitHub Actions
- Runner: ubuntu-latest
- Workflow: BCA CI-CD Pipeline
- Run ID: 45564129159
- Result: Success
- Observed execution time: 19 seconds

## Experiment 2: Manual Local Validation

- Platform: WSL Ubuntu
- Python version: 3.14.4
- Docker image: bca-cicd-manual-test
- Pytest result: 5 passed, 0 failed
- Docker image build: Successful
- Temporary container: Started successfully
- Health check: Passed
- Container cleanup: Successful
- Observed execution time: 4 seconds

## Interpretation and Limitations

Both validation processes completed successfully.

The observed times are not a controlled performance comparison.
The automated workflow ran on a GitHub-hosted runner, while the
manual validation ran locally in WSL Ubuntu. The local Docker build
used cached image layers. Hardware, environment, dependency setup,
and caching may affect execution time.

Further repeated and controlled experiments are required before
drawing conclusions about relative deployment performance.

These measurements represent validation workflows, not production
server deployment times.
