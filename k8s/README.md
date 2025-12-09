# BrandBook Kubernetes Deployment

This folder contains the Kubernetes manifest files required to deploy BrandBook to a Kubernetes cluster.

## 📁 File Structure

```
k8s/
├── namespace.yaml    # Kubernetes namespace
├── configmap.yaml    # Application configuration
├── secret.yaml       # API keys (base64 encoded)
├── deployment.yaml   # Pod deployment
├── service.yaml      # NodePort service
├── ingress.yaml      # Ingress (optional)
├── deploy.sh         # Automated deployment script
└── README.md         # This file
```

## 🚀 Quick Start

### 1. Start Kubernetes Cluster

**Docker Desktop Kubernetes:**
- Docker Desktop > Settings > Kubernetes > Enable Kubernetes

**Minikube:**
```bash
brew install minikube
minikube start
```

### 2. Configure API Keys

Encode your API keys with base64 and add them to `k8s/secret.yaml`:

```bash
# Encode OpenAI key
echo -n "sk-your-openai-key" | base64

# Paste the result into secret.yaml
```

### 3. Deploy

```bash
# Automated deployment
./k8s/deploy.sh

# Or manual deployment
kubectl apply -f k8s/
```

### 4. Access the Application

```bash
# Docker Desktop Kubernetes
http://localhost:30080

# Minikube
minikube service brandbook-service -n brandbook --url
```

## 📊 Management Commands

```bash
# List pods
kubectl get pods -n brandbook

# View logs
kubectl logs -f -n brandbook -l app=brandbook

# Check pod status
kubectl describe pod -n brandbook -l app=brandbook

# Scale deployment
kubectl scale deployment brandbook -n brandbook --replicas=3

# Delete all resources
kubectl delete -f k8s/
```

## ⚙️ Configuration

### Replica Count
Change the `replicas` value in `deployment.yaml`:
```yaml
spec:
  replicas: 3  # Run 3 pods
```

### Resource Limits
```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### Ingress (Optional)
Enable domain access with ingress.yaml:
```bash
kubectl apply -f k8s/ingress.yaml

# Add to /etc/hosts
echo "127.0.0.1 brandbook.local" | sudo tee -a /etc/hosts
```

## 🔧 Troubleshooting

**Pod not starting:**
```bash
kubectl describe pod -n brandbook -l app=brandbook
kubectl logs -n brandbook -l app=brandbook
```

**Image not found (minikube):**
```bash
minikube image load brandbook:latest
```

**Cannot access service:**
```bash
kubectl get svc -n brandbook
kubectl port-forward svc/brandbook-service 8000:8000 -n brandbook
```
