import os

import ffmpy
import gradio as gr

from trans import generate_subtitles

print("Loading model...")

supported_languages = [
    "Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Assamese",
    "Azerbaijani", "Bashkir", "Basque", "Belarusian", "Bengali", "Bosnian",
    "Breton", "Bulgarian", "Burmese", "Castilian", "Catalan", "Chinese",
    "Croatian", "Czech", "Danish", "Dutch", "English", "Estonian", "Faroese",
    "Finnish", "Flemish", "French", "Galician", "Georgian", "German", "Greek",
    "Gujarati", "Haitian", "Haitian Creole", "Hausa", "Hawaiian", "Hebrew",
    "Hindi", "Hungarian", "Icelandic", "Indonesian", "Italian", "Japanese",
    "Javanese", "Kannada", "Kazakh", "Khmer", "Korean", "Lao", "Latin",
    "Latvian", "Letzeburgesch", "Lingala", "Lithuanian", "Luxembourgish",
    "Macedonian", "Malagasy", "Malay", "Malayalam", "Maltese", "Maori",
    "Marathi", "Moldavian", "Moldovan", "Mongolian", "Myanmar", "Nepali",
    "Norwegian", "Nynorsk", "Occitan", "Panjabi", "Pashto", "Persian",
    "Polish", "Portuguese", "Punjabi", "Pushto", "Romanian", "Russian",
    "Sanskrit", "Serbian", "Shona", "Sindhi", "Sinhala", "Sinhalese", "Slovak",
    "Slovenian", "Somali", "Spanish", "Sundanese", "Swahili", "Swedish",
    "Tagalog", "Tajik", "Tamil", "Tatar", "Telugu", "Thai", "Tibetan",
    "Turkish", "Turkmen", "Ukrainian", "Urdu", "Uzbek", "Valencian",
    "Vietnamese", "Welsh", "Yiddish", "Yoruba"
]

language_codes = {
    "Afrikaans": "af",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Assamese": "as",
    "Azerbaijani": "az",
    "Bashkir": "ba",
    "Basque": "eu",
    "Belarusian": "be",
    "Bengali": "bn",
    "Bosnian": "bs",
    "Breton": "br",
    "Bulgarian": "bg",
    "Burmese": "my",
    "Castilian": "es",
    "Catalan": "ca",
    "Chinese": "zh",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Estonian": "et",
    "Faroese": "fo",
    "Finnish": "fi",
    "Flemish": "nl",
    "French": "fr",
    "Galician": "gl",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Gujarati": "gu",
    "Haitian": "ht",
    "Haitian Creole": "ht",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "he",
    "Hindi": "hi",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Indonesian": "id",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jv",
    "Kannada": "kn",
    "Kazakh": "kk",
    "Khmer": "km",
    "Korean": "ko",
    "Lao": "lo",
    "Latin": "la",
    "Latvian": "lv",
    "Letzeburgesch": "lb",
    "Lingala": "ln",
    "Lithuanian": "lt",
    "Luxembourgish": "lb",
    "Macedonian": "mk",
    "Malagasy": "mg",
    "Malay": "ms",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Maori": "mi",
    "Marathi": "mr",
    "Moldavian": "mo",
    "Moldovan": "mo",
    "Mongolian": "mn",
    "Myanmar": "my",
    "Nepali": "ne",
    "Norwegian": "no",
    "Nynorsk": "nn",
    "Occitan": "oc",
    "Panjabi": "pa",
    "Pashto": "ps",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Pushto": "ps",
    "Romanian": "ro",
    "Russian": "ru",
    "Sanskrit": "sa",
    "Serbian": "sr",
    "Shona": "sn",
    "Sindhi": "sd",
    "Sinhala": "si",
    "Sinhalese": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Spanish": "es",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tagalog": "tl",
    "Tajik": "tg",
    "Tamil": "ta",
    "Tatar": "tt",
    "Telugu": "te",
    "Thai": "th",
    "Tibetan": "bo",
    "Turkish": "tr",
    "Turkmen": "tk",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uzbek": "uz",
    "Valencian": "ca",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Yiddish": "yi",
    "Yoruba": "yo"
}



audio_files = gr.Files(label="Audio or video files to transcribe",
                       file_types=['audio', 'video', '.flv'])
translate_lang = gr.Dropdown(choices=supported_languages,
                             label="Translate to language")
language = gr.Dropdown(choices=supported_languages, label="Force language")
translate = gr.Checkbox(label="Automatic translation", value=True)
word_ts = gr.Checkbox(label="Word-level timestamps", value=True)
attach = gr.Checkbox(label="Produce a video with embedded subtitles")
beam_size = gr.Number(label="Beam size", value=5, precision=0)

output_text = gr.Files(label='Output subtitle files')

gradio_app = gr.Interface(
    fn=generate_subtitles,
    inputs=[
        audio_files, translate_lang, language, translate, word_ts, attach,
        beam_size
    ],
    outputs=output_text,
    title="Faster Whisper Transcription",
)

if __name__ == '__main__':
    gradio_app.launch(server_name='0.0.0.0')