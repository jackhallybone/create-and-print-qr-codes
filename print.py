from brother_ql.backends.helpers import send
from brother_ql.conversion import convert
from brother_ql.raster import BrotherQLRaster


def print_to_brother_ql(img, paper_name):
    """Send image to a wired Brother QL printer using `brother_ql`.

    Driver setup and paper sizes: https://pypi.org/project/brother-ql/

    The image size should match the paper requirements. For example,
    38mm endless paper is called "38" and has a printable width of 413px.
    """

    qlr = BrotherQLRaster("QL-800")  # printer model
    qlr.exception_on_warning = True
    instructions = convert(qlr=qlr, images=[img], label=paper_name)  # images as a list
    send(
        instructions=instructions,
        printer_identifier="usb://0x04f9:0x209b",  # libusb filter address
        backend_identifier="pyusb",
        blocking=True,
    )
