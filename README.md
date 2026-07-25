# 🎮 Game Glossary RAG

A fully offline RAG (Retrieval-Augmented Generation) system for game terminology lookup, built for localization PMs and translators.

Solves the classic pain point: players say "皇子" but your glossary only has "Jarvan IV". Traditional keyword search fails on aliases, slang, and parameterized strings like `Duration of Burning +{i18n0}%`. This system understands semantics and preserves formatting.

![demo](demo.gif)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Semantic Search** | Find terms by meaning, not just exact keywords. "Prime 的点燃时长" → matches "Duration of Burning inflicted by Prime" |
| **Cross-Lingual** | Query in Chinese, get English results (and vice versa). Powered by multilingual embeddings |
| **Placeholder-Safe** | `{i18n0}`, `{value}%` and other game string parameters are preserved intact |
| **Fully Offline** | No API calls, no cloud dependency. Runs entirely on local hardware |
| **Sub-10s Indexing** | 6 terms indexed in seconds. Scales to thousands without breaking a sweat |
| **Interactive CLI** | Clean query interface with similarity scores |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+ (tested on 3.14)
- ~500MB disk space for the embedding model

### Installation