#!/bin/bash
# DVC and MLflow initialization script for MLOps tracking

echo "Initializing MLOps Tracking..."

# Check if dvc is installed
if ! command -v dvc &> /dev/null
then
    echo "DVC could not be found. Please install via 'pip install dvc'."
    exit 1
fi

# Init DVC
if [ ! -d ".dvc" ]; then
    dvc init
    echo "DVC initialized."
    
    # Setup remote (dummy s3 bucket for illustration)
    dvc remote add -d myremote s3://mybucket/dvcstore
    
    # Commit
    git add .dvc/config
    git commit -m "Initialize DVC"
else
    echo "DVC already initialized."
fi

# Create mlflow tracking directory
mkdir -p ./mlruns
echo "MLflow tracking directory initialized."

echo "MLOps initialization complete."
