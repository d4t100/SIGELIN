import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

def generar_qr_para_equipo(equipo):
    """
    Genera un código QR para un equipo y lo guarda como imagen.
    """
    # 1️⃣ Define la información que contendrá el QR
    data = f"http://localhost:8000/equipos/<id_del_equipo>/qr/"

    # 2️⃣ Genera el QR con la librería qrcode
    img = qrcode.make(data)

    # 3️⃣ Convierte la imagen en bytes (para guardarla en la BD)
    buffer = BytesIO()
    img.save(buffer, format='PNG')

    # 4️⃣ Si tu modelo tiene un campo qr_image, guarda el archivo allí
    filename = f"qr_{equipo.id}.png"
    equipo.qr_image.save(filename, ContentFile(buffer.getvalue()), save=True)

    # 5️⃣ También puedes guardar el texto en codigo_qr (opcional)
    equipo.codigo_qr = data
    equipo.save()

    return equipo.qr_image.url  # Devuelve la URL de la imagen si usas MEDIA_URL
