import torch
import pytorch_lightning as pl
from torch.nn import CrossEntropyLoss
import torchmetrics

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.classifiers import DREnsembleClassifier

class DRClassifierLightningModule(pl.LightningModule):
    def __init__(self, lr=1e-4, num_classes=5):
        super().__init__()
        self.save_hyperparameters()
        self.model = DREnsembleClassifier(num_classes=num_classes)
        self.criterion = CrossEntropyLoss()
        
        # Metrics
        self.train_acc = torchmetrics.Accuracy(task="multiclass", num_classes=num_classes)
        self.val_acc = torchmetrics.Accuracy(task="multiclass", num_classes=num_classes)
        self.val_f1 = torchmetrics.F1Score(task="multiclass", num_classes=num_classes)

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        logits, _ = self(x)
        loss = self.criterion(logits, y)
        self.log('train_loss', loss, on_step=True, on_epoch=True, prog_bar=True)
        self.train_acc(logits, y)
        self.log('train_acc', self.train_acc, on_step=False, on_epoch=True, prog_bar=True)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        logits, _ = self(x)
        loss = self.criterion(logits, y)
        self.log('val_loss', loss, on_epoch=True, prog_bar=True)
        self.val_acc(logits, y)
        self.val_f1(logits, y)
        self.log('val_acc', self.val_acc, on_epoch=True, prog_bar=True)
        self.log('val_f1', self.val_f1, on_epoch=True, prog_bar=True)
        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(self.parameters(), lr=self.hparams.lr, weight_decay=1e-4)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=10)
        return [optimizer], [scheduler]

if __name__ == "__main__":
    print("Trainer module for Classification loaded.")
