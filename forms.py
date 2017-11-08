from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required


class LoginForm(FlaskForm):
    usuario = StringField('Nombre de usuario', validators=[Required()])
    password = PasswordField('Contraseña', validators=[Required()])
    enviar = SubmitField('Ingresar')

class RegistrarForm(LoginForm):
    password_check = PasswordField('Verificar Contraseña', validators=[Required()])
    enviar = SubmitField('Registrarse')

class ProductoForm(FlaskForm):
    producto = StringField('Ingrese el nombre del producto que desea Buscar ', validators=[Required()])
    enviar = SubmitField('Buscar')

class ClienteForm(FlaskForm):
    cliente = StringField('Ingrese el nombre del cliente que desea Buscar ', validators=[Required()])
    enviar = SubmitField('Buscar')


