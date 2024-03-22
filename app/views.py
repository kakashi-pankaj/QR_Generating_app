from django.shortcuts import render
import qrcode
from PIL import Image
from io import BytesIO
# from encryption_helper import EncDecData
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import QRCode

def home(request):
    if request.method == 'POST':
        text = request.POST['text']
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        '''# Add a encryption layer(if using sensitive info)
                Encrypting code
                message = str(text)
                encrypted_txt = EncDecData.encrypt(message, workingkey)'''
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Convert the image to bytes
        img_byte_array = BytesIO()
        img.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)

        # Create an InMemoryUploadedFile object from the bytes
        qr_image = InMemoryUploadedFile(
            img_byte_array,
            None,  # field_name
            f'{text}.png',  # file name
            'image/png',  # content_type
            img.tell,  # size
            None  # content_type_extra
        )

        qr_code = QRCode(text=text)
        qr_code.image = qr_image
        qr_code.save()

        return render(request, 'qrgenerator/home.html', {'qr_code': qr_code})

    return render(request, 'qrgenerator/home.html')
