import torch
import torch.nn as nn
import timm

class DREnsembleClassifier(nn.Module):
    def __init__(self, num_classes=5, pretrained=True):
        super().__init__()
        # EfficientNet-B4
        self.effnet_b4 = timm.create_model('efficientnet_b4', pretrained=pretrained, num_classes=num_classes)
        # EfficientNet-B5
        self.effnet_b5 = timm.create_model('efficientnet_b5', pretrained=pretrained, num_classes=num_classes)
        # Vision Transformer
        self.vit = timm.create_model('vit_base_patch16_224', pretrained=pretrained, num_classes=num_classes)
        # Swin Transformer
        self.swin = timm.create_model('swin_base_patch4_window7_224', pretrained=pretrained, num_classes=num_classes)
        
        # Stacking Meta-Learner Layer
        self.meta_learner = nn.Sequential(
            nn.Linear(num_classes * 4, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        out_b4 = self.effnet_b4(x)
        out_b5 = self.effnet_b5(x)
        
        # ViT and Swin might need specific image sizes; standardizing to 224x224 for transformers if x is larger
        x_224 = torch.nn.functional.interpolate(x, size=(224, 224), mode='bilinear', align_corners=False)
        out_vit = self.vit(x_224)
        out_swin = self.swin(x_224)
        
        # Concatenate outputs for meta-learner
        features = torch.cat([out_b4, out_b5, out_vit, out_swin], dim=1)
        final_out = self.meta_learner(features)
        
        return final_out, [out_b4, out_b5, out_vit, out_swin]

if __name__ == "__main__":
    model = DREnsembleClassifier(num_classes=5, pretrained=False)
    dummy_input = torch.randn(2, 3, 512, 512)
    out, ensembles = model(dummy_input)
    print("Final Output Shape:", out.shape)
    print("Ensemble Outputs:", [o.shape for o in ensembles])
