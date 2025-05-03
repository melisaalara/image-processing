from PIL import Image
import io

async def binary_transformation(image_data, threshold):
  
    image = Image.open(io.BytesIO(image_data)).convert("L")
    width, height = image.size

    binary_image = Image.new("L", (width, height))

    for y in range(height):
        for x in range(width):
            pixel_value = image.getpixel((x, y))
            binary_value = 255 if pixel_value > threshold else 0
            binary_image.putpixel((x, y), binary_value)

  
    img_byte_arr = io.BytesIO()
    binary_image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)
    return img_byte_arr
