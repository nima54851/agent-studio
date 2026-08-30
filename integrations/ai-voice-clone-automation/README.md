# 🎙️ AI Voice Clone Automation — Integration

n8n 工作流集合，用于 AI 声音克隆 + TTS 自动化。

## 📦 包含工作流

| 工作流 | 功能 | 触发方式 |
|--------|------|---------|
| `n8n-voice-clone-workflow.json` | 声音克隆 + TTS 生成 | Webhook |
| `n8n-brand-voice-manager.json` | 品牌音色库管理 + 版本控制 | Webhook |
| `n8n-batch-tts-pipeline.json` | 批量 TTS 生成（长文本分片） | Schedule |

## 导入方法

1. n8n → **Import from File**
2. 选择工作流 JSON
3. 配置凭证（ElevenLabs API Key / Coqui 模型路径）
4. Activate

## API 调用示例

### 声音克隆 + TTS
```bash
curl -X POST https://your-n8n.com/webhook/voice-clone \
  -H "Content-Type: application/json" \
  -d '{
    "source_audio_base64": "'"$(base64 -w0 voice.wav)"'",
    "text": "您好，欢迎致电客服中心",
    "emotion": "warm",
    "language": "zh"
  }'
```

### 批量 TTS（文件列表）
```bash
curl -X POST https://your-n8n.com/webhook/batch-tts \
  -H "Content-Type: application/json" \
  -d '{
    "texts_file": "texts.txt",
    "voice_id": "brand_voice_v2",
    "output_format": "wav"
  }'
```

## 环境变量

```
ELEVENLABS_API_KEY=sk_xxxxxxxxxxxxx
ELEVENLABS_API_URL=https://api.elevenlabs.io
COQUI_MODEL_PATH=./models/xtts_v2
OUTPUT_DIR=./audio_output
DEFAULT_LANGUAGE=zh
DEFAULT_EMOTION=warm
```

## 适用场景
- 🏢 企业 IVR 语音（自动客服接听）
- 🎙️ 品牌播客 / 有声内容批量生产
- 📚 有声书 / 在线教育配音
- 🤖 AI Agent 语音交互
- 📢 品牌宣传广告配音

## 自托管方案（替代 ElevenLabs）

如需自托管，使用 Coqui XTTS v2：
```python
from TTS.api import TTS
tts = TTS(model_name="xtts_v2", gpu=True)
tts.tts_to_file(
    text="欢迎致电客服中心",
    speaker_wav="my_voice.wav",
    file_path="output.wav"
)
```

---
*克隆你的声音，规模化品牌影响力*
