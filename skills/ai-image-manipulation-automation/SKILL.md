# AI Image Manipulation Automation

> 基于 Replicate / Adobe Firefly / Pillow 的 AI 图片处理：风格迁移、修复、扩图、OCR、抠图

## 概述

自动化图片处理流水线，支持 AI 风格迁移、智能修复、背景移除、OCR 识别、批量处理。

## 核心能力

- **风格迁移**：梵高/毕加索/浮世绘/赛博朋克等艺术风格
- **智能修复**：Inpainting / Outpainting，移除/添加物体
- **背景处理**：背景移除、背景生成、背景替换
- **图像放大**：AI 超分辨率（Real-ESRGAN / SwinIR）
- **OCR 识别**：图片文字提取，支持多语言
- **批量处理**：CSV/JSON 批量输入，批量输出

## 平台支持

| 平台 | 能力 | 备注 |
|------|------|------|
| Replicate | SDXL, ControlNet, Firefly | 模型丰富，按量计费 |
| Adobe Firefly | 生成式填充，文字特效 | 企业级质量 |
| Pillow | 基础处理，OCR | 免费，本地运行 |

## 工作流

```json
// integrations/ai-image-manipulation-automation/image-pipeline.json
// 节点: Cloud Storage Watcher → Pre-process (Sharp) → Replicate API → Post-process (compress) → S3 Upload
```

## 配置

| 参数 | 说明 |
|------|------|
| `REPLICATE_API_KEY` | Replicate API Key |
| `IMAGE_INPUT_DIR` | 监控文件夹 |
| `S3_BUCKET` | S3 桶名 |
| `DEFAULT_IMAGE_PROMPT` | 默认提示词 |

## 开始使用

1. 获取 Replicate API Key: https://replicate.com/account/api-tokens
2. 导入 `integrations/ai-image-manipulation-automation/image-pipeline.json`
3. 配置源存储和 S3 凭证
4. 运行工作流

## 相关技能

- `image-generation-automation`：AI 图片生成
- `browser-automation`：网页截图处理

---

*版本 1.0 | 2026-08-01*
