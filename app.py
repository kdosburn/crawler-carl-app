import streamlit as st
import os
import re
import nltk

# Download tokenizer if not already present
nltk.download('punkt', quiet=True)

# Load and sort text files
TEXT_FOLDER = "texts"
files = sorted([f for f in os.listdir(TEXT_FOLDER) if f.endswith(".txt")])

def search_texts(query, window=50):
    """Search all text files for query and return snippets with context."""
    results = []
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    for filename in files:
        with open(os.path.join(TEXT_FOLDER, filename), encoding="utf-8") as f:
            text = f.read()
            for match in pattern.finditer(text):
                start = max(0, match.start() - window)
                end = min(len(text), match.end() + window)
                snippet = text[start:end].replace("\n", " ")
                results.append((filename, snippet))
    return results

st.title("Search My Text Files")

# Context slider
context_chars = st.slider("Context characters", 20, 300, 50, step=10)

# Search input (ENTER will auto-run because Streamlit reruns on change)
search = st.text_input("Enter a search term and press Enter:")

# Also provide a button to run search manually
run_search = st.button("Search") or search  # True if button clicked OR there's text

if run_search and search:
    results = search_texts(search, window=context_chars)
    if results:
        for fname, snippet in results:
            # Highlight the search term in the snippet
            highlighted = re.sub(
                f"(?i)({re.escape(search)})",
                r"<mark>\1</mark>",
                snippet,
            )
            st.markdown(f"**{fname}:** …{highlighted}…", unsafe_allow_html=True)
    else:
        st.write("No matches found.")
