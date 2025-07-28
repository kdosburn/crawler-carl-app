import streamlit as st
import os
import re
import nltk

BOOK_TITLES = {
    "CARL_01.txt": "Dungeon Crawler Carl",
    "CARL_02.txt": "Carl's Doomsday Scenario",
    "CARL_03.txt": "The Dungeon Anarchist's Cookbook",
    "CARL_04.txt": "The Gate of the Feral Gods",
    "CARL_05.txt": "The Butcher's Masquerade",
    "CARL_06.txt": "The Eye of the Bedlam Bride",
    "CARL_07.txt": "This Inevitable Ruin",
}

# Download tokenizer if not already present
nltk.download('punkt', quiet=True)

# Folder with your .txt files
TEXT_FOLDER = "texts"
files = sorted([f for f in os.listdir(TEXT_FOLDER) if f.endswith(".txt")])

def search_texts(query, window=200):
    """Search all books for query and return merged snippets with context."""
    results = []
    pattern = re.compile(re.escape(query), re.IGNORECASE)

    for filename in files:
        with open(os.path.join(TEXT_FOLDER, filename), encoding="utf-8") as f:
            text = f.read()

            matches = list(pattern.finditer(text))
            if not matches:
                continue

            i = 0
            while i < len(matches):
                # Start of this merged snippet
                start_index = max(0, matches[i].start() - window)
                end_index = min(len(text), matches[i].end() + window)

                # Merge consecutive matches that fall inside the same window
                j = i + 1
                while j < len(matches) and matches[j].start() <= end_index:
                    # Extend the end of the snippet to include this match
                    end_index = min(len(text), matches[j].end() + window)
                    j += 1

                snippet = text[start_index:end_index].replace("\n", " ")
                results.append((filename, snippet))

                # Jump ahead to the next non-overlapping group of matches
                i = j

    return results

st.title("Dungeon Crawler Carl Crawler")
st.markdown(
    "### All text credit goes to the brilliant "
    "[Matt Dinniman](https://mattdinniman.com/)",
    unsafe_allow_html=False
)


# Slider for context size
context_chars = st.slider("Context characters", 20, 1000, 200, step=10)

# Text input (press Enter to search)
search = st.text_input("Enter a search term or phrase (ex: 'goddamnit, donut') and press Enter:")

# Button also triggers search
run_search = st.button("Search") or search

if run_search and search:
    results = search_texts(search, window=context_chars)
    if results:
        for fname, snippet in results:
            # Highlight search term(s)
            highlighted = re.sub(
                f"(?i)({re.escape(search)})",
                r"<mark>\1</mark>",
                snippet,
            )
            title = BOOK_TITLES.get(fname, fname)
            st.markdown(f"**{title}:**")
            st.markdown(f"…{highlighted}…", unsafe_allow_html=True)
            st.divider()
    else:
        st.write("No matches found.")
