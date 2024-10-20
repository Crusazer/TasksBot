import dataclasses
import logging
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename="bot.log",
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)


@dataclasses.dataclass
class Config:
    TOKEN: str = os.getenv('TOKEN')
    DB_NAME: str = os.getenv('DB_NAME')
    TIME_ZONE: int = 3  # Minsk/Europe


settings = Config()
