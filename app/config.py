import dataclasses
import os
import logging

logging.basicConfig(level=logging.INFO)


@dataclasses.dataclass
class Config:
    TOKEN: str = os.getenv('TOKEN')
    DB_NAME: str = os.getenv('DB_NAME')


settings = Config()
