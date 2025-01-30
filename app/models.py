from app import db, app
from flask_sqlalchemy import SQLAlchemy


class Barcode(db.Model):
    """
    Модель для хранения штрихкодов.
    Связана c Optobox и Device через One-to-One.
    """
    __tablename__ = 'barcode'
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.String(12), nullable=False, unique=True)   
    
    # Связь One-to-One с муфтой
    box = db.relationship('Optobox', back_populates='barcode')    
   
    # Связь One-to-One с устройством
    device = db.relationship('Device', back_populates='barcode')

    def __repr__(self):
        return f"<Barcode(id={self.id}, num={self.num})>"


class OpticalCable(db.Model):
    """
    Модель для хранения оптических кабелей.
    Связана c Optobox через One-to-Many.
    """
    __tablename__ = 'opticalCable'
    id = db.Column(db.Integer, primary_key=True)
    from_box = db.Column(db.String(5), nullable=False)
    fiber_color = db.Column(db.String(20), nullable=False)
    
    # Внешний ключ для связи с таблицей Optobox
    box_id = db.Column(db.Integer, db.ForeignKey('optobox.id'))    
    # Связь с Optobox
    box = db.relationship('Optobox', back_populates='cables')

    def __repr__(self):
        return f"<OpticalCable(id={self.id}, from_box={self.from_box}, fiber_color={self.fiber_color})>"


class Optobox(db.Model):
    """
    Модель для хранения муфт.
    Связана c OpticalCablets и Barcode.
    """
    __tablename__ = 'optobox'
    id = db.Column(db.Integer, primary_key=True)
    box_description = db.Column(db.String(50), nullable=False, unique=True)
    box_coordinates = db.Column(db.String(50), nullable=True)
    
    # Связь с таблицей OpticalCablets
    cables = db.relationship('OpticalCable', back_populates='box', cascade='all, delete-orphan', lazy='dynamic')
    
    # Связь One-to-One со штрихкодом
    barcode_id = db.Column(db.Integer, db.ForeignKey('barcode.id'))
    barcode = db.relationship('Barcode', back_populates='box')
    

    def __repr__(self):
        return f"<Optobox(id={self.id}, box_description={self.box_description})>"


class DeviceType(db.Model):
    """
    Модель для хранения типов устройств.
    Связана c Device One-to-Many.
    """
    __tablename__ = 'device_type'
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(50), nullable=False, unique=True)
    devices = db.relationship('Device', back_populates='device_type')

    def __repr__(self):
        return f"<DeviceType(id={self.id}, type_name={self.type_name})>"


class Device(db.Model):
    """
    Модель для хранения  устройств.
    Связана c Many-to-One → DeviceType (через device_type_id)
    One-to-One → Barcode.
    """
    __tablename__ = 'device'
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(100), nullable=False)
    device_model = db.Column(db.String(64))
    device_location = db.Column(db.String(128))
    device_coordinates = db.Column(db.String(50))
    device_ip = db.Column(db.String(15))
    device_mask = db.Column(db.String(15))
    device_nodal = db.Column(db.Boolean, default=False, nullable=False)

    # Связь с типом устройства
    device_type_id = db.Column(db.Integer, db.ForeignKey('device_type.id'), nullable=False)
    device_type = db.relationship('DeviceType', back_populates='devices')
    
    # Связь One-to-One со штрихкодом
    barcode_id = db.Column(db.Integer, db.ForeignKey('barcode.id'))
    barcode = db.relationship('Barcode', back_populates='device')

    # Связь с родительским устройством
    parent_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=True)
    parent = db.relationship('Device', remote_side=[id], backref='children')

    def __repr__(self):
        return f"<Device(id={self.id}, device_name={self.device_name}, parent_id={self.parent_id})>"


# Создаём таблицы в базе данных
with app.app_context():
    db.create_all()
