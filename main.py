"""Streamlit entrypoint.

This repo uses Streamlit's built-in multipage support (the `pages/` folder).
Running this file is equivalent to running `app.py`.
"""

# Importing `app` renders the main page.
# The Analysis page lives in `pages/generate_analysis.py`.
import app  # noqa: F401
