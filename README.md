# faster-whisper-transcribe
Gradio WebUI for Faster Whisper model

This efficient script utilizes the Faster-Whisper model (available at https://github.com/guillaumekln/faster-whisper) to generate highly accurate word-level ASS subtitles. By leveraging this model, the script achieves a significant speed-up and lower VRAM usage compared to original Whisper model. Before running the script, be sure to follow the installation instructions for Faster-Whisper.

![ui](ui.png)

## Run

You can run this app by running `gradio_app.py`.
Before first run, make sure to install all the dependencies by running `pip install -r requirements.txt`.

## Command line Usage

```bash
python3 transcribe.py *.flac -f -l ja -t zh
```

* `*.flac`: Indicates that all files in the current directory with the file extension ".flac" will be translated.
* `-f`: Indicates that the instruction will be forcefully executed, overwriting the output target file if it already exists.
* `-l ja`: Indicates that the input language is Japanese.
* `-t zh`: Indicates that the input language will be translated into Chinese.

-----

利用Gradio编写的Faster-Whisper模型WebUI

这个高效的脚本利用 Faster-Whisper 模型（可在 [https://github.com/guillaumekln/faster-whisper](https://github.com/guillaumekln/faster-whisper)  获取）生成高度准确的单词级别 ASS 字幕。通过这个模型，该脚本相比原版Whisper模型实现了更高的效率和更低的显存占用。在运行脚本之前，请确保按照 Faster-Whisper 的安装说明进行安装。

## 运行

你可以通过运行`gradio_app.py`来启动WebUI。
在首次运行前，请先确保安装所有依赖，通过`pip install -r requirements.txt`来安装。

## 命令行使用示例

```bash
python3 transcribe.py *.flac -f -l ja -t zh
```

 
- `*.flac`：表示将当前目录下所有扩展名为 .flac 的文件都进行识别和翻译。 
- `-f`：表示强制执行，如果输出目标文件已经存在，则覆盖它。 
- `-l ja`：表示输入语言为日语。 
- `-t zh`：表示将输入语言翻译成中文。
