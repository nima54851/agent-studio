# Prompt Engineering Automation

自动优化 AI Prompt：版本管理、A/B 测试、Chain-of-Thought 模板、热词注入、成本分析。

## 核心能力
- **版本控制**：像 Git 一样管理 Prompt 演化历史
- **A/B 测试**：自动对比不同 Prompt 效果并打分
- **Chain-of-Thought**：自动注入思维链模板提升推理质量
- **热词注入**：动态插入系统指令优化输出格式
- **成本分析**：Token 消耗追踪与优化建议

## 适用场景
- 大量使用 LLM API 的产品
- 需要持续优化 Prompt 效果的团队
- Prompt 版本迭代频繁的项目

## 快速开始
1. 将 `prompts/` 目录放入项目
2. 运行 `scripts/prompt_optimizer.py analyze` 分析当前 Prompt
3. 使用 `scripts/prompt_optimizer.py ab-test` 启动 A/B 测试
