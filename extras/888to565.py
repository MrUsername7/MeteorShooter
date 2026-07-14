from PIL import Image

TRANSPARENT_BYTES = (0x56, 0x78)

def image_to_python_bytearray(image_path, output_file):
    img = Image.open(image_path).convert("RGBA")

    hex_data = []

    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = img.getpixel((x, y))

            if a == 0:
                hex_data.append("\\x56")
                hex_data.append("\\x78")
                continue

            # RGB888 -> RGB565
            rgb565 = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)

            hex_data.append(f"\\x{(rgb565 >> 8) & 0xFF:02X}")
            hex_data.append(f"\\x{rgb565 & 0xFF:02X}")

    with open(output_file, "w") as f:
        f.write("bytearray(b'")
        f.write("".join(hex_data))
        f.write("')\n")

image_to_python_bytearray("image.png", "image_data.txt")
