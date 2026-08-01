# AI Avatar Animation Automation

> 将文本/语音转换为逼真的 AI 数字人动画，支持 D-ID、HeyGen、Synthesia、Live2D

## 概述

AI Avatar 自动化技能可以将脚本转化为数字人视频，覆盖从文案到交付的全流程。适用于营销视频、客服数字人、培训教程等场景。

## 核心能力

- **文本 → 数字人视频**：输入文案，生成带数字人的视频
- **多平台支持**：D-ID、HeyGen、Synthesia、Live2D
- **多语言配音**：DeepL / Google TTS 语音合成
- **背景/服装定制**：API 控制数字人外观
- **Webhook 回调**：完成后自动通知

## 适用场景

- 产品介绍视频自动化
- AI 客服数字人
- 内部培训视频批量生成
- 社交媒体数字人内容

## 工作流 (n8n)

```json
// integrations/ai-avatar-animation-automation/avatar-pipeline.json
// 节点: Manual Trigger → LLM Script Generator → TTS → Avatar Generator (D-ID API) → Slack Notify
```

## 配置

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `avatar_provider` | D-ID / HeyGen / Synthesia / Live2D | D-ID |
| `voice_language` | zh-CN / en-US / ja-JP | zh-CN |
| `video_resolution` | 720p / 1080p / 4K | 1080p |

## 开始使用

1. 在 D-ID / HeyGen / Synthesia 获取 API Key
2. 导入 `integrations/ai-avatar-animation-automation/avatar-pipeline.json` 到 n8n
3. 配置环境变量：DID_API_KEY, ELEVENLABS_API_KEY, SLACK_CHANNEL
4. 修改 Trigger 输入文案并运行

## 依赖

- OpenAI API（脚本生成）
- ElevenLabs / Google Cloud TTS（语音）
- D-ID / HeyGen / Synthesia API（视频生成）
- n8n workflow

## 相关技能

- `video-automation`：视频生成与剪辑
- `voice-ai-automation`：语音合成与识别

---

*版本 1.0 | 2026-08-01*
