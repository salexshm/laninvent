from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, IPAddress
from app.models import DeviceType, Device, Vlans


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
  
    
class Dev_typeForm(FlaskForm):
    type_name = StringField('Тип устройства', validators=[DataRequired()])
    submit = SubmitField('Добавить')
  

class PortForm(FlaskForm):
    port_number = StringField('Номер порта', validators=[DataRequired()])
    port_description = StringField('Описание порта', validators=[DataRequired()])
    port_type = SelectField(
        'Тип порта',
        choices=[('tag', 'Tag'), ('untag', 'Untag')],
        validators=[DataRequired()]
    )
    vlan = SelectMultipleField('Vlans', coerce=int)
    submit = SubmitField('Добавить')
    
    def __init__(self, *args, **kwargs):
        super(PortForm, self).__init__(*args, **kwargs)
        self.vlan.choices = [(t.id, t.vlan_id) for t in Vlans.query.all()] or [(0, "Нет доступных VLAN")]
    
    
class VlanForm(FlaskForm):
    vlan_id = StringField('Valn ID', validators=[DataRequired()])
    vlan_description = StringField('Vlan описание', validators=[DataRequired()])
    submit = SubmitField('Добавить')

  
class DeviceForm(FlaskForm):
    dev_name = StringField('Название', validators=[DataRequired()])
    dev_model = StringField('Модель', validators=[DataRequired()])
    dev_barcode = StringField('Штрихкод', validators=[DataRequired()])
    dev_locations = StringField('Расположение', validators=[DataRequired()])
    dev_coordinates = StringField('Координаты', validators=[DataRequired()])
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
  