from crewai import Crew, Process
from agents.diagnostician import create_diagnostician
from agents.treatment_advisor import create_treatment_advisor
from tasks.diagnosis_task import create_diagnosis_task
from tasks.treatment_task import create_treatment_task

def create_medical_crew(patient_info):
    diagnostician = create_diagnostician()
    treatment_advisor = create_treatment_advisor()
    
    diagnosis_task = create_diagnosis_task(diagnostician, patient_info)
    treatment_task = create_treatment_task(treatment_advisor, patient_info, diagnosis_task)
    
    return Crew(
        agents=[diagnostician, treatment_advisor],
        tasks=[diagnosis_task, treatment_task],
        verbose=True,
        process=Process.sequential
    )