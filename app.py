import streamlit as st
import os
import nltk
import re

# Make sure punkt tokenizer is available
nltk.download('punkt', quiet=True)

# Load all text files from "texts" folder
TEXT_FOLDER = "texts"
files = [f for f in os.listdir(TEXT_FOLDER) if f.endswith(".txt")]

def search_texts(query, window=500):
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

# Streamlit UI
st.title("Search My Text Files")
query = st.text_input("Enter a search term:")

if st.button("Search") and query:
    results = search_texts(query)
    if results:
        for fname, snippet in results:
            st.markdown(f"**{fname}:** …{snippet}…")
    else:
        st.write("No matches found.")
