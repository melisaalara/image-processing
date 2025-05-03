from PIL import Image
import io

async def motion_blur(image_data, kernel_size):
    image = Image.open(io.BytesIO(image_data)).convert("RGB")
    width, height = image.size
    pixels = image.load()

    output = Image.new("RGB", (width, height))
    out_pixels = output.load()

    offset = kernel_size // 2

    for y in range(height):
        for x in range(width):
            r_total = g_total = b_total = 0
            count = 0

            for k in range(-offset, offset + 1):
                nx = x + k
                if 0 <= nx < width:
                    r, g, b = pixels[nx, y]
                    r_total += r
                    g_total += g
                    b_total += b
                    count += 1

            out_pixels[x, y] = (r_total // count, g_total // count, b_total // count)

    img_byte_arr = io.BytesIO()
    output.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)
    return img_byte_arr
