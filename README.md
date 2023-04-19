# fastapi_co_app

$ mkdir -p app/log app/storage/{images,video,audio}

# make database models
$ alembic init alembic

In alembic.ini:\
sqlalchemy.url = <database_url>

In alembic/env.py:\
from app.models import BaseModel\
target_metadata = BaseModel.metadata

Create tables:\
$ alembic revision --autogenerate -m "Create tables"\
$ alembic upgrade head

# redis
$ redis-server

# celery
$ celery -A app.services.celery worker -l INFO

# Test Mail Server:
$ python3 -m smtpd -c DebuggingServer -n localhost:1025
