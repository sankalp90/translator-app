from django.shortcuts import render
from deep_translator import GoogleTranslator
from PIL import Image
import pytesseract
import fitz  # PyMuPDF
from docx import Document



# Point pytesseract to your Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Create your views here
def index(request):
    translated_text = ''
    input_text = ''
    source_lang = ''
    target_lang = ''
    error_message = ''

    # Languages dictionary
    languages = {
    'auto': 'Auto Detect',
    'af': 'Afrikaans', 'sq': 'Albanian', 'am': 'Amharic', 'ar': 'Arabic',
    'hy': 'Armenian', 'as': 'Assamese', 'ay': 'Aymara', 'az': 'Azerbaijani',
    'eu': 'Basque', 'be': 'Belarusian', 'bn': 'Bengali', 'bs': 'Bosnian',
    'bg': 'Bulgarian', 'ca': 'Catalan', 'ceb': 'Cebuano', 'ny': 'Chichewa (Nyanja)',
    'zh-CN': 'Chinese (Simplified)', 'zh-TW': 'Chinese (Traditional)', 'co': 'Corsican',
    'hr': 'Croatian', 'cs': 'Czech', 'da': 'Danish', 'nl': 'Dutch', 'en': 'English',
    'eo': 'Esperanto', 'et': 'Estonian', 'tl': 'Filipino', 'fi': 'Finnish', 'fr': 'French',
    'fy': 'Frisian', 'gl': 'Galician', 'ka': 'Georgian', 'de': 'German', 'el': 'Greek',
    'gu': 'Gujarati', 'ht': 'Haitian Creole', 'ha': 'Hausa', 'haw': 'Hawaiian',
    'he': 'Hebrew', 'hi': 'Hindi', 'hmn': 'Hmong', 'hu': 'Hungarian', 'is': 'Icelandic',
    'ig': 'Igbo', 'id': 'Indonesian', 'ga': 'Irish', 'it': 'Italian', 'ja': 'Japanese',
    'jw': 'Javanese', 'kn': 'Kannada', 'kk': 'Kazakh', 'km': 'Khmer', 'ko': 'Korean',
    'ku': 'Kurdish', 'ky': 'Kyrgyz', 'lo': 'Lao', 'la': 'Latin', 'lv': 'Latvian',
    'lt': 'Lithuanian', 'lb': 'Luxembourgish', 'mk': 'Macedonian', 'mg': 'Malagasy',
    'ms': 'Malay', 'ml': 'Malayalam', 'mt': 'Maltese', 'mi': 'Maori', 'mr': 'Marathi',
    'mn': 'Mongolian', 'my': 'Myanmar (Burmese)', 'ne': 'Nepali', 'no': 'Norwegian',
    'or': 'Odia (Oriya)', 'ps': 'Pashto', 'fa': 'Persian', 'pl': 'Polish', 'pt': 'Portuguese',
    'pa': 'Punjabi', 'ro': 'Romanian', 'ru': 'Russian', 'sm': 'Samoan', 'gd': 'Scots Gaelic',
    'sr': 'Serbian', 'st': 'Sesotho', 'sn': 'Shona', 'sd': 'Sindhi', 'si': 'Sinhala',
    'sk': 'Slovak', 'sl': 'Slovenian', 'so': 'Somali', 'es': 'Spanish', 'su': 'Sundanese',
    'sw': 'Swahili', 'sv': 'Swedish', 'tg': 'Tajik', 'ta': 'Tamil', 'te': 'Telugu',
    'th': 'Thai', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu', 'uz': 'Uzbek',
    'vi': 'Vietnamese', 'cy': 'Welsh', 'xh': 'Xhosa', 'yi': 'Yiddish', 'yo': 'Yoruba',
    'zu': 'Zulu'
    }

    if request.method == 'POST':
        source_lang = request.POST.get('source_lang')
        target_lang = request.POST.get('target_lang')

        # 1️ Text translation
        if 'input_text' in request.POST and request.POST.get('input_text').strip():
            input_text = request.POST.get('input_text')
            if len(input_text) > 5000:
                error_message = 'Text too long! Maximum 5000 characters allowed.'
            else:
                translated_text = GoogleTranslator(source=source_lang, target=target_lang).translate(input_text)

        # 2️ Image translation
        elif 'image' in request.FILES:
            image_file = request.FILES['image']
            image = Image.open(image_file)
            extracted_text = pytesseract.image_to_string(image)
            if extracted_text.strip():
                translated_text = GoogleTranslator(source=source_lang, target=target_lang).translate(extracted_text)
            else:
                error_message = "No text found in the image."

        # 3️ Document translation (PDF or Word)
        elif 'document' in request.FILES:
            doc_file = request.FILES['document']
            file_name = doc_file.name.lower()
            full_text = ''

            if file_name.endswith('.pdf'):
                doc = fitz.open(stream=doc_file.read(), filetype='pdf')
                for page in doc:
                    full_text += page.get_text()
            elif file_name.endswith('.docx'):
                doc = Document(doc_file)
                for para in doc.paragraphs:
                    full_text += para.text + '\n'
            elif file_name.endswith('.txt'):
                full_text = doc_file.read().decode('utf-8')
            else:
                error_message = "Unsupported document format!"
            
            if full_text.strip() and not error_message:
                translated_text = GoogleTranslator(source=source_lang, target=target_lang).translate(full_text)
            elif not full_text.strip():
                error_message = "No text found in the document."

    context = {
        'languages': languages,
        'translated_text': translated_text,
        'input_text': input_text,
        'source_lang': source_lang,
        'target_lang': target_lang,
        'error_message': error_message
    }
    return render(request, 'translator/index.html', context)
