from app import db
from app import app


ports_vlans = db.Table(
    'ports_vlans',
    db.Column('port_id', db.Integer, db.ForeignKey('ports.id'), primary_key=True),
    db.Column('vlan_id', db.Integer, db.ForeignKey('vlans.id'), primary_key=True)
)


class DeviceType(db.Model):
    __tablename__ = 'device_type'
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(50), nullable=False, unique=True)
    devices = db.relationship('Device', back_populates='device_type', lazy=True)
    

class Vlans(db.Model):
    __tablename__ = 'vlans'
    id = db.Column(db.Integer, primary_key=True)
    vlan_id = db.Column(db.String(50), nullable=False, unique=True)
    vlan_description = db.Column(db.String(100))

    ports = db.relationship('Ports', secondary=ports_vlans, back_populates='vlans')

    def __repr__(self):
        return f"<Vlans(id={self.id}, vlan_id={self.vlan_id}, vlan_description={self.vlan_description})>"


class Ports(db.Model):
    __tablename__ = 'ports'
    id = db.Column(db.Integer, primary_key=True)
    port_number = db.Column(db.String(10), nullable=False)
    port_description = db.Column(db.String(100))
    port_type = db.Column(db.Enum('tag', 'untag', name='port_types'), nullable=False)
    
     # Внешний ключ для связи с таблицей Devices
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
    
    # Связь с устройством
    device = db.relationship('Device', back_populates='ports')
    
    vlans = db.relationship('Vlans', secondary=ports_vlans, back_populates='ports')

    def __repr__(self):
        return f"<Ports(id={self.id}, port_number={self.port_number}, port_type={self.port_type}, device_id={self.device_id})>"


class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(100), nullable=False)
    device_model = db.Column(db.String(64))
    device_barcode = db.Column(db.String(12))
    device_locations = db.Column(db.String(128))
    device_coordinates =db.Column(db.String(50))
    device_ip = db.Column(db.String(15))
    device_mask = db.Column(db.String(15))
    device_nodal = db.Column(db.Boolean, default=False, nullable=False)
    
    # Связь с родительским устройством
    device_type_id = db.Column(db.Integer, db.ForeignKey('device_type.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=True)  

    # Отношения. Связь с дочерними устройствами
    device_type = db.relationship('DeviceType', back_populates='devices')
    parent = db.relationship('Device', remote_side=[id], backref='children')   
    
     # Связь с таблицей Ports
    ports = db.relationship('Ports', back_populates='device', cascade='all, delete-orphan', lazy='dynamic')

    def __repr__(self):
        return f"<Device(id={self.id}, device_name={self.device_name}, parent_id={self.parent_id})>"


with app.app_context():
    db.create_all()
