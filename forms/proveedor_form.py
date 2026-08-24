from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ProveedorForm(FlaskForm):

    nombre = StringField(
        'Nombre del proveedor',
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    contacto = StringField(
        'Contacto',
        validators=[
            DataRequired(),
            Length(min=10, max=10)
        ]
    )

    producto = StringField(
        'Producto que suministra',
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    submit = SubmitField('Guardar')