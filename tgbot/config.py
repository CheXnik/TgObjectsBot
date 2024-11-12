from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str

    @staticmethod
    def from_env(env: Env):
        token = env.str('BOT_TOKEN')

        return TgBot(token=token)


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    misc: Miscellaneous


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot.from_env(env),
        misc=Miscellaneous(),
    )
