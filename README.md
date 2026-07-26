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
bash
Clone the repo
git clone https://github.com/lesleys95/game-glossary-rag.git
cd game-glossary-rag
Install dependencies
python -m pip install -r requirements.txt
> **Note**: If you encounter encoding issues on Windows, ensure your terminal uses UTF-8:
> ```cmd
> chcp 65001
> ```

---

### Model Setup (Important for China-based users)

The embedding model (`paraphrase-multilingual-MiniLM-L12-v2`) must be downloaded manually due to network restrictions:

#### Option 1: Download via mirror (Recommended)
cmd
set HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 --local-dir ./models/paraphrase-multilingual-MiniLM-L12-v2
#### Option 2: Manual download
1. Visit [hf-mirror.com/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2](https://hf-mirror.com/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)
2. Download these files:
   - `pytorch_model.bin` (~471MB)
   - `sentencepiece.bpe.model`
   - `tokenizer.json`
   - `config.json`, `tokenizer_config.json`, `special_tokens_map.json`
3. Place them in `models/paraphrase-multilingual-MiniLM-L12-v2/`

Verify your structure:
game-glossary-rag/
└── models/
└── paraphrase-multilingual-MiniLM-L12-v2/
├── pytorch_model.bin
├── sentencepiece.bpe.model
├── tokenizer.json
└── ... (other config files)
---

### Build the Vector Store
bash
cmd
cd src
python embed_store.py
*Expected output:*
text
🎮 游戏术语库 RAG - 向量入库工具 📋
✅ 加载了 6 条术语
🗑️ 已删除旧集合 game_glossary
🧠 加载嵌入模型...
✅ 模型加载完成
🔄 向量化 6 条术语... 100%
📁 数据库位置: D:\game-glossary-rag\game-glossary-rag\chroma_db
🧪 测试检索 'Prime 的点燃时长': 结果: Key: prime_burning_duration ...
---

### Start Querying
bash
cmd
python query.py
*Example session:*
text
🎮 游戏术语库 RAG - 交互查询 📊
当前库中有 6 条术语
输入 'quit' 退出 输入 'help' 查看示例查询
查询> Prime 点燃
🎯 找到 3 条结果:
【prime_burning_duration】(Super Snail / 战斗数值) 相似度: 87.42%
中文: 战技附加的点燃时长+{i18n0}%
English: Duration of Burning inflicted by Prime +{i18n0}%
---

## 📊 Example Queries

| Query | What You Get |
|-------|-------------|
| `Prime 的点燃时长` | `战技附加的点燃时长+{i18n0}%` |
| `暴击伤害` | `暴击伤害提高{i18n0}%` |
| `移动速度 buff` | `移动速度提升{i18n0}%，持续{i18n1}秒` |
| `burning duration` | `Duration of Burning inflicted by Prime +{i18n0}%` |
| `药水掉落` | `药水掉落率+i18n0%` |
| `potion drop rate` | `Potion drop rate +{i18n0}%` |

---

## 🏗️ Architecture

mermaid
graph LR
    A[User Query: "Prime 点燃"] --> B(query.py);
    B --> C{Encode query};
    C --> D[Embedding Model];
    D --> E[Vector search in ChromaDB];
    F[sample_terms.csv] --> G(embed_store.py);
    G --> E;
    E --> H(Return Results);
    H --> B;
---

## 🛠️ Tech Stack

| Component | Choice | Why |
|-----------|--------|-----|
| **Vector DB** | [ChromaDB](https://www.trychroma.com/) | Lightweight, persistent, zero-config |
| **Embedding Model** | [paraphrase-multilingual-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2) | 384-dim, 50+ languages, fast inference |
| **Data Processing** | Pandas | CSV handling, cleaning pipelines |
| **Tokenization** | Jieba | Chinese word segmentation |
| **Runtime** | Python 3.14 | Latest stable |

---

## 📁 Project Structure
game-glossary-rag/
├── .gitignore # Excludes chroma_db/, models/, venv/
├── README.md # You're reading it
├── demo.gif # Demo animation
├── requirements.txt # Dependency list
│
├── data/
│ └── sample/
│ └── sample_terms.csv # Sample glossary (6 terms)
│
├── src/
│ ├── embed_store.py # Vector indexing pipeline
│ ├── query.py # Interactive query CLI
│ └── download_model.py # Helper script for model download
│
├── models/ # ⚠️ gitignored, download separately
│ └── paraphrase-multilingual-MiniLM-L12-v2/
│
└── chroma_db/ # ⚠️ gitignored, auto-generated
---

## ➕ Adding Your Own Terms

1. Create a new CSV file in `data/raw/`:
csv
term_key,zh_cn,en_us,category,game,variables
my_new_term,中文翻译,English Translation,UI文本,My Game,i18n0
2. Update `CSV_PATH` in `embed_store.py`:
python
CSV_PATH = r"D:\game-glossary-rag\game-glossary-rag\data\raw\your_terms.csv"
3. Rebuild:
cmd
python embed_store.py
---

## 📋 requirements.txt

Create this file in the project root:
txt
chromadb>=0.4.0
sentence-transformers>=2.2.0
rank-bm25>=0.2.0
jieba>=0.42.0
pandas>=2.0.0
huggingface-hub>=0.20.0
Install with:
cmd
python -m pip install -r requirements.txt
---

## 🎯 Use Cases

| Role | How This Helps |
|------|---------------|
| **Localization PM** | Verify translation consistency across patches. Answer stakeholder questions instantly. |
| **Translator** | Look up official terminology while working. Understand context via similar matches. |
| **QA Tester** | Validate in-game text against approved glossary. Catch drift early. |
| **Game Dev** | Plug this into a chatbot or help system. Provide contextual terminology explanations to players. |

---

## 🐛 Troubleshooting

### `ModuleNotFoundError: No module named 'pandas'`
cmd
python -m pip install pandas
### `UnicodeDecodeError` when reading CSV
Ensure your CSV is saved as UTF-8 (not ANSI/GBK):
- Notepad → Save As → Encoding: UTF-8
- Or use VS Code (recommended)

### `ConnectTimeout` when downloading model
Use the mirror approach documented above. Or download manually via browser.

### `httpx.ReadTimeout` during query
This means ChromaDB tried to download its default ONNX model. Ensure `HF_HUB_OFFLINE=1` is set in both `embed_store.py` and `query.py`.

### `IndentationError` in embed_store.py
Check that all code blocks align properly. The provided code in this repo is pre-validated.

---

## 🚧 Roadmap

- [ ] BM25 + Vector hybrid re-ranking
- [ ] BGE re-ranker integration
- [ ] Web UI (Gradio/Streamlit)
- [ ] Batch CSV import with validation
- [ ] Export to TMX/XLIFF for CAT tool integration
- [ ] Support for multi-variable extraction from `{i18nN}` patterns
- [ ] Fuzzy matching fallback for typo tolerance

---

## 🤝 Contributing

Found a bug? Have an idea? PRs welcome!

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License - feel free to use this in your own projects.

---

## 👋 About

Built by a game localization professional who got tired of manually looking up terms every time a stakeholder asked "what's the official translation for X?"

If you're a localization PM, translator, or QA tester in the games industry, this tool was made for you.

**Questions?** Open an issue or reach out on [LinkedIn](#).

---

⭐ **Star this repo if it helped you!** ⭐

