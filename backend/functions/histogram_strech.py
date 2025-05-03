from PIL import Image
from io import BytesIO
from fastapi import HTTPException

def histogram_stretch(image_bytes, operation, min_in, max_in, min_out, max_out):
    try:
        image = Image.open(BytesIO(image_bytes)).convert("L")
        pixels = image.load()
        width, height = image.size

        img_min = 255
        img_max = 0
        for i in range(width):
            for j in range(height):
                value = pixels[i, j]
                if value < img_min:
                    img_min = value
                if value > img_max:
                    img_max = value

        result = Image.new("L", (width, height))
        result_pixels = result.load()

        for i in range(width):
            for j in range(height):
                p = pixels[i, j]

                if operation == "stretch":
                    if img_max != img_min:
                        norm = (p - img_min) / (img_max - img_min)
                    else:
                        norm = 0
               
                elif operation == "expand":
                    if max_in != min_in:
                        norm = (p - min_in) / (max_in - min_in)
                    else:
                        norm = 0
                else:
                    raise HTTPException(status_code=400, detail="İşlem türü geçersiz. 'stretch' veya 'expand' olmalı.")

                new_val = int(norm * (max_out - min_out) + min_out)
                new_val = max(0, min(255, new_val))
                result_pixels[i, j] = new_val

        img_byte_arr = BytesIO()
        result.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)
        return img_byte_arr

    except Exception as e:
        print(f"Histogram işlem hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Histogram işleminde hata: {str(e)}")
