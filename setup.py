from setuptools import setup, find_packages

setup(
    name="medical_ai_app",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'crewai',
        'python-dotenv',
        'python-docx'
    ],
)