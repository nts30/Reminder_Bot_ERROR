import configparser
from dataclasses import dataclass


@dataclass
class Bot:
    BOT_TOKEN: str
    HOST_URL:str
    ADMIN_ID: int
    TIME_DIRECTION: int


@dataclass
class Config:
    tg_bot: Bot


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    settings = config['BOT_CONFIG']

    return Config(
        tg_bot=Bot(
            BOT_TOKEN=settings['BOT_TOKEN'],
            HOST_URL=settings['HOST_URL'],
            ADMIN_ID =int(settings['ADMIN_ID']),
            TIME_DIRECTION=int(settings['TIMEDELTA'])
        )
    )

