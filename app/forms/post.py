from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired
from wtforms.widgets import CheckboxInput, ListWidget


class AddPostForm(FlaskForm):
    title = StringField(
        'Title:', validators=[DataRequired()])
    text = TextAreaField(
        'Text:', validators=[DataRequired()])
    tags = SelectMultipleField(
        'Tags:',
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput(),
        coerce=int
    )


class SearchPostsForm(FlaskForm):
    text = StringField(
        'Enter text:', validators=[DataRequired()])
