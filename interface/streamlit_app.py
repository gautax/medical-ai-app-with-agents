import sys
import os
from pathlib import Path
from pydantic import BaseModel
from typing import Optional
import json

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Now import your modules
import json
from crew.appointment_crew import create_appointment_crew
from crew.medical_crew import create_medical_crew
from utils.report_generator import create_docx
import streamlit as st

# Streamlit UI Configuration
st.set_page_config(page_title="Medical AI Assistant", page_icon="🏥", layout="wide")
st.title("🏥 Comprehensive Medical Diagnosis Assistant")

def get_patient_info():
    with st.expander("Patient Information", expanded=True):
        # Add name field at the top
        name = st.text_input("Full Name", "")
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=0, max_value=120, value=30)
            sex = st.selectbox("Sex", ["Male", "Female", "Other"])
        with col2:
            weight = st.number_input("Weight (kg)", min_value=0, value=70)
            height = st.number_input("Height (cm)", min_value=0, value=170)

    with st.expander("Clinical Information", expanded=True):
        symptoms = st.text_area("Primary Symptoms", "Itchy eyes, fatigue, rapid heart rate, headache")
        symptom_duration = st.selectbox("Symptom Duration", ["<24 hours", "1-7 days", "1-4 weeks", ">1 month"])
        symptom_severity = st.slider("Symptom Severity (1-10)", 1, 10, 5)
        
        col1, col2 = st.columns(2)
        with col1:
            history = st.text_area("Medical History", "None")
            allergies = st.text_input("Known Allergies", "None")
        with col2:
            medications = st.text_input("Current Medications", "None")
            family_history = st.text_input("Family History", "None")

    return {
        'name': name,
        'age': age,
        'sex': sex,
        'weight': weight,
        'height': height,
        'symptoms': symptoms,
        'symptom_duration': symptom_duration,
        'symptom_severity': symptom_severity,
        'history': history,
        'allergies': allergies,
        'medications': medications,
        'family_history': family_history
    }

def extract_email_content(full_output):
    """Extract email content from agent output"""
    if "## Email Draft:" in full_output:
        return full_output.split("## Email Draft:")[1].strip()
    return full_output

