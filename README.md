# Create and print QR codes from python

Helper scripts to create, annotate and print QR codes in python using the [qrcode](https://pypi.org/project/qrcode/) and [brother_ql](https://pypi.org/project/brother-ql/) packages.


I'm sure this can be done more efficiently, but solves my requirements.

## Creating

The `size` argument defines the square size of the image in pixels, unless the image is annotated in which case the image is extended down to include the annotation text.

### CLI Example

To encode "ABC213" into a 100px wide image containing the QR code annotated with the text "ABC123" and saved to "ABC123.png"

    python create.py ABC123 100 --annotate --save

### Automating

The helper can be imported into other projects

    cd path/to/this_repo
    pip install .

which could act as data sources, for example

    import qrcode_helper.create

    box_codes = [
        "ABC123",
        "DEF456"
    ]

    for box_code in box_codes:
        qr_code = qrcode_helper.create.qr_code(box_code, 100)
        qr_code = qrcode_helper.create.annotate(qr_code, box_code)
        qr_code.save(f"{box_code}.png")

By default the annotation text is displayed in 14pt Arial font and is character wrapped to within the `size` width, but these settings can be overruled.

## Printing

Currently the only printing supported is to Brother QL label printers using the [brother_ql](https://pypi.org/project/brother-ql/) package. This requires driver setup detailed in https://pypi.org/project/brother-ql#backends. The 'Editor Lite' button must be off on the printer.