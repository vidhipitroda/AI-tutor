"""
Download HuggingFace Transformers / PEFT / Tokenizer docs as .txt files.
Fetches raw markdown from GitHub (no JS rendering issues).
Saves to: Data/HF_Docs/
"""
import os
import time
import requests

SAVE_DIR = "/Users/vidhipitroda/Desktop/Projects/AI tutor/Data/HF_Docs"
os.makedirs(SAVE_DIR, exist_ok=True)

BASE = "https://raw.githubusercontent.com/huggingface/transformers/main/docs/source/en"
PEFT_BASE = "https://raw.githubusercontent.com/huggingface/peft/main/docs/source"
TOK_BASE  = "https://raw.githubusercontent.com/huggingface/tokenizers/main/docs/source/api"

DOCS = [
    # Transformers
    ("transformers_overview",           f"{BASE}/index.md"),
    ("transformers_quicktour",          f"{BASE}/quicktour.md"),
    ("transformers_philosophy",         f"{BASE}/philosophy.md"),
    ("transformers_pipeline_tutorial",  f"{BASE}/pipeline_tutorial.md"),
    ("transformers_autoclass_tutorial", f"{BASE}/autoclass_tutorial.md"),
    ("transformers_preprocessing",      f"{BASE}/preprocessing.md"),
    ("transformers_training",           f"{BASE}/training.md"),
    ("transformers_tokenizer_summary",  f"{BASE}/tokenizer_summary.md"),
    # LLM guides
    ("llm_tutorial",                    f"{BASE}/llm_tutorial.md"),
    ("llm_generate",                    f"{BASE}/main_classes/text_generation.md"),
    ("llm_chat_templating",             f"{BASE}/chat_templating.md"),
    ("llm_optims",                      f"{BASE}/llm_optims.md"),
    # PEFT
    ("peft_overview",                   f"{PEFT_BASE}/index.md"),
    ("peft_quicktour",                  f"{PEFT_BASE}/quicktour.md"),
    ("peft_conceptual_intro",           f"{PEFT_BASE}/conceptual_guides/intro.md"),
    ("peft_conceptual_adapter",         f"{PEFT_BASE}/conceptual_guides/adapter.md"),
    ("peft_conceptual_prompting",       f"{PEFT_BASE}/conceptual_guides/prompting.md"),
    ("peft_lora_based_methods",         f"{PEFT_BASE}/conceptual_guides/lora_based_methods.md"),
    ("peft_model_merging",              f"{PEFT_BASE}/conceptual_guides/model_merging.md"),
    ("peft_quantization",               f"{PEFT_BASE}/developer_guides/quantization.md"),
    ("peft_model_config",               f"{PEFT_BASE}/package_reference/config.md"),
    ("lora_conceptual_guide",           f"{PEFT_BASE}/conceptual_guides/lora.md"),
    ("lora_config_api",                 f"{PEFT_BASE}/package_reference/lora.md"),
    ("lora_config_api_ref",             f"{PEFT_BASE}/package_reference/tuners.md"),
    # Tokenizers
    ("tokenizers_overview",             f"{TOK_BASE}/index.rst"),
    ("tokenizers_pipeline",             "https://raw.githubusercontent.com/huggingface/tokenizers/main/docs/source/pipeline.md"),
    ("tokenizers_quicktour",            "https://raw.githubusercontent.com/huggingface/tokenizers/main/docs/source/quicktour.md"),
    ("tokenizers_components",           "https://raw.githubusercontent.com/huggingface/tokenizers/main/docs/source/components.md"),
]

headers = {"User-Agent": "AITutor/1.0"}

print(f"Downloading {len(DOCS)} HuggingFace doc pages to {SAVE_DIR}/\n")
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
