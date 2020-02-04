from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    TextAreaField,
    PasswordField,
)
from wtforms.validators import DataRequired, Length


class VerifyForm(FlaskForm):
    password = PasswordField(
        u"Code: ", validators=[DataRequired(message=u"Null is unacceptable")]
    )
    submit = SubmitField(u"GO")


class DiaryForm(FlaskForm):
    content = TextAreaField(
        u"Content",
        validators=[DataRequired(message=u"Null is unacceptable"), Length(1, 2 ** 15),],
        render_kw={
            "class": "text-body",
            "style": "margin: auto; width:100%; height:500px;",
        },
    )

    submit = SubmitField(u"GO", render_kw={"style": "margin: auto; width:100%; ",},)
