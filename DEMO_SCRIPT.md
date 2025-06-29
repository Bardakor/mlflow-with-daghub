# 📹 Demo Recording Script - Step by Step

## **IMPORTANT: Complete Setup BEFORE Recording**

### **Phase 1: Account Setup & Configuration** (Do this FIRST, before recording)

1. **Create DagHub Account**
   - Go to https://dagshub.com and create account
   - Create new repository or connect your GitHub repo
   - Get your token from https://dagshub.com/user/settings/tokens

2. **Create DockerHub Account** 
   - Go to https://hub.docker.com and create account
   - Create new repository (e.g., `your-username/mlflow-model`)

3. **Configure GitHub Secrets**
   - Go to your GitHub repo → Settings → Secrets and variables → Actions
   - Add these secrets:
     ```
     DAGSHUB_USERNAME=your-dagshub-username
     DAGSHUB_TOKEN=your-dagshub-token
     DOCKER_USERNAME=your-dockerhub-username  
     DOCKER_PASSWORD=your-dockerhub-password
     ```

4. **Update Repository Configuration**
   - Update `.dvc/config` with your DagHub repo URL
   - Update workflow file if using different repo name

5. **Trigger the Pipeline**
   ```bash
   git push origin main
   ```
   - Wait for GitHub Actions to complete successfully
   - Verify image is pushed to DockerHub

---

## **Phase 2: Recording the Demo** 🎬

### **Setup Before Recording**
```bash
# Make sure you're in the project directory
cd /path/to/mlflow-with-daghub

# Ensure no local processes are running
pkill -f "python app.py" 2>/dev/null || true

# Clear terminal for clean recording
clear
```

---

### **🎬 START RECORDING NOW**

### **Step 1: Show GitHub Actions Pipeline** (2-3 minutes)

1. **Open GitHub Repository**
   - Navigate to your GitHub repository
   - Click on "Actions" tab
   - Show the successful workflow run(s)

2. **Explain what you're showing:**
   ```
   "Here is my GitHub repository with the MLOps pipeline. 
   You can see in the Actions tab that the CI/CD pipeline 
   has run successfully. This pipeline automatically:
   - Trains the ML models using the MLflow notebook
   - Builds a Docker image with the best model
   - Pushes the image to DockerHub"
   ```

3. **Click on the latest successful run**
   - Show the workflow steps (build, test, deploy)
   - Point out the "Build and push Docker image" step
   - Show that it completed successfully

---

### **Step 2: Show DagHub Experiments** (2-3 minutes)

1. **Navigate to DagHub**
   - Go to https://dagshub.com/YOUR-USERNAME/YOUR-REPO-NAME.mlflow
   - Or click the MLflow link from your DagHub repository

2. **Show the Experiments**
   ```
   "Here is my DagHub MLflow tracking page. You can see 
   the experiments that were automatically logged by the pipeline.
   Each run shows different hyperparameters and their results."
   ```

3. **Click on experiment runs**
   - Show the parameters (n_estimators, max_depth)
   - Show the metrics (accuracy)
   - Show the model artifacts if available

4. **Explain the tracking:**
   ```
   "The pipeline automatically tracks all experiments with 
   different hyperparameters and saves the best performing model 
   for deployment in the Docker container."
   ```

---

### **Step 3: Show DockerHub Repository** (1-2 minutes)

1. **Navigate to DockerHub**
   - Go to https://hub.docker.com
   - Navigate to your repository (your-username/mlflow-model)

2. **Show the uploaded image:**
   ```
   "Here is my DockerHub repository showing the Docker image 
   that was automatically built and pushed by the GitHub Actions 
   pipeline. You can see the 'latest' tag and when it was uploaded."
   ```

3. **Show image details**
   - Click on the image to show details
   - Show the size and layers
   - Note the recent push time

---

### **Step 4: Pull and Run Docker Image Locally** (3-4 minutes)

