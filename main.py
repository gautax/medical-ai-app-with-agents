from interface.streamlit_app import main
import streamlit as st

if __name__ == "__main__":
    st.session_state.setdefault('diagnosis', '')
    main()