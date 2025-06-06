from crewai import Task
from pydantic import BaseModel

class ReferralOutput(BaseModel):
    reasoning: str
    specialist_type: str
    urgency: int
    justification: str

def create_specialist_referral_task(agent, diagnosis):
    return Task(
        description=f"""Analyze this diagnosis to determine the appropriate specialist type:
        {diagnosis}

        You MUST follow this reasoning process:
        1. Identify key symptoms and conditions
        2. Determine which medical specialties treat these conditions
        3. Consider patient factors (age, severity, medical history)
        4. Use the search_tool to verify specialist availability
        5. Select the most appropriate specialist type
        6. Justify your recommendation with medical evidence
        
        Important: Use search_tool to validate your recommendation!""",
        expected_output="""### Reasoning Process
        [Your step-by-step analysis including search validation]

        ### Final Recommendation
        - Specialist Type: [Cardiologist/Neurologist/etc.]
        - Urgency Level: [1-5]
        - Justification: [Detailed explanation]""",
        agent=agent,
        output_json=ReferralOutput
    )