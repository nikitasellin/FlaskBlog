from logging import getLogger

from flask import render_template, request, url_for, Blueprint
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.exceptions import InternalServerError
from werkzeug.utils import redirect

import config
from models.user import User
from models.post import Post
from models.database import db
from forms.user import LogInForm, SignUpForm

logger = getLogger(__name__)

users_app = Blueprint('users_app', __name__)


@users_app.route('/homepage', methods=('GET',), endpoint='index')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(
        user=current_user).order_by(
        Post.post_time.desc()).paginate(
        page=page, per_page=config.POSTS_PER_PAGE)
    return render_template(
        'users/index.html',
        user=current_user.username,
        posts=posts
    )


def get_credentials_from_form(form: dict):
    username = form.get('username')
    password = form.get('password')
    return username, password


@users_app.route('/signup', methods=('GET', 'POST'), endpoint='signup')
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('users_app.index', user=current_user.username))

    form = SignUpForm(request.form)
    if form.validate_on_submit():
        # Assuming POST method
        username, password = get_credentials_from_form(request.form)
        user = User(username, password)
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            logger.exception('Could not create new user.')
            raise InternalServerError(f'Could not create new user: {e}')

        login_user(user)
        return redirect(url_for('users_app.index'))

    return render_template('users/sign_up.html', form=form)


@users_app.route('/login/', methods=('GET', 'POST'), endpoint='login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users_app.index'))

    form = LogInForm(request.form)
    if form.validate_on_submit():
        # Assuming POST method
        username, password = get_credentials_from_form(request.form)
        user = db.session.query(User).filter_by(username=username).one_or_none()
        login_user(user)
        next_page = request.args.get('next', '')
        if next_page:
            return redirect(next_page)
        return redirect(url_for('users_app.index'))

    return render_template('users/login.html', form=form)


@users_app.route('/logout/', endpoint='logout')
def logout():
    logout_user()
    return redirect(url_for('users_app.login'))
