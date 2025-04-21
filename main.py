import streamlit as st
from scrape import *
from parse import *

# Streamlit UI
st.title("AI Webscraper")
st.set_page_config()
url : str = st.text_input("Enter a website URL: ")

# Step 1: Scrape the website
if st.button("Scrape Site"):
    st.write("Scraping website...")

    content = scrape_website(url)
    body_content = extract_body_content(content)
    cleaned_content = clean_body_content(body_content)

    st.session_state.dom_content = cleaned_content

    # Display the website content in a rezisable box 
    with st.expander("View DOM Content"):
        st.text_area("DOM Content", cleaned_content, height=300)

# Step 2: Ask Question about DOM Content
if "dom_content" in st.session_state:
    parse_describtion = st.text_area("Describe, what you want to parse?")

    if st.button("Parse Content"):
        st.write("Parsing Content...")

        # Parsing question about content and get answer
        dom_chunks = split_dom_content(st.session_state.dom_content)
        result = parse_with_ollama(dom_chunks, parse_describtion)
        st.write(result)
