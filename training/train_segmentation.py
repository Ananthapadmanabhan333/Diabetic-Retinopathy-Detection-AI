import torch
import pytorch_lightning as pl
import segmentation_models_pytorch as smp

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.segmentation import create_segmentation_model

class DRSegmentationLightningModule(pl.LightningModule):
    def __init__(self, model_name="unetplusplus", encoder_name="resnet34", lr=1e-4, num_classes=6):
        super().__init__()
        self.save_hyperparameters()
        self.model = create_segmentation_model(model_name, encoder_name, num_classes)
        
        # Loss function commonly used for segmentation: DiceLoss + FocalLoss
        self.criterion = smp.losses.DiceLoss(smp.losses.MULTILABEL_MODE, from_logits=True)

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = self.criterion(logits, y)
        self.log('train_seg_loss', loss, on_step=True, on_epoch=True, prog_bar=True)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = self.criterion(logits, y)
        self.log('val_seg_loss', loss, on_epoch=True, prog_bar=True)
        # TODO: Add specific metrics like IoU or Dice score
        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(self.parameters(), lr=self.hparams.lr, weight_decay=1e-4)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=3)
        return {"optimizer": optimizer, "lr_scheduler": scheduler, "monitor": "val_seg_loss"}

if __name__ == "__main__":
    print("Trainer module for Segmentation loaded.")
