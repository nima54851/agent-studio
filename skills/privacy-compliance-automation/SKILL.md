# Privacy Compliance Automation

隐私合规自动化技能——GDPR/CCPA/PIPEDA/数据本地化一站式合规方案。

## 🎯 功能

- **数据发现与分类**：自动扫描用户数据、敏感字段（PII/金融/医疗）
- **同意管理（Consent Management）**：Cookie Banner、同意记录、随时撤回
- **数据主体权利（DSR）**：访问/删除/导出请求自动处理管道
- **数据保护影响评估（DPIA）**：自动生成隐私影响报告
- **违规检测与报告**：实时监控、72h 违规通知模板

## 🛠️ 核心框架

| 框架 | 用途 |
|---|---|
| OneTrust | 企业级隐私合规管理平台 |
| Cookiebot | Cookie 同意管理 |
| Osano | 同意管理 CMP |
| TrustArc | 隐私合规工作流 |
| Fides | 开源隐私工程框架 |

## 📁 目录结构

```
privacy-compliance-automation/
├── SKILL.md                  # 本文件
├── README.md                 # 详细文档
├── n8n-privacy-workflow.json # n8n workflow
└── scripts/
    ├── pii_scanner.py        # PII 扫描器
    ├── dsr_processor.py      # DSR 请求处理器
    └── dpia_generator.py     # DPIA 报告生成器
```

## 🔧 使用方式

```bash
# 扫描项目 PII
python3 scripts/pii_scanner.py --path ./data

# 处理 GDPR 删除请求
python3 scripts/dsr_processor.py --request-id <id> --action delete

# 生成 DPIA 报告
python3 scripts/dpia_generator.py --project <name> --output dpia.pdf
```

## 🔗 集成

- **n8n**: `n8n-privacy-workflow.json` 包含完整合规管道
- **OpenClaw MCP**: 合规检查自动化调用

## ⚖️ 支持的法规

- GDPR（欧盟）
- CCPA（加州）
- PIPEDA（加拿大）
- LGPD（巴西）
- 中国《个人信息保护法》（PIPL）
- 日本 APPI

---

*版本 1.0 | 2026-07-26*
