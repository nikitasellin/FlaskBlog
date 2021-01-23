from datetime import datetime

from flask_image_alchemy.fields import StdImageField
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.exceptions import NotFound

from .database import db
from .user import User
from config import storage

posts_to_tags = db.Table(
    'posts_to_tags',
    db.Model.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


class Post(db.Model):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    text = Column(Text, nullable=False)
    post_time = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now())
    author_id = Column(Integer, ForeignKey(User.id), nullable=False)
    image = Column(StdImageField(
        storage=storage,
        variations={
                'thumbnail': {
                    "width": 100,
                    "height": 100,
                    "crop": True
                }
        }), nullable=True)
    tags = relationship('Tag', secondary=posts_to_tags)

    user = relationship(User, back_populates='posts')

    @classmethod
    def get_post_by_id(cls, post_id):
        post = cls.query.filter_by(id=post_id).one_or_none()
        if post is None:
            raise NotFound(f'Post #{post_id} not found!')
        return post

    @classmethod
    def search(cls, q):
        # @TODO! Make it more securely.
        posts = cls.query.filter(
            cls.title.ilike(f'%{q}%') | cls.text.ilike(f'%{q}%')
        )
        return posts

    def __repr__(self):
        return f'<Post #{self.title} {self.text} {self.user}>'


class Tag(db.Model):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    text = Column(String(30), nullable=False)
    posts = relationship(Post, secondary=posts_to_tags)

    @classmethod
    def get_tags_for_form(cls):
        tags = cls.query.all()
        if not tags:
            return []
        tags_list = []
        for tag in tags:
            tags_list.append((tag.id, tag.text))
        return tags_list

    @classmethod
    def get_tag_by_id(cls, pk):
        tag = cls.query.filter_by(id=pk).one_or_none()
        return tag

    @classmethod
    def get_tag_by_text(cls, text):
        tag = cls.query.filter_by(text=text).one_or_none()
        return tag

    def __repr__(self):
        return self.text
