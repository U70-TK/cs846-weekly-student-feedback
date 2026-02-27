from dataclasses import dataclass

import torch
import torch.nn.functional as F


@dataclass
class AMRLossConfig:
    margin: float = 0.35
    temperature: float = 0.07
    reg_weight: float = 0.15


class AMRLoss(torch.nn.Module):
    """Angular Margin Regression loss.

    We interpret the scalar target as a direction in 1D and
    penalize angular deviation between projection vectors and a
    target direction. This requires unit-norm embeddings.
    """

    def __init__(self, cfg: AMRLossConfig):
        super().__init__()
        self.cfg = cfg

    def forward(self, z: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        # z: [B, D], y: [B, 1]
        # Normalize targets into [-1, 1] and map to angle
        y_clamped = y.clamp(-1.0, 1.0)
        theta = torch.acos(y_clamped)

        # cosine similarity between z and a fixed direction e1
        e1 = torch.zeros_like(z)
        e1[:, 0] = 1.0
        cos_sim = (z * e1).sum(dim=1, keepdim=True)

        # angular margin penalty
        angular = torch.cos(theta + self.cfg.margin)
        margin_loss = F.mse_loss(cos_sim, angular)

        # regular regression loss to keep scale stable
        reg_loss = F.mse_loss(cos_sim, y_clamped)

        return margin_loss + self.cfg.reg_weight * reg_loss
