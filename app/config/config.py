from pathlib import Path
from pydantic import (
    RedisDsn,
    EmailStr,
    DirectoryPath,
    BaseSettings as BaseConfig,
)
from kombu import Exchange, Queue

__all__ = ('cfg',)



class Config(BaseConfig):
    server_host: str = '127.0.0.1'
    server_port: int = 8000
    secret_key: str = '*** change me ***'
    root_path: DirectoryPath = Path(__file__).parents[1]
    resources_dir: str = 'resources'
    log_dir: str = 'log'

    company_alias = 'grkr'

    photo_width: int = 80

    image_width: dict = {
        'THUMBNAIL': 60,
        'SHOWCASE': 120,
        'SLIDER': 500,
        'LOGO': 180,
    }
    allowed_file_extensions: dict = {
        'image': ['jpg', 'jpeg', 'png',],
        'video': ['mp4',],
        'audio': ['mp3',],
    }
    cache_timeout: dict = {
        'year':         60 * 60 * 24 * 364,
        'month':        60 * 60 * 24 * 364,
        'day':          60 * 60 * 24 * 364,
        'five_minutes': 60 * 60 * 5
    }
    upload_folder_dir: str = 'storage'
    chunk_size = 1024
    block_size = 8192

    database_url: str = 'sqlite:///./fastapi_co_db.sqlite3'
    database_echo: bool = True

    languages: list = ['eu', 'ru', 'fr', 'de']
    default_lang = 'en'

    jwt_secret: str = '*** change me ***'
    jwt_algorithm: str = 'HS256'
    jwt_expires_s: int = 3600
    
    login_router: str ='/auth/sign-in/'

    items_in_list: int = 15

    activated_account_by_email: bool = False
    mail_server: str = 'localhost'
    mail_port: int = 1025
    mail_use_tls: bool = False
    mail_use_ssl: bool = False
    mail_username: str = ''
    mail_password: str = ''
    mail_default_sender: EmailStr = 'admin@mail.com'
    mail_max_emails: int | None = None
    
    
    broker: RedisDsn = 'redis://0.0.0.0:6379/0'
    result_backend: RedisDsn = 'redis://0.0.0.0:6379/0'
    task_serializer: str = 'json'
    accept_content: list = ['json',]

    task_queues: tuple = (
        Queue('high', Exchange('high'), routing_key='high'),
        Queue('normal', Exchange('normal'), routing_key='normal'),
        Queue('low', Exchange('low'), routing_key='low'),
    )
    task_default_queue: str = 'normal'
    task_default_exchange: str = 'normal'
    task_default_routing_key: str = 'normal'
    task_routes: dict = {
        # -- HIGH PRIORITY QUEUE -- #
        # -- NORMAL PRIORITY QUEUE -- # 
        'app.tasks.mail.send_async_email': {'queue': 'normal'},
        # -- LOW PRIORITY QUEUE -- #
    }
    


cfg = Config(
    _env_file = '.env',
    _env_file_encoding = 'utf-8'
)