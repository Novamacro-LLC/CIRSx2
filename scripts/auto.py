import os
import io
import platform
import urllib.request
import pytesseract
import llm
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from tempfile import TemporaryDirectory
from pathlib import Path
from PIL import Image
from library.models import Document
from django.db.models import Q

sys = platform.system()


def chatgpt_init():
    try:
        model = llm.get_model('gpt-3.5-turbo')
        model.key = os.environ.get('open_ai_key')  # Changed from os.environ() to os.environ.get()
        conversation = model.conversation()
        return conversation
    except Exception as e:
        print(f"Error initializing ChatGPT: {str(e)}")
        return None


def author(text):
    output = chatgpt_init()
    if output:
        chat = 'Please provide me a list of the authors of this text.' + text + 'Please provide only the names in a list.'
        try:
            auth = output.prompt(chat)
            return auth.text()
        except Exception as e:
            print(f"Error getting author information: {str(e)}")
            return ""
    return ""


def pub_date(text):
    output = chatgpt_init()
    if output:
        chat = 'Please provide me a publication date of this text.' + text + 'Please provide the response only in the YYYY-MM-DD date format.  If no day is provided please set to 01.'
        try:
            pub_dt = output.prompt(chat)
            return pub_dt.text()
        except Exception as e:
            print(f"Error getting publication date: {str(e)}")
            return ""
    return ""


def run():
    docs = Document.objects.filter(
        Q(doctyp_num=1) | Q(doctyp_num=2) | Q(doctyp_num=4),
        doc_txt__isnull=True
    )

    for d in docs:
        image_file_list = []  # Moved inside the loop to ensure fresh list for each document
        try:
            pdf_file = d.doc_path
            print(f"Processing PDF file: {pdf_file}")

            # Set up system-specific configurations
            if platform.system() == 'Windows':
                pytesseract.pytesseract.tesseract_cmd = (
                    r'C:\Program Files\Tesseract-OCR\tesseract.exe'
                )
                path_to_poppler_exe = Path(r'C:\Program Files\poppler-23.11.0\Library\bin')
            else:
                path_to_poppler_exe = Path('usr/share/poppler')  # Fixed path separator

            # Initialize variables
            full_text = ''

            # Fetch and read PDF
            req = urllib.request.Request(pdf_file, headers={'User-Agent': 'Magic Browser'})
            file = urllib.request.urlopen(req).read()
            file_bytes = io.BytesIO(file)
            remote_file = PdfReader(file_bytes)
            count = len(remote_file.pages)
            print(f"Number of pages in PDF: {count}")

            with TemporaryDirectory() as tempdir:
                # Convert PDF to images
                if count >= 100:
                    pdf_pages = convert_from_path(
                        pdf_file, 500,
                        poppler_path=path_to_poppler_exe,
                        last_page=75
                    )
                else:
                    pdf_pages = convert_from_path(
                        pdf_file, 500,
                        poppler_path=path_to_poppler_exe
                    )

                # Save pages as images
                for page_enumeration, page in enumerate(pdf_pages, start=1):
                    filename = str(Path(tempdir) / f'page_{page_enumeration:03}.jpg')  # Fixed path creation
                    page.save(filename, 'JPEG')
                    image_file_list.append(filename)

                print(f"Number of images created: {len(image_file_list)}")

                # Process first two pages for sample text
                if len(image_file_list) >= 2:
                    data1 = str(pytesseract.image_to_string(Image.open(image_file_list[0])))
                    data1 = data1.replace('-\n', '')
                    data2 = str(pytesseract.image_to_string(Image.open(image_file_list[1])))
                    data2 = data2.replace('-\n', '')
                    sample = data1 + ' ' + data2
                else:
                    # Handle cases with fewer pages
                    sample = str(pytesseract.image_to_string(Image.open(image_file_list[0]))) if image_file_list else ""
                    sample = sample.replace('-\n', '')

                # Process all pages for full text
                for image_file in image_file_list:
                    text = str(pytesseract.image_to_string(Image.open(image_file)))
                    text = text.replace('-\n', '')
                    full_text += text

                print("Full text extraction completed")

                # Update document
                d.doc_txt = full_text
                d.author = author(sample)
                print(f"Authors: {d.author}")
                d.pub_dt = pub_date(sample)
                print(f"Publication date: {d.pub_dt}")
                d.save()

                print(f"Successfully processed document: {pdf_file}")

        except Exception as e:
            print(f"Error processing document {d.doc_path}: {str(e)}")
            continue  # Continue with next document if current one fails

        finally:
            # Clear list even if an error occurred
            image_file_list.clear()