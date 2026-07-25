# Code Search Automation

AI 语义代码搜索：自然语言查询代码库、语义相似度排序、上下文注入、多语言支持。

## 核心能力
- **自然语言搜索**：用中文/英文描述你想找的代码
- **语义排序**：基于代码语义相似度而非关键词匹配
- **上下文注入**：搜索结果自动附带调用链和依赖图
- **多语言支持**：Python/JavaScript/TypeScript/Go/Rust/Java
- **正则增强**：支持 Glob + Regex 混合精确匹配

## 适用场景
- 大型代码库导航
- 代码复用和最佳实践查找
- 遗留代码理解和重构

## 快速开始
1. 索引代码库：`python3 scripts/code_indexer.py index ./`
2. 自然语言搜索：`python3 scripts/code_search.py "如何实现 JWT 验证"`
