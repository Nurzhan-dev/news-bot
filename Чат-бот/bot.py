import os
import pytesseract
import fitz  # PyMuPDF
import logging
from PIL import Image
from io import BytesIO
from telegram import Update, InputMediaPhoto
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from docx import Document
import zipfile
import shutil
import tempfile

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
logging.basicConfig(level=logging.INFO)

# --- Текст из PDF ---
def extract_text_from_pdf(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    return "\n".join([page.get_text() for page in doc]).strip()

# --- Картинки из PDF ---
def extract_images_from_pdf(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    images = []
    for page in doc:
        for img in page.get_images(full=True):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            images.append(BytesIO(image_bytes))
    return images

# --- Текст из DOCX ---
def extract_text_from_docx(file_bytes):
    with open("temp.docx", "wb") as f:
        f.write(file_bytes)
    doc = Document("temp.docx")
    return "\n".join([p.text for p in doc.paragraphs])

# --- Картинки из DOCX ---
def extract_images_from_docx(file_bytes):
    with tempfile.TemporaryDirectory() as tmpdir:
        docx_path = os.path.join(tmpdir, "file.docx")
        with open(docx_path, "wb") as f:
            f.write(file_bytes)
        with zipfile.ZipFile(docx_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)
        media_path = os.path.join(tmpdir, "word", "media")
        images = []
        if os.path.exists(media_path):
            for file in os.listdir(media_path):
                if file.lower().endswith(('png', 'jpg', 'jpeg')):
                    with open(os.path.join(media_path, file), "rb") as img_file:
                        images.append(BytesIO(img_file.read()))
        return images

# --- Текст из изображения на казахском ---
def extract_text_from_image(image_bytes):
    image = Image.open(BytesIO(image_bytes))
    return pytesseract.image_to_string(image, lang='kaz+rus+eng')

# --- Генерация поста ---
def generate_post(text):
    lines = text.strip().split("\n")
    title = lines[0][:100] if lines else "Пост"
    description = " ".join(lines[1:4])[:300]
    hashtags = "#казақша #бот #мәтін"
    return f"<b>{title}</b>\n\n{description}\n\n{hashtags}"

# --- Обработка файла ---
def handle_file(update: Update, context: CallbackContext):
    file = update.message.document or update.message.photo[-1]
    file_obj = file.get_file()
    file_bytes = file_obj.download_as_bytearray()
    file_name = file.file_name if hasattr(file, "file_name") else "image.jpg"
    ext = file_name.split(".")[-1].lower()

    text, images = "", []

    if ext in ["jpg", "jpeg", "png"]:
        text = extract_text_from_image(file_bytes)
        images = [BytesIO(file_bytes)]
    elif ext == "pdf":
        text = extract_text_from_pdf(file_bytes)
        images = extract_images_from_pdf(file_bytes)
    elif ext == "docx":
        text = extract_text_from_docx(file_bytes)
        images = extract_images_from_docx(file_bytes)
    else:
        update.message.reply_text("Формат не поддерживается. Отправь PDF, DOCX или изображение.")
        return

    post = generate_post(text)
    update.message.reply_html(post)

    if images:
        media_group = [InputMediaPhoto(media=img) for img in images[:10]]  # до 10 изображений
        update.message.reply_media_group(media=media_group)

# --- Запуск ---
if __name__ == '__main__':
    updater = Updater("TELEGRAM_TOKEN", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.document | Filters.photo, handle_file))
    logging.info("🤖 Бот запущен")
    updater.start_polling()
    updater.idle()