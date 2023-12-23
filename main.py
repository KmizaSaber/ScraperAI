import streamlit as st
import langchain_helper as lch
import textwrap

tab1, tab2, tab3 = st.tabs(["PDF", "Video", "YouTube"])
with tab1:
   st.title(":bookmark_tabs: :red[PDF] Scraper")
   #st.image('./pdf_icon.png', width = 60)
with st.form(key='My_form'):
  file_uploader = st.file_uploader(label="Upload file", type="pdf")
  query = st.text_input(label = "Chiedi qualcosa sul file inserito", max_chars=50, key = "query", label_visibility = "hidden", placeholder = "Chiedi qualcosa sul file inserito")      
  submit_button = st.form_submit_button(label="submit")
with tab2:
  st.header("A dog")
  st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
  st.header("An owl")
  st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
      
if query and file_uploader:
  db = lch.create_vector_db_from_pdf(file_uploader)
  response = lch.get_response_from_query(db, query)
  with st.container(border=True):
    st.title("Risposta:")
    st.text(textwrap.fill(response))

