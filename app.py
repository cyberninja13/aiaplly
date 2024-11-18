import streamlit as st
from selenium import webdriver
import undetected_chromedriver.v2 as uc
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import pdfplumber
import docx2txt
from io import BytesIO

# Function to process the uploaded CV (PDF or DOCX)
def process_cv(uploaded_file):
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    if file_extension == 'pdf':
        # Process PDF
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        return text
    
    elif file_extension == 'docx':
        # Process DOCX
        text = docx2txt.process(uploaded_file)
        return text
    
    else:
        return "Unsupported file format. Please upload a PDF or DOCX file."

# Function to start the automation process
def start_automation(url):
    try:
        # Set up Chrome options
        options = uc.ChromeOptions()

        # For cloud environments (like Streamlit), ensure Chrome is installed.
        # You may specify the binary location if needed.
        if 'CHROME_BIN' in os.environ:
            options.binary_location = os.environ['CHROME_BIN']  # For cloud setups like Streamlit
        else:
            # For local development (Windows path), specify the path to Chrome binary
            options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Adjust if needed

        # Use WebDriver Manager to install the correct version of ChromeDriver
        driver = uc.Chrome(executable_path=ChromeDriverManager().install(), options=options)

        # Visit the URL for automation
        driver.get(url)
        st.write(f"Automation started! Opened URL: {driver.current_url}")

        # Optional: Perform further actions like clicking, scraping, etc.
        # Example:
        # element = driver.find_element_by_xpath("your_xpath_here")
        # element.click()

        # Close the driver when done
        driver.quit()

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.stop()

# Streamlit user interface
st.title("Automation with Streamlit and Selenium")

# File upload for CV
uploaded_file = st.file_uploader("Upload your CV (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file is not None:
    st.write("File uploaded successfully!")
    cv_text = process_cv(uploaded_file)
    st.text_area("Extracted CV Text", cv_text, height=300)

# Input for URL to automate
url_input = st.text_input("Enter the URL to automate", placeholder="https://example.com")

# Button to start the automation
if st.button('Start Automation') and url_input:
    st.write(f"Starting automation on {url_input}...")
    start_automation(url_input)
