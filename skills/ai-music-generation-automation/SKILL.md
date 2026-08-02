# AI Music Generation Automation

> 音乐生成管线：文本描述 → 音乐生成（Udio / Suno / MusicGen）+ 自动混音 + 发布

## 概述

本技能提供一套端到端的 AI 音乐生成自动化解决方案，通过文本描述（Prompt）生成原创音乐，支持风格控制、节拍调整、自动混音，以及一键发布到主流平台。

适用场景：短视频 BGM、游戏配乐、播客片头、品牌音乐、广告配乐。

## 核心能力

- **文本生成音乐**：Udio / Suno API / MusicGen，支持中文 Prompt
- **风格控制**：流派（BGM、电子、古典、流行）、情绪（BGM、激烈、忧伤）、乐器配置
- **节拍 BPM**：自动适配场景（快节奏/慢节奏）
- **自动混音**：音量均衡、淡入淡出、降噪
- **多格式输出**：MP3、WAV、OGG，适配不同平台
- **n8n 自动化**：Webhook 触发 → 音乐生成 → 结果推送

## 文件结构

```
ai-music-generation-automation/
├── SKILL.md                    ← 本文件
├── README.md                   ← 详细文档
├── configs/
│   ├── generator_config.json   ← 生成器配置
│   └── style_presets.json      ← 风格预设
├── generators/
│   ├── music_generator.py       ← 主生成器
│   ├── audio_mixer.py           ← 混音处理器
│   └── format_converter.py      ← 格式转换
├── prompts/
│   └── music_prompt_templates.md ← Prompt 模板库
├── n8n_workflow.json           ← n8n 工作流
└── examples/
    ├── ambient_bg.py           ← 氛围 BGM 示例
    └── corporate_jingle.py      ← 企业宣传片配乐
```

## 快速使用

### 基本生成

```python
from generators.music_generator import MusicGenerator

gen = MusicGenerator(
    provider="udio",        # udio / suno / musicgen
    api_key=os.getenv("UDIO_API_KEY")
)

result = gen.generate(
    prompt="Cinematic ambient, slow pad synth, 70 BPM, melancholic piano, film score",
    duration=30,            # 秒
    style="cinematic",
    output_format="mp3",
    filename="/tmp/bgm_cinematic.mp3"
)

print(result.audio_url)    # 生成的音乐 URL
print(result.duration)     # 时长
print(result.waveform)     # 波形数据（用于可视化）
```

### 带情绪控制的生成

```python
result = gen.generate_with_mood(
    description="一个轻松的科技产品发布会开场音乐",
    mood="energetic",       # calm / energetic / emotional / corporate
    genre="electronic",
    instruments=["synth", "drums", "bass"],
    bpm=120,
    duration=45
)
```

### 自动混音 + 格式转换

```python
from generators.audio_mixer import AudioMixer
from generators.format_converter import FormatConverter

mixer = AudioMixer()

# 混音处理
mixed = mixer.mix(
    input_file="/tmp/raw_music.wav",
    output_file="/tmp/mixed_bgm.mp3",
    fade_in=2.0,           # 淡入 2 秒
    fade_out=3.0,          # 淡出 3 秒
    normalize=True,        # 音量归一化
    bitrate="320k"
)

# 多格式输出
converter = FormatConverter()
converter.convert(
    input="/tmp/mixed_bgm.mp3",
    outputs=["mp3_320", "mp3_128", "wav", "ogg"]
)
```

## Prompt 模板

| 场景 | Prompt 示例 |
|------|------------|
| 短视频 BGM | `Upbeat pop, catchy melody, 120 BPM, acoustic guitar, happy vibes` |
| 科技发布会 | `Electronic ambient, synth pads, 90 BPM, futuristic, corporate` |
| 游戏战斗 | `Epic orchestral, fast tempo, 160 BPM, drums, strings, intense` |
| 冥想/瑜伽 | `Ambient drone, nature sounds, 60 BPM, peaceful, minimal` |
| 品牌广告 | `Cinematic, emotional piano, 80 BPM, uplifting, inspiring` |
| 恐怖氛围 | `Dark ambient, low drone, eerie, 40 BPM, tension` |

## 风格预设

```json
{
  "presets": {
    "corporate": {
      "genre": "electronic",
      "mood": "professional",
      "bpm_range": [90, 110],
      "instruments": ["piano", "synth", "soft_drums"],
      "description": "专业商务风格，适合企业宣传"
    },
    "cinematic": {
      "genre": "orchestral",
      "mood": "epic",
      "bpm_range": [70, 100],
      "instruments": ["strings", "brass", "piano", "drums"],
      "description": "电影配乐风格，戏剧性强"
    },
    "lofi": {
      "genre": "lofi",
      "mood": "relaxed",
      "bpm_range": [70, 90],
      "instruments": ["piano", "vinyl", "drums"],
      "description": "Lo-Fi 风格，适合学习/工作背景"
    },
    "electronic": {
      "genre": "electronic",
      "mood": "energetic",
      "bpm_range": [120, 140],
      "instruments": ["synth", "bass", "drums"],
      "description": "电子舞曲风格，节奏强劲"
    }
  }
}
```

## n8n 工作流

```
内容需求（Webhook）
    ↓
AI 音乐生成（Udio/Suno API）
    ↓
自动混音（音量均衡 + 淡入淡出）
    ↓
多格式转换（MP3/WAV/OGG）
    ↓
上传至云存储（AWS S3 / Cloudflare R2）
    ↓
推送下载链接（Slack/Email）
```

## 提供商对比

| 提供商 | 优点 | 限制 | API |
|--------|------|------|-----|
| Udio | 高质量、多语言 | 需要申请 | udio.ai |
| Suno | 完整歌曲生成 | 需要积分 | api.suno.ai |
| MusicGen | 开源可自部署 | 需要 GPU | Meta 模型 |
| Riffusion | 实时生成 | 质量一般 | riffusion.com |

## 与其他技能的关系

- `video-automation`：视频自动化使用本技能生成 BGM
- `voice-ai-automation`：配音 + 背景音乐组合
- `content-promoter`：推广内容自动配上音乐

---

*版本 1.0 | 适用于 agent-studio*
