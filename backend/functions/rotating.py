from PIL import Image
import io

async def rotate_image(image_bytes, angle):
   
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    pixels = list(image.getdata())
    width, height = image.size

    matrix = [pixels[i * width:(i + 1) * width] for i in range(height)]

    angle = angle % 360
    if angle not in [90, 180, 270]:
        raise ValueError("Sadece 90, 180 veya 270 derece döndürme destekleniyor.")

    if angle == 90:
        rotated = [[matrix[height - 1 - i][j] for i in range(height)] for j in range(width)]
    elif angle == 180:
        rotated = [[matrix[height - 1 - i][width - 1 - j] for j in range(width)] for i in range(height)]
    elif angle == 270:
        rotated = [[matrix[i][width - 1 - j] for i in range(height)] for j in range(width)]

    if angle in [90, 270]:
        new_width, new_height = height, width
    else:
        new_width, new_height = width, height

    rotated_pixels = [pixel for row in rotated for pixel in row]
    rotated_img = Image.new("RGB", (new_width, new_height))
    rotated_img.putdata(rotated_pixels)

    img_byte_arr = io.BytesIO()
    rotated_img.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)
    return img_byte_arr
