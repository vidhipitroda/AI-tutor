"""
download_langchain_openai_docs.py
----------------------------------
Downloads LangChain docs directly from GitHub raw (langchain-ai/docs repo)
and saves them as .txt files in Data/LangChain_OpenAI_Docs/

Source: https://docs.langchain.com/oss/python/langchain/overview
GitHub: https://github.com/langchain-ai/docs/tree/main/src/oss/langchain
"""

import os
import time
import requests

DOCS_DIR = "/Users/vidhipitroda/Desktop/Projects/AI tutor/Data/LangChain_OpenAI_Docs"
os.makedirs(DOCS_DIR, exist_ok=True)

RAW_BASE = "https://raw.githubusercontent.com/langchain-ai/docs/main/src/oss/langchain"
HEADERS  = {"User-Agent": "AITutor/1.0"}

# name → filename in the repo (all .mdx)
LANGCHAIN_DOCS = {
    # Core concepts
    "langchain_overview":               "overview.mdx",
    "langchain_quickstart":             "quickstart.mdx",
    "langchain_agents":                 "agents.mdx",
    "langchain_rag":                    "rag.mdx",
    "langchain_retrieval":              "retrieval.mdx",
    "langchain_knowledge_base":         "knowledge-base.mdx",
    "langchain_models":                 "models.mdx",
    "langchain_tools":                  "tools.mdx",
    "langchain_messages":               "messages.mdx",
    "langchain_streaming":              "streaming.mdx",
    "langchain_structured_output":      "structured-output.mdx",
    "langchain_memory_short_term":      "short-term-memory.mdx",
    "langchain_memory_long_term":       "long-term-memory.mdx",
    "langchain_context_engineering":    "context-engineering.mdx",
    "langchain_component_architecture": "component-architecture.mdx",
    "langchain_mcp":                    "mcp.mdx",
    "langchain_guardrails":             "guardrails.mdx",
    "langchain_human_in_the_loop":      "human-in-the-loop.mdx",
    "langchain_observability":          "observability.mdx",
    "langchain_sql_agent":              "sql-agent.mdx",
    "langchain_install":                "install.mdx",
}


def download_doc(name: str, filename: str) -> bool:
    url      = f"{RAW_BASE}/{filename}"
    out_path = os.path.join(DOCS_DIR, f"{name}.txt")

    if os.path.exists(out_path):
        print(f"   ⏭️  Already downloaded: {name}.txt")
        return True

    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        text = r.text

        if len(text) < 200:
            print(f"   ⚠️  Too short: {name}")
            return False

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"SOURCE: https://docs.langchain.com/oss/python/langchain/{filename.replace('.mdx','')}\n")
            f.write(f"GITHUB: {url}\n")
            f.write("=" * 60 + "\n\n")
            f.write(text)

        size_kb = os.path.getsize(out_path) // 1024
        print(f"   ✅ {name}.txt  ({size_kb} KB, {len(text):,} chars)")
        return True

    except Exception as e:
        print(f"   ❌ Failed [{name}]: {e}")
        return False


def main():
    print(f"📂 Saving to: {DOCS_DIR}")
    print(f"📋 LangChain docs to download: {len(LANGCHAIN_DOCS)}\n")
    print("🦜 LangChain Docs (from GitHub raw)")
    print("-" * 45)

    success, failed = [], []

    for name, filename in LANGCHAIN_DOCS.items():
        ok = download_doc(name, filename)
        (success if ok else failed).append(name)
        time.sleep(0.3)

    print(f"\n{'='*50}")
    print(f"✅ Downloaded: {len(success)}/{len(LANGCHAIN_DOCS)}")
    if failed:
        print(f"❌ Failed: {', '.join(failed)}")
    print(f"\n📂 Total files in {DOCS_DIR}: {len(os.listdir(DOCS_DIR))}")


if __name__ == "__main__":
    main()

