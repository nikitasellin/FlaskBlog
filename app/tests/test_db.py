import json

from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from models.user import User
from models.post import Tag, Post

SQLALCHEMY_DATABASE_URI = config.SQLALCHEMY_DATABASE_URI

'''
6. Выбрать все посты конкретного пользователя, попробовать сделать другие запросы 
(Рекомендуется сделать это в виде тестов pytest, можно просто с помощью print)
'''


@fixture(scope='module')
def initial_posts_dict():
    with open(config.initial_posts_file) as file:
        content = json.loads(file.read())
    return content


@fixture(scope='module')
def session():
    Session = sessionmaker()
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session.configure(bind=engine)
    return Session()


class TestModels:
    def test_initial_users_list(self, session):
        users = session.query(User).all()
        assert len(users) == len(config.initial_users)
        db_usernames = [user.username for user in users]
        for iu in config.initial_users:
            assert iu['username'] in db_usernames

    def test_initial_tags_list(self, session):
        tags = session.query(Tag).all()
        assert len(tags) == len(config.initial_tags)
        for tag in tags:
            assert tag.text in config.initial_tags

    def test_true(self, initial_posts_dict, session):
        for item in initial_posts_dict:
            for key in item.keys():
                assert key == key
