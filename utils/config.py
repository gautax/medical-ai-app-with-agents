import os
from dotenv import load_dotenv
from crewai import LLM
from crewai_tools import SerperDevTool
import google.generativeai as genai
load_dotenv()

medical_llm = LLM(
    model='gemini/gemini-1.5-pro-latest',  
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3,
    top_p=0.9,
    top_k=40,
    additional_kwargs={"vertex_project": None}  # Still block Vertex AI
)

admin_llm = LLM(
    model="gemini/gemini-1.5-flash-latest", 
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.1,
    top_p=0.95,
    top_k=20,
    additional_kwargs={"vertex_project": None}
)

search_tool = SerperDevTool(
    params={
        "hl": "en",
        "gl": "ma",  # Morocco country code
        "num": 5,    # Get more results
        "page": 1    # First page results
    }
)