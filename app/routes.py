from app import app
from flask import render_template, redirect, url_for, flash, request
from app import db
from app.models import DeviceType, Device, Barcode, Optobox, OpticalCable
from app.forms import Dev_typeForm, DeviceForm, BoxForm, CableForm
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
    filename = f'{device.barcode.num}.png'
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
    form = DeviceForm()  # Форма для ввода данных об устройстве
    
    if form.validate_on_submit():
        # Генерируем новый штрихкод
        barcode_num = generate_barcode()
        
        # Создаём объект штрихкода
        new_barcode = Barcode(num=barcode_num)
        db.session.add(new_barcode)
        db.session.flush()  # Фиксируем, чтобы получить new_barcode.id
        
        # Создаём объект устройства
        new_device = Device(
            device_name=form.dev_name.data,
            device_model=form.dev_model.data,
            device_location=form.dev_location.data,
            device_coordinates=form.dev_coordinates.data,
            device_ip=form.dev_ip.data,
            device_mask=form.dev_mask.data,
            device_nodal=form.device_nodal.data,
            device_type_id=form.dev_type.data,
            parent_id=int(form.parent.data) if form.parent.data else None,  # Родительское устройство
            barcode_id=new_barcode.id  # Привязываем штрихкод
        )
        
        db.session.add(new_device)
        db.session.commit()

        flash(f'Устройство "{new_device.device_name}" добавлено! Штрихкод: {barcode_num}', 'success')
        return redirect(url_for('devices'))  # Перенаправляем на список устройств
    
    return render_template('device-add.html', form=form)


@app.route('/boxes', methods=['GET'])
def boxes():
    boxes = Optobox.query.all()
    return render_template('boxes.html', boxes=boxes)


@app.route('/boxes/add', methods=['GET', 'POST'])
def box_add():
    form = BoxForm()
    
    if form.validate_on_submit():
        # Генерируем новый штрихкод
        barcode_num = generate_barcode()
        
        # Создаём объект штрихкода
        new_barcode = Barcode(num=barcode_num)
        db.session.add(new_barcode)
        db.session.flush()  # Фиксируем, чтобы получить new_barcode.id
        
        new_box = Optobox(
            box_description=form.box_description.data,
            box_coordinates=form.box_coordinates.data,
            barcode_id=new_barcode.id  
            )        

        db.session.add(new_box)
        db.session.commit()

        flash(f'Устройство добавлено!')
        return redirect(url_for('boxes'))
    
    return render_template('box-add.html', form=form)


@app.route('/boxes/detail/<int:id>', methods=['GET', 'POST'])
def box_detail(id):
    box = Optobox.query.get_or_404(id)
    filename = f'{box.barcode.num}.png'
    file_url = url_for("static", filename=f"barcode/{filename}") 
    return render_template('box-detail.html',  box=box, file_url=file_url)


@app.route('/boxes/delete/<int:id>')
def box_delete(id):
    box = Optobox.query.get_or_404(id)
    db.session.delete(box)
    db.session.commit()
    flash('Муфта успешно удалена', 'success')
    return redirect(url_for('boxes'))


@app.route('/boxes/cable/add/<int:id>', methods=['GET', 'POST'])
def cable_add(id):
    form = CableForm()
    box = Optobox.query.get_or_404(id)
    
    if form.validate_on_submit():
        new_cable = OpticalCable(
            from_box=form.from_box.data,
            fiber_color=str(form.fiber_color.data),  
            box_id=box.id 
            )
        db.session.add(new_cable)
        db.session.commit()
        
        flash('Кабель успешно создан', 'success')
        return redirect(url_for('box_detail', id=box.id))
    
    return render_template('cable-add.html', form=form)


@app.route('/boxes/cable/delete/<int:id>')
def cable_delete(id):
    cable = OpticalCable.query.get_or_404(id)
    db.session.delete(cable)
    db.session.commit()
    flash('Кабель успешно удален', 'success')
    return redirect(url_for('boxes'))