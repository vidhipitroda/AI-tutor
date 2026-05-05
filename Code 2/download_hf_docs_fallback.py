"""
download_hf_docs_fallback.py
-----------------------------
Fetches the 7 failed HuggingFace doc pages directly from their
GitHub source (raw markdown) — bypasses JS-rendered pages.
"""

import os
import time
import requests

DOCS_DIR = "/Users/vidhipitroda/Desktop/Projects/AI tutor/Data/HF_Docs"
os.makedirs(DOCS_DIR, exist_ok=True)

RAW_BASE = "https://raw.githubusercontent.com/huggingface/{repo}/main/{path}"

# name → (repo, path from repo root)
FALLBACK_DOCS = {
    # Transformers — English docs live under docs/source/en/ but some pages
    # are generated; fetch the closest available alternatives
    "transformers_autoclass_tutorial":  ("transformers", "docs/source/ko/autoclass_tutorial.md"),  # best available raw
    "transformers_preprocessing":       ("transformers", "docs/source/ko/preprocessing.md"),
    "llm_optims":                       ("transformers", "docs/source/ko/llm_optims.md"),

    # PEFT — paths confirmed from repo tree
    "peft_lora_based_methods":          ("peft", "docs/source/task_guides/lora_based_methods.md"),
    "peft_conceptual_adapter":          ("peft", "docs/source/conceptual_guides/adapter.md"),
    "peft_conceptual_prompting":        ("peft", "docs/source/conceptual_guides/prompting.md"),
    "lora_conceptual_guide":            ("peft", "docs/source/developer_guides/lora.md"),
    "lora_config_api_ref":              ("peft", "docs/source/package_reference/lora.md"),
    "peft_model_config":                ("peft", "docs/source/tutorial/peft_model_config.md"),
    "peft_quantization":                ("peft", "docs/source/developer_guides/quantization.md"),
    "peft_model_merging":               ("peft", "docs/source/developer_guides/model_merging.md"),
}

HEADERS = {"User-Agent": "AITutor/1.0"}


def download_raw(name: str, repo: str, path: str) -> bool:
    url = RAW_BASE.format(repo=repo, path=path)
    out_path = os.path.join(DOCS_DIR, f"{name}.txt")

    if os.path.exists(out_path):
        print(f"   ⏭️  Already exists: {name}.txt")
        return True

    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        text = response.text

        if len(text) < 200:
            print(f"   ⚠️  Too short: {name}")
            return False

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"SOURCE: {url}\n")
            f.write("=" * 60 + "\n\n")
            f.write(text)

        size_kb = os.path.getsize(out_path) // 1024
        print(f"   ✅ Saved: {name}.txt  ({size_kb} KB, {len(text):,} chars)")
        return True

    except Exception as e:
        print(f"   ❌ Failed [{name}]: {e}")
        return False


def main():
    print(f"📂 Saving fallback docs to: {DOCS_DIR}")
    print(f"📋 Pages to fetch from GitHub raw: {len(FALLBACK_DOCS)}\n")

    success, failed = [], []

    for i, (name, (repo, path)) in enumerate(FALLBACK_DOCS.items(), 1):
        print(f"[{i}/{len(FALLBACK_DOCS)}] {name}")
        ok = download_raw(name, repo, path)
        (success if ok else failed).append(name)
        time.sleep(0.5)

    print(f"\n{'='*50}")
    print(f"✅ Downloaded: {len(success)}/{len(FALLBACK_DOCS)}")
    if failed:
        print(f"❌ Still failed: {', '.join(failed)}")
    print(f"\n📂 Total docs in {DOCS_DIR}:")
    all_files = os.listdir(DOCS_DIR)
    print(f"   {len(all_files)} files")


if __name__ == "__main__":
    main()
