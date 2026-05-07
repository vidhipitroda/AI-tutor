#!/bin/bash
# Start the AI Tutor Streamlit UI

cd "$(dirname "$0")/.."
source .venv/bin/activate
streamlit run Code/ui.py
