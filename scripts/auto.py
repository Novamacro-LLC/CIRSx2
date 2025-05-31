import os
import io
import platform
import urllib.request
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'D:\Users\bdavison\Tesseract\tesseract.exe'
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
        model.key = os.environ.get('open_ai_key')
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
        image_file_list = []
        try:
            pdf_file = d.doc_path
            print(f"Processing PDF file: {pdf_file}")

            if platform.system() == 'Windows':
                pytesseract.pytesseract.tesseract_cmd = (
                    r'D:\Users\bdavison\Tesseract\tesseract.exe'
                )
                path_to_poppler_exe = Path(r'D:\Users\bdavison\poppler-24.07.0\Library\bin')
            else:
                path_to_poppler_exe = Path('usr/share/poppler')

            full_text = ''

            try:
                req = urllib.request.Request(pdf_file, headers={'User-Agent': 'Magic Browser'})
                file = urllib.request.urlopen(req).read()
                file_bytes = io.BytesIO(file)
                remote_file = PdfReader(file_bytes)
                count = len(remote_file.pages)
                print(f"Number of pages in PDF: {count}")
            except Exception as e:
                print(f"Error reading PDF file: {str(e)}")
                continue

            with TemporaryDirectory() as tempdir:
                try:
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

                    for page_enumeration, page in enumerate(pdf_pages, start=1):
                        filename = str(Path(tempdir) / f'page_{page_enumeration:03}.jpg')
                        page.save(filename, 'JPEG')
                        image_file_list.append(filename)

                    print(f"Number of images created: {len(image_file_list)}")

                    if not image_file_list:
                        print(f"Warning: No images were created for {pdf_file}")
                        continue

                    # Process first page
                    data1 = str(pytesseract.image_to_string(Image.open(image_file_list[0])))
                    data1 = data1.replace('-\n', '')

                    # Set sample text based on number of pages
                    if len(image_file_list) > 1:
                        data2 = str(pytesseract.image_to_string(Image.open(image_file_list[1])))
                        data2 = data2.replace('-\n', '')
                        sample = data1 + ' ' + data2
                        print("Processed first two pages for sample text")
                    else:
                        sample = data1
                        print("Processed single page for sample text")

                    # Process all available pages for full text
                    for image_file in image_file_list:
                        text = str(pytesseract.image_to_string(Image.open(image_file)))
                        text = text.replace('-\n', '')
                        full_text += text

                    print("Text extraction completed")

                    # Update document with extracted information
                    d.doc_txt = full_text
                    d.author = author(sample)
                    print(f"Authors extracted: {d.author}")
                    d.pub_dt = pub_date(sample)
                    print(f"Publication date extracted: {d.pub_dt}")
                    d.save()

                    print(f"Successfully processed document: {pdf_file}")

                except Exception as e:
                    print(f"Error during PDF processing: {str(e)}")
                    continue

        except Exception as e:
            print(f"Error processing document {d.doc_path}: {str(e)}")
            continue

        finally:
            image_file_list.clear()