# faster-whisper-transcribe
Speed up and Improve Accuracy of Whisper Transcription with Faster-Whisper Model

This efficient script utilizes the Faster-Whisper model (available at https://github.com/guillaumekln/faster-whisper) to generate highly accurate word-level ASS subtitles. By leveraging this model, the script achieves a significant speed-up compared to traditional transcription methods. Before running the script, be sure to follow the installation instructions for Faster-Whisper.

## Example Usage

```bash
python3 transcribe.py *.flac -f -l ja -t zh
```

`*.flac`: Indicates that all files in the current directory with the file extension ".flac" will be translated.
`-f`: Indicates that the instruction will be forcefully executed, overwriting the output target file if it already exists.
`-l ja`: Indicates that the input language is Japanese.
`-t zh`: Indicates that the input language will be translated into Chinese.
