# AMR Loss Debug Project

This is a PyTorch project about AMR (Angular Margin Regression) loss.

## Scenario
We implement **Angular Margin Regression (AMR) loss**, a custom regression loss with an angular margin penalty on normalized embeddings. The model contains a `ProjectHead` layer.

Training looks plausible but you feel like it converges to worse-than-expected results.

## Structure
- `amr/loss.py`: AMR loss implementation
- `amr/model.py`: encoder + ProjectHead
- `amr/trainer.py`: training loop
- `amr/data.py`: toy dataset and loader
- `amr/utils.py`: metrics and helpers
- `train.py`: entry point

## Expected Behavior
- Embeddings used by AMR loss must be unit-norm.
- Training should steadily reduce loss and reach low error on toy data.

## Run
```
python train.py
```
