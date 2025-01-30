import os
import random
import barcode
import string
from barcode.writer import ImageWriter

from app import app
from app.models import Barcode

def generate_barcode():
    """Генерирует уникальный 12-значный штрихкод"""
    while True:
        barcode_num = ''.join(random.choices(string.digits, k=12))
        existing_barcode = Barcode.query.filter_by(num=barcode_num).first()
        if not existing_barcode:
            code128 = barcode.get_barcode_class("code128")
            barcode_object = code128(barcode_num, writer=ImageWriter())
            static_folder = os.path.join(app.root_path, "static/barcode")
            if not os.path.exists(static_folder):
                os.makedirs(static_folder)                
            file_path = os.path.join(static_folder, f"{barcode_num}")
            barcode_object.save(file_path)
            return barcode_num
