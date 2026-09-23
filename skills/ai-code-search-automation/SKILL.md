# AI Code Search Automation

> Semantic code search powered by embeddings + LLM re-ranking. Find code by intent, not just keywords.

## What It Does

Natural language → semantic code search across repositories, with LLM-powered ranking and explanation.

## Core Capabilities

- **Semantic Search**: Embed query and code files; cosine similarity match
- **Multi-repo Support**: Index local repos, GitHub repos, or package registries
- **LLM Re-ranking**: Use LLM to score relevance of top-k candidates
- **Code Explanation**: LLM explains why each result matches the query
- **Context Window**: Return matches with surrounding context (configurable lines)

## Supported Embedding Models

- OpenAI 
- Ollama local embeddings ()
- Voyage AI ()

## Usage



## n8n Workflow Included



## Prompt Template

```
Query: {user_query}
Top results: {results}
Explain why each result is relevant to the query.
``'

## Related Skills

- ai-code-explainer-automation
- rag-knowledge-base
- mcp-integration
