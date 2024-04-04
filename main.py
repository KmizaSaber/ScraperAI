import streamlit as st
import langchain_helper as lch
import textwrap
import shutil
import os

tab1, tab2 = st.tabs(["PDF", "Video"])



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
    video_uploader = st.file_uploader(label="Carica audio", type=["mp4","mp3","wav"], accept_multiple_files=True, key="video_uploader")
    if video_uploader is not None:
      for file in video_uploader:
      #print(video_uploader.name)
        with open(os.path.join(".", file.name),"wb") as f: 
          f.write(file.getbuffer())
        #print(f.name)
      submit_button2 = st.form_submit_button(label="Invia")
  with st.container(border=True):
    if submit_button2:
      for video in video_uploader:
        name = video.name[:-4]
        audio = lch.convert_video_to_audio_moviepy(video.name)
        transcript = lch.speech_to_text(audio)
        with open(os.path.join("./temp/", name+".txt"),"w") as f: 
          f.write(transcript)
      shutil.make_archive("Transcript", 'zip', "./temp/")
      folder = './temp/'
      for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
          if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
          elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
        except Exception as e:
          print('Failed to delete %s. Reason: %s' % (file_path, e))
      st.title("Risposta:")
      with open("Transcript.zip", "rb") as file:
        DownloadBtn = st.download_button(
          label="Download transcript",
          data= file,
          file_name="Transcript.zip",
          key=name
          )
      os.unlink("./Transcript.zip")
        #st.download_button("Download Transcript",transcript)
      st.text(textwrap.fill(transcript)) 
