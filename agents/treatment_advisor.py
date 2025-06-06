from crewai import Agent
from utils.config import medical_llm, search_tool

def create_treatment_advisor():
    return Agent(
        role="Treatment Specialist",
        goal="Develop personalized, evidence-based treatment plans",
        backstory="Clinical pharmacologist and therapeutic specialist with expertise in personalized medicine",
        tools=[search_tool],
        llm=medical_llm,
        verbose=True
    )