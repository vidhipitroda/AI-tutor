"""
download_hf_docs.py
--------------------
Downloads Hugging Face documentation pages (Transformers, LLMs, Tokenizers, PEFT, LoRA)
and saves them as clean .txt files in Data/HF_Docs/
"""

import os
import time
import requests
from bs4 import BeautifulSoup

DOCS_DIR = "/Users/vidhipitroda/Desktop/Projects/AI tutor/Data/HF_Docs"
os.makedirs(DOCS_DIR, exist_ok=True)

# --- Doc registry: filename → URL ---
HF_DOCS = {
    # --- Transformers ---
    "transformers_overview":            "https://huggingface.co/docs/transformers/index",
    "transformers_quicktour":           "https://huggingface.co/docs/transformers/quicktour",
    "transformers_philosophy":          "https://huggingface.co/docs/transformers/philosophy",
    "transformers_pipeline_tutorial":   "https://huggingface.co/docs/transformers/pipeline_tutorial",
    "transformers_autoclass_tutorial":  "https://huggingface.co/docs/transformers/autoclass_tutorial",
    "transformers_preprocessing":       "https://huggingface.co/docs/transformers/preprocessing",
    "transformers_training":            "https://huggingface.co/docs/transformers/training",

    # --- LLMs ---
    "llm_tutorial":                     "https://huggingface.co/docs/transformers/llm_tutorial",
    "llm_optims":                       "https://huggingface.co/docs/transformers/llm_optims",
    "llm_generate":                     "https://huggingface.co/docs/transformers/main_classes/text_generation",
    "llm_chat_templating":              "https://huggingface.co/docs/transformers/chat_templating",

    # --- Tokenizers ---
    "tokenizers_overview":              "https://huggingface.co/docs/tokenizers/index",
    "tokenizers_quicktour":             "https://huggingface.co/docs/tokenizers/quicktour",
    "tokenizers_pipeline":              "https://huggingface.co/docs/tokenizers/pipeline",
    "tokenizers_components":            "https://huggingface.co/docs/tokenizers/components",
    "transformers_tokenizer_summary":   "https://huggingface.co/docs/transformers/tokenizer_summary",

    # --- PEFT ---
    "peft_overview":                    "https://huggingface.co/docs/peft/index",
    "peft_quicktour":                   "https://huggingface.co/docs/peft/quicktour",
    "peft_conceptual_intro":            "https://huggingface.co/docs/peft/conceptual_guides/adapter",
    "peft_task_guides_lm":              "https://huggingface.co/docs/peft/task_guides/clm-prompt-tuning",

    # --- LoRA ---
    "lora_conceptual_guide":            "https://huggingface.co/docs/peft/conceptual_guides/lora",
    "lora_config_api":                  "https://huggingface.co/docs/peft/package_reference/lora",
    "lora_image_classification":        "https://huggingface.co/docs/peft/task_guides/image_classification_lora",
    "lora_semantic_segmentation":       "https://huggingface.co/docs/peft/task_guides/semantic_segmentation_lora",
}

HEADERS = {
    "User-Agent": "AITutor/1.0 (educational project; github.com/vidhipitroda)"
}


def extract_clean_text(html: str) -> str:
    """Extract readable text from HuggingFace docs HTML."""
    soup = BeautifulSoup(html, "html.parser")

    # Remove nav, footer, sidebar, scripts, styles
    for tag in soup(["nav", "footer", "script", "style", "aside", "header"]):
        tag.decompose()

    # HuggingFace docs main content lives in <main> or article div
    main = soup.find("main") or soup.find("div", {"class": "prose"}) or soup.body
    text = main.get_text(separator="\n") if main else soup.get_text(separator="\n")

    # Clean up excessive blank lines
    lines = [line.strip() for line in text.splitlines()]
    cleaned = "\n".join(line for line in lines if line)
    return cleaned


def download_doc(name: str, url: str) -> bool:
    out_path = os.path.join(DOCS_DIR, f"{name}.txt")

    if os.path.exists(out_path):
        print(f"   ⏭️  Already downloaded: {name}.txt")
        return True

    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()

        text = extract_clean_text(response.text)

        if len(text) < 200:
            print(f"   ⚠️  Too short / likely blocked: {name}")
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
    print(f"📂 Saving docs to: {DOCS_DIR}")
    print(f"📋 Pages to download: {len(HF_DOCS)}\n")

    success, failed = [], []

    # Group by category for nicer output
    categories = {
        "🤗 Transformers":  [k for k in HF_DOCS if k.startswith("transformers")],
        "🧠 LLMs":          [k for k in HF_DOCS if k.startswith("llm")],
        "🔤 Tokenizers":    [k for k in HF_DOCS if k.startswith("tokenizer")],
        "🔧 PEFT":          [k for k in HF_DOCS if k.startswith("peft")],
        "🎯 LoRA":          [k for k in HF_DOCS if k.startswith("lora")],
    }

    for category, keys in categories.items():
        print(f"\n{category}")
        print("-" * 40)
        for key in keys:
            url = HF_DOCS[key]
            print(f"   [{key}]")
            ok = download_doc(key, url)
            (success if ok else failed).append(key)
            time.sleep(0.5)   # be polite to HF servers

    print(f"\n{'='*50}")
    print(f"✅ Downloaded: {len(success)}/{len(HF_DOCS)}")
    if failed:
        print(f"❌ Failed ({len(failed)}): {', '.join(failed)}")
    print(f"📂 All docs saved to: {DOCS_DIR}")


if __name__ == "__main__":
    main()
