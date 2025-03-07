import argparse

import qrcode
from PIL import Image, ImageDraw, ImageFont


def create_qr_code(data, size):
    """Create a QR code using `qrcode` and resize."""

    qr = qrcode.QRCode(
        version=None,  # decide version based on data
        # use defaults for border, etc
    )
    qr.add_data(data)
    qr.make(fit=True)  # decide version based on data
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img = qr_img.resize((size, size))

    return qr_img


def get_text_size(font, text):
    """Find the xy size of the text when displayed with the font, in px."""

    img = Image.new(mode="RGB", size=(0, 0))
    draw = ImageDraw.Draw(img)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)

    return width, height


def wrap_text(max_width, font, text):
    """Split text into multiple lines based on a maximum width when displayed in the font."""

    line = ""
    lines = []
    for char in text:
        if get_text_size(font, line + char)[0] <= max_width:
            line += char
        else:
            lines.append(line)
            line = ""
    if line:
        lines.append(line)

    return "\n".join(lines)


def annotate_qr_code(qr_img, font, text):
    """Produce a new image with the text displayed below the QR code."""

    qr_width, qr_height = qr_img.size
    text_width, text_height = get_text_size(font, text)

    annotated_qr_img = Image.new(
        "RGB", (qr_width, qr_height + text_height), color="white"
    )
    annotated_qr_img.paste(qr_img, (0, 0))

    draw = ImageDraw.Draw(annotated_qr_img)
    x_position = (qr_width - text_width) // 2  # center aligned
    y_position = qr_height  # below the QR image
    draw.text((x_position, y_position), text, font=font, fill="black")

    return annotated_qr_img


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "data", type=str, help="The data to encode in the QR code (required)."
    )
    parser.add_argument("size", type=int, help="Width of the QR code in px (required).")
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save the QR code image to a file (default: False).",
    )
    parser.add_argument(
        "--annotate", action="store_true", help="Add an annotation (default: False)."
    )
    args = parser.parse_args()

    qr_img = create_qr_code(args.data, args.size)

    if args.annotate:
        font = ImageFont.truetype("arial.ttf", size=14)
        text = wrap_text(qr_img.size[0], font, args.data)
        qr_img = annotate_qr_code(qr_img, font, text)

    if args.save:
        qr_img.save("qr_code.png")
    else:
        qr_img.show()
