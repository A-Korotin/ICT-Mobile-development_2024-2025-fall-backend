from fastapi import APIRouter, UploadFile, File, HTTPException

from src.router.error_dto import ErrorDto
from src.router.ocr.dto import PdfContents, PageContents
from pdf2image import convert_from_bytes
import pytesseract
import os

router = APIRouter()

@router.post("/pdf-contents", response_model=PdfContents, status_code=200,
             responses={
                 200: {"model": PdfContents},
                 400: {"model": ErrorDto},
             })
async def ocr_pdf_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Файл должен быть в формате PDF.")

    try:
        # Считываем содержимое файла
        pdf_bytes = await file.read()

        # Преобразуем PDF-страницы в изображения (одна страница — одно изображение)
        images = convert_from_bytes(pdf_bytes)

        # Распознаем текст на каждой странице
        pages = []
        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image, lang='rus+eng')  # Поддержка русского и английского
            contents = PageContents(number=i, content=text)
            pages.append(contents)

        return PdfContents(pages=pages)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке файла: {str(e)}")