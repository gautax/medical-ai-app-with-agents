from crewai import Agent
from utils.config import medical_llm, search_tool

def create_diagnostician():
    return Agent(
        role="Senior Diagnostician",
        goal="Provide accurate differential diagnoses considering all patient factors",
        backstory="Board-certified physician with 20+ years clinical experience in internal medicine",
        tools=[search_tool],
        llm=medical_llm,
        verbose=True
    )