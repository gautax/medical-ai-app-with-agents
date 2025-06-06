from crewai import Crew, Process
from agents.specialist_referral import create_specialist_referral
from agents.appointment_coordinator import create_appointment_coordinator
from tasks.specialist_referral_task import create_specialist_referral_task
from tasks.appointment_task import create_appointment_task
import streamlit as st

def create_appointment_crew(diagnosis, location):
    referral_agent = create_specialist_referral()
    coordinator_agent = create_appointment_coordinator()
    
    referral_task = create_specialist_referral_task(referral_agent, diagnosis)
    appointment_task = create_appointment_task(
        coordinator_agent, 
        location, 
        context={
        'diagnosis': diagnosis,
        'referral_output': referral_task.output,
        'patient_info': st.session_state.patient_info
    }  
    )
    
    return Crew(
        agents=[referral_agent, coordinator_agent],
        tasks=[referral_task, appointment_task],
        verbose=True,
        process=Process.sequential,
        full_output=True  # Ensure we get all reasoning steps
    )