# MLOps Pipeline Setup Checklist ✅

## Before You Start
- [ ] Have GitHub account and repository access
- [ ] Docker installed and running locally
- [ ] Python 3.11+ with pip installed

## Account Setup
- [ ] Create DagHub account at https://dagshub.com
- [ ] Create DockerHub account at https://hub.docker.com
- [ ] Get DagHub token from https://dagshub.com/user/settings/tokens

## GitHub Configuration
- [ ] Go to Repository → Settings → Secrets and variables → Actions
- [ ] Add secret: `DAGSHUB_USERNAME` (your DagHub username)
- [ ] Add secret: `DAGSHUB_TOKEN` (token from DagHub)
- [ ] Add secret: `DOCKER_USERNAME` (your DockerHub username)  
- [ ] Add secret: `DOCKER_PASSWORD` (your DockerHub password/token)

## Repository Configuration
- [ ] Update `.dvc/config` with your DagHub repository URL
- [ ] Update workflow file if needed (change `Bardakor/mlflow-with-daghub` references)

## Local Testing (Optional)
- [ ] Run `pip install -r requirements.txt`
- [ ] Run `python run_notebook.py`
- [ ] Run `python generate_metadata.py`
- [ ] Run `./test_docker_local.sh`

## Deployment
- [ ] Push to main branch: `git push origin main`
- [ ] Monitor GitHub Actions in your repository
- [ ] Check DagHub for MLflow experiments
- [ ] Verify DockerHub image upload

## Final Testing
- [ ] Pull image: `docker pull YOUR_DOCKERHUB_USERNAME/mlflow-model:latest`
- [ ] Run container: `docker run -d -p 5000:5000 --name test YOUR_DOCKERHUB_USERNAME/mlflow-model:latest`
- [ ] Test API: `python test_api.py`
- [ ] Clean up: `docker stop test && docker rm test`

## Demo Recording
Record your screen showing:
- [ ] DagHub experiments page with your ML runs
- [ ] GitHub Actions successful pipeline
- [ ] DockerHub repository with uploaded image
- [ ] Local test of pulled DockerHub image
- [ ] API working and returning predictions

## Quick Commands

### Local API Test:
```bash
python app.py &
sleep 5
python test_api.py
pkill -f "python app.py"
```

### Docker Test:
```bash
./test_docker_local.sh
```

### Pull and Test DockerHub Image:
```bash
# Replace YOUR_USERNAME with your actual DockerHub username
docker pull YOUR_USERNAME/mlflow-model:latest
docker run -d -p 5000:5000 --name api-test YOUR_USERNAME/mlflow-model:latest
sleep 10
python test_api.py
docker stop api-test && docker rm api-test
```

## Expected API Endpoints:
- `GET http://localhost:5000/health` - Health check
- `GET http://localhost:5000/model_info` - Model metadata
- `POST http://localhost:5000/predict` - Make predictions

## Need Help?
Check `SETUP_GUIDE.md` for detailed instructions and troubleshooting! 