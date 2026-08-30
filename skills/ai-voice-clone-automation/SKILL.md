# 🎙️ AI Voice Clone Automation Skill

AI 声音克隆 + TTS 自动化：输入文本 → 克隆音色 → 生成自然语音，应用于客服、播客、有声书、品牌语音。

## 能力矩阵

| 能力 | 描述 | 技术 |
|------|------|------|
| 声音克隆 | 5-30秒音频 → 建立音色模型 | Coqui/Tacotron2/xtts |
| 多语言 TTS | 中文/英文/日语等 30+ 语言 | ElevenLabs / VALL-E / fish-speech |
| 情感控制 | 开心/悲伤/兴奋/平静 四种情感 | Emvoice / StyleTTS2 |
| 批量生成 | 长文本自动分片 + 并发生成 | FFmpeg + Python |
| 品牌语音库 | 企业音色标准化管理 + 版本控制 | 本地存储 + API |

## 快速开始

```bash
pip install TTS pydub openai elevenlabs
python3 scripts/voice_clone.py --source=my_voice.wav --text="欢迎致电某某公司"
python3 scripts/batch_tts.py --file=texts.txt --voice=brand_voice_v2
```

## 目录结构
```
ai-voice-clone-automation/
├── SKILL.md
├── README.md
└── scripts/
    ├── voice_clone.py      # 声音克隆
    ├── batch_tts.py        # 批量 TTS 生成
    ├── voice_brand_manager.py # 品牌音色管理
    └── audio_post_processor.py # 音频后处理
```

## 使用示例

```python
from voice_clone import clone_and_speak

# 克隆声音并生成语音
result = clone_and_speak(
    source_audio="speaker.wav",  # 5秒以上人声
    text="您好，这里是客服中心，请问有什么可以帮您？",
    emotion="warm",
    output="response.wav"
)
# result: {"audio_path": "response.wav", "duration": 3.2, "sample_rate": 22050}
```

## 品牌音色管理
```python
from voice_brand_manager import BrandVoiceManager

manager = BrandVoiceManager("/data/brand_voices")
manager.register("brand_v2", "brand_voice_model.pt")
manager.list_voices()
manager.set_active("brand_v2")  # 设置默认音色
```

---
*AI 声音 × 品牌 = 统一的品牌听觉形象*
