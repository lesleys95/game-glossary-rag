import os
import time

# 强制走国内镜像
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
# 延长超时时间，避免 WinError 10060
os.environ['HF_HUB_DOWNLOAD_TIMEOUT'] = '60'

from huggingface_hub import snapshot_download
from pathlib import Path

MODEL_ID = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
LOCAL_DIR = r"D:\game-glossary-rag\game-glossary-rag\models\paraphrase-multilingual-MiniLM-L12-v2"

Path(LOCAL_DIR).parent.mkdir(parents=True, exist_ok=True)

print(f"📥 开始下载模型到: {LOCAL_DIR}")
print(f"🌐 使用镜像: {os.environ['HF_ENDPOINT']}")

max_retry = 5
for attempt in range(max_retry):
    try:
        path = snapshot_download(
            repo_id=MODEL_ID,
            local_dir=LOCAL_DIR
        )
        print(f"\n✅ 模型下载完成: {path}")
        print("🎉 可以运行 python embed_store.py 了！")
        break
    except Exception as e:
        print(f"\n⚠️ 第 {attempt+1} 次尝试失败: {e}")
        if attempt < max_retry - 1:
            wait = 3 * (attempt + 1)
            print(f"⏳ {wait} 秒后重试...")
            time.sleep(wait)
        else:
            print("\n❌ 5 次重试都失败了，建议使用方案2（手动下载）")