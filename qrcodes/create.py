import math

import qrcode
from PIL import Image, ImageDraw, ImageFont


def create_qr(
    data: str,
    width: int,
    annotation: str | None = None,
    background: str | None = "white",
    foreground: str = "black",
    font_size: int = 14,
) -> Image.Image:
    """Create and annotate a QR code using some default formatting."""
    qr_img, num_boxes = generate_qr(data, background=background, foreground=foreground)
    qr_img = resize_qr(qr_img, width)
    if annotation:
        text_img = text_annotation(
            width,
            annotation,
            background=background,
            foreground=foreground,
            font_size=font_size,
            padding=width / num_boxes,
        )
        qr_img = annotate_qr_img(qr_img, text_img, background=background)
    return qr_img


def generate_qr(
    data: str, background: str | None = "white", foreground: str = "black"
) -> tuple[Image.Image, int]:
    """Create a black on white QR code with version determined by the data."""

    qr = qrcode.QRCode(version=None, border=1)
    qr.add_data(data)
    qr.make(fit=True)
    matrix = qr.get_matrix()
    num_boxes = len(matrix)

    qr_img = qr.make_image(
        fill_color=foreground, back_color=background or "white"
    ).convert("RGBA")

    if background is None:
        data = qr_img.getdata()
        qr_img.putdata(
            [
                (r, g, b, 0) if (r, g, b) == (255, 255, 255) else (r, g, b, 255)
                for r, g, b, *_ in data
            ]
        )

    return qr_img, num_boxes


def resize_qr(qr_img: Image.Image, width: int):
    """Resize the QR code to a square with size `width`."""
    return qr_img.resize((width, width))


def text_annotation(
    width: int,
    text: str,
    background: str | None = "white",
    foreground: str = "black",
    font_ttf: str = "arial.ttf",
    font_size: int = 14,
    character_wrap: bool = True,
    padding: int | float = 0,
) -> Image.Image:
    """Create an image containing the annotation text.

    Padding is applied to the left and right and botton because the QR code already pads the gap
    """

    if padding < 0:
        raise ValueError("Padding must be non-negative")
    padding = math.ceil(padding)

    font = _get_font(font_ttf, font_size)

    if character_wrap:
        text = _character_wrap(text, font, width - (2 * padding))

    _, text_height = _get_displayed_text_size(font, text)

    annotated_qr_img = Image.new(
        "RGBA", (width, text_height + padding), color=background
    )

    # Draw each line of text center aligned
    draw = ImageDraw.Draw(annotated_qr_img)
    y = 0
    for line in text.split("\n"):
        line_width, line_height = _get_displayed_text_size(font, line)
        x = (width - line_width) // 2  # center aligned
        draw.text((x, y), line, font=font, fill=foreground)
        y += line_height

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
    dummy_img = Image.new("RGBA", (1, 1))
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


def annotate_qr_img(
    qr_img: Image.Image,
    annotation_img: Image.Image,
    background: str | None = "white",
    padding: int | float = 0,
):
    """Vertically combine the QR code image with an annotation image.

    The annotation image can be padded to make it smaller than the full QR width.
    """

    if padding < 0:
        raise ValueError("Padding must be non-negative")
    padding = math.ceil(padding)

    qr_width, qr_height = qr_img.size
    orig_width, orig_height = annotation_img.size

    available_width = qr_width - 2 * padding
    aspect_ratio = orig_height / orig_width
    new_height = round(available_width * aspect_ratio)

    annotation_img = annotation_img.resize((available_width, new_height), Image.LANCZOS)

    total_height = qr_height + new_height + 2 * padding
    annotated_qr_img = Image.new("RGBA", (qr_width, total_height), color=background)

    annotated_qr_img.paste(qr_img, (0, 0))
    annotated_qr_img.paste(annotation_img, (padding, qr_height + padding))

    return annotated_qr_img
