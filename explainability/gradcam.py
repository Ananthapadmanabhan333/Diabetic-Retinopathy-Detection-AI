import torch
from pytorch_grad_cam import GradCAM, GradCAMPlusPlus
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image
import numpy as np

class XAIExplainer:
    def __init__(self, model, target_layer):
        """
        Initializes GradCAM and GradCAM++ on the specified target layer.
        """
        self.model = model
        self.model.eval()
        self.target_layer = target_layer
        
        self.cam = GradCAM(model=self.model, target_layers=[self.target_layer])
        self.cam_plus = GradCAMPlusPlus(model=self.model, target_layers=[self.target_layer])

    def generate_heatmap(self, input_tensor, target_category=None, method="gradcam"):
        """
        Generates a heatmap for the specified input tensor.
        input_tensor: shape (1, 3, H, W)
        """
        targets = [ClassifierOutputTarget(target_category)] if target_category is not None else None
        
        if method.lower() == "gradcam++":
            grayscale_cam = self.cam_plus(input_tensor=input_tensor, targets=targets)
        else:
            grayscale_cam = self.cam(input_tensor=input_tensor, targets=targets)
            
        grayscale_cam = grayscale_cam[0, :]
        return grayscale_cam

    def overlay_heatmap(self, rgb_img, grayscale_cam):
        """
        rgb_img: float32 numpy array in [0, 1] of shape (H, W, 3)
        grayscale_cam: numpy array of shape (H, W)
        """
        visualization = show_cam_on_image(rgb_img, grayscale_cam, use_rgb=True)
        return visualization

if __name__ == "__main__":
    print("XAI Explainer module loaded.")
