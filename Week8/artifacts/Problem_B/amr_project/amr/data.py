from dataclasses import dataclass
from typing import Tuple

import torch
from torch.utils.data import Dataset, DataLoader


@dataclass
class DataConfig:
    num_samples: int = 2000
    input_dim: int = 8
    noise_std: float = 0.05
    batch_size: int = 64


class ToyRegressionDataset(Dataset):
    def __init__(self, cfg: DataConfig, seed: int = 7):
        g = torch.Generator().manual_seed(seed)
        self.x = torch.randn(cfg.num_samples, cfg.input_dim, generator=g)
        # target is a nonlinear projection of x onto a random direction
        w = torch.randn(cfg.input_dim, generator=g)
        w = w / (w.norm() + 1e-12)
        y = (self.x @ w).tanh()
        # randn_like in some PyTorch versions does not accept a generator
        # argument; the generator passed from the config is only for
        # reproducibility, so we create the noise separately.
        noise = cfg.noise_std * torch.randn_like(y)
        y = y + noise
        self.y = y.unsqueeze(1)

    def __len__(self) -> int:
        return self.x.shape[0]

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        return self.x[idx], self.y[idx]


def make_loader(cfg: DataConfig) -> DataLoader:
    ds = ToyRegressionDataset(cfg)
    return DataLoader(ds, batch_size=cfg.batch_size, shuffle=True, drop_last=True)
