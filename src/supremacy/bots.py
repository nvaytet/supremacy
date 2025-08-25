import importlib
from functools import partial, cache
import importlib.resources
from collections.abc import Callable
import tomllib
from typing import Any


class Bot:
    def __init__(self, package: str, overrides: dict[str, Any] | None) -> None:
        self._package = package
        self._config = {
            **_load_bot_config(package),
            **(overrides or {}),
            "id": package,
        }

    @property
    def name(self) -> str:
        return self._config["name"]

    def get(self, key: str) -> Any:
        return self._config.get(key)

    def class_(self) -> type:
        return getattr(
            importlib.import_module(self._package), self._config["class_name"]
        )

    def factory(self) -> Callable[..., Any]:
        return partial(self.class_(), name=self._config["name"])

    def __repr__(self) -> str:
        return f"Bot({self._package}, {self._config})"


def load_bots(config: dict[str, Any]) -> dict[str, Bot]:
    bots = (
        Bot(package=cfg["package"], overrides=cfg.get("overrides"))
        for cfg in config["player"]
    )
    return {bot.name: bot for bot in bots}


@cache
def _load_bot_config(package: str) -> dict[str, Any]:
    with importlib.resources.open_binary(package, "config.toml") as file:
        return tomllib.load(file)
