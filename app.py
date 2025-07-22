import streamlit as st
from deep_translator import GoogleTranslator
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image


st.title("📄 PDF Language Translator")



languages = {
    'af': 'Afrikaans', 'sq': 'Albanian', 'am': 'Amharic', 'ar': 'Arabic', 'hy': 'Armenian',
    'az': 'Azerbaijani', 'eu': 'Basque', 'be': 'Belarusian', 'bn': 'Bengali', 'bs': 'Bosnian',
    'bg': 'Bulgarian', 'ca': 'Catalan', 'ceb': 'Cebuano', 'ny': 'Chichewa', 'zh-cn': 'Chinese (Simplified)',
    'zh-tw': 'Chinese (Traditional)', 'co': 'Corsican', 'hr': 'Croatian', 'cs': 'Czech', 'da': 'Danish',
    'nl': 'Dutch', 'en': 'English', 'eo': 'Esperanto', 'et': 'Estonian', 'tl': 'Filipino', 'fi': 'Finnish',
    'fr': 'French', 'fy': 'Frisian', 'gl': 'Galician', 'ka': 'Georgian', 'de': 'German', 'el': 'Greek',
    'gu': 'Gujarati', 'ht': 'Haitian Creole', 'ha': 'Hausa', 'haw': 'Hawaiian', 'iw': 'Hebrew',
    'hi': 'Hindi', 'hmn': 'Hmong', 'hu': 'Hungarian', 'is': 'Icelandic', 'ig': 'Igbo', 'id': 'Indonesian',
    'ga': 'Irish', 'it': 'Italian', 'ja': 'Japanese', 'jw': 'Javanese', 'kn': 'Kannada', 'kk': 'Kazakh',
    'km': 'Khmer', 'ko': 'Korean', 'ku': 'Kurdish (Kurmanji)', 'ky': 'Kyrgyz', 'lo': 'Lao',
    'la': 'Latin', 'lv': 'Latvian', 'lt': 'Lithuanian', 'lb': 'Luxembourgish', 'mk': 'Macedonian',
    'mg': 'Malagasy', 'ms': 'Malay', 'ml': 'Malayalam', 'mt': 'Maltese', 'mi': 'Maori', 'mr': 'Marathi',
    'mn': 'Mongolian', 'my': 'Myanmar (Burmese)', 'ne': 'Nepali', 'no': 'Norwegian',
    'ps': 'Pashto', 'fa': 'Persian', 'pl': 'Polish', 'pt': 'Portuguese', 'pa': 'Punjabi', 'ro': 'Romanian',
    'ru': 'Russian', 'sm': 'Samoan', 'gd': 'Scots Gaelic', 'sr': 'Serbian', 'st': 'Sesotho',
    'sn': 'Shona', 'sd': 'Sindhi', 'si': 'Sinhala', 'sk': 'Slovak', 'sl': 'Slovenian', 'so': 'Somali',
    'es': 'Spanish', 'su': 'Sundanese', 'sw': 'Swahili', 'sv': 'Swedish', 'tg': 'Tajik', 'ta': 'Tamil',
    'te': 'Telugu', 'th': 'Thai', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu', 'ug': 'Uyghur',
    'uz': 'Uzbek', 'vi': 'Vietnamese', 'cy': 'Welsh', 'xh': 'Xhosa', 'yi': 'Yiddish', 'yo': 'Yoruba',
    'zu': 'Zulu'
}



target_language = st.selectbox("🌐 Select the output language for translation", options=languages.keys(), format_func=lambda x: languages[x])



uploaded_file = st.file_uploader("📁 Upload a PDF file to translate", type=["pdf"])


if uploaded_file is not None:
    try:


        images = convert_from_bytes(uploaded_file.read())
        pdf_text = ""
        for page_num, image in enumerate(images):
            text = pytesseract.image_to_string(image)
            if text:
                pdf_text += text + "\n"

        if len(pdf_text.strip()) == 0:
            st.warning("⚠️ PDF appears to be empty or not text-based.")
        else:
            st.subheader("📄 Extracted PDF Text Preview:")
            st.text_area("Extracted Text", pdf_text, height=200)
            if st.button("🌍 Translate PDF Text"):
                batch_size = 1000
                batches = [pdf_text[i:i+batch_size] for i in range(0, len(pdf_text), batch_size)]
                translated_batches = []
                progress = st.progress(0)
                for i, batch in enumerate(batches):
                    try:
                        translated = GoogleTranslator(source='auto', target=target_language).translate(batch)
                        if not translated:
                            translated = "[No translation returned]"
                        translated_batches.append(translated)
                    except Exception as e:
                        translated_batches.append(f"[Translation error: {e}]")
                    progress.progress((i + 1) / len(batches))
                translated_text = '\n\n'.join(translated_batches)
                st.subheader("✅ Translated Output:")
                st.text_area("Translated Text", translated_text, height=300)
    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
