from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_username: str
    database_password: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    email_password : str
    email_sender: str

    class Config:
        env_file = ".env"


    

Settings = Settings()

