from pytest import fixture, mark
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from models.user import User
from models.post import Tag, Post

SQLALCHEMY_DATABASE_URI = config.SQLALCHEMY_DATABASE_URI


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

    @mark.parametrize(
        'username,expected_posts_count,expected_post_title',
        [
            ('Soupmaker', 1, 'Amazing borscht recipe.'),
            ('Grillmaker', 1, 'Impossible grilled steak.'),
        ])
    def test_users_post(self, username, expected_posts_count, expected_post_title, session):
        user = session.query(User).filter_by(username=username).one_or_none()
        assert len(user.posts) == expected_posts_count
        for post in user.posts:
            assert post.title == expected_post_title

    @mark.parametrize(
        'post_title,expected_tags',
        [
            ('Amazing borscht recipe.', ['Soups', 'Hot meals']),
            ('Impossible grilled steak.', ['Main dishes', 'Hot meals']),
        ])
    def test_post_tags(self, post_title, expected_tags, session):
        post = session.query(Post).filter_by(title=post_title).one_or_none()
        assert post.tags is not None
        tags = [tag.text for tag in post.tags]
        assert tags == expected_tags
