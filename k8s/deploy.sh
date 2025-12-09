#!/bin/bash
# BrandBook Kubernetes Deployment Script
# This script deploys BrandBook to a local Kubernetes cluster

set -e

echo "🚀 BrandBook Kubernetes Deployment"
echo "===================================="

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install it first."
    echo "   brew install kubectl"
    exit 1
fi

# Check if cluster is running
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Kubernetes cluster is not running."
    echo "   Start minikube: minikube start"
    echo "   Or Docker Desktop Kubernetes"
    exit 1
fi

echo "✅ Kubernetes cluster is running"

# Build Docker image
echo ""
echo "📦 Building Docker image..."
docker build -t brandbook:latest .

# For minikube: load image into minikube
if command -v minikube &> /dev/null; then
    echo "📤 Loading image to minikube..."
    minikube image load brandbook:latest
fi

# Apply Kubernetes manifests
echo ""
echo "🔧 Applying Kubernetes manifests..."

kubectl apply -f k8s/namespace.yaml
echo "✅ Namespace created"

kubectl apply -f k8s/configmap.yaml
echo "✅ ConfigMap created"

# Check if secret has API keys
echo ""
echo "⚠️  Make sure to add your API keys to k8s/secret.yaml"
echo "   Run: echo -n 'your-api-key' | base64"
echo ""

kubectl apply -f k8s/secret.yaml
echo "✅ Secret created"

kubectl apply -f k8s/deployment.yaml
echo "✅ Deployment created"

kubectl apply -f k8s/service.yaml
echo "✅ Service created"

# Wait for deployment
echo ""
echo "⏳ Waiting for deployment to be ready..."
kubectl rollout status deployment/brandbook -n brandbook --timeout=120s

# Get service info
echo ""
echo "===================================="
echo "🎉 BrandBook deployed successfully!"
echo "===================================="
echo ""

# Check if using minikube
if command -v minikube &> /dev/null; then
    echo "🌐 Access URL (minikube):"
    minikube service brandbook-service -n brandbook --url
else
    echo "🌐 Access URL: http://localhost:30080"
fi

echo ""
echo "📊 Useful commands:"
echo "   kubectl get pods -n brandbook        # List pods"
echo "   kubectl logs -f -n brandbook -l app=brandbook  # View logs"
echo "   kubectl delete -f k8s/               # Delete all resources"
