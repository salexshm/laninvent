from flask_wtf import FlaskForm
from wtforms_components import ColorField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired, IPAddress
from app.models import DeviceType, Device


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
  
    
class Dev_typeForm(FlaskForm):
    type_name = StringField('Тип устройства', validators=[DataRequired()])
    submit = SubmitField('Добавить')
  
  
class DeviceForm(FlaskForm):
    dev_name = StringField('Название', validators=[DataRequired()])
    dev_model = StringField('Модель', validators=[DataRequired()])
    dev_location = StringField('Расположение', validators=[DataRequired()])
    dev_coordinates = StringField('Координаты (широта, долгота)', validators=[DataRequired()])
    dev_ip = StringField('IP адрес', validators=[IPAddress()])
    dev_mask = StringField('Маска подсети', validators=[DataRequired()])
    dev_type = SelectField('Тип', coerce=int, choices=[])
    parent = SelectField('Родитель', coerce=int, choices=[])
    device_nodal = BooleanField('Узловой')
    
    submit = SubmitField('Добавить')
  
    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        self.dev_type.choices = [(t.id, t.type_name) for t in DeviceType.query.all()] or [(0, "Нет доступных типов")]
        self.parent.choices = [(t.id, t.device_name) for t in Device.query.filter_by(device_nodal=True)] or [(0, "Нет доступных родителей")]
  
  
class BoxForm(FlaskForm):
    box_description = StringField('Описание', validators=[DataRequired()])
    box_coordinates = StringField('Координаты (широта, долгота)', validators=[DataRequired()])
    
    submit = SubmitField('Добавить')
    
    
class CableForm(FlaskForm):
    from_box = StringField('От какой коробки', validators=[DataRequired()])
    fiber_color = ColorField('Цвет волокна', validators=[DataRequired()])
    submit = SubmitField('Добавить')
