import pathlib


BASE_DIR = pathlib.Path(__file__).parent


class Config:
    DB_HOST = 'localhost'
    DB_PORT = 5433

    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379


class UserConfig(Config):
    DB_NAME = 'aiohttpdemo_blog'
    DB_USER = 'aiohttpdemo_user'
    DB_PASS = 'aiohttpdemo_pass'


class AdminConfig(Config):
    DB_NAME = 'postgres'
    DB_USER = 'postgres'
    DB_PASS = 'postgres'


user_config = UserConfig()
admin_config = AdminConfig()
