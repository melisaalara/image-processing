from PIL import Image
import io

async def zoom_image(image_bytes, scale, center_x, center_y):
   
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    width, height = image.size

    crop_w = int(width / scale)
    crop_h = int(height / scale)

    left = max(center_x - crop_w // 2, 0)
    top = max(center_y - crop_h // 2, 0)
    right = min(left + crop_w, width)
    bottom = min(top + crop_h, height)

   
    zoomed_image = Image.new("RGB", (width, height))

    for y in range(height):
        for x in range(width):
           
            src_x = int((x * (right - left)) / width)
            src_y = int((y * (bottom - top)) / height)

            src_pixel_x = left + src_x
            src_pixel_y = top + src_y

            if src_pixel_x < width and src_pixel_y < height:
                color = image.getpixel((src_pixel_x, src_pixel_y))
                zoomed_image.putpixel((x, y), color)

    img_byte_arr = io.BytesIO()
    zoomed_image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)
    return img_byte_arr
