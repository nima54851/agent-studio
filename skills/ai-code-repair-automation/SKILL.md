# AI Code Repair Automation

AI 自动代码修复系统 — 静态分析 → LLM 修复 → 回归测试 → 自动提交 PR。

## 功能
- 静态分析：PyLint / ESLint / Go vet
- LLM 修复：自动生成修复补丁
- 回归测试：pytest / jest 自动跑
- 自动 PR：GitHub API 提交修复 PR
- n8n 流水线：完整自动化工作流

## 工具
- `n8n workflow`: `ai-code-repair-pipeline.json`
- `scripts/static_analyzer.py`: 静态分析
- `scripts/llm_fixer.py`: LLM 修复生成
- `scripts/autopatch.py`: 自动打补丁
- `prompts/code-repair-prompt.md`: 修复提示词

## 流程
```
代码扫描 → 问题识别 → LLM 生成修复 → 验证测试 → PR 提交
```

## 示例
```bash
python scripts/llm_fixer.py --file src/main.py --rule E501,W0612
python scripts/autopatch.py --dry-run  # 预览修复
python scripts/autopatch.py --apply     # 应用修复
```
