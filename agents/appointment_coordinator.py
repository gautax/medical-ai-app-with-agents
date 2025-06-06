from crewai import Agent
from utils.config import admin_llm, search_tool

def create_appointment_coordinator():
    agent = Agent(
        role="Appointment Coordinator",
        goal="""Find specialist contact information and generate appointment emails
        Output MUST contain:
        ## Specialist Options:
        - [Name], [Clinic/Hospital], [Contact], [Location]
        
        ## Email Draft:
        Subject: Appointment Request - [Specialty]
        Body: [FULLY COMPLETED TEMPLATE]
        
        ## Next Steps:
        [Clear instructions]""",
        backstory="""Medical administrative assistant with expertise in navigating healthcare systems 
        and booking platforms across Morocco""",
        tools=[search_tool],
        llm=admin_llm,
        verbose=True,
        allow_delegation=False,
        max_iter=5,  # Limit search attempts
        memory=True  # Remember previous search attempts
    )
    
    # Add debug callbacks
    def tool_start_callback(tool, input):
        print(f"🔧 Using {tool.name} with input: {input}")
        
    def tool_end_callback(output):
        print(f"✅ Tool output: {output[:200]}...")
        
    agent.callbacks.on_tool_start = tool_start_callback
    agent.callbacks.on_tool_end = tool_end_callback
    
    return agent