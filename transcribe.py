import argparse

parser = argparse.ArgumentParser()
parser.add_argument('audio_files', nargs='+', help='Audio files to transcribe')
parser.add_argument('--model_path',
                    '-m',
                    default='whisper-large-v2-ct2/',
                    help='Path to model (default: whisper-large-v2-ct2/)')
parser.add_argument('--output-format',
                    '-o',
                    default='ass',
                    help='Output format (default: ass)')
parser.add_argument('--device',
                    '-d',
                    default='cuda',
                    help='Device to use for inference (default: cuda)')
parser.add_argument('--compute_type',
                    default='float16',
                    help='Compute type for inference (default: float16)')
parser.add_argument('--no-translate',
                    action='store_true',
                    help='Disable automatic translation')
# parser.add_argument('--trans-word-ts', action='store_true', help='If set, the program will generate word-level timestamps for translations. It may be unreliable.')
parser.add_argument(
    '--force-overwrite',
    '-f',
    action='store_true',
    help=
    'If set, the program will overwrite any existing output files. If not set (default behavior), the program will skip writing to an output file that already exists.'
)
parser.add_argument(
    '--translate-lang',
    '-t',
    default=None,
    help=
    'Translate to another language other than English. This is not an official behavior.'
)
parser.add_argument('--language', '-l', default=None, help='Force language')
args = parser.parse_args()

import glob
import os
import json

print('Importing whisper...')
from faster_whisper import WhisperModel

model = WhisperModel(args.model_path,
                     device=args.device,
                     compute_type=args.compute_type)

from assgen import gen_ass, gen_lrc

imported = False

# Iterate through each audio file provided in the command line arguments
for entry in args.audio_files:
    for audio_file in glob.glob(entry):
        # Extract the name of the file without its extension
        name = '.'.join(audio_file.split('.')[:-1])
        print('Transcribing ' + name)

        if args.language is None:
            # Transcribe the audio using the provided model
            segments, info = model.transcribe(audio_file,
                                              beam_size=5,
                                              word_timestamps=True)

            # Print the detected language and its probability
            print(
                f"Detected language '{info.language}' with probability {info.language_probability}"
            )

            language = info.language
        else:
            segments, info = model.transcribe(audio_file,
                                              beam_size=5,
                                              word_timestamps=True,
                                              language=args.language)
            language = args.language

        # Generate subtitles file with the same name as the original audio file and the detected language as the extension
        output_file = f"{name}.{language}.{args.output_format}"

        if args.force_overwrite or not os.path.exists(output_file):

            # Generate ass file
            if args.output_format == 'ass':
                raw_segments = gen_ass(segments, output_file)
            elif args.output_format == 'lrc':
                raw_segments = gen_lrc(segments, output_file)

            # write raw result to json file
            with open(f'{name}.{language}.json', 'w',
                      encoding='utf-8') as json_output:
                results = []
                for e in raw_segments:
                    results.append({
                        'start': e.start,
                        'end': e.end,
                        'text': e.text
                    })

                json.dump(results, json_output)

            # If the detected language is not English, transcribe the audio using translation
            if not args.no_translate and (
                (args.translate_lang is None and language != 'en') or
                (args.translate_lang is not None
                 and language != args.translate_lang)):

                if args.translate_lang is not None:
                    segments, info = model.transcribe(
                        audio_file,
                        beam_size=5,
                        language=args.translate_lang,
                        word_timestamps=True)  #args.trans_word_ts)
                else:
                    segments, info = model.transcribe(audio_file,
                                                      beam_size=5,
                                                      task='translate',
                                                      word_timestamps=True)

                # output_file = f"{name}.en.translated"

                # Append English translation
                if args.output_format == 'ass':
                    gen_ass(segments, output_file, append=True)

            # Print the name of the output subtitle file
            print(f"Subtitles saved to {output_file}")

        else:
            print(
                f"Skipping {output_file} (file already exists). Pass -f to overwrite existing files."
            )
