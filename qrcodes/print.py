from brother_ql.backends.helpers import send
from brother_ql.conversion import convert
from brother_ql.raster import BrotherQLRaster


def print_to_brother_ql(
    img,
    paper_name,
    printer_name="QL-800",
    printer_identifier="usb://0x04f9:0x209b",  # libusb filter address
    backend_identifier="pyusb",
    blocking=True,
):
    """Send image to a Brother QL printer using the `brother_ql` package.

    Driver setup and paper sizes: https://pypi.org/project/brother-ql/

    The image size should match the paper requirements. For example,
    38mm endless paper is called "38" and has a printable width of 413px.
    """

    qlr = BrotherQLRaster(printer_name)  # printer model
    qlr.exception_on_warning = True
    instructions = convert(qlr=qlr, images=[img], label=paper_name)  # image as a list
    send(
        instructions=instructions,
        printer_identifier=printer_identifier,
        backend_identifier=backend_identifier,
        blocking=blocking,
    )
