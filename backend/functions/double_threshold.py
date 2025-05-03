from PIL import Image
import io

async def double_threshold(image_data, low_thresh, high_thresh):
  
    image = Image.open(io.BytesIO(image_data)).convert("L")
    width, height = image.size
    pixels = image.load()

    result = Image.new("L", (width, height))
    result_pixels = result.load()

    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            if pixel >= high_thresh:
                result_pixels[x, y] = 255  
            elif pixel >= low_thresh:
                result_pixels[x, y] = 127  
            else:
                result_pixels[x, y] = 0    

    img_byte_arr = io.BytesIO()
    result.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return img_byte_arr
