import shutil
import qrcode

qr = qrcode.QRCode(
    error_correction = qrcode.constants.ERROR_CORRECT_H,
    box_size = 5,
    border = 2
)

url = 'http://127.0.0.1:8000/otpcheck/'
qr.add_data(url)
qr.make()
qr_img = qr.make_image(fill_color="green", back_color="white")
qr_img.save('main/static/img/qrqr.png')       #main/static에 저장

# src = 'main/static/img/qrimg0.png'
# dst = 'static/img/'                             #static/에 복사 후 저장
# shutil.copy2(src, dst)