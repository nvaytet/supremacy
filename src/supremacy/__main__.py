import argparse
from importlib.resources import open_binary
import importlib
from pathlib import Path
import tomllib

def main():
    args = parse_arguments()
    config = load_config(args.config)
    bot_configs = load_bot_configs(config)
    bot_classes = load_bot_classes(config, bot_configs)
    print(config)
    print(bot_configs)
    print(bot_classes)


    # players = {name: supremacy_ai for name in names}
    # # players[my_ai.CREATOR] = my_ai

    # supremacy.start(
    #     players=players,
    #     time_limit=8 * 60,  # Time limit in seconds
    #     fullscreen=False,  # Set to True for fullscreen
    #     seed=None,  # Set seed to always generate the same map
    #     high_contrast=False,  # Set to True for high contrast mode
    #     crystal_boost=1,  # Set to > 1 to artificially increase crystal production
    # )

def parse_arguments():
    parser = argparse.ArgumentParser(description="Supremacy game")
    parser.add_argument("config", type=Path, default="config.toml", help="Path to config file")
    return parser.parse_args()


def load_config(path):
    with open(path, "rb") as f:
        return tomllib.load(f)


def load_bot_config(package_name):
    with open_binary(package_name, "config.toml") as file:
        return tomllib.load(file)

def load_bot_configs(config):
    return [
        (cfg["package"], load_bot_config(cfg["package"]))
        for cfg in config["bots"]
    ]

def load_bot_classes(config, bot_configs):
    return {cfg["package"]: getattr(importlib.import_module(cfg["package"]), bot_configs[cfg["package"]])
        for cfg in config["bots"]}


if __name__ == "__main__":
    main()
