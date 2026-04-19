import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash",
              google_api_key=os.getenv("GEMINI_API_KEY"),
              temperature=0)
try:
    response= llm.invoke("Are you ready to start the ThreatLens project?")
    print(response.content)
except Exception as e:
    print(f"An error occured: {e}")