from dataclasses import dataclass

import torch
from torch import nn
import torch.nn.functional as F


@dataclass
class ModelConfig:
    input_dim: int = 8
    hidden_dim: int = 64
    proj_dim: int = 16


class Encoder(nn.Module):
    def __init__(self, cfg: ModelConfig):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(cfg.input_dim, cfg.hidden_dim),
            nn.ReLU(),
            nn.Linear(cfg.hidden_dim, cfg.hidden_dim),
            nn.ReLU(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class ProjectHead(nn.Module):

    def __init__(self, cfg: ModelConfig):
        super().__init__()
        self.proj = nn.Sequential(
            nn.Linear(cfg.hidden_dim, cfg.hidden_dim),
            nn.ReLU(),
            nn.Linear(cfg.hidden_dim, cfg.proj_dim),
        )

    def forward(self, h: torch.Tensor) -> torch.Tensor:
        z = self.proj(h)
        return z


class AMRModel(nn.Module):
    def __init__(self, cfg: ModelConfig):
        super().__init__()
        self.encoder = Encoder(cfg)
        self.project = ProjectHead(cfg)
        self.regressor = nn.Linear(cfg.proj_dim, 1, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = self.encoder(x)
        z = self.project(h)
        y_hat = self.regressor(z)
        return z, y_hat
