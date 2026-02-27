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
    """Project embeddings into a lower-dim space.

    Intended behavior: return L2-normalized vectors.
    """

    def __init__(self, cfg: ModelConfig):
        super().__init__()
        self.proj = nn.Sequential(
            nn.Linear(cfg.hidden_dim, cfg.hidden_dim),
            nn.ReLU(),
            nn.Linear(cfg.hidden_dim, cfg.proj_dim),
        )

    def forward(self, h: torch.Tensor) -> torch.Tensor:
        z = self.proj(h)
        # the angular margin regression loss assumes the projection
        # vectors are unit norm.  previously we were returning the raw
        # output of the linear head which could have arbitrary scale
        # (and indeed the training loss plateaued at a high value).
        # a unit test in the suite checks that the projection is
        # normalized, so make sure to enforce it here.

        # normalize each example to unit length; add a small eps to avoid
        # divide-by-zero just in case (mirrors behaviour of F.normalize).
        z = F.normalize(z, p=2, dim=1, eps=1e-12)
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
