import argparse
from pathlib import Path
import tomllib

import supremacy
from supremacy.bots import load_bots


def main():
    args = parse_arguments()
    config = load_config(args.config)
    bots = load_bots(config)

    cfg = config["supremacy"]
    supremacy.start(
        players=bots,
        time_limit=cfg["time-limit"],
        fullscreen=cfg["fullscreen"],
        high_contrast=cfg["high-contrast"],
        crystal_boost=cfg["crystal-boost"],
        seed=cfg.get("seed", None),
    )


def parse_arguments():
    parser = argparse.ArgumentParser(description="Supremacy game")
    parser.add_argument(
        "config", type=Path, default="config.toml", help="Path to config file"
    )
    return parser.parse_args()


def load_config(path):
    with open(path, "rb") as f:
        return tomllib.load(f)


if __name__ == "__main__":
    main()
