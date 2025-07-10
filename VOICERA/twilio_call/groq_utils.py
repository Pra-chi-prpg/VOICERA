import os
import uuid
import subprocess
import edge_tts
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings  

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

GROQ_API_KEY = "gs#################################################" 
NGROK_URL = "https://51454ccf829a.ngrok-free.app" 

def load_pdf_vector_store(pdf_path="hdfc_credit_card.pdf"):
    loader = PyMuPDFLoader(pdf_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.from_documents(split_docs, embeddings)

retriever = load_pdf_vector_store()

llm = ChatOpenAI(
    openai_api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
    model="llama3-8b-8192",
    temperature=0.4,
    max_tokens=200
)

async def get_answer_from_pdf(question: str) -> str:
    try:
        qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever.as_retriever())
        # result = await qa.ainvoke({"query": question}) 
        # return result["result"].strip()
        return qa.run(question).strip()
    except Exception as e:
        print(f"[Groq QA Error] {e}")
        return "Did not catch that."

async def translate_to_hindi(text: str) -> str:
    try:
        messages = [
            SystemMessage(content="You are a professional Hindi translator."),
            HumanMessage(content=f"Translate this to Hindi: {text}")
        ]
        response = await llm.ainvoke(messages)
        return response.content.strip()
    except Exception as e:
        print(f"[Translation Error] {e}")
        return text

async def convert_to_speech(text, filename="response.mp3", voice="en-IN-NeerjaNeural"):
    folder = "static"
    os.makedirs(folder, exist_ok=True)
    raw_path = os.path.join(folder, f"raw_{uuid.uuid4().hex}.mp3")
    final_path = os.path.join(folder, filename)

    communicate = edge_tts.Communicate(text=text, voice=voice, rate="+0%")
    print("[Edge-TTS] Generating voice...")
    await communicate.save(raw_path)

    subprocess.run([
        r"C:\new\ffmpeg\bin\ffmpeg.exe",  # adjust path
        "-y", "-i", raw_path,
        "-ar", "8000", "-ac", "1", final_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    os.remove(raw_path)
    return f"{NGROK_URL}/static/{filename}"


