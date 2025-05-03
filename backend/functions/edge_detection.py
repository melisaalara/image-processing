from PIL import Image
import io
import math

async def edge_detection(image_data, low_thresh, high_thresh):
    image = Image.open(io.BytesIO(image_data)).convert("L")
    width, height = image.size
    pixels = image.load()

    
    def gaussian_blur(img):
        kernel = [
            [1, 2, 1],
            [2, 4, 2],
            [1, 2, 1]
        ]
        result = [[0] * width for _ in range(height)]
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                total = 0
                for j in range(3):
                    for i in range(3):
                        total += img[x - 1 + i, y - 1 + j] * kernel[j][i]
                result[y][x] = total // 16
        return result

    blurred = gaussian_blur(pixels)

  

    gx_kernel = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    gy_kernel = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

    magnitude = [[0] * width for _ in range(height)]
    direction = [[0] * width for _ in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            gx = gy = 0
            for j in range(3):
                for i in range(3):
                    val = blurred[y - 1 + j][x - 1 + i]
                    gx += gx_kernel[j][i] * val
                    gy += gy_kernel[j][i] * val

            mag = math.hypot(gx, gy)
            magnitude[y][x] = mag
            angle = math.degrees(math.atan2(gy, gx)) % 180
            direction[y][x] = angle

   

    nms = [[0] * width for _ in range(height)]

    def get_neighbor(mag, x, y, angle):
        if (0 <= x < width) and (0 <= y < height):
            return mag[y][x]
        return 0

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            angle = direction[y][x]
            m = magnitude[y][x]

            if (0 <= angle < 22.5) or (157.5 <= angle <= 180):
                before = get_neighbor(magnitude, x - 1, y, angle)
                after = get_neighbor(magnitude, x + 1, y, angle)
            elif 22.5 <= angle < 67.5:
                before = get_neighbor(magnitude, x - 1, y - 1, angle)
                after = get_neighbor(magnitude, x + 1, y + 1, angle)
            elif 67.5 <= angle < 112.5:
                before = get_neighbor(magnitude, x, y - 1, angle)
                after = get_neighbor(magnitude, x, y + 1, angle)
            elif 112.5 <= angle < 157.5:
                before = get_neighbor(magnitude, x - 1, y + 1, angle)
                after = get_neighbor(magnitude, x + 1, y - 1, angle)

            if m >= before and m >= after:
                nms[y][x] = m
            else:
                nms[y][x] = 0

   

    strong, weak = 255, 75
    result = [[0] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            val = nms[y][x]
            if val >= high_thresh:
                result[y][x] = strong
            elif val >= low_thresh:
                result[y][x] = weak
            else:
                result[y][x] = 0



    def is_connected_to_strong(x, y):
        for j in range(-1, 2):
            for i in range(-1, 2):
                nx, ny = x + i, y + j
                if 0 <= nx < width and 0 <= ny < height:
                    if result[ny][nx] == strong:
                        return True
        return False

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if result[y][x] == weak:
                if is_connected_to_strong(x, y):
                    result[y][x] = strong
                else:
                    result[y][x] = 0


    final_image = Image.new("L", (width, height))
    final_pixels = final_image.load()
    for y in range(height):
        for x in range(width):
            final_pixels[x, y] = int(result[y][x])


    output = io.BytesIO()
    final_image.save(output, format="PNG")
    output.seek(0)
    return output
