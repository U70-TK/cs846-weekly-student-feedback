import torch


def batch_l2_norm(x: torch.Tensor) -> torch.Tensor:
    return torch.sqrt((x * x).sum(dim=1) + 1e-12)
