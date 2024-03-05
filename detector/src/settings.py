from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class Project(BaseModel):
    """
    Описание проекта.
    """

    #: название проекта
    title: str = "Ecg Detector"
    #: описание проекта
    description: str = "Сервис для детекции отведений ЭКГ."
    #: версия релиза
    release_version: str = Field(default="0.0.1")


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
    #: ключ для roboflow
    roboflow_api_key: str = Field(default="secret")

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"


# инициализация настроек приложения
settings = Settings()
