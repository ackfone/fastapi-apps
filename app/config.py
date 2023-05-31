from pydantic import BaseSettings

class Configs(BaseSettings):
    db_host:str
    db_port:str
    db_username:str
    db_password:str
    db_name:str

    secret_key:str
    algorithm :str
    token_expire_time_minutes:int
    
    class Config:
        env_file = ".env"


setting = Configs()