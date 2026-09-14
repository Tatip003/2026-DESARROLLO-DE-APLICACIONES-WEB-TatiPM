from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class ProductoForm(FlaskForm):

    nombre = StringField(
        'Nombre del producto',
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    categoria = StringField(
        'Categoría',
        validators=[
            DataRequired(),
            Length(min=3, max=50)
        ]
    )

    precio = FloatField(
        'Precio',
        validators=[
            DataRequired(),
            NumberRange(min=0)
        ]
    )

    stock = IntegerField(
        'Stock',
        validators=[
            DataRequired(),
            NumberRange(min=0)
        ]
    )

    proveedor = SelectField(
        'Proveedor',
        coerce=int,
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField('Guardar')