#importing all langchain dependencies
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
#bring in streamlit for UI DEV
import streamlit as st
#bring in watsonx interface
from watsonxlangchain import LangChainInterface
#seup the app title

st.title('Ask watsonx')

#build a prompt input template to display the prompts
prompt = st.chat_input('Pass your prompt here')

if prompt:
    #DISPLAY THE PROMPT
    st.chat_message('user').markdown(prompt)