import argparse
import importlib
from functools import partial
from importlib.resources import open_binary
from pathlib import Path
import tomllib

import supremacy


def main():
    args = parse_arguments()
    config = load_config(args.config)
    bot_configs = load_bot_configs(config)
    bot_classes = load_bot_classes(bot_configs)
    bot_factories = make_bot_factories(config, bot_classes, bot_configs)

    cfg = config["supremacy"]
    supremacy.start(
        players=bot_factories,
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


def collect_bot_packages(config):
    packages = set(config["game"]["bots"])
    if extra := config["game"].get("extra-bots"):
        packages.add(extra["package"])
    return packages


def load_bot_config(package_name):
    with open_binary(package_name, "config.toml") as file:
        return tomllib.load(file)


def load_bot_configs(config):
    return {
        package: load_bot_config(package) for package in collect_bot_packages(config)
    }


def load_bot_classes(bot_configs):
    return {
        package: getattr(importlib.import_module(package), cfg["class_name"])
        for package, cfg in bot_configs.items()
    }


def make_bot_factories(config, bot_classes, bot_configs):
    base = {
        bot_configs[package]["name"]: partial(
            bot_classes[package], team=bot_configs[package]["name"]
        )
        for package in config["game"]["bots"]
    }
    extra_config = config["game"]["extra-bots"]
    extra = {
        f"Bot{i}": partial(bot_classes[extra_config["package"]], team=f"Bot{i}")
        for i in range(extra_config["n"])
    }
    return {**base, **extra}


if __name__ == "__main__":
    main()
