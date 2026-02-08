# Medical Reasoning SFT (Trinity-Mini)

🔧 **Location:** `Week5/artifacts/medical_reasoning_SFT`

Overview
--------
This folder contains training utilities and example Axolotl configs for fine-tuning models on the Medical-Reasoning-SFT (Trinity-Mini) dataset using LoRA adapters.

Contents
--------
- `train.py` — helper script to list configs and run training or preprocessing.
- `axolotl_configs/` — YAML configs for supported base models.
- `axolotl_datasets/` — prepared datasets (empty in this repo; update with your local data or prepared datasets).

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

Usage
-----
- List available configs:
  ```bash
  python train.py --list
  ```
- Train using a config key:
  ```bash
  python train.py --config "llama2-chat/lora-openmed_Trinity-Mini"
  ```
- Train using a direct config path:
  ```bash
  python train.py --config-path path/to/config.yaml
  ```
- Use `accelerate` for multi-GPU:
  ```bash
  python train.py --config "..." --accelerate
  ```
- To only run preprocessing (no training):
  ```bash
  python train.py --config "..." --preprocess-only
  ```
- Add `--debug` to enable debug mode.

Notes about configs
-------------------
- Both provided configs point to the `OpenMed/Medical-Reasoning-SFT-Trinity-Mini` dataset and use LoRA adapters (r=32, alpha=64) with micro batch size 8 and 1000 steps by default.
- Check each YAML for paths such as `dataset_prepared_path` and `output_dir` and adjust them to match your local filesystem or workspace mount points.

Troubleshooting
---------------
- If the script complains about a missing command, ensure `axolotl` (and `accelerate` if used) are installed. Example error text suggests `pip install axolotl`.
- The repository ignores `venv/` in `.gitignore`.

License & Attribution
---------------------
Refer to individual component licenses (base models, Axolotl, datasets) when redistributing or publishing results.

Questions
---------
If you want, I can extend this README with environment-specific setup (CUDA/cuDNN notes, exact dependency versions), or add example CLI commands for running on a Slurm/cluster environment.
