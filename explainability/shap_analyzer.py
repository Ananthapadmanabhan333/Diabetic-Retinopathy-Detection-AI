import shap
import numpy as np
import torch

class ShapAnalyzer:
    def __init__(self, model, background_data):
        """
        Initialize DeepExplainer with the PyTorch model and background dataset.
        background_data: A representative sample of the training set used for computing base values.
        """
        self.model = model
        self.model.eval()
        # DeepExplainer is ideal for PyTorch models
        self.explainer = shap.DeepExplainer(self.model, background_data)

    def analyze(self, input_tensor):
        """
        Generate SHAP values for the given input tensor.
        Returns the feature attributions.
        """
        shap_values = self.explainer.shap_values(input_tensor)
        return shap_values

    def plot_image_shap(self, shap_values, input_tensor):
        """
        Visualizes SHAP values over the image.
        """
        shap_numpy = [np.swapaxes(np.swapaxes(s, 1, -1), 1, 2) for s in shap_values]
        test_numpy = np.swapaxes(np.swapaxes(input_tensor.cpu().numpy(), 1, -1), 1, 2)
        
        # In a real environment, this displays the plot
        shap.image_plot(shap_numpy, -test_numpy)

if __name__ == "__main__":
    print("SHAP Analyzer module loaded.")
