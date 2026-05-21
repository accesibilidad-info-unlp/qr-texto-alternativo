import os
import sys
import qrcode
from PIL import Image

# config base
BASE_URL = "https://accesibilidad-info-unlp.github.io/plataforma-texto-alternativo/posts"
OUTPUT_DIR = "output"
LOGO_PATH = "assets/logo.png"
COLOR = "black"
BG_COLOR = "white"
LOGO_DIM = 0.2

# parámetros
MATERIA = sys.argv[1]
ANIO = sys.argv[2]
START = int(sys.argv[3])
END = int(sys.argv[4])

def generate_qr(post_id):
    url = f"{BASE_URL}/{MATERIA}/{ANIO}/post-{post_id:02}/"

    qr = qrcode.QRCode(
            version = None,
            error_correction = qrcode.constants.ERROR_CORRECT_H,
            box_size = 10,
            border = 4,
            )

    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(
            fill_color=COLOR,
            back_color=BG_COLOR
            ).convert("RGB")

    if LOGO_PATH and os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH)

        qr_width, qr_height = img.size
        logo_size = int(qr_width * LOGO_DIM)


        logo = logo.resize((logo_size, logo_size))

        pos = (
                (qr_width - logo_size) // 2,
                (qr_height - logo_size) // 2
                )
        
        if logo.mode in ("RGBA", "LA"):
            img.paste(logo, pos, logo)
        else:
            img.paste(logo, pos)

    filename = f"qr-{post_id:02}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)

    img.save(filepath)
    print(f"[OK] {filename} -> {url}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for i in range (START, END + 1):
        generate_qr(i)

if __name__ == "__main__":
    main()
