import streamlit as st
from langchain.llms import OpenAIChat
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv 
from openai import OpenAI
from moviepy.editor import VideoFileClip
import os
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

embeddings = OpenAIEmbeddings()

#def file_selector(folder_path='.'):
#    filenames = os.listdir(folder_path)
#    selected_filename = st.selectbox('Select a file', filenames)
#   return os.path.join(folder_path, selected_filename)
    
def convert_video_to_audio_moviepy(video_file):
    OutputExt = ".mp3"
    wait = input("")
    filename, ext = os.path.splitext(video_file)
    clip = VideoFileClip(video_file)
    print(f"{filename}"+ OutputExt)
    clip.audio.write_audiofile(f"{filename}"+ OutputExt)
    OutputFile = f"{filename}" +'.ogg'
    os.system('ffmpeg -i '+ f"{filename}"+ ext +' -vn -map_metadata -1 -ac 1 -c:a libopus -b:a 48k -application voip '+ OutputFile)
    return OutputFile

def speech_to_text(video_file:str):
    client = OpenAI()
    audio_file = open(video_file, "rb")
    transcript = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file, 
    response_format="text")
    return transcript

def create_vector_db_from_pdf(pdf_file:str) -> FAISS:
    reader = PdfReader(pdf_file)
    docs = ""
    i = 1
    pagina = ""
    for page in reader.pages:
        pagina = pagina + page.extract_text()

    textsplitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
    output = textsplitter.create_documents([pagina])
    docs = textsplitter.split_documents(output)
    db = FAISS.from_documents(docs,embeddings)
    return db

def get_response_from_query(db, query, k=15):
    #4097
    docs = db.similarity_search(query, k=k)
    docs_page_content = " ".join([d.page_content for d in docs])

    llm = ChatOpenAI(
        model_name = 'gpt-3.5-turbo-16k', 
        temperature = 0.1,
        openai_api_key = os.environ.get("OPENAI_API_KEY"),         
        )

    
    prompt = PromptTemplate(
        input_variables=["question","docs"],
        template = """
        You are a helpful assistant that that can answer questions based on the pdf that will be passed to you.
        
        Answer the following question: {question}
        By searching the following pdf file: {docs}
        
        Only use the factual information from the pdf file to answer the question and speak only in italian.
        
        If you feel like you don't have enough information to answer the question, say "I don't know".
        
        Your answers should be verbose and detailed.
        """,
    )

    chain = LLMChain(llm = llm, prompt=prompt)
    response = chain.run(question=query, docs = docs_page_content)
    response = response.replace("\n","")
    return response