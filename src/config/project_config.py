from dotenv import load_dotenv

from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    ADMIN_TOKEN: str
    OPERATOR_TOKEN: str
    ADMINS: str


settings = Settings()
