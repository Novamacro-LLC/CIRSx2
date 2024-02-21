import platform
import urllib.request
import pytesseract
import llm
import io
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from tempfile import TemporaryDirectory
from pathlib import Path
from PIL import Image
from library.models import Document
from django.db.models import Q

sys = platform.system()


def chatgpt_init():
    model = llm.get_model('gpt-3.5-turbo')
    model.key = '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'
    conversation = model.conversation()
    return conversation


def author(text):
    output = chatgpt_init()
    chat = 'Please provide me a list of the authors of this text.' + text + 'Please provide only the names in a list.'
    auth = output.prompt(chat)
    return auth.text()


def pub_date(text):
    output = chatgpt_init()
    chat = 'Please provide me a publication date of this text.' + text + 'Please provide the response only in the YYYY-MM-DD date format.  If no day is provided please set to 01.'
    pub_dt = output.prompt(chat)
    return pub_dt.text()


def run():
    docs = Document.objects.filter(
        Q(doctyp_num=1) | Q(doctyp_num=2) | Q(doctyp_num=4),
        doc_txt__isnull=True
    )
    image_file_list = []
    if platform.system() == 'Windows':
        pytesseract.pytesseract.tesseract_cmd = (
            r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        )
        path_to_poppler_exe = Path(r'C:\Program Files\poppler-23.11.0\Library\bin')
    for d in docs:
        pdf_file = d.doc_path
        print(pdf_file)
        full_text = ''
        req = urllib.request.Request(pdf_file, headers={'User-Agent': 'Magic Browser'})
        file = urllib.request.urlopen(req).read()
        file_bytes = io.BytesIO(file)
        remote_file = PdfReader(file_bytes)
        count = len(remote_file.pages)
        print(count)
        with TemporaryDirectory() as tempdir:
            if count >= 100:
                if sys == 'Windows':
                    pdf_pages = convert_from_path(
                        pdf_file, 500, poppler_path=path_to_poppler_exe, last_page=75
                    )
                else:
                    pdf_pages = convert_from_path(pdf_file, 500, last_page=75)
            else:
                if sys == 'Windows':
                    pdf_pages = convert_from_path(
                        pdf_file, 500, poppler_path=path_to_poppler_exe
                    )
                else:
                    pdf_pages = convert_from_path(pdf_file, 500)
            for page_enumeration, page in enumerate(pdf_pages, start=1):
                filename = f'{tempdir}\page_{page_enumeration:03}.jpg'
                page.save(filename, 'JPEG')
                image_file_list.append(filename)
            print(image_file_list)
            data1 = str((pytesseract.image_to_string(Image.open(image_file_list[0]))))
            data1 = data1.replace('-\n', '')
            data2 = str((pytesseract.image_to_string(Image.open(image_file_list[1]))))
            data2 = data2.replace('-\n', '')
            sample = data1 + ' ' + data2
            for image_file in image_file_list:
                text = str((pytesseract.image_to_string(Image.open(image_file))))
                text = text.replace('-\n', '')
                full_text = full_text + text
            print(full_text)
            image_file_list.clear()
            d.doc_txt = full_text
            d.author = author(sample)
            print(author(sample))
            d.pub_dt = pub_date(sample)
            print(pub_date(sample))
            d.save()
