from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class FacturacionForm(FlaskForm):

    numero = StringField(
        'Número de factura',
        validators=[
            DataRequired(),
            Length(min=5, max=30)
        ]
    )

    cliente = StringField(
        'Cliente',
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    total = FloatField(
        'Total',
        validators=[
            DataRequired(),
            NumberRange(min=0)
        ]
    )

    submit = SubmitField('Guardar')