import chromadb
from sentence_transformers import SentenceTransformer
import os

# ============ 配置 ============
PERSIST_DIR = r"D:\game-glossary-rag\game-glossary-rag\chroma_db"
COLLECTION_NAME = "game_glossary"
EMBED_MODEL = r"D:\game-glossary-rag\game-glossary-rag\models\paraphrase-multilingual-MiniLM-L12-v2"
# ==============================

def main():
    # 完全离线
    os.environ['HF_HUB_OFFLINE'] = '1'
    
    os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
    
    # 加载本地模型（只加载一次）
    print("📥 加载嵌入模型...")
    embedder = SentenceTransformer(EMBED_MODEL)
    print("✅ 模型加载完成")
    
    client = chromadb.PersistentClient(path=PERSIST_DIR)
    collection = client.get_collection(COLLECTION_NAME)
    
    count = collection.count()
    print(f"🎮 游戏术语库 RAG - 交互查询")
    print(f"📊 当前库中有 {count} 条术语")
    print("=" * 50)
    print("输入 'quit' 退出")
    print("输入 'help' 查看示例查询")
    print()
    
    while True:
        q = input("查询> ").strip()
        
        if q.lower() == 'quit':
            print("👋 再见！")
            break
        
        if q.lower() == 'help':
            print("示例:")
            print("  Prime 的点燃时长")
            print("  移动速度 buff")
            print("  暴击伤害")
            print("  Super Snail 战斗数值")
            print()
            continue
        
        if not q:
            continue
        
        # 手动编码查询文本
        query_embedding = embedder.encode([q])
        
        # 检索（传向量，不传文本！）
        results = collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=3,
            include=['documents', 'metadatas', 'distances']
        )
        
        docs = results['documents'][0]
        metadatas = results['metadatas'][0]
        distances = results['distances'][0]
        
        if not docs:
            print("❌ 没找到相关内容，试试换个说法？\n")
            continue
        
        print(f"\n🎯 找到 {len(docs)} 条结果:\n")
        for i, (doc, meta, dist) in enumerate(zip(docs, metadatas, distances), 1):
            similarity = 1 - dist  # 距离越小越相似
            print(f"{i}. 【{meta['term_key']}】({meta['game']} / {meta['category']})")
            print(f"   相似度: {similarity:.2%}")
            print(f"   {doc[:200]}...")
            print()
        
        print("-" * 50)

if __name__ == "__main__":
    main()