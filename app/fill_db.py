import json
from logging import getLogger

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import config
from models.user import User
from models.post import Tag, Post

SQLALCHEMY_DATABASE_URI = config.SQLALCHEMY_DATABASE_URI
logger = getLogger(__name__)


def create_users(db_session):
    if not db_session.query(User).all():
        for initial_user in config.initial_users:
            user = User(
                username=initial_user['username'],
                password=initial_user['password']
            )
            db_session.add(user)
            try:
                db_session.commit()
            except Exception as e:
                logger.exception(f'Could not create new user: {e}')
        return
    logger.error('Users were already added!')


def create_tags(db_session):
    if not db_session.query(Tag).all():
        for tag_text in config.initial_tags:
            tag = Tag(text=tag_text)
            db_session.add(tag)
            try:
                db_session.commit()
            except Exception as e:
                logger.exception(f'Could not create new tags: {e}')
        return
    logger.error('Tags were already added!')


def create_posts(db_session):
    if db_session.query(Post).all():
        logger.error('Posts were already added!')
        return
    with open('posts.json') as file:
        content = json.loads(file.read())
    for item in content:
        user = db_session.query(User).filter_by(
            username=item['username']).one_or_none()
        title = item['title']
        text = item['text']
        if not (user and title and text):
            logger.error('Invalid post!')
            continue
        post = Post(
            author_id=user.id,
            title=title,
            text=text
        )
        db_session.add(post)
        db_session.flush()
        for tag_text in item['tags']:
            tag = db_session.query(Tag).filter_by(
                text=tag_text).one_or_none()
            post.tags.append(tag)
        try:
            db_session.commit()
        except Exception as e:
            logger.exception(f'Could not create new post: {e}')


if __name__ == '__main__':
    Session = sessionmaker()
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session.configure(bind=engine)
    session = Session()

    # Create users if not exists
    create_users(session)

    # Create Tags if not exists
    create_tags(session)

    # Create posts if not exists
    create_posts(session)
