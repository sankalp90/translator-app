from django.shortcuts import render
from deep_translator import GoogleTranslator
# Create your views here.

def index(request):
    translated_text = ''
    input_text = ''
    source_lang = ''
    target_lang = ''

    if request.method == 'POST':
        input_text = request.POST.get('input_text')
        source_lang = request.POST.get('source_lang')
        target_lang = request.POST.get('target_lang')
        
        translated_text = GoogleTranslator(
            source=source_lang,
            target=target_lang
        ).translate(input_text)

    languages = {
        'en': 'English', 'hi': 'Hindi', 'fr': 'French', 'es': 'Spanish',
        'de': 'German', 'ta': 'Tamil', 'te': 'Telugu', 'mr': 'Marathi',
        'gu': 'Gujarati', 'ja': 'Japanese', 'ko': 'Korean',
        'zh-cn': 'Chinese (Simplified)', 'ru': 'Russian', 'ar': 'Arabic', 'it': 'Italian'
    }

    context = {
        'languages': languages,
        'translated_text': translated_text,
        'input_text': input_text,
        'source_lang': source_lang,
        'target_lang': target_lang
    }

    return render(request, 'translator/index.html', context)