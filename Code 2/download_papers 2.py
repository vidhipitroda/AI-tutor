"""
download_papers.py
------------------
Downloads foundational LLM papers as PDFs from arXiv into the Data/Papers folder.
"""

import os
import time
import requests

# Output folder
PAPERS_DIR = "/Users/vidhipitroda/Desktop/Projects/AI tutor/Data/Papers"
os.makedirs(PAPERS_DIR, exist_ok=True)

# --- Paper registry: name → arXiv ID ---
PAPERS = {
    "attention_is_all_you_need": "1706.03762",   # Transformer
    "gpt3":                      "2005.14165",   # GPT-3
    "bert":                      "1810.04805",   # BERT
    "rag_original":              "2005.11401",   # RAG (Lewis et al.)
    "lora":                      "2106.09685",   # LoRA
    "instructgpt_rlhf":          "2203.02155",   # InstructGPT / RLHF
    "toolformer":                "2302.04761",   # Toolformer
    "llama":                     "2302.13971",   # LLaMA 1
    "llama2":                    "2307.09288",   # LLaMA 2
    "mistral7b":                 "2310.06825",   # Mistral 7B
    "mistral_mixtral":           "2401.04088",   # Mixtral MoE
    "chain_of_thought":          "2201.11903",   # Chain-of-Thought prompting
    "react_agent":               "2210.03629",   # ReAct agent
    "generative_agents":         "2304.03442",   # Generative Agents
    "self_refine":               "2303.17651",   # Self-Refine
}

def download_paper(name: str, arxiv_id: str) -> bool:
    pdf_url  = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    out_path = os.path.join(PAPERS_DIR, f"{name}.pdf")

    if os.path.exists(out_path):
        print(f"   ⏭️  Already downloaded: {name}.pdf")
        return True

    try:
        print(f"   ⬇️  Downloading {name} ({arxiv_id})...")
        response = requests.get(pdf_url, timeout=60, stream=True)
        response.raise_for_status()

        with open(out_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        size_kb = os.path.getsize(out_path) // 1024
        print(f"   ✅ Saved: {name}.pdf  ({size_kb} KB)")
        return True

    except Exception as e:
        print(f"   ❌ Failed [{name}]: {e}")
        # Remove partial file if any
        if os.path.exists(out_path):
            os.remove(out_path)
        return False


def main():
    print(f"📂 Saving PDFs to: {PAPERS_DIR}")
    print(f"📋 Papers to download: {len(PAPERS)}\n")

    success, failed = [], []

    for i, (name, arxiv_id) in enumerate(PAPERS.items(), 1):
        print(f"[{i}/{len(PAPERS)}] {name}")
        ok = download_paper(name, arxiv_id)
        (success if ok else failed).append(name)
        time.sleep(1)  # be polite to arXiv servers

    print(f"\n{'='*50}")
    print(f"✅ Downloaded: {len(success)}/{len(PAPERS)}")
    if failed:
        print(f"❌ Failed ({len(failed)}): {', '.join(failed)}")
    print(f"📂 All PDFs are in: {PAPERS_DIR}")


if __name__ == "__main__":
    main()
