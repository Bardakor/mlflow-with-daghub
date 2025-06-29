# ✅ Pre-Recording Checklist

## **MUST COMPLETE BEFORE RECORDING**

### **Account Setup** ✅
- [ ] DagHub account created at https://dagshub.com
- [ ] DagHub repository created/connected
- [ ] DagHub token obtained from settings/tokens
- [ ] DockerHub account created at https://hub.docker.com  
- [ ] DockerHub repository created (e.g., your-username/mlflow-model)

### **GitHub Configuration** ✅
- [ ] GitHub repository contains all the MLOps pipeline code
- [ ] GitHub Secrets configured:
  - [ ] `DAGSHUB_USERNAME` 
  - [ ] `DAGSHUB_TOKEN`
  - [ ] `DOCKER_USERNAME`
  - [ ] `DOCKER_PASSWORD`

### **Repository Updates** ✅
- [ ] Updated `.dvc/config` with your DagHub repository URL
- [ ] Updated workflow references if using different repo name
- [ ] All code committed and pushed to main branch

### **Pipeline Execution** ✅
- [ ] Pushed code to main branch to trigger GitHub Actions
- [ ] GitHub Actions pipeline completed successfully
- [ ] Docker image pushed to DockerHub successfully
- [ ] DagHub shows MLflow experiments from the pipeline run

### **Verification Tests** ✅
Run these commands to verify everything works:

```bash
# 1. Check GitHub Actions status
# Go to GitHub repo → Actions tab → Should show green checkmarks

# 2. Check DagHub experiments  
# Go to https://dagshub.com/YOUR-USERNAME/YOUR-REPO-NAME.mlflow
# Should show experiment runs with metrics

# 3. Check DockerHub image
# Go to https://hub.docker.com/r/YOUR-USERNAME/mlflow-model
# Should show recent image push

# 4. Test local Docker pull and run
docker pull YOUR-USERNAME/mlflow-model:latest
docker run -d -p 5001:5000 --name test-container YOUR-USERNAME/mlflow-model:latest
sleep 10
curl http://localhost:5001/health
docker stop test-container && docker rm test-container
```

### **Recording Setup** ✅
- [ ] Screen recording software ready
- [ ] Browser bookmarks ready:
  - [ ] Your GitHub repository
  - [ ] Your DagHub MLflow page
  - [ ] Your DockerHub repository
- [ ] Terminal ready with project directory
- [ ] No local Flask processes running: `pkill -f "python app.py"`
- [ ] Demo script handy for reference

---

## **Quick Pre-Flight Test** 🧪

Run this to make sure everything is working:

```bash
# Navigate to project directory
cd /path/to/mlflow-with-daghub

# Stop any running processes
pkill -f "python app.py" 2>/dev/null || true

# Quick test of DockerHub image
echo "Testing DockerHub image..."
docker pull YOUR-USERNAME/mlflow-model:latest
docker run -d -p 5001:5000 --name preflight-test YOUR-USERNAME/mlflow-model:latest
sleep 15

# Test API
if curl -s http://localhost:5001/health | grep -q "healthy"; then
    echo "✅ Docker image working!"
else
    echo "❌ Docker image not working - check setup"
fi

# Cleanup
docker stop preflight-test && docker rm preflight-test

echo "Ready for recording!"
```

---

## **If Something Doesn't Work** ❌

### **GitHub Actions Failed**
- Check GitHub Secrets are correctly set
- Check `.dvc/config` has correct DagHub URL
- Re-run the workflow manually

### **No DagHub Experiments**
- Verify DAGSHUB_TOKEN has correct permissions
- Check notebook runs successfully locally with `python run_notebook.py`
- Check DagHub repository connection

### **DockerHub Image Missing** 
- Verify DOCKER_USERNAME and DOCKER_PASSWORD secrets
- Check DockerHub repository exists and is public
- Re-run GitHub Actions workflow

### **Docker Pull/Run Fails**
- Verify image name matches your DockerHub repository
- Check image was actually pushed (check DockerHub website)
- Try different port if 5000 is in use

---

## **Recording Day Checklist** 📹

**30 minutes before recording:**
- [ ] Run pre-flight test above
- [ ] Clear browser cache/history for clean demo
- [ ] Close unnecessary applications
- [ ] Prepare clean desktop
- [ ] Test screen recording software

**Just before recording:**
- [ ] Clear terminal: `clear`
- [ ] Navigate to project directory
- [ ] Have demo script open for reference
- [ ] Have URLs ready in browser tabs
- [ ] Start screen recording

**Ready to record!** 🎬 