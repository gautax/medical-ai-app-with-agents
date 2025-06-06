from crewai import Task

def create_diagnosis_task(diagnostician, patient_info):
    return Task(
        description=f"""Analyze these symptoms considering patient context:
        Patient: {patient_info['age']}y/o {patient_info['sex']}, {patient_info['weight']}kg, {patient_info['height']}cm
        Symptoms: {patient_info['symptoms']} (Duration: {patient_info['symptom_duration']}, Severity: {patient_info['symptom_severity']}/10)
        History: {patient_info['history']}
        Allergies: {patient_info['allergies']}
        Medications: {patient_info['medications']}
        Family History: {patient_info['family_history']}""",
        expected_output="""Top 3 differential diagnoses with:
        - Confidence percentages
        - Key diagnostic criteria
        - Recommended tests
        - Risk factors from patient profile""",
        agent=diagnostician
    )