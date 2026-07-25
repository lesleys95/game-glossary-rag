import os
os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

# ============ 配置 ============
CSV_PATH = r"D:\game-glossary-rag\game-glossary-rag\data\sample\sample_terms.csv"
PERSIST_DIR = r"D:\game-glossary-rag\game-glossary-rag\chroma_db"
COLLECTION_NAME = "game_glossary"
EMBED_MODEL = r"D:\game-glossary-rag\game-glossary-rag\models\paraphrase-multilingual-MiniLM-L12-v2"
# ==============================


def load_and_clean(csv_path):
    """加载并清洗术语库"""
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    print(f"📋 CSV 列名: {list(df.columns)}")
    
    # 删掉中英文任一为空的行
    df = df.dropna(subset=['zh_cn', 'en_us'])
    # 去重
    df = df.drop_duplicates(subset=['term_key'])
    # 别名转列表
    if 'aliases' in df.columns:
        df['alias_list'] = df['aliases'].fillna('').apply(
            lambda x: [a.strip() for a in str(x).split(',') if a.strip()]
        )
    else:
        df['alias_list'] = [[] for _ in range(len(df))]
    
    print(f"✅ 加载了 {len(df)} 条术语")
    return df


def term_to_chunk(row):
    """一条术语 = 一个 chunk"""
    parts = [
        f"Key: {row['term_key']}",
        f"中文: {row['zh_cn']}",
        f"English: {row['en_us']}",
        f"分类: {row['category']}",
        f"所属游戏: {row['game']}"
    ]
    if pd.notna(row.get('variables')) and row['variables']:
        parts.append(f"变量: {row['variables']}")
    
    text = '\n'.join(parts)
    metadata = {
        'term_key': row['term_key'],
        'game': row['game'],
        'category': row['category'],
        'variables': row['variables'] if pd.notna(row.get('variables')) else ''
    }
    return text, metadata


def build_vector_store(df):
    """向量化并存入 ChromaDB"""
    client = chromadb.PersistentClient(path=PERSIST_DIR)
    
    # 如果集合已存在则删除重建
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"🗑️ 已删除旧集合 {COLLECTION_NAME}")
    except:
        pass
    
    collection = client.create_collection(COLLECTION_NAME)
    
    # 加载嵌入模型（本地，离线）
    print(f"📥 加载嵌入模型...")
    embedder = SentenceTransformer(EMBED_MODEL)
    print(f"✅ 模型加载完成")
    
    texts, metadatas, ids = [], [], []
    for i, (_, row) in enumerate(df.iterrows()):
        text, metadata = term_to_chunk(row)
        texts.append(text)
        metadatas.append(metadata)
        ids.append(f"term_{i}")
    
    print(f"🔄 向量化 {len(texts)} 条术语...")
    embeddings = embedder.encode(texts, show_progress_bar=True)
    
    collection.add(
        embeddings=embeddings.tolist(),
        documents=texts,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"✅ 成功入库 {len(texts)} 条术语到 ChromaDB")
    print(f"📁 数据库位置: {os.path.abspath(PERSIST_DIR)}")
    
    # 测试检索（手动编码，避免 Chroma 偷跑）
    print("\n🧪 测试检索 'Prime 的点燃时长':")
    query_embedding = embedder.encode(["Prime 的点燃时长"])
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=1
    )
    doc = results['documents'][0][0]
    meta = results['metadatas'][0][0]
    print(f"结果:\n{doc[:300]}...")
    print(f"✅ 命中: {meta['term_key']}")
    
    return collection


def main():
    print("🎮 游戏术语库 RAG - 向量入库工具")
    print("=" * 50)
    
    df = load_and_clean(CSV_PATH)
    collection = build_vector_store(df)
    
    print("\n🎉 全部完成！可以运行 query.py 开始检索了")


if __name__ == "__main__":
    main()