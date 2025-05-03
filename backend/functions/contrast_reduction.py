from PIL import Image
import io

async def contrast_reduction(image_data, factor):
    image = Image.open(io.BytesIO(image_data)).convert("RGB")
    width, height = image.size
    pixels = image.load()

    result_image = Image.new("RGB", (width, height))
    result_pixels = result_image.load()

    # 3x3 pencere
    for y in range(height):
        for x in range(width):
            sum_r = sum_g = sum_b = count = 0

            for j in range(-1, 2):
                for i in range(-1, 2):
                    nx, ny = x + i, y + j
                    if 0 <= nx < width and 0 <= ny < height:
                        r, g, b = pixels[nx, ny]
                        sum_r += r
                        sum_g += g
                        sum_b += b
                        count += 1

         
            mean_r = sum_r / count
            mean_g = sum_g / count
            mean_b = sum_b / count

            r, g, b = pixels[x, y]
            new_r = (r - mean_r) * factor + mean_r
            new_g = (g - mean_g) * factor + mean_g
            new_b = (b - mean_b) * factor + mean_b

            new_r = int(min(max(0, new_r), 255))
            new_g = int(min(max(0, new_g), 255))
            new_b = int(min(max(0, new_b), 255))

            result_pixels[x, y] = (new_r, new_g, new_b)

    img_byte_arr = io.BytesIO()
    result_image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)
    return img_byte_arr