1. **Open Terminal** 
   ```bash
   # Clear terminal for clean demo
   clear
   
   # Show current directory
   pwd
   ```

2. **Pull the image from DockerHub:**
   ```bash
   # Replace YOUR_USERNAME with your actual DockerHub username
   docker pull YOUR_USERNAME/mlflow-model:latest
   ```
   
   **Say while it's pulling:**
   ```
   "Now I'm pulling the Docker image that was automatically 
   built and uploaded by the pipeline from DockerHub to my local machine."
   ```

3. **Run the container:**
   ```bash
   # Run the container
   docker run -d -p 5000:5000 --name mlflow-demo YOUR_USERNAME/mlflow-model:latest
   
   # Wait a moment for it to start
   sleep 10
   
   # Check if it's running
   docker ps
   ```

4. **Test the API endpoints:**
   ```bash
   # Test health endpoint
   curl http://localhost:5000/health
   
   # Test model info endpoint  
   curl http://localhost:5000/model_info
   ```

5. **Run comprehensive API test:**
   ```bash
   # Run the test script
   python test_api.py
   ```

6. **Explain what's happening:**
   ```
   "The API is now running locally from the DockerHub image. 
   You can see it responds to health checks, provides model 
   information including accuracy and parameters, and can 
   make predictions on new data. This proves the entire 
   pipeline works end-to-end."
   ```

---

### **Step 5: Show API Response in Browser** (1 minute)

1. **Open web browser**
   - Navigate to http://localhost:5000/health
   - Navigate to http://localhost:5000/model_info

2. **Show the JSON responses:**
   ```
   "Here you can see the API responding with JSON data including 
   the model metadata, accuracy metrics, and health status."
   ```

---

### **Step 6: Cleanup and Summary** (1 minute)

1. **Stop the container:**
   ```bash
   # Stop and remove the container
   docker stop mlflow-demo
   docker rm mlflow-demo
   
   # Verify it's stopped
   docker ps
   ```

2. **Final summary:**
   ```
   "To summarize what I've demonstrated:
   
   1. ✅ GitHub Actions pipeline automatically builds and deploys
   2. ✅ MLflow experiments are tracked in DagHub  
   3. ✅ Docker image is automatically pushed to DockerHub
   4. ✅ The deployed model works perfectly when pulled and run locally
   5. ✅ The REST API serves predictions with the best trained model
   
   This shows a complete MLOps pipeline from training to deployment."
   ```

---

## **🎬 STOP RECORDING**

### **Total Recording Time: ~10-15 minutes**

---

## **Quick Commands Reference** (Keep this handy during recording)

```bash
# Before recording - clear terminal
clear

# Pull from DockerHub (replace YOUR_USERNAME)
docker pull YOUR_USERNAME/mlflow-model:latest

# Run container
docker run -d -p 5000:5000 --name mlflow-demo YOUR_USERNAME/mlflow-model:latest

# Wait and check
sleep 10 && docker ps

# Test API
curl http://localhost:5000/health
curl http://localhost:5000/model_info
python test_api.py

# Cleanup
docker stop mlflow-demo && docker rm mlflow-demo
```

## **URLs to Have Ready**
- GitHub repo: `https://github.com/YOUR_USERNAME/YOUR_REPO_NAME`
- DagHub MLflow: `https://dagshub.com/YOUR_USERNAME/YOUR_REPO_NAME.mlflow`  
- DockerHub: `https://hub.docker.com/r/YOUR_USERNAME/mlflow-model`

## **What NOT to Show**
- ❌ Don't show setup/configuration steps
- ❌ Don't show failed attempts or errors
- ❌ Don't show account creation process
- ❌ Don't show secret configuration

## **Recording Tips**
- 🎯 Keep narration clear and concise
- 🎯 Wait for pages to load completely before speaking
- 🎯 Use full screen for each application
- 🎯 Speak while actions are happening
- 🎯 Have URLs ready in bookmarks or text file 