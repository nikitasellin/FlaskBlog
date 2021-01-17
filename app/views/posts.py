from logging import getLogger

from flask import Blueprint, request, render_template, url_for
from flask_login import login_required, current_user
from werkzeug.exceptions import NotFound, InternalServerError
from werkzeug.utils import redirect

import config
from models.post import Post, Tag
from models.database import db
from forms.post import AddPostForm, SearchPostsForm

logger = getLogger(__name__)

posts_app = Blueprint('posts_app', __name__)


@posts_app.route('/view/<int:pk>', methods=('GET',), endpoint='view_post')
def view_post(pk):
    post = Post.get_post_by_id(pk)
    return render_template('posts/view_post.html', post=post)


@posts_app.route('/add', methods=('GET', 'POST'), endpoint='add_post')
@login_required
def add_post():
    form = AddPostForm(request.form)
    form.tags.choices = Tag.get_tags_for_form()
    if form.validate_on_submit():
        # Assuming POST method
        title = request.form.get('title')
        text = request.form.get('text')
        new_post = Post(
            title=title, text=text, author_id=current_user.id)
        db.session.add(new_post)
        tags = form.tags.data
        if tags:
            for tag_id in tags:
                tag = Tag.get_tag_by_id(tag_id)
                new_post.tags.append(tag)
        try:
            db.session.commit()
        except Exception as e:
            logger.exception('Could not add new post.')
            raise InternalServerError(f'Could not add new post: {e}')

        return redirect(url_for('posts_app.view_post', pk=new_post.id))
    return render_template('posts/add_post.html', form=form)


@posts_app.route('/search', methods=('GET', 'POST'), endpoint='search_posts')
def search_posts():
    form = SearchPostsForm(request.form)
    page = request.args.get('page', 1, type=int)
    if form.validate_on_submit():
        # Assuming POST method
        text = request.form.get('text')
        return redirect(url_for('posts_app.search_results', q=text))
    return render_template('posts/search_posts.html', form=form)


@posts_app.route('/search/<q>', methods=('GET',), endpoint='search_results')
def search_results(q):
    page = request.args.get('page', 1, type=int)
    posts = Post.search(q).order_by(
        Post.post_time.desc())
    return render_template(
        'posts/search_results.html',
        posts=posts.paginate(
            page=page, per_page=config.POSTS_PER_PAGE)
        )


@posts_app.route('/tags/<tag_text>', methods=('GET',), endpoint='filter_by_tag')
def filter_by_tag(tag_text):
    page = request.args.get('page', 1, type=int)
    tag = Tag.get_tag_by_text(tag_text)
    if not tag:
        raise NotFound(f'No such tag!')
    query = (
        db.session.query(Post).join(Post.tags).filter(Tag.text == tag_text)
    ).order_by(Post.post_time.desc())
    posts = query.paginate(
        page=page, per_page=config.POSTS_PER_PAGE
    )
    return render_template(
        'posts/search_results.html',
        posts=posts
    )
