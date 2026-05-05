"""
download_ml_dl_docs.py
-----------------------
Downloads Machine Learning and Deep Learning educational content
from two sources:
  1. Dive into Deep Learning (d2l-ai/d2l-en) — GitHub raw .md files
  2. Scikit-learn User Guide — GitHub raw .rst files

Saves everything to Data/ML_DL_Docs/
"""

import os
import time
import requests

DOCS_DIR = "/Users/vidhipitroda/Desktop/Projects/AI tutor/Data/ML_DL_Docs"
os.makedirs(DOCS_DIR, exist_ok=True)

HEADERS = {"User-Agent": "AITutor/1.0"}

# -----------------------------------------------------------------------
# SOURCE 1: Dive into Deep Learning (d2l-ai/d2l-en)
# Raw base: https://raw.githubusercontent.com/d2l-ai/d2l-en/master/
# Each chapter is a folder; the main file is index.md
# -----------------------------------------------------------------------
D2L_BASE = "https://raw.githubusercontent.com/d2l-ai/d2l-en/master"

# name → (chapter_folder, filename)
D2L_DOCS = {
    # Foundations
    "dl_introduction":              ("chapter_introduction",             "index.md"),
    "dl_preliminaries_data":        ("chapter_preliminaries",            "pandas.md"),
    "dl_preliminaries_linear_algebra": ("chapter_preliminaries",         "linear-algebra.md"),
    "dl_preliminaries_calculus":    ("chapter_preliminaries",            "calculus.md"),
    "dl_preliminaries_prob":        ("chapter_preliminaries",            "probability.md"),

    # Linear models
    "dl_linear_regression":         ("chapter_linear-regression",        "index.md"),
    "dl_linear_classification":     ("chapter_linear-classification",    "index.md"),

    # Neural Networks
    "dl_mlp":                       ("chapter_multilayer-perceptrons",   "mlp.md"),
    "dl_dropout":                   ("chapter_multilayer-perceptrons",   "dropout.md"),
    "dl_backprop":                  ("chapter_multilayer-perceptrons",   "backprop.md"),
    "dl_builders_guide":            ("chapter_builders-guide",           "index.md"),

    # CNNs
    "dl_cnn":                       ("chapter_convolutional-neural-networks", "index.md"),
    "dl_modern_cnn":                ("chapter_convolutional-modern",     "index.md"),

    # RNNs
    "dl_rnn":                       ("chapter_recurrent-neural-networks","index.md"),
    "dl_modern_rnn":                ("chapter_recurrent-modern",         "index.md"),

    # Attention & Transformers
    "dl_attention_mechanisms":      ("chapter_attention-mechanisms-and-transformers", "index.md"),
    "dl_attention_cues":            ("chapter_attention-mechanisms-and-transformers", "attention-cues.md"),
    "dl_self_attention":            ("chapter_attention-mechanisms-and-transformers", "self-attention-and-positional-encoding.md"),
    "dl_transformer":               ("chapter_attention-mechanisms-and-transformers", "transformer.md"),
    "dl_large_pretraining":         ("chapter_attention-mechanisms-and-transformers", "large-pretraining-transformers.md"),

    # NLP pretraining
    "dl_nlp_pretraining":           ("chapter_natural-language-processing-pretraining", "index.md"),
    "dl_bert":                      ("chapter_natural-language-processing-pretraining", "bert.md"),
    "dl_bert_pretraining":          ("chapter_natural-language-processing-pretraining", "bert-pretraining.md"),

    # NLP applications
    "dl_nlp_applications":          ("chapter_natural-language-processing-applications", "index.md"),
    "dl_finetuning_bert":           ("chapter_natural-language-processing-applications", "natural-language-inference-bert.md"),

    # Optimization
    "dl_optimization":              ("chapter_optimization",             "index.md"),
    "dl_sgd":                       ("chapter_optimization",             "sgd.md"),
    "dl_adam":                      ("chapter_optimization",             "adam.md"),

    # Math for DL
    "dl_math_eigendecomposition":   ("chapter_appendix-mathematics-for-deep-learning", "eigendecomposition.md"),
    "dl_math_stats":                ("chapter_appendix-mathematics-for-deep-learning", "statistics.md"),
    "dl_math_info_theory":          ("chapter_appendix-mathematics-for-deep-learning", "information-theory.md"),
}

# -----------------------------------------------------------------------
# SOURCE 2: Scikit-learn User Guide (scikit-learn/scikit-learn)
# Raw base: https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/doc/modules/
# -----------------------------------------------------------------------
SKLEARN_BASE = "https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/doc/modules"

SKLEARN_DOCS = {
    "ml_supervised_learning":       "supervised_learning.rst",
    "ml_linear_models":             "linear_model.rst",
    "ml_svm":                       "svm.rst",
    "ml_tree":                      "tree.rst",
    "ml_ensemble":                  "ensemble.rst",
    "ml_neural_net_supervised":     "neural_networks_supervised.rst",
    "ml_clustering":                "clustering.rst",
    "ml_decomposition":             "decomposition.rst",
    "ml_feature_extraction":        "feature_extraction.rst",
    "ml_preprocessing":             "preprocessing.rst",
    "ml_cross_validation":          "cross_validation.rst",
    "ml_model_evaluation":          "model_evaluation.rst",
    "ml_pipeline":                  "pipeline.rst",
    "ml_dimensionality_reduction":  "unsupervised_reduction.rst",
}


def download_raw(name: str, url: str, source_label: str) -> bool:
    out_path = os.path.join(DOCS_DIR, f"{name}.txt")

    if os.path.exists(out_path):
        print(f"   ⏭️  Already downloaded: {name}.txt")
        return True

    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        text = r.text

        if len(text) < 300:
            print(f"   ⚠️  Too short ({len(text)} chars): {name}")
            return False

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"SOURCE: {source_label}\n")
            f.write(f"RAW: {url}\n")
            f.write("=" * 60 + "\n\n")
            f.write(text)

        size_kb = os.path.getsize(out_path) // 1024
        print(f"   ✅ {name}.txt  ({size_kb} KB, {len(text):,} chars)")
        return True

    except Exception as e:
        print(f"   ❌ Failed [{name}]: {e}")
        return False


def main():
    print(f"📂 Saving to: {DOCS_DIR}\n")

    success, failed = [], []

    # --- Dive into Deep Learning ---
    print("📘 Dive into Deep Learning (d2l.ai)")
    print("-" * 45)
    for name, (chapter, filename) in D2L_DOCS.items():
        url = f"{D2L_BASE}/{chapter}/{filename}"
        source = f"https://d2l.ai/chapter_{chapter.replace('chapter_', '')}/{filename.replace('.md','')}.html"
        ok = download_raw(name, url, source)
        (success if ok else failed).append(name)
        time.sleep(0.3)

    # --- Scikit-learn ---
    print(f"\n🤖 Scikit-learn User Guide")
    print("-" * 45)
    for name, filename in SKLEARN_DOCS.items():
        url = f"{SKLEARN_BASE}/{filename}"
        source = f"https://scikit-learn.org/stable/modules/{filename.replace('.rst','')}.html"
        ok = download_raw(name, url, source)
        (success if ok else failed).append(name)
        time.sleep(0.3)

    print(f"\n{'='*50}")
    total = len(D2L_DOCS) + len(SKLEARN_DOCS)
    print(f"✅ Downloaded: {len(success)}/{total}")
    if failed:
        print(f"❌ Failed ({len(failed)}): {', '.join(failed)}")
    print(f"📂 Total files in {DOCS_DIR}: {len(os.listdir(DOCS_DIR))}")


if __name__ == "__main__":
    main()
