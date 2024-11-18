import streamlit as st
from selenium import webdriver
import undetected_chromedriver.v2 as uc
from webdriver_manager.chrome import ChromeDriverManager
import os

# Function to start the automation
def start_automation():
    # Detect the environment (cloud or local)
    try:
        # Set up options for Chrome
        options = uc.ChromeOptions()

        # For cloud environments (like Streamlit), ensure Chrome is installed.
        # This is where you may specify the path to the Chrome binary if needed.
        if 'CHROME_BIN' in os.environ:
            options.binary_location = os.environ['CHROME_BIN']
        else:
            # For local development, specify the path to Chrome (Windows example)
            options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Adjust path if needed
        
        # Use the WebDriver Manager to automatically install the correct version of ChromeDriver
        driver = uc.Chrome(executable_path=ChromeDriverManager().install(), options=options)
        
        # Perform automation task (replace with your task)
        driver.get("https://example.com")
        st.write(f"Automation started! Opened URL: {driver.current_url}")
        
        # Close the driver when done
        driver.quit()

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.stop()

# Streamlit UI code
st.title("Automation with Streamlit")

if st.button('Start Applying'):
    st.write("Starting automation...")
    start_automation()