def render_diagnosis_page():
    st.header("Medical Diagnosis & Treatment Plan")
    patient_info = get_patient_info()
    
    if st.button("Generate Comprehensive Report"):
        if not patient_info['symptoms'].strip():
            st.error("Please describe the patient's symptoms")
            return
        
        with st.spinner('Medical Team Analyzing (this may take 1-2 minutes)...'):
            try:
                medical_crew = create_medical_crew(patient_info)
                result = medical_crew.kickoff()
                
                # Store results in session state
                st.session_state.diagnosis = medical_crew.tasks[0].output
                st.session_state.treatment_plan = medical_crew.tasks[1].output
                st.session_state.patient_info = patient_info
                
                # Display Results
                st.success("Analysis Complete!")
                
                with st.expander("Diagnosis Summary", expanded=True):
                    st.markdown(st.session_state.diagnosis)
                
                with st.expander("Personalized Treatment Plan", expanded=True):
                    st.markdown(st.session_state.treatment_plan)
                
                # Generate downloadable report
                docx_file = create_docx(
                    patient_info,
                    str(st.session_state.diagnosis),
                    str(st.session_state.treatment_plan))
                
                st.download_button(
                    label="📄 Download Full Medical Report",
                    data=docx_file.getvalue(),
                    file_name=f"medical_report_{patient_info['age']}_{patient_info['sex']}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
                
                st.success("Visit the 'Specialist Referral' page to find appropriate doctors")
                
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
                st.code("Common fixes:\n1. Verify API keys\n2. Check internet connection", language="bash")

def render_appointment_page():
    st.header("🧑‍⚕️ Specialist Referral & Appointment Booking")
    
    # Check if diagnosis exists
    if 'diagnosis' not in st.session_state:
        st.warning("Please complete a diagnosis on the 'Medical Diagnosis' page first")
        return
    
    st.subheader("Diagnosis Summary")
    st.info(st.session_state.diagnosis)
    
    st.subheader("Appointment Details")
    col1, col2 = st.columns(2)
    with col1:
        location = st.text_input("Your Location (City or ZIP Code):", key="location")
    with col2:
        insurance = st.text_input("Insurance Provider (Optional):", key="insurance")
    
    preferred_days = st.multiselect("Preferred Days:", 
                                  ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                                  default=["Monday", "Wednesday", "Friday"])
    
    urgency = st.selectbox("Urgency Level:", 
                         ["Routine (within 2 weeks)", 
                          "Moderate (within 1 week)", 
                          "Urgent (within 2 days)"])
    
    if st.button("Find Specialists & Generate Email"):
        if not location:
            st.error("Please enter your location")
            return
            
        # Validate and normalize location
        location = location.strip().title()
        if len(location) < 3:
            st.error("Please enter a valid location (at least 3 characters)")
            return
            
        with st.spinner('Analyzing diagnosis and finding specialists...'):
            try:
                # Clear previous results
                if 'specialist_output' in st.session_state:
                    del st.session_state.specialist_output
                
                appointment_crew = create_appointment_crew(st.session_state.diagnosis, location)
                result = appointment_crew.kickoff()
                
                # Store raw output
                result_str = str(result)
                st.session_state.specialist_output = result_str
                
                # Display Reasoning Section if found
                if "### Reasoning Process" in result_str:
                    reasoning_content = result_str.split("### Reasoning Process")[1].split("### Final Recommendation")[0].strip()
                    with st.expander("🧠 Specialist Selection Reasoning", expanded=True):
                        st.markdown(reasoning_content)
                
                # Display Final Recommendation if found
                if "### Final Recommendation" in result_str:
                    recommendation_content = result_str.split("### Final Recommendation")[1].split("## Specialist Options:")[0].strip()
                    st.subheader("Recommended Specialist")
                    st.markdown(recommendation_content)
                
                # Display specialist options
                if "## Specialist Options:" in result_str:
                    specialist_section = result_str.split("## Specialist Options:")[1].split("## Email Draft:")[0].strip()
                    st.subheader("Specialist Options")
                    st.markdown(specialist_section)
                
                # Display email template with proper formatting
                if "## Email Draft:" in result_str:
                    email_content = result_str.split("## Email Draft:")[1].strip()
                    formatted_email = email_content.replace("{location}", location) \
                                                 .replace("{preferred_days}", ", ".join(preferred_days)) \
                                                 .replace("{urgency}", urgency)
                    st.subheader("Appointment Email Template")
                    st.code(formatted_email, language='text')
                    
                    st.button("📋 Copy Email Template", 
                             on_click=lambda: st.session_state.update({"copied": True}))
                    
                    if st.session_state.get("copied", False):
                        st.success("Template copied to clipboard!")
                
                # Add direct search links
                st.markdown(f"""
                ### You can also search directly:
                - [Google Search - Specialists in {location}](https://www.google.com/search?q=medical+specialist+in+{location.replace(" ", "+")})
                - [Zocdoc (US)](https://www.zocdoc.com/search?q=specialist&location={location.replace(" ", "+")})
                - [DabaDoc (Morocco)](https://www.dabadoc.com/ma/search?q=specialist&location={location.replace(" ", "+")})
                """)

            except json.JSONDecodeError as e:
                st.error("Failed to process specialist data. Please try again.")
                st.code(f"Error details: {repr(e)}", language="bash")
                
            except Exception as e:
                st.error("Appointment coordination encountered an error")
                
                # Get diagnosis text safely
                diagnosis_text = "[Brief description]"
                try:
                    if hasattr(st.session_state.diagnosis, 'output'):
                        # Handle TaskOutput object
                        diagnosis_text = str(st.session_state.diagnosis.output).split('\n')[0]
                    elif isinstance(st.session_state.diagnosis, str):
                        # Handle string directly
                        diagnosis_text = st.session_state.diagnosis.split('\n')[0]
                except:
                    pass
                
                # Get patient name safely
                patient_name = st.session_state.get('patient_info', {}).get('name', '[Your Name]')
                
                # Generate fallback email template
                email_template = f"""
                ### Appointment Email Template (Generic)
                ```text
                Subject: Appointment Request - Medical Consultation

                Body:
                Dear Dr. [Specialist's Name],

                I would like to schedule a consultation regarding:
                - Diagnosis: {diagnosis_text}
                - Location: {location}
                - Preferred Days: {', '.join(preferred_days)}
                - Urgency: {urgency}
                - Insurance: {st.session_state.get('insurance', 'Not specified')}

                Please contact me at your earliest convenience.

                Sincerely,
                {patient_name}
                [Your Phone Number]
                ```
                """
                st.markdown(email_template)

                # Add troubleshooting guidance
                st.markdown("""
                **Next Steps:**
                1. Try searching manually using the links below
                2. Contact your insurance provider for specialist recommendations
                3. Verify your location spelling (e.g., 'Casablanca' not 'casablanca')

                **Quick Search Links:**
                - [DabaDoc (Morocco)](https://www.dabadoc.com)
                - [Google Search](https://www.google.com/search?q=medical+specialist+in+{location})
                """.replace("{location}", location.replace(" ", "+")))
def main():
    # Initialize session state variables
    if 'diagnosis' not in st.session_state:
        st.session_state.diagnosis = None
    if 'treatment_plan' not in st.session_state:
        st.session_state.treatment_plan = None
    if 'patient_info' not in st.session_state:
        st.session_state.patient_info = None
    if 'specialist_output' not in st.session_state:
        st.session_state.specialist_output = None
        
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to:", ["Medical Diagnosis", "Specialist Referral"])
    
    # Sidebar disclaimer
    st.sidebar.warning("⚠️ Important Disclaimer: This AI provides preliminary information only.")
    
    # Render selected page
    if page == "Medical Diagnosis":
        render_diagnosis_page()
    else:
        render_appointment_page()

if __name__ == "__main__":
    main()