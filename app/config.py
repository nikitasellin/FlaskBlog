import os

PG_USER = os.environ.get('PG_USER', '')
PG_PASSWORD = os.environ.get('PG_PASSWORD', '')
PG_HOST = os.environ.get('PG_HOST', 'db')
PG_PORT = '5432'
PG_DB = os.environ.get('PG_DB', 'postgres')
SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}'

SECRET_KEY = os.environ.get('SECRET_KEY')

POSTS_PER_PAGE = 5
# @TODO! Refactor adding tags to DB.
initial_tags = ('Tag1', 'Tag2', 'Tag3')
