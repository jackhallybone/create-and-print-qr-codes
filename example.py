from qrcodes import create

# Use the helper function:
qr_img = create.create_qr("www.example.com", 150, "Scan to visit\nwww.example.com")
qr_img.show()
