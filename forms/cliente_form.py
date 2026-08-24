from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class ClienteForm(FlaskForm):

    nombre = StringField(
        'Nombre del cliente',
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    correo = StringField(
        'Correo electrónico',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    telefono = StringField(
        'Teléfono',
        validators=[
            DataRequired(),
            Length(min=10, max=10)
        ]
    )

    submit = SubmitField('Guardar')