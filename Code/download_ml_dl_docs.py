"""
Download ML/DL textbook chapters from d2l.ai and scikit-learn user guide.
Saves to: Data/ML_DL_Docs/
"""
import os
import time
import requests
from bs4 import BeautifulSoup

SAVE_DIR = "/Users/vidhipitroda/Desktop/Projects/AI tutor/Data/ML_DL_Docs"
os.makedirs(SAVE_DIR, exist_ok=True)

# d2l.ai chapters (raw markdown from GitHub)
D2L_BASE = "https://raw.githubusercontent.com/d2l-ai/d2l-en/master"
D2L_DOCS = [
    ("d2l_intro",                    f"{D2L_BASE}/chapter_introduction/index.md"),
    ("d2l_linear_regression",        f"{D2L_BASE}/chapter_linear-regression/index.md"),
    ("d2l_linear_classification",    f"{D2L_BASE}/chapter_linear-classification/index.md"),
    ("d2l_mlp",                      f"{D2L_BASE}/chapter_multilayer-perceptrons/index.md"),
    ("d2l_model_selection",          f"{D2L_BASE}/chapter_multilayer-perceptrons/underfit-overfit.md"),
    ("d2l_dropout",                  f"{D2L_BASE}/chapter_multilayer-perceptrons/dropout.md"),
    ("d2l_backprop",                 f"{D2L_BASE}/chapter_multilayer-perceptrons/backprop.md"),
    ("d2l_cnn",                      f"{D2L_BASE}/chapter_convolutional-neural-networks/index.md"),
    ("d2l_rnn",                      f"{D2L_BASE}/chapter_recurrent-neural-networks/index.md"),
    ("d2l_lstm",                     f"{D2L_BASE}/chapter_recurrent-modern/lstm.md"),
    ("d2l_attention",                f"{D2L_BASE}/chapter_attention-mechanisms-and-transformers/index.md"),
    ("d2l_transformer",              f"{D2L_BASE}/chapter_attention-mechanisms-and-transformers/transformer.md"),
    ("d2l_bert",                     f"{D2L_BASE}/chapter_natural-language-processing-pretraining/bert.md"),
    ("d2l_bert_pretraining",         f"{D2L_BASE}/chapter_natural-language-processing-pretraining/bert-pretraining.md"),
    ("d2l_optimization",             f"{D2L_BASE}/chapter_optimization/index.md"),
    ("d2l_adam",                     f"{D2L_BASE}/chapter_optimization/adam.md"),
    ("d2l_computational_performance",f"{D2L_BASE}/chapter_computational-performance/index.md"),
    ("d2l_hyperparameter_optimization",f"{D2L_BASE}/chapter_hyperparameter-optimization/index.md"),
    ("d2l_generative",               f"{D2L_BASE}/chapter_generative-adversarial-networks/index.md"),
    ("d2l_large_scale",              f"{D2L_BASE}/chapter_large-scale-optimization/index.md"),
]

# scikit-learn user guide sections (raw rst from GitHub)
SKLEARN_BASE = "https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/doc/modules"
SKLEARN_DOCS = [
    ("sklearn_linear_models",    f"{SKLEARN_BASE}/linear_model.rst"),
    ("sklearn_svm",              f"{SKLEARN_BASE}/svm.rst"),
    ("sklearn_tree",             f"{SKLEARN_BASE}/tree.rst"),
    ("sklearn_ensemble",         f"{SKLEARN_BASE}/ensemble.rst"),
    ("sklearn_neural_network",   f"{SKLEARN_BASE}/neural_networks_supervised.rst"),
    ("sklearn_clustering",       f"{SKLEARN_BASE}/clustering.rst"),
    ("sklearn_decomposition",    f"{SKLEARN_BASE}/decomposition.rst"),
    ("sklearn_feature_selection",f"{SKLEARN_BASE}/feature_selection.rst"),
    ("sklearn_preprocessing",    f"{SKLEARN_BASE}/preprocessing.rst"),
    ("sklearn_cross_validation", f"{SKLEARN_BASE}/cross_validation.rst"),
    ("sklearn_model_evaluation", f"{SKLEARN_BASE}/model_evaluation.rst"),
    ("sklearn_pipeline",         f"{SKLEARN_BASE}/pipeline.rst"),
]

ALL_DOCS = D2L_DOCS + SKLEARN_DOCS
headers = {"User-Agent": "AITutor/1.0"}

print(f"Downloading {len(ALL_DOCS)} ML/DL doc pages to {SAVE_DIR}/\n")
ok, fail = 0, 0
for i, (name, url) in enumerate(ALL_DOCS):
    out_path = os.path.join(SAVE_DIR, f"{name}.txt")
    if os.path.exists(out_path):
        print(f"  [{i+1}/{len(ALL_DOCS)}] Already exists: {name}.txt")
        ok += 1
        continue
    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(r.text)
        print(f"  [{i+1}/{len(ALL_DOCS)}] OK  {name}.txt  ({len(r.text):,} chars)")
        ok += 1
        time.sleep(0.3)
    except Exception as e:
        print(f"  [{i+1}/{len(ALL_DOCS)}] FAIL {name}: {e}")
        fail += 1

print(f"\nDone! {ok} saved, {fail} failed -> {SAVE_DIR}")
