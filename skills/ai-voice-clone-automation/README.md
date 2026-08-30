# 🎙️ AI Voice Clone Automation

AI 声音克隆 + TTS 自动化技能包：5秒音频克隆音色，支持多语言、情感控制、批量生成，适用客服、播客、品牌语音场景。

## 📦 包含内容

- **SKILL.md** — 技能定义与使用说明
- **n8n-voice-clone-workflow.json** — 声音克隆 + TTS n8n 工作流
- **n8n-brand-voice-manager.json** — 品牌音色库管理 + 版本控制工作流
- **n8n-batch-tts-pipeline.json** — 批量 TTS 生成管道（长文本自动分片）
- **scripts/voice_clone.py** — 声音克隆主脚本（Coqui/Tacotron2）
- **scripts/batch_tts.py** — 批量 TTS 生成（支持 FFmpeg 分片）
- **scripts/voice_brand_manager.py** — 品牌音色管理器
- **scripts/audio_post_processor.py** — 音频后处理（降噪、标准化、混音）
- **.env.example** — 环境变量模板

## 🚀 快速开始

### 声音克隆
```bash
pip install TTS pydub openai elevenlabs
python3 scripts/voice_clone.py \
  --source=my_voice.wav \
  --text="您好，欢迎致电客服中心" \
  --emotion=warm \
  --output=output.wav
```

### 批量 TTS
```bash
# texts.txt: 每行一段文本
python3 scripts/batch_tts.py \
  --file=texts.txt \
  --voice=brand_v2 \
  --output_dir=./audio_output \
  --parallel=4
```

### n8n 工作流
1. n8n → Import → 选择 `n8n-voice-clone-workflow.json`
2. 配置 ElevenLabs / Coqui API Key
3. 设置 Webhook 触发
4. Activate

## 功能详情

### 声音克隆
- 输入：5-30秒清晰人声（WAV/MP3）
- 支持：中文、英文、日语、韩语、西班牙语等 30+ 语言
- 输出：克隆音色 WAV/MP3，22.05kHz/44.1kHz 可选

### 情感控制
| 情感 | 适用场景 | 参数 |
|------|---------|------|
| warm / 温暖 | 客服、品牌宣传 | `emotion="warm"` |
| excited / 兴奋 | 促销、活动 | `emotion="excited"` |
| calm / 平静 | 有声书、冥想 | `emotion="calm"` |
| serious / 严肃 | 通知、公告 | `emotion="serious"` |

### 品牌音色管理
```python
from voice_brand_manager import BrandVoiceManager

manager = BrandVoiceManager("/data/brand_voices")
manager.register("brand_v2", "voice_model_v2.pt", description="品牌音色 v2")
manager.set_active("brand_v2")  # 全局默认
voices = manager.list_voices()  # 查看所有音色
```

### 批量生成管道
- 自动将长文本（>500字）分片
- 并发生成（可配置并发数）
- FFmpeg 合并 + 添加静音间隔
- 输出格式：WAV、MP3、AAC

## 适用场景
- 🏢 企业客服语音（IVR、自动接听）
- 🎙️ 品牌播客 / 有声内容
- 📚 有声书 / 在线教育
- 📢 品牌宣传 / 广告配音
- 🤖 AI Agent 语音交互

## API 集成
- **ElevenLabs API** — 高质量商业级 TTS
- **Coqui / XTTS** — 开源自托管克隆方案
- **Fish-Speech** — 国产开源中文克隆

## 配置
```bash
# .env
ELEVENLABS_API_KEY=sk_xxx
COQUI_MODEL_PATH=./models/xtts_v2
OUTPUT_FORMAT=wav
SAMPLE_RATE=22050
```

---
*克隆你的声音，规模化你的品牌*
