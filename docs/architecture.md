# Architecture Overview

## AI Engine
- **Ensemble Classifier:** EfficientNet-B4, EfficientNet-B5, Vision Transformer (ViT), and Swin Transformer. A meta-learner stack combines the features.
- **Segmentation:** U-Net++ and DeepLabV3+ with EfficientNet-B3 encoders.
- **Explainability:** Grad-CAM, Grad-CAM++, and SHAP integration to provide visualization of disease indicators.
- **Risk Prediction:** XGBoost/CatBoost models for longitudinal disease progression forecasting.

## Backend (FastAPI)
- Exposes RESTful endpoints for inference and report generation.
- Secures endpoints with JWT Auth.
- Implements async processing and integrates tightly with PyTorch models.

## Frontend (React)
- Vite + React + TS + Tailwind CSS for a modern, responsive, glassmorphic UI.
- Displays inference results, lesion bounding/segmentation masks, and longitudinal risk prediction graphs.

## MLOps & Deployment
- Model tracking using MLflow and DVC.
- CI/CD via GitHub Actions.
- Dockerized deployment targeting Kubernetes clusters with GPU node support.
