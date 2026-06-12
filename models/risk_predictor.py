import xgboost as xgb
from catboost import CatBoostClassifier
import pandas as pd
import numpy as np

class DiseaseProgressionPredictor:
    def __init__(self, model_type="xgboost"):
        """
        Risk prediction engine for 1-year, 3-year, and 5-year DR progression.
        Inputs typically include: clinical data (HbA1c, BP, duration of diabetes) + image features
        """
        self.model_type = model_type.lower()
        if self.model_type == "xgboost":
            self.model = xgb.XGBClassifier(
                objective="binary:logistic",
                eval_metric="auc",
                max_depth=5,
                learning_rate=0.05,
                n_estimators=200
            )
        elif self.model_type == "catboost":
            self.model = CatBoostClassifier(
                iterations=500,
                learning_rate=0.05,
                depth=6,
                loss_function="Logloss",
                verbose=False
            )
        else:
            raise ValueError(f"Unknown model type {model_type}")

    def train(self, X_train, y_train, X_val=None, y_val=None):
        if self.model_type == "xgboost" and X_val is not None:
            self.model.fit(X_train, y_train, eval_set=[(X_val, y_val)], early_stopping_rounds=20, verbose=False)
        else:
            self.model.fit(X_train, y_train)

    def predict_risk(self, X_test):
        """
        Returns probability of progression.
        """
        probs = self.model.predict_proba(X_test)
        return probs[:, 1]  # Return prob of positive class (progression)

    def get_risk_category(self, prob):
        if prob < 0.2:
            return "Low Risk (Routine follow-up 12mo)"
        elif prob < 0.5:
            return "Moderate Risk (Follow-up 6mo)"
        elif prob < 0.8:
            return "High Risk (Refer within 3mo)"
        else:
            return "Very High Risk (Urgent referral)"

if __name__ == "__main__":
    predictor = DiseaseProgressionPredictor("xgboost")
    # Dummy data
    X = np.random.rand(100, 10)  # 10 features: age, HbA1c, etc.
    y = np.random.randint(0, 2, 100)
    predictor.train(X, y)
    print("Test Prediction Prob:", predictor.predict_risk(X[:5]))
