from PIL import Image
import io
import random

async def salt_and_pepper(image_bytes, salt_ratio, pepper_ratio):
    
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    width, height = image.size
    pixels = image.load()

    total_pixels = width * height
    num_salt = int(total_pixels * salt_ratio)
    num_pepper = int(total_pixels * pepper_ratio)

    # Salt
    for _ in range(num_salt):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        pixels[x, y] = (255, 255, 255)

    # Pepper
    for _ in range(num_pepper):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        pixels[x, y] = (0, 0, 0)

    
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)
    return img_byte_arr
