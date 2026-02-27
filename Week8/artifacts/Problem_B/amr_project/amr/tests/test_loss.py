import torch

from amr.model import ModelConfig, ProjectHead

def batch_l2_norm(x: torch.Tensor) -> torch.Tensor:
    return torch.sqrt((x * x).sum(dim=1) + 1e-12)

def test_project_head_outputs_unit_norm():
    cfg = ModelConfig()
    head = ProjectHead(cfg)
    x = torch.randn(16, cfg.hidden_dim)
    z = head(x)
    norms = batch_l2_norm(z)
    assert torch.allclose(norms, torch.ones_like(norms), atol=1e-3)
