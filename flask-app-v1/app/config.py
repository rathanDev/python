import os 

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI =  "sqlite:///:memory"  # os.getenv("DATABASE_URL")
    DEBUG = True

class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"

class ProdConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        "mssql+pyodbc://sa:YourPassword@localhost:1443/YourDB"
        "?driver=ODBC+Driver+17+for+SQL+Server"        
    )

config_map = {
    "development": DevConfig,
    "production": ProdConfig
}