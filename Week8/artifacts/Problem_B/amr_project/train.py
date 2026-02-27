from amr.data import DataConfig, make_loader
from amr.model import ModelConfig
from amr.loss import AMRLossConfig
from amr.trainer import TrainConfig, Trainer


def main() -> None:
    data_cfg = DataConfig()
    model_cfg = ModelConfig()
    loss_cfg = AMRLossConfig()
    train_cfg = TrainConfig()

    loader = make_loader(data_cfg)
    trainer = Trainer(model_cfg, loss_cfg, train_cfg)

    for epoch in range(train_cfg.epochs):
        metrics = trainer.train_epoch(loader)
        if (epoch + 1) % 5 == 0:
            print(f"epoch {epoch+1:02d} | loss={metrics['loss']:.4f}")


if __name__ == "__main__":
    main()
