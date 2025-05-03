from PIL import Image
import io

async def convolution(image_data, kernel_size):
    image = Image.open(io.BytesIO(image_data)).convert("L")
    pixels = image.load()
    width, height = image.size

    pad = kernel_size // 2

    result_image = Image.new("L", (width, height))
    result_pixels = result_image.load()

    for y in range(height):
        for x in range(width):
            region = []

            for dy in range(-pad, pad + 1):
                for dx in range(-pad, pad + 1):
                    ny = min(height - 1, max(0, y + dy))
                    nx = min(width - 1, max(0, x + dx))
                    region.append(pixels[nx, ny])

            for i in range(len(region)):
                for j in range(i + 1, len(region)):
                    if region[j] < region[i]:
                        region[i], region[j] = region[j], region[i]

            median = region[len(region) // 2]
            result_pixels[x, y] = median

    
    img_byte_arr = io.BytesIO()
    result_image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)
    return img_byte_arr
