import math

import qrcode
from PIL import Image, ImageDraw, ImageFont


def create_qr(data: str, width: int, annotation: str | None = None, font_size: int = 14) -> Image.Image:
    qr_img, num_boxes = generate_qr(data)
    qr_img = resize_qr(qr_img, width)
    if annotation:
        qr_img = annotate_qr(
            qr_img, annotation, font_size=font_size, padding=width / num_boxes
        )
    return qr_img


def generate_qr(data: str) -> tuple[Image.Image, int]:
    """Create a black on white QR code with version determined by the data."""

    qr = qrcode.QRCode(version=None, border=1)
    qr.add_data(data)
    qr.make(fit=True)
    matrix = qr.get_matrix()
    num_boxes = len(matrix)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    return qr_img, num_boxes


def resize_qr(qr_img: Image.Image, width: int):
    """Resize the QR code to a square with size `width`."""
    return qr_img.resize((width, width))


def annotate_qr(
    qr_img: Image.Image,
    text: str,
    font_ttf: str = "arial.ttf",
    font_size: int = 14,
    character_wrap: bool = True,
    padding: int | float = 0,
) -> Image.Image:
    """Extend the image and add text below the QR code."""

    if padding < 0:
        raise ValueError("Padding must be non-negative")
    padding = math.ceil(padding)

    font = _get_font(font_ttf, font_size)

    qr_width, qr_height = qr_img.size

    if character_wrap:
        text = _character_wrap(text, font, qr_width - (2 * padding))

    text_width, text_height = _get_displayed_text_size(font, text)

    annotated_qr_img = Image.new(
        "RGB", (qr_width, qr_height + text_height + padding), color="white"
    )
    annotated_qr_img.paste(qr_img, (0, 0))

    # Draw each line of text center aligned
    draw = ImageDraw.Draw(annotated_qr_img)
    y = qr_height  # below the QR image
    for line in text.split("\n"):
        text_width, text_height = _get_displayed_text_size(font, line)
        x = (qr_width - text_width) // 2  # center aligned
        draw.text((x, y), line, font=font, fill="black")
        y += text_height + 4

    return annotated_qr_img


def _get_font(ttf: str, size: int):
    try:
        return ImageFont.truetype(font=ttf, size=size)
    except (OSError, IOError):
        try:
            return ImageFont.load_default(size=size)
        except TypeError:
            return ImageFont.load_default()


def _get_displayed_text_size(font: ImageFont.ImageFont, text: str) -> tuple[int, int]:
    """Get the rendered text size."""
    # Calculate width based on rendered text size
    dummy_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    bbox = draw.textbbox((0, 0), text, font=font)
    width = math.ceil(bbox[2])

    # Calculate height based on the font ascenders and descender heights
    ascent, descent = font.getmetrics()
    line_height = ascent + descent
    height = line_height * len(text.split("\n"))

    return width, height


def _character_wrap(text: str, font: ImageFont.ImageFont, width: int) -> str:
    """Character wrap text to fit within a defined width."""
    line = ""
    lines = []
    for char in text:
        if _get_displayed_text_size(font, line + char)[0] > width:
            lines.append(line.strip())
            line = char
        else:
            line += char
    if line:
        lines.append(line.strip())
    return "\n".join(lines)
