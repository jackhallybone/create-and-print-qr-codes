from qrcodes import create

# Using the create helper function with default formatting
boxes_of_serial_numbers = [
    ["abc", "def", "ghi"],
    ["123", "456", "789"],
]
for i, box_contents in enumerate(boxes_of_serial_numbers):
    data = ",".join(box_contents)
    annotation = f"Box Contains:\n{"\n".join(box_contents)}"
    label = create.create_qr(
        data, 150, annotation, background="white", foreground="black"
    )
    label.show()
    label.save(f"box_{i}.png")
