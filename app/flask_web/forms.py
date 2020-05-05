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
    provider = SelectField("Provider", validators=[Optional()])
    consumer = SelectField("Consumer", validators=[Optional()])
    #vital = BooleanField("Vital")
    submit = SubmitField("Submit")
