import streamlit as st
import langchain_helper as lch
import textwrap
import os

tab1, tab2 = st.tabs(["PDF", "Video", "YouTube"])



with tab1:
  st.header(':bookmark_tabs: :red[PDF] Scraper', divider='red')
  st.markdown('##')
  with st.form(key='My_form'):
    file_uploader = st.file_uploader(label="Carica documento", type="pdf")
    query = st.text_input(label = "Chiedi qualcosa sul file inserito", max_chars=50, key = "query", label_visibility = "hidden", placeholder = "Chiedi qualcosa sul file inserito")      
    submit_button = st.form_submit_button(label="submit")
    #st.image('./pdf_icon.png', width = 60)  
  if query and file_uploader:
    db = lch.create_vector_db_from_pdf(file_uploader)
    response = lch.get_response_from_query(db, query)
    with st.container(border=True):
      st.title("Risposta:")
      st.text(textwrap.fill(response, width=500))

with tab2:
  st.header(':speaking_head_in_silhouette: Speech-To-Text', divider='red')
  st.markdown('##')
  with st.form(key='My_form2'):
    #video_uploader = lch.file_selector()
    video_uploader = st.file_uploader(label="Carica audio", type=["mp4","mp3","wav"])
    if video_uploader is not None:
      #print(video_uploader.name)
      with open(os.path.join(".", video_uploader.name),"wb") as f: 
        f.write(video_uploader.getbuffer())
        #print(f.name)
    submit_button2 = st.form_submit_button(label="Invia")
  if submit_button2:
    audio = lch.convert_video_to_audio_moviepy(f.name)
    transcript = lch.speech_to_text(audio)
    with st.container(border=True):
      st.title("Risposta:")
      DownloadBtn = st.download_button(
        label="Download transcript",
        data=transcript,
        file_name="Transcript.txt"
      )
      #st.download_button("Download Transcript",transcript)
      st.text(textwrap.fill(transcript)) 
