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
    #datastructure = TextAreaField("Datastructure", validators=[DataRequired()])
    datastructure = TextAreaField("Datastructure")
    empty = SubmitField("Empty template")
    example1 = SubmitField("Example 1")
    example2 = SubmitField("Example 2")
    example3 = SubmitField("Example 3")
    submit = SubmitField("Submit")


class DescribeForm(FlaskForm):
    servicelabel = StringField("Servicelabel", validators=[DataRequired()])
    servicename = StringField("Servicename", validators=[DataRequired()])
    customerid = StringField("Customer ID", validators=[DataRequired()])
    itsmprepend = StringField("ITSM Prepend", validators=[Optional()])
    itsmappend = StringField("ITSM Append", validators=[Optional()])
    submit = SubmitField("Submit")


class PatchForm(FlaskForm):
    csv = TextAreaField("csv", validators=[DataRequired()])
    clear = BooleanField("Clear all relations?")
    submit = SubmitField("Submit")


class RelateForm(FlaskForm):
    provider = SelectField("Provider", coerce=str)
    consumer = SelectField("Consumer", coerce=str)
    vital = BooleanField("Vital")
    submit = SubmitField("Submit")


class DetachForm(FlaskForm):
    relation = SelectField("Relation", validators=[DataRequired()])
    submit = SubmitField("Submit")


class DownloadForm(FlaskForm):
    json = SubmitField("JSON")
    pdf = SubmitField("PDF")
