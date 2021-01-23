import os

from flask_image_alchemy.storages import FileStorage

# Database settings
PG_USER = os.environ.get('PG_USER', '')
PG_PASSWORD = os.environ.get('PG_PASSWORD', '')
PG_HOST = os.environ.get('PG_HOST', 'db')
PG_PORT = '5432'
PG_DB = os.environ.get('PG_DB', 'postgres')
SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}'

# Secret Key
SECRET_KEY = os.environ.get('SECRET_KEY')

# Pagination settings
POSTS_PER_PAGE = 5

# Initial users
user1 = {
    'username': 'Soupmaker',
    'password': '123456'}
user2 = {
    'username': 'Grillmaker',
    'password': '123456'}
initial_users = (user1, user2)
# Initial tags
initial_tags = ('Soups', 'Main dishes', 'Hot meals', 'Salads', 'Cold meals')


# Media storage settings
MEDIA_PATH = 'media/'
MAX_IMAGE_SIZE = 1024 * 1024
storage = FileStorage()
