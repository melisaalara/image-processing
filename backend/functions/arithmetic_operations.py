from PIL import Image
import io

async def arithmetic_operations(file1_bytes, file2_bytes, operation):

    img1 = Image.open(io.BytesIO(file1_bytes)).convert("RGB")
    img2 = Image.open(io.BytesIO(file2_bytes)).convert("RGB")

    img2 = img2.resize(img1.size)

    w, h = img1.size

    result_img = Image.new("RGB", (w, h))
    pixels1 = img1.load()
    pixels2 = img2.load()
    pixels_result = result_img.load()

    for y in range(h):
        for x in range(w):
            r1, g1, b1 = pixels1[x, y]
            r2, g2, b2 = pixels2[x, y]

            if operation == "subtract":
                r = max(0, r1 - r2)
                g = max(0, g1 - g2)
                b = max(0, b1 - b2)
            elif operation == "multiply":
                r = int(r1 * r2 / 255)
                g = int(g1 * g2 / 255)
                b = int(b1 * b2 / 255)
            else:
                raise ValueError("Geçersiz işlem türü: 'subtract' veya 'multiply' olmalı.")

            pixels_result[x, y] = (r, g, b)


    img_byte_arr = io.BytesIO()
    result_img.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)
    return img_byte_arr
