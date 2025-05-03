from PIL import Image
import io

async def gray_conversion(image_data):
   
    image = Image.open(io.BytesIO(image_data)).convert("RGB")
    width, height = image.size

    gray_image = Image.new("L", (width, height))

    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y)) 
           
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            gray_image.putpixel((x, y), gray)

    img_byte_arr = io.BytesIO()
    gray_image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)
    return img_byte_arr
