import argparse
import subprocess
import sys
from pathlib import Path


def get_available_configs(config_dir: Path) -> dict:
    configs = {}
    if config_dir.exists():
        for model_dir in config_dir.iterdir():
            if model_dir.is_dir():
                for config_file in model_dir.glob("*.yaml"):
                    key = f"{model_dir.name}/{config_file.stem}"
                    configs[key] = config_file
    return configs


def main():
    script_dir = Path(__file__).parent.resolve()
    config_dir = script_dir / "axolotl_configs"

    available_configs = get_available_configs(config_dir)

    parser = argparse.ArgumentParser(
        description="Train models using Axolotl with predefined configs",
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        "--config",
        type=str,
        help="Config name (e.g., 'qwen2.5-7B/lora-openmed_Trinity-Mini')",
    )
    parser.add_argument(
        "--config-path",
        type=str,
        help="Direct path to a YAML config file (overrides --config)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available configs and exit",
    )
    parser.add_argument(
        "--accelerate",
        action="store_true",
        help="Run with accelerate launch for multi-GPU training",
    )
    parser.add_argument(
        "--preprocess-only",
        action="store_true",
        help="Only preprocess the dataset without training",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode",
    )

    args = parser.parse_args()

    if args.list:
        print("Available configs:")
        for name in sorted(available_configs.keys()):
            print(f"  - {name}")
        sys.exit(0)

    if args.config_path:
        config_path = Path(args.config_path).resolve()
        if not config_path.exists():
            print(f"Error: Config file not found: {config_path}", file=sys.stderr)
            sys.exit(1)
    elif args.config:
        if args.config in available_configs:
            config_path = available_configs[args.config]
        else:
            config_key = args.config
            if config_key in available_configs:
                config_path = available_configs[config_key]
            else:
                print(f"Error: Config '{args.config}' not found.", file=sys.stderr)
                print("Available configs:", file=sys.stderr)
                for name in sorted(available_configs.keys()):
                    print(f"  - {name}", file=sys.stderr)
                sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

    print(f"Using config: {config_path}")

    if args.accelerate:
        cmd = ["accelerate", "launch", "-m", "axolotl.cli.train", str(config_path)]
    else:
        cmd = ["python", "-m", "axolotl.cli.train", str(config_path)]

    if args.preprocess_only:
        cmd = ["python", "-m", "axolotl.cli.preprocess", str(config_path)]

    if args.debug:
        cmd.append("--debug")

    print(f"Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=True)
        sys.exit(result.returncode)
    except subprocess.CalledProcessError as e:
        print(f"Training failed with exit code {e.returncode}", file=sys.stderr)
        sys.exit(e.returncode)
    except FileNotFoundError as e:
        print(f"Error: Command not found. Make sure axolotl is installed.", file=sys.stderr)
        print(f"Install with: pip install axolotl", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
