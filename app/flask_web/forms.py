from flask_wtf import FlaskForm
from wtforms import (
    TextAreaField,
    StringField,
    SelectField,
    SubmitField,
    BooleanField
)
from wtforms.validators import DataRequired, Length, InputRequired, Optional


class HomeForm(FlaskForm):
    view = TextAreaField("View")


class LoadForm(FlaskForm):
    datastructure = TextAreaField("Datastructure", validators=[DataRequired()])
    submit = SubmitField("Submit")


class PatchForm(FlaskForm):
    csv = TextAreaField("csv", validators=[DataRequired()])
    submit = SubmitField("Submit")


class RelateForm(FlaskForm):
    provider = SelectField("Provider", coerce=str)
    consumer = SelectField("Consumer", coerce=str)
    vital = BooleanField("Vital")
    submit = SubmitField("Submit")


class DetachForm(FlaskForm):
    relation = SelectField("Relation", validators=[DataRequired()])
    submit = SubmitField("Submit")
