import streamlit as st
from scrape import (
    scrape_website, 
    split_dom_content,  # Ensure this function is implemented correctly
    clean_body_content, 
    extract_body_content 
)
from parse import parse_with_ollama

st.title("AI Web Scraper")

# User input for the website URL
url = st.text_input("Enter a Website URL:")

# Scrape Site Button
if st.button("Scrape Site"):
    if not url.strip():
        st.error("Please enter a valid URL.")
    else:
        st.write("Scraping the website...")
        try:
            result = scrape_website(url)
            body_content = extract_body_content(result)
            cleaned_content = clean_body_content(body_content)

            # Store content in session state
            st.session_state.dom_content = cleaned_content

            # Display the scraped DOM content
            with st.expander("View DOM Content"):
                st.text_area("DOM Content", cleaned_content, height=300)
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Parsing Section
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse:")

    if st.button("Parse the content"):
        if parse_description:
            st.write("Parsing the content...")
            try:
                # Split content and parse with Ollama
                dom_chunks = split_dom_content(st.session_state.dom_content)
                result = parse_with_ollama(dom_chunks, parse_description)
                st.write(result)
            except Exception as e:
                st.error(f"An error occurred during parsing: {e}")
        else:
            st.error("Please enter a description for parsing.")
