# Medical Reasoning SFT (Trinity-Mini)

🔧 **Location:** `Week5/artifacts/medical_reasoning_SFT`

Overview
--------
This folder contains training utilities and example Axolotl configs for fine-tuning models on the Medical-Reasoning-SFT (Trinity-Mini) dataset using LoRA adapters.

Contents
--------
- `train.py` — helper script to list configs and run training or preprocessing.
- `axolotl_configs/` — YAML configs for supported base models.
- `axolotl_datasets/` — prepared datasets.

Quickstart
----------
1. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Install required packages (at minimum):
   ```bash
   pip install -U pip
   pip install axolotl
   ```
   (If you plan to use multi-GPU training, install `accelerate` and any device-specific dependencies.)

License & Attribution
---------------------
Refer to individual component licenses (base models, Axolotl, datasets) when redistributing or publishing results.
