from PIL import Image
import io

async def crop_image(image_data, x1, y1, x2, y2):
  
    image = Image.open(io.BytesIO(image_data)).convert("RGBA")
    width, height = image.size

    x1 = max(0, min(x1, width))
    x2 = max(0, min(x2, width))
    y1 = max(0, min(y1, height))
    y2 = max(0, min(y2, height))

    if x2 <= x1 or y2 <= y1:
        raise ValueError("Geçersiz kırpma koordinatları: x2 > x1 ve y2 > y1 olmalıdır.")

    crop_width = x2 - x1
    crop_height = y2 - y1


    result_image = Image.new("RGBA", (crop_width, crop_height))
    original_pixels = image.load()
    result_pixels = result_image.load()

    for y in range(crop_height):
        for x in range(crop_width):
            result_pixels[x, y] = original_pixels[x1 + x, y1 + y]

  
    img_byte_arr = io.BytesIO()
    result_image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)
    return img_byte_arr
