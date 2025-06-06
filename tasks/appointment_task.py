from crewai import Task

def create_appointment_task(agent, location, context=None):
    return Task(
        description=f"""Find medical specialists in {location} and create appointment request materials:
        1. Use the search_tool to find appropriate specialists using queries like:
           - "Top [specialty] specialists in {location}"
           - "Best hospitals for [condition] in {location}"
        2. Gather available contact information from search results
        3. Prepare clear instructions for booking
        4. Create email template with placeholders
        
        Important: Always use the search_tool for finding specialist information!""",
        expected_output="""Format your response clearly with these sections:
        
        ## Specialist Options:
        List any available specialist information including:
        - Names
        - General location
        - Booking links (when available)
        
        ## Email Draft:
        Create a professional email template with placeholders
        
        ## Next Steps:
        Provide clear instructions for the patient""",
        agent=agent,
        context=context
    )