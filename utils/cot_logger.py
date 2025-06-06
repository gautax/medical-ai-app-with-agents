import streamlit as st

def log_cot_step(step):
    """Callback function to log Chain-of-Thought steps"""
    if not hasattr(st.session_state, 'cot_log'):
        st.session_state.cot_log = ""
    
    # Only log the reasoning steps, not tool executions
    if "reasoning" in step.lower() or "step" in step.lower():
        st.session_state.cot_log += f"\n\n{step}"