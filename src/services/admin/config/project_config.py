from dotenv import load_dotenv

from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    TOKEN: str
    SHEBIK: int
    JAKA2005: int
    ADMIN_3: int


settings = Settings()
