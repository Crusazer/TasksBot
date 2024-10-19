import dataclasses
import os


@dataclasses.dataclass
class Config:
    TOKEN: str = os.getenv('TOKEN')


settings = Config()
