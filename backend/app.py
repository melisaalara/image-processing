from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO


from functions.gray_conversion import gray_conversion
from functions.binary_transformation import binary_transformation
from functions.rotating import rotate_image
from functions.cropping import crop_image
from functions.zoom import zoom_image
from functions.color_space_conversion import color_space_conversion
from functions.histogram_strech import histogram_stretch
from functions.contrast_reduction import contrast_reduction
from functions.convolution import convolution
from functions.double_threshold import double_threshold
from functions.edge_detection import edge_detection
from functions.saltandpepper import salt_and_pepper
from functions.meanmedianfiltering import mean_median_filter
from functions.motion_blur import motion_blur
from functions.morphology import morphology  
from functions.arithmetic_operations import arithmetic_operations

app = FastAPI(
    title="Görüntü İşleme API",
    description="Yüklenen görsellere çeşitli işlemler uygulamak için FastAPI tabanlı servis.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_response(image_bytes_io: BytesIO):
    return StreamingResponse(image_bytes_io, media_type="image/png")



@app.post("/process/gray", tags=["Gri Dönüşüm"])
async def gray_endpoint(file: UploadFile = File(...)):
    return get_response(await gray_conversion(await file.read()))

@app.post("/process/binary", tags=["Binary Dönüşüm"])
async def binary_endpoint(file: UploadFile = File(...), threshold: int = Form(...)):
    return get_response(await binary_transformation(await file.read(), threshold))

@app.post("/process/rotate", tags=["Görüntü Döndürme"])
async def rotate_endpoint(file: UploadFile = File(...), angle: int = Form(...)):
    return get_response(await rotate_image(await file.read(), angle))

@app.post("/process/crop", tags=["Görüntü Kırpma"])
async def crop_endpoint(file: UploadFile = File(...), x: int = Form(...), y: int = Form(...),
                        width: int = Form(...), height: int = Form(...)):
    return get_response(await crop_image(await file.read(), x, y, width, height))

@app.post("/process/zoom", tags=["Yakınlaştırma/Uzaklaştırma"])
async def zoom_endpoint(file: UploadFile = File(...), scale: float = Form(...),
                        center_x: int = Form(...), center_y: int = Form(...)):
    return get_response(await zoom_image(await file.read(), scale, center_x, center_y))

@app.post("/process/color", tags=["Renk Uzayı Dönüşümü"])
async def color_endpoint(file: UploadFile = File(...), mode: str = Form(...)):
    return get_response(await color_space_conversion(await file.read(), mode))

@app.post("/process/histogram", tags=["Histogram İşlemleri"])
async def histogram_endpoint(file: UploadFile = File(...),
                             operation: str = Form(...),
                             min_in: int = Form(...), max_in: int = Form(...),
                             min_out: int = Form(...), max_out: int = Form(...)):
    return get_response(histogram_stretch(await file.read(), operation, min_in, max_in, min_out, max_out))


@app.post("/process/contrast", tags=["Kontrast Azaltma"])
async def contrast_endpoint(file: UploadFile = File(...), factor: float = Form(...)):
    return get_response(await contrast_reduction(await file.read(), factor))


@app.post("/process/denoise", tags=["Gürültü Temizleme"])
async def denoise_endpoint(file: UploadFile = File(...),
                           filter_type: str = Form(...), kernel_size: int = Form(...)):
    if kernel_size % 2 == 0:
        kernel_size += 1
    return get_response(await mean_median_filter(await file.read(), filter_type, kernel_size))

@app.post("/process/double_threshold", tags=["Çift Eşikleme"])
async def double_threshold_endpoint(file: UploadFile = File(...),
                                    low_thresh: int = Form(...), high_thresh: int = Form(...)):
    return get_response(await double_threshold(await file.read(), low_thresh, high_thresh))

@app.post("/process/edge", tags=["Kenar Algılama"])
async def edge_endpoint(file: UploadFile = File(...), threshold1: int = Form(...), threshold2: int = Form(...)):
    return get_response(await edge_detection(await file.read(), threshold1, threshold2))

@app.post("/process/noise", tags=["Gürültü Ekleme"])
async def noise_endpoint(file: UploadFile = File(...),
                         salt_amount: float = Form(...), pepper_amount: float = Form(...)):
    return get_response(await salt_and_pepper(await file.read(), salt_amount, pepper_amount))

@app.post("/process/motion", tags=["Motion Filtresi"])
async def motion_endpoint(file: UploadFile = File(...), kernel_size: int = Form(...)):
    return get_response(await motion_blur(await file.read(), kernel_size))

@app.post("/process/morphology", tags=["Morfolojik İşlemler"])
async def morphology_endpoint(file: UploadFile = File(...),
                              morph_op: str = Form(...), kernel_size: int = Form(...)):
    return get_response(await morphology(await file.read(), morph_op, kernel_size))

@app.post("/process/arithmetic", tags=["Aritmetik İşlemler"])
async def arithmetic_endpoint(file: UploadFile = File(...), file2: UploadFile = File(...),
                              arithmetic_op: str = Form(...)):
    return get_response(await arithmetic_operations(await file.read(), await file2.read(), arithmetic_op))


@app.post("/process/convolution", tags=["Konvolüsyon (Median)"])
async def convolution_endpoint(file: UploadFile = File(...), kernel_size: int = Form(...)):
    if kernel_size % 2 == 0:
        kernel_size += 1
    return get_response(await convolution(await file.read(), kernel_size))