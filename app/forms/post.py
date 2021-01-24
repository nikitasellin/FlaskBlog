import os

from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, SelectMultipleField, FileField
from wtforms.validators import DataRequired, ValidationError
from wtforms.widgets import CheckboxInput, ListWidget

from config import MAX_IMAGE_SIZE

images = UploadSet('images', IMAGES)


class AddPostForm(FlaskForm):
    title = StringField(
        'Title:', validators=[DataRequired()])
    text = TextAreaField(
        'Text:', validators=[DataRequired()])
    image = FileField(
        'Image:', validators=[FileAllowed(images, 'Images only!')])
    tags = SelectMultipleField(
        'Tags:',
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput(),
        coerce=int
    )

    def validate_image(self, field):
        file = field.data
        file.seek(0, os.SEEK_END)
        if file.tell() > MAX_IMAGE_SIZE:
            raise ValidationError(
                f'Image size is > {MAX_IMAGE_SIZE / (1024 * 1024)} MB!')
        file.seek(0, 0)


class SearchPostsForm(FlaskForm):
    text = StringField(
        'Enter text:', validators=[DataRequired()])
