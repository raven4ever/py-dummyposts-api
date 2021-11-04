from pydantic import BaseSettings


class Settings(BaseSettings):
    db_host: str
    db_port: str
    db_pass: str
    db_user: str
    db_dbname: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_token_expire_min: int

    class Config:
        env_file = '.env'


settings = Settings()
