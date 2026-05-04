"""
Download 15 key AI/LLM research papers from arXiv as PDFs.
Saves to: Data/Papers/
"""
import os
import time
import requests

SAVE_DIR = "/Users/vidhipitroda/Desktop/Projects/AI tutor/Data/Papers"
os.makedirs(SAVE_DIR, exist_ok=True)

PAPERS = [
    ("attention_is_all_you_need",  "https://arxiv.org/pdf/1706.03762"),
    ("bert",                        "https://arxiv.org/pdf/1810.04805"),
    ("gpt3",                        "https://arxiv.org/pdf/2005.14165"),
    ("instructgpt_rlhf",            "https://arxiv.org/pdf/2203.02155"),
    ("chain_of_thought",            "https://arxiv.org/pdf/2201.11903"),
    ("rag_original",                "https://arxiv.org/pdf/2005.11401"),
    ("lora",                        "https://arxiv.org/pdf/2106.09685"),
    ("llama",                       "https://arxiv.org/pdf/2302.13971"),
    ("llama2",                      "https://arxiv.org/pdf/2307.09288"),
    ("mistral7b",                   "https://arxiv.org/pdf/2310.06825"),
    ("mistral_mixtral",             "https://arxiv.org/pdf/2401.04088"),
    ("react_agent",                 "https://arxiv.org/pdf/2210.03629"),
    ("toolformer",                  "https://arxiv.org/pdf/2302.04761"),
    ("generative_agents",           "https://arxiv.org/pdf/2304.03442"),
    ("self_refine",                 "https://arxiv.org/pdf/2303.17651"),
]

headers = {"User-Agent": "AITutor/1.0 (research project)"}

print(f"Downloading {len(PAPERS)} papers to {SAVE_DIR}/\n")
for i, (name, url) in enumerate(PAPERS):
    out_path = os.path.join(SAVE_DIR, f"{name}.pdf")
    if os.path.exists(out_path):
        print(f"  [{i+1}/{len(PAPERS)}] Already exists: {name}.pdf")
        continue
    try:
        print(f"  [{i+1}/{len(PAPERS)}] Downloading {name}...")
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        with open(out_path, "wb") as f:
            f.write(r.content)
        size_kb = len(r.content) / 1024
        print(f"             Saved {name}.pdf ({size_kb:.0f} KB)")
        time.sleep(1)  # be polite to arXiv
    except Exception as e:
        print(f"  FAILED {name}: {e}")

print(f"\nDone! Papers saved to {SAVE_DIR}")
