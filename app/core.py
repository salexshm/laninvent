import os
import barcode
from barcode.writer import ImageWriter

from app import app

def generate_barcode(record_id):
    # Ensure the ID is at least 12 characters long, pad with zeros if necessary
    record_id = str(record_id).zfill(12)

    if len(record_id) < 12 or not record_id.isalnum():  # Check for alphanumeric
        raise ValueError("ID должен содержать не менее 12 символов и может включать буквы и цифры.")

    # Use Code128, which supports alphanumeric characters
    code128 = barcode.get_barcode_class("code128")
    barcode_object = code128(record_id, writer=ImageWriter())

    # Define the path for saving the barcode
    static_folder = os.path.join(app.root_path, "static/barcode")
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)

    # Save the barcode image
    file_path = os.path.join(static_folder, f"{record_id}.png")
    barcode_object.save(file_path)

    return record_id

# def generate_barcode(record_id):

#     record_id = str(record_id).zfill(12)

#     if len(record_id) != 12 or not record_id.isdigit():
#         raise ValueError("ID должен содержать ровно 12 цифр.")

#     code128 = barcode.get_barcode_class("code128")
#     barcode_object = code128(record_id, writer=ImageWriter())
    
#     static_folder = os.path.join(app.root_path, "static/barcode")
#     if not os.path.exists(static_folder):
#         os.makedirs(static_folder)

#     file_path = os.path.join(static_folder, record_id)
    
#     barcode_object.save(file_path)

#     return record_id
