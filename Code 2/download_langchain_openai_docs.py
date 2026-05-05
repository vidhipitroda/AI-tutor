"""
Download LangChain docs as .txt files.
Fetches raw .mdx from github.com/langchain-ai/docs (avoids JS-rendered site).
Saves to: Data/LangChain_OpenAI_Docs/
"""
import os
import time
import requests

SAVE_DIR = "/Users/vidhipitroda/Desktop/Projects/AI tutor/Data/LangChain_OpenAI_Docs"
os.makedirs(SAVE_DIR, exist_ok=True)

RAW = "https://raw.githubusercontent.com/langchain-ai/langchain/master/docs/docs"

DOCS = [
    ("langchain_overview",               f"{RAW}/introduction.mdx"),
    ("langchain_install",                f"{RAW}/how_to/installation.mdx"),
    ("langchain_quickstart",             f"{RAW}/tutorials/llm_chain.mdx"),
    ("langchain_rag",                    f"{RAW}/tutorials/rag.mdx"),
    ("langchain_retrieval",              f"{RAW}/how_to/vectorstore_retriever.mdx"),
    ("langchain_agents",                 f"{RAW}/tutorials/agents.mdx"),
    ("langchain_tools",                  f"{RAW}/how_to/tools_builtin.mdx"),
    ("langchain_messages",               f"{RAW}/concepts/messages.mdx"),
    ("langchain_models",                 f"{RAW}/concepts/chat_models.mdx"),
    ("langchain_streaming",              f"{RAW}/how_to/streaming.mdx"),
    ("langchain_structured_output",      f"{RAW}/how_to/structured_output.mdx"),
    ("langchain_memory_short_term",      f"{RAW}/how_to/chatbots_memory.mdx"),
    ("langchain_memory_long_term",       f"{RAW}/concepts/memory.mdx"),
    ("langchain_knowledge_base",         f"{RAW}/how_to/chatbots_retrieval.mdx"),
    ("langchain_sql_agent",              f"{RAW}/tutorials/sql_qa.mdx"),
    ("langchain_guardrails",             f"{RAW}/concepts/output_parsers.mdx"),
    ("langchain_human_in_the_loop",      f"{RAW}/concepts/human_in_the_loop.mdx"),
    ("langchain_observability",          f"{RAW}/concepts/tracing.mdx"),
    ("langchain_mcp",                    f"{RAW}/integrations/tools/mcp.mdx"),
    ("langchain_context_engineering",    f"{RAW}/concepts/prompt_templates.mdx"),
    ("langchain_component_architecture", f"{RAW}/concepts/architecture.mdx"),
]

headers = {"User-Agent": "AITutor/1.0"}

print(f"Downloading {len(DOCS)} LangChain doc pages to {SAVE_DIR}/\n")
ok, fail = 0, 0
for i, (name, url) in enumerate(DOCS):
    out_path = os.path.join(SAVE_DIR, f"{name}.txt")
    if os.path.exists(out_path):
        print(f"  [{i+1}/{len(DOCS)}] Already exists: {name}.txt")
        ok += 1
        continue
    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(r.text)
        print(f"  [{i+1}/{len(DOCS)}] OK  {name}.txt  ({len(r.text):,} chars)")
        ok += 1
        time.sleep(0.3)
    except Exception as e:
        print(f"  [{i+1}/{len(DOCS)}] FAIL {name}: {e}")
        fail += 1

print(f"\nDone! {ok} saved, {fail} failed -> {SAVE_DIR}")
