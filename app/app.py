import os

from flask import Flask, render_template, url_for, request
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.utils import redirect

import config
from models.database import db
from models.post import Post, Tag
from models.user import User
from views.users import users_app
from views.posts import posts_app

app = Flask(__name__)

media_path = os.path.join(os.getcwd(), config.MEDIA_PATH)

app.config.update(
    SQLALCHEMY_DATABASE_URI=config.SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    SECRET_KEY=config.SECRET_KEY,
    UPLOADED_IMAGES_DEST=media_path,
    MEDIA_PATH=media_path
)

db.init_app(app)
Migrate(app, db, compare_type=True)

storage = config.storage
print()
storage.init_app(app)

images = UploadSet('images', IMAGES)
configure_uploads(app, images)

login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(users_app, url_prefix='/users')
app.register_blueprint(posts_app, url_prefix='/posts')


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).filter_by(id=user_id).one_or_none()


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('users_app.login', next=request.path))


@app.route('/', methods=('GET',), endpoint='index')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.post_time.desc()).paginate(
        page=page, per_page=config.POSTS_PER_PAGE
    )
    return render_template('index.html', posts=posts)


if __name__ == '__main__':
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=5000)
