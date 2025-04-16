import streamlit as st
from src.api import get_pubmed_ids, get_pubmed_doc_by_ids

# Remove the argparse from api.py since we're using a web interface
import sys
# sys.modules['api'].parser = None

st.title("PubMed Search")

# Create the search input and button
query = st.text_input("Enter your search query:")
search_button = st.button("Search")

if search_button and query:
    with st.spinner("Searching PubMed..."):
        # Get PubMed IDs
        pmids = get_pubmed_ids(query)
        st.write(f"Found {len(pmids)} documents")
        
        # Get document details
        docs = get_pubmed_doc_by_ids(pmids)
        
        # Display results
        for doc in docs:
            st.write("---")
            st.write(f"**PMID:** {doc.pmid}")
            st.write(f"**Link:** {doc.href}")
            st.write(f"**DOI:** {doc.doi}")
            st.write(f"**Title:** {doc.title}")
            st.write(f"**Authors:** {doc.authors}")  # Using the simplified authors list
            if doc.abstract:
                st.write(f"**Abstract:** {doc.abstract[:200]}...")
            st.write("\n")