from PIL import Image
import io

async def morphology(image_data, morph_op, kernel_size):
    image = Image.open(io.BytesIO(image_data)).convert("L")
    width, height = image.size
    pixels = image.load()

    offset = kernel_size // 2

    output = Image.new("L", (width, height))
    out_pixels = output.load()

    def get_region(i, j):
        region = []
        for y in range(i - offset, i + offset + 1):
            for x in range(j - offset, j + offset + 1):
                if 0 <= x < width and 0 <= y < height:
                    region.append(pixels[x, y])
        return region

    for i in range(height):
        for j in range(width):
            region = get_region(i, j)
           
            if morph_op == "dilate":
                out_pixels[j, i] = max(region)
           
            elif morph_op == "erode":
                out_pixels[j, i] = min(region)
           
            elif morph_op == "open":
                eroded_val = min(region)
                out_pixels[j, i] = eroded_val 
            
            elif morph_op == "close":
                dilated_val = max(region)
                out_pixels[j, i] = dilated_val  
           
            else:
                raise ValueError("İşlem geçersiz: 'dilate', 'erode', 'open', 'close' olabilir.")

    if morph_op == "open":
        image = output.copy()
        pixels = image.load()
        out_pixels = output.load()
        for i in range(height):
            for j in range(width):
                region = get_region(i, j)
                out_pixels[j, i] = max(region)

    elif morph_op == "close":
        image = output.copy()
        pixels = image.load()
        out_pixels = output.load()
        for i in range(height):
            for j in range(width):
                region = get_region(i, j)
                out_pixels[j, i] = min(region)

    # Byte dönüşümü
    img_byte_arr = io.BytesIO()
    output.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)
    return img_byte_arr
