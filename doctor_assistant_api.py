"""
Fast API ile GPT doktor asistani

her kullanici icin ayri bir memory tutalim
"""

import os 
from typing import Dict 


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic  import BaseModel
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains import ConversationChain

import warnings
warnings.filterwarnings("ignore")

# ortam degiskenlerini tanimla (openai api key tanimla)
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

#Fast API uygulamasini baslat 
app = FastAPI(tittle = "Doktor Asistani API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LLM + memeory
# buyuk dil modeli 
llm = ChatOpenAI(
    model = "gpt-5.4-nano", # hangi gpt yi kullandigimiz
    temperature = 0.7, # 0-1, 0 a yakinsa garanti cevap verir, 1 e yakinsa dusunerek cevap verir. 1 e yaklastikca halusinasyon riski artar
    openai_api_key = api_key
)

#Memory yapilandirmasi
user_memories: Dict[str, ConversationBufferMemory] = {}

#istek ve cevap modelleri
class ChatRequest(BaseModel):#CHAT -> API ye gonderilen istek modeli
    name: str
    age: int
    message: str

class ChatResponse(BaseModel):# CHAT -> API den donen cevap modeli
    response: str

# sohbet endpointi
@app.post("/chat", response_model = ChatResponse)
async def chat_with_doctor(request: ChatRequest):
    try:
        #hafiza varsa al, yoksa yeni olustur
        if request.name not in user_memories:
            user_memories[request.name] = ConversationBufferMemory(return_messages = True)
        memory = user_memories[request.name]

        #intro mesajini olustur
        if len(memory.chat_memory.messages) == 0:
            intro = (
                f"sen bir doktor asistansin. Hasta: {request.name} ve yasi {request.age} "
                "sağlık sorunları hakkında konuşmak istiyor."
                "Yaşına uygun, dikkatli ve nazik tavsiyeler ver."
                "Kullanıcıya ismyle hitap et"
            )
            memory.chat_memory.add_user_message(intro)

        #llm ve memory ile chain olustur
        conversation = ConversationChain(llm = llm, memory = memory, verbose = False)
        reply = conversation.predict(input = request.message)

        #hafizayi terminale yazdir
        print(f"\n Memory: ")
        for idx, m in enumerate(memory.chat_memory.messages, start = 1):
            print(f"{idx:02d}. {m.type.upper()}: {m.content}")
        print("-------------------------------")

        return ChatResponse(response = reply)
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))

if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/ui", StaticFiles(directory="static", html=True), name="static")
    
#swagger UI icin baslangic http://127.0.0.1:8000/docs  

 