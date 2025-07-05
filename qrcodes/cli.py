import argparse

from create import create_qr


def main():
    parser = argparse.ArgumentParser(description="Create and annotate QR codes")
    parser.add_argument("data", type=str, help="The data to encode in the QR code.")
    parser.add_argument(
        "width", type=int, help="The width (square size) of the QR code."
    )
    parser.add_argument(
        "--annotation", type=str, help="The text to display under the QR code."
    )
    parser.add_argument("--filename", type=str, help="Filename to save the QR code.")

    args = parser.parse_args()

    qr_img = create_qr(args.data, args.width, args.annotation)

    if args.filename:
        qr_img.save(args.filename)
    else:
        qr_img.show()


if __name__ == "__main__":
    main()
