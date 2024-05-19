import os

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class Project(BaseModel):
    """
    Описание проекта.
    """

    #: название проекта
    title: str = "Ecg Digitizer"
    #: описание проекта
    description: str = "Сервис для оцифровки отведений ЭКГ."
    #: версия релиза
    release_version: str = Field(default="0.5.1")


class Settings(BaseSettings):
    """
    Настройки проекта.
    """

    #: режим отладки
    debug: bool = Field(default=False)
    #: уровень логирования
    log_level: str = Field(default="INFO")
    #: описание проекта
    project: Project = Project()
    #: базовый адрес приложения
    base_url: str = Field(default="http://0.0.0.0:8010")
    #: ключи для S3
    AWS_ACCESS_KEY_ID: str = Field(default=os.getenv("AWS_ACCESS_KEY_ID"))
    AWS_SECRET_ACCESS_KEY: str = Field(default=os.getenv("AWS_ACCESS_KEY_ID"))
    #: бакет с изображениями
    AWS_INPUT_BUCKET: str = Field(default=os.getenv("AWS_INPUT_BUCKET"))
    #: бакет с разметкой
    AWS_OUTPUT_BUCKET: str = Field(default=os.getenv("AWS_OUTPUT_BUCKET"))

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"


# инициализация настроек приложения
settings = Settings()
