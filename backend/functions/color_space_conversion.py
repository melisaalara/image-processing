from PIL import Image
import io

async def color_space_conversion(image_bytes, mode):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    width, height = image.size
    pixels = image.load()

    result_img = Image.new("RGB", (width, height))
    result_pixels = result_img.load()

    def rgb_to_hsv_pixel(r, g, b):
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        cmax = max(r, g, b)
        cmin = min(r, g, b)
        delta = cmax - cmin

        if delta == 0:
            h = 0
        elif cmax == r:
            h = (60 * ((g - b) / delta)) % 360
        elif cmax == g:
            h = (60 * ((b - r) / delta)) + 120
        else:
            h = (60 * ((r - g) / delta)) + 240

        s = 0 if cmax == 0 else delta / cmax
        v = cmax

        return (int(h / 360 * 255), int(s * 255), int(v * 255))

    def rgb_to_ycbcr_pixel(r, g, b):
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        y  = 0.299 * r + 0.587 * g + 0.114 * b
        cb = -0.168736 * r - 0.331264 * g + 0.5 * b + 0.5
        cr = 0.5 * r - 0.418688 * g - 0.081312 * b + 0.5
        return (
            int(y * 255),
            int(cb * 255),
            int(cr * 255)
        )

    def rgb_to_lab_pixel(r, g, b):
        def f(t):
            delta = 6 / 29
            if t > delta**3:
                return t ** (1/3)
            else:
                return (t / (3 * delta ** 2)) + (4 / 29)

        #  0–1
        r, g, b = r / 255.0, g / 255.0, b / 255.0

     
        X = 0.412453 * r + 0.357580 * g + 0.180423 * b
        Y = 0.212671 * r + 0.715160 * g + 0.072169 * b
        Z = 0.019334 * r + 0.119193 * g + 0.950227 * b

        # white
        X /= 0.95047
        Z /= 1.08883

        fx, fy, fz = f(X), f(Y), f(Z)
        L = 116 * fy - 16
        a = 500 * (fx - fy)
        b = 200 * (fy - fz)

    
        return (
            int(max(0, min(255, L / 100 * 255))),
            int(max(0, min(255, a + 128))),
            int(max(0, min(255, b + 128)))
        )

    
    mode = mode.lower()
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            if mode == "hsv":
                result_pixels[x, y] = rgb_to_hsv_pixel(r, g, b)
            elif mode == "ycbcr":
                result_pixels[x, y] = rgb_to_ycbcr_pixel(r, g, b)
            elif mode == "lab":
                result_pixels[x, y] = rgb_to_lab_pixel(r, g, b)
            else:
                raise ValueError("Geçersiz dönüşüm modu: hsv, ycbcr veya lab olmalı.")

    img_byte_arr = io.BytesIO()
    result_img.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)
    return img_byte_arr
