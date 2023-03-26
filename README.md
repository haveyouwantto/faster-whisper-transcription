# faster-whisper-transcribe
Speed up and Improve Accuracy of Whisper Transcription with Faster-Whisper Model

This efficient script utilizes the Faster-Whisper model (available at https://github.com/guillaumekln/faster-whisper) to generate highly accurate word-level ASS subtitles. By leveraging this model, the script achieves a significant speed-up compared to original Whisper model. Before running the script, be sure to follow the installation instructions for Faster-Whisper.

## Example Usage

```bash
python3 transcribe.py *.flac -f -l ja -t zh
```

* `*.flac`: Indicates that all files in the current directory with the file extension ".flac" will be translated.
* `-f`: Indicates that the instruction will be forcefully executed, overwriting the output target file if it already exists.
* `-l ja`: Indicates that the input language is Japanese.
* `-t zh`: Indicates that the input language will be translated into Chinese.

-----

使用 Faster-Whisper 模型提高Whisper识别的速度和准确性

这个高效的脚本利用 Faster-Whisper 模型（可在 [https://github.com/guillaumekln/faster-whisper](https://github.com/guillaumekln/faster-whisper)  获取）生成高度准确的单词级别 ASS 字幕。通过这个模型，该脚本相比原版Whisper模型实现了显著的加速。在运行脚本之前，请确保按照 Faster-Whisper 的安装说明进行安装。
## 使用示例

```bash
python3 transcribe.py *.flac -f -l ja -t zh
```

 
- `*.flac`：表示将当前目录下所有扩展名为 .flac 的文件都进行识别和翻译。 
- `-f`：表示强制执行，如果输出目标文件已经存在，则覆盖它。 
- `-l ja`：表示输入语言为日语。 
- `-t zh`：表示将输入语言翻译成中文。
