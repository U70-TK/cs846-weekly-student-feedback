from dataclasses import dataclass
from typing import Dict

import torch
from torch import nn

from .loss import AMRLoss, AMRLossConfig
from .model import AMRModel, ModelConfig


@dataclass
class TrainConfig:
    lr: float = 3e-3
    epochs: int = 30
    device: str = "cpu"


class Trainer:
    def __init__(self, model_cfg: ModelConfig, loss_cfg: AMRLossConfig, train_cfg: TrainConfig):
        self.model = AMRModel(model_cfg).to(train_cfg.device)
        self.loss_fn = AMRLoss(loss_cfg)
        self.optim = torch.optim.Adam(self.model.parameters(), lr=train_cfg.lr)
        self.train_cfg = train_cfg

    def train_epoch(self, loader) -> Dict[str, float]:
        self.model.train()
        total = 0.0
        count = 0
        for x, y in loader:
            x = x.to(self.train_cfg.device)
            y = y.to(self.train_cfg.device)
            z, y_hat = self.model(x)
            loss = self.loss_fn(z, y)
            self.optim.zero_grad()
            loss.backward()
            self.optim.step()
            total += loss.item() * x.size(0)
            count += x.size(0)
        return {"loss": total / max(count, 1)}
