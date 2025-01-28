from app import app
from flask import render_template, redirect, url_for, flash, request
from app import db
from app.models import DeviceType, Device, Ports, Vlans
from app.forms import Dev_typeForm, DeviceForm, PortForm, VlanForm
from app.core import generate_barcode


@app.route('/')
def index():
    user = {"username": "Alexandr"}
    return render_template('index.html', user=user)


@app.route('/dev_types', methods=['GET'])
def dev_types():
    dev_types = DeviceType.query.all()
    return render_template('dev-types.html', dev_types=dev_types)


@app.route('/dev_types/add', methods=['GET', 'POST'])
def add_dev_type():
    form = Dev_typeForm()
    if form.validate_on_submit():
        device_type = DeviceType(type_name=form.type_name.data)
        db.session.add(device_type)
        db.session.commit()
        flash('Тип устройства успешно добавлен', 'success')
        return redirect(url_for('dev_types'))
    
    return render_template('type-add.html', form=form)


@app.route('/dev_types/delete/<int:id>')
def dev_type_delete(id):
    dev_type = DeviceType.query.get_or_404(id)
    db.session.delete(dev_type)
    db.session.commit()
    flash('Устройство удалено успешно', 'success')
    return redirect(url_for('dev_types'))


@app.route('/devices', methods=['GET'])
def devices():
    devices = Device.query.all()
    return render_template('devices.html', devices=devices)


@app.route('/devices/detail/<int:id>', methods=['GET', 'POST'])
def device_detail(id):
    device = Device.query.get_or_404(id)
    filename = f'{device.device_barcode}.png'
    file_url = url_for("static", filename=f"barcode/{filename}") 
    return render_template('device-detail.html',  device=device, file_url=file_url)


@app.route('/devices/delete/<int:id>')
def device_delete(id):
    device = Device.query.get_or_404(id)
    db.session.delete(device)
    db.session.commit()
    flash('Устройство удалено успешно', 'success')
    return redirect(url_for('devices'))


@app.route('/devices/add', methods=['GET', 'POST'])
def device_add():
    form = DeviceForm()
    barcode = form.dev_barcode.data
    if form.validate_on_submit():
        device = Device(
            device_name=form.dev_name.data,
            device_model=form.dev_model.data,
            device_barcode=generate_barcode(barcode),
            device_locations=form.dev_locations.data,
            device_coordinates=form.dev_coordinates.data,
            device_ip=form.dev_ip.data,
            device_mask=form.dev_mask.data,
            device_type_id=form.dev_type.data,
            device_nodal=form.device_nodal.data,
            parent_id=form.parent.data if form.parent.data != 0 else None,            
            )
        db.session.add(device)
        db.session.commit()
        flash('Тип устройства успешно добавлен', 'success')
        return redirect(url_for('devices'))
    
    return render_template('device-add.html', form=form)


@app.route('/devices/port/add/<int:id>', methods=['GET', 'POST'])
def port_add(id):
    form = PortForm()
    device = Device.query.get_or_404(id)
    
    if form.validate_on_submit():
        selected_vlans = form.vlan.data
        port = Ports(
            port_number=form.port_number.data,
            port_description=form.port_description.data,
            port_type=form.port_type.data,
            device_id=device.id,     
            )
        db.session.add(port)
        db.session.commit()
        
        for vlan_id in selected_vlans:
            vlan = Vlans.query.get(vlan_id)
            if vlan:
                port.vlans.append(vlan)
                db.session.commit()
        flash('Порт успешно добавлен', 'success')
        return redirect(url_for('device_detail', id=device.id))
    
    return render_template('port-add.html', form=form)



@app.route('/vlans', methods=['GET'])
def vlans():
    vlan = Vlans.query.all()
    return render_template('vlans.html', vlans_all=vlan)


@app.route('/vlan/add', methods=['GET', 'POST'])
def vlan_add():
    form = VlanForm()    
    if form.validate_on_submit():
        vlan = Vlans(
            vlan_id=form.vlan_id.data,
            vlan_description=form.vlan_description.data,
                 
            )
        db.session.add(vlan)
        db.session.commit()
        flash('Vlan успешно добавлен', 'success')
        return redirect(url_for('vlans'))
    
    return render_template('vlan-add.html', form=form)
