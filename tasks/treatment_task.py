from crewai import Task

def create_treatment_task(treatment_advisor, patient_info, diagnosis_task):
    return Task(
        description=f"""Create personalized treatment plan for:
        Patient Profile: {patient_info['age']}y/o {patient_info['sex']}, {patient_info['weight']}kg, {patient_info['height']}cm
        Known Allergies: {patient_info['allergies']}
        Current Medications: {patient_info['medications']}
        Based on this diagnosis: {{diagnosis}}""",
        expected_output="""Comprehensive plan including:
        - First-line treatments (with dosage adjustments)
        - Contraindications checking
        - Medication interaction warnings
        - Lifestyle modifications
        - Follow-up schedule
        - Red flags to watch for""",
        agent=treatment_advisor,
        context=[diagnosis_task]
    )