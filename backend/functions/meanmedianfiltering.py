from PIL import Image
import io

async def mean_median_filter(image_data, filter_type, kernel_size):
    image = Image.open(io.BytesIO(image_data)).convert("L")
    pixels = image.load()
    width, height = image.size

    pad = kernel_size // 2
    output = Image.new("L", (width, height))
    output_pixels = output.load()

    for i in range(height):
        for j in range(width):
            region = []

            for ki in range(-pad, pad + 1):
                for kj in range(-pad, pad + 1):
                    ni = min(max(i + ki, 0), height - 1)
                    nj = min(max(j + kj, 0), width - 1)
                    region.append(pixels[nj, ni]) 

            if filter_type == "mean":
                value = sum(region) // len(region)
            elif filter_type == "median":
                region.sort()
                mid = len(region) // 2
                if len(region) % 2 == 0:
                    value = (region[mid - 1] + region[mid]) // 2
                else:
                    value = region[mid]
            else:
                raise ValueError("Geçersiz filtre tipi: 'mean' veya 'median' olmalı.")

            output_pixels[j, i] = value

    img_byte_arr = io.BytesIO()
    output.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)
    return img_byte_arr
