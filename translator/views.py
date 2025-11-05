from django.shortcuts import render
from deep_translator import GoogleTranslator
from deep_translator.exceptions import NotValidPayload

# Full language dictionary with readable names
LANGUAGES = {
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

def index(request):
    translated_text = ''
    input_text = ''
    source_lang = 'auto'
    target_lang = 'en'
    error_message = ''

    if request.method == 'POST':
        input_text = request.POST.get('input_text', '').strip()
        source_lang = request.POST.get('source_lang', 'auto')
        target_lang = request.POST.get('target_lang', 'en')

        if not input_text:
            error_message = "⚠️ Please enter some text."
        elif len(input_text) > 5000:
            error_message = "⚠️ Text too long! Max 5000 characters."
        else:
            try:
                translated_text = GoogleTranslator(
                    source=source_lang,
                    target=target_lang
                ).translate(input_text)
            except NotValidPayload:
                error_message = "⚠️ Invalid input for translation."
            except Exception as e:
                error_message = f"❌ Translation failed: {str(e)}"

    context = {
        'languages': LANGUAGES,
        'translated_text': translated_text,
        'input_text': input_text,
        'source_lang': source_lang,
        'target_lang': target_lang,
        'error_message': error_message
    }

    return render(request, 'translator/index.html', context)
