from dataclasses import dataclass

import toml


@dataclass
class BotConfig:
    channel_id: int
    token: str


@dataclass
class OwnerConfig:
    id: int
    post_text: str
    

@dataclass
class Config:
    bot: BotConfig
    owner: OwnerConfig


def load_config() -> Config:
    with open("config.toml") as file:
        data = toml.load(file)
    
    return Config(
        bot=BotConfig(**data["bot"]),
        owner=OwnerConfig(**data["owner"])
    )


config = load_config()
