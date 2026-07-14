import struct
import numpy as np
from PIL import Image

def rgb565_to_png(raw_bytes, width, height, output_filename="output.png"):
    # 1. Parse into a numpy array of 16-bit integers (Little-Endian)
    # '<u2' forces Little-Endian format regardless of the host system architecture
    pixels = np.frombuffer(raw_bytes, dtype='>u2')
    
    # 2. Extract channels using bitwise operations
    # Red:   5 bits (bits 11 to 15) -> Shift 11 bits right, mask with 0x1F
    # Green: 6 bits (bits 5 to 10)  -> Shift 5 bits right, mask with 0x3F
    # Blue:  5 bits (bits 0 to 4)   -> Mask with 0x1F
    r = ((pixels >> 11) & 0x1F) * 255 // 31
    g = ((pixels >> 5) & 0x3F) * 255 // 63
    b = (pixels & 0x1F) * 255 // 31
    
    # 3. Stack channels together into RGB888 format and reshape to image grid
    rgb888 = np.stack([r, g, b], axis=-1).astype(np.uint8)
    rgb888_grid = rgb888.reshape((height, width, 3))
    
    # 4. Generate and save the PNG file
    img = Image.fromarray(rgb888_grid, 'RGB')
    img.save(output_filename)
    print(f"Success: Image saved as {output_filename} ({width}x{height})")

# --- Executable Context ---
if __name__ == "__main__":
    # Your raw frame buffer data from the question
    fb_data = bytearray(b'\x56\x78\xEE\x95\x56\x78\xBC\x2A\xEE\x95\xEE\x95\xEE\x95\xBC\x2A\xEE\x95\xEE\x95\xBC\x2A\xEE\x95\xEE\x95\xEE\x95\xBC\x2A\x56\x78\xEE\x95\x56\x78')
    
    # Image constraints
    width = 3
    height = 6
    
    # Execute conversion
    rgb565_to_png(fb_data, width, height, "framebuffer_output.png")
