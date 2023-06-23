
from assgen import gen_ass
from faster_whisper import WhisperModel


model = WhisperModel('whisper-large-v2-ct2/',
                     device='cuda',
                     compute_type='float16')

def generate_subtitles(audio_files,
                       translate_lang='',
                       language='',
                       translate=True,
                       word_ts=True,
                       attach=False,
                       beam_size=5):

    output_files = []

    if type(audio_files) != list:
        audio_files = [audio_files]

    if language != '':
        language = language_codes[language]

    if translate_lang != '':
        translate_lang = language_codes[translate_lang]

    print(audio_files)
    for entry in audio_files:
        audio_file = entry.name
        print(audio_file)
        # Extract the name of the file without its extension
        name = '.'.join(audio_file.split('.')[:-1])
        print('Transcribing ' + name)

        if language == '':
            # Transcribe the audio using the provided model
            segments, info = model.transcribe(audio_file,
                                              beam_size=beam_size,
                                              word_timestamps=word_ts)

            # Print the detected language and its probability
            print(
                f"Detected language '{info.language}' with probability {info.language_probability}"
            )

            language = info.language
        else:
            segments, info = model.transcribe(audio_file,
                                              beam_size=beam_size,
                                              word_timestamps=word_ts,
                                              language=language)
            language = language

        # Generate subtitles file with the same name as the original audio file and the detected language as the extension
        output_file = f"{name}.{language}.ass"

        gen_ass(segments, output_file)

        # If the detected language is not English, transcribe the audio using translation
        if translate and (
            (translate_lang == '' and language != 'en') or
            (translate_lang != '' and language != translate_lang)):
            if translate_lang != '':
                segments, info = model.transcribe(audio_file,
                                                  beam_size=beam_size,
                                                  language=translate_lang,
                                                  word_timestamps=word_ts)
            else:
                segments, info = model.transcribe(audio_file,
                                                  beam_size=beam_size,
                                                  task='translate',
                                                  word_timestamps=word_ts)

            # output_file = f"{name}.en.translated"

            # Append English translation
            gen_ass(segments, output_file, append=True)

        # Print the name of the output subtitle file
        print(f"Subtitles saved to {output_file}")

        if attach:
            embed = name + '-embed.mkv'
            ff = ffmpy.FFmpeg(inputs={
                audio_file: None,
                output_file: None
            },
                              outputs={embed: ['-c', 'copy', '-metadata:s:s:0',f'language={language}','-y']})
            ff.run()
            output_files.append(embed)
        else:
            output_files.append(output_file)

    return output_files