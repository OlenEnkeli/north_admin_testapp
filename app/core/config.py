from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class JWTSettings(BaseModel):
    algorithm: str = 'HS256'
    secret_key: str = 'devkey'
    expires: int | None = None


class RootUserSettings(BaseModel):
    email: str
    password: str


class ProjectSettings(BaseSettings):
    title: str = 'NorthAdmin Test App'
    debug: bool = False
    backend_url: str = 'http://127.0.0.1:8000'


class PostgresSettings(BaseModel):
    user: str
    password: str
    server: str
    db: str

    @property
    def postgres_url(self) -> str:
        return (
            'postgresql+asyncpg://'
            f'{self.user}:'
            f'{self.password}@'
            f'{self.server}/'
            f'{self.db}'
        )

    @property
    def postgres_sync_url(self) -> str:
        return (
            'postgresql+psycopg://'
            f'{self.user}:'
            f'{self.password}@'
            f'{self.server}/'
            f'{self.db}'
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter='__',
        env_file='.env',
        env_file_encoding='UTF-8',
    )

    project: ProjectSettings = ProjectSettings()
    jwt: JWTSettings = JWTSettings()

    postgres: PostgresSettings
    root_user: RootUserSettings


settings = Settings()
