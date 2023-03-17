import argparse

parser = argparse.ArgumentParser()
parser.add_argument('audio_files', nargs='+', help='Audio files to transcribe')
parser.add_argument('--model_path', default='whisper-large-v2-ct2/', help='Path to model (default: whisper-large-v2-ct2/)')
parser.add_argument('--device', default='cuda', help='Device to use for inference (default: cuda)')
parser.add_argument('--compute_type', default='float16', help='Compute type for inference (default: float16)')
parser.add_argument('--no-translate', action='store_true', help='Disable automatic translation')
args = parser.parse_args()

from faster_whisper import WhisperModel
model = WhisperModel(args.model_path, device=args.device, compute_type=args.compute_type)

ass_header = '''
[Script Info]
Title: My Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Sans,16,&H00FFFFFF,&H000019FF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,0.8,0,2,50,50,24,1
Style: Small,Sans,10,&H00FFFFFF,&H000019FF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,0.8,0,8,50,50,258,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''

def format_srt_time(seconds):
    ms= seconds % 1
    s = int(seconds % 60)
    minutes = seconds / 60
    m = int(minutes % 60)
    hours = minutes / 60
    h = int(hours % 60)

    return '%02d:%02d:%02d,%03d' % (h,m,s,ms*1000)


def format_ass_time(seconds):
    ms= seconds % 1
    s = int(seconds % 60)
    minutes = seconds / 60
    m = int(minutes % 60)
    hours = minutes / 60
    h = int(hours % 60)

    return '%01d:%02d:%02d.%02d' % (h,m,s,ms*100)

# This function generates an ASS subtitle file for a list of segments.
# It takes the segments, the output file name, and an optional boolean argument to indicate if the subtitle 
# should be appended to an existing file instead of overwriting it.
def gen_subtitles(segments, outname, append=False):
    # Open the output file for writing or appending
    t = open(outname + '.ass', 'a' if append else 'w', encoding='utf-8')

    # Write the ASS subtitle file header
    if not append:
        t.write(ass_header)

    # Set the style based on whether the subtitle is being appended or not
    style = 'Small' if append else 'Default'

    # Iterate through each segment and generate the corresponding subtitle lines
    for i, segment in enumerate(segments):
        # Format the start and end times for the subtitle line
        start_time = format_srt_time(segment.start)
        end_time = format_srt_time(segment.end)

        # Replace any newline characters in the segment text with a space
        text = segment.text.replace('\n', ' ')

        # Create the subtitle line with the index, start and end times, and segment text
        line = f"{i+1}\n{start_time} --> {end_time}\n{text}"

        # Print the segment information to the console
        print("[%s -> %s] %s" % (start_time, end_time, segment.text))

        # Write the subtitle line to the output file
        # f.write(line+'\n\n')

        # if word_ts:
        # Iterate through each word in the segment and generate the corresponding subtitle lines
        pos = 0
        last_end = segment.start
        for word in segment.words:
            st = word.start
            ed = word.end
            start_time = format_ass_time(st)
            end_time = format_ass_time(ed)

            # If the current word starts after the end of the last word, generate a subtitle line for the gap
            if st > last_end:
                line = f"Dialogue: 0,{format_ass_time(last_end)},{format_ass_time(st)},{style},,0,0,0,,{segment.text}"
                t.write(line+'\n')

            # Insert the formatting codes for the word in the segment text
            wordlen = len(word.word)
            text = list(segment.text)
            text.insert(pos+wordlen, '{\c}')
            text.insert(pos, '{\c&H9628E6&}')

            # Create the subtitle line for the word
            line = f"Dialogue: 0,{start_time},{end_time},{style},,0,0,0,,{''.join(text)}"
            t.write(line+'\n')
            pos += wordlen

            # Set the end time of the last word to the current word's end time
            last_end = ed
    
    # Close the output file
    # f.close()
    # if word_ts:
    t.close()

# Iterate through each audio file provided in the command line arguments
for audio_file in args.audio_files:
    # Extract the name of the file without its extension
    name = '.'.join(audio_file.split('.')[:-1])

    # Transcribe the audio using the provided model
    segments, info = model.transcribe(audio_file, beam_size=5, word_timestamps=True)
    
    # Print the detected language and its probability
    print(f"Detected language '{info.language}' with probability {info.language_probability}")
    
    # Generate subtitles file with the same name as the original audio file and the detected language as the extension
    output_file = f"{name}.{info.language}"
    gen_subtitles(segments, output_file)

    # If the detected language is not English, transcribe the audio using translation
    if not args.no_translate and info.language != 'en':
        segments, info = model.transcribe(audio_file, beam_size=5, task='translate', word_timestamps=True)

        # output_file = f"{name}.en.translated"

        # Append English translation
        gen_subtitles(segments, output_file, append=True)
    
    # Print the name of the output subtitle file
    print(f"Subtitles saved to {output_file}")
