from crewai import Agent
from utils.config import admin_llm, search_tool

def create_specialist_referral():
    agent = Agent(
        role="Specialist Referral Coordinator",
        goal="Recommend medical specialists based on diagnosis with clear reasoning",
        backstory="Medical referral expert with 10+ years matching patients to specialists",
        tools=[search_tool],
        llm=admin_llm,
        verbose=True,
        reasoning=True,  # Enable CoT reasoning
        max_reasoning_attempts=3,  # Number of refinement attempts
        memory=True
    )
    
    # Add debug callbacks
    def tool_start_callback(tool, input):
        print(f"🔧 Using {tool.name} with input: {input}")
        
    def tool_end_callback(output):
        print(f"✅ Tool output: {output[:200]}...")
        
    agent.callbacks.on_tool_start = tool_start_callback
    agent.callbacks.on_tool_end = tool_end_callback
    
    return agent