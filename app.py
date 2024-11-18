import streamlit as st
from selenium import webdriver
import undetected_chromedriver as uc
import time
import os

# Title of the app
st.title("LinkedIn Easy Apply Bot")

# Upload CV
uploaded_cv = st.file_uploader("Upload your CV (PDF or DOCX)", type=["pdf", "docx"])

# LinkedIn Jobs Link
linkedin_jobs_url = st.text_input("Enter LinkedIn Jobs URL (with Easy Apply options)")

# Start Button
if st.button("Start Applying"):
    if not uploaded_cv or not linkedin_jobs_url:
        st.error("Please upload your CV and provide the LinkedIn jobs link!")
    else:
        st.info("Starting automation...")

        # Configure undetected_chromedriver
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Headless mode for cloud
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Specify the path to the Chrome browser executable (adjust based on your environment)
        chrome_executable_path = "/usr/bin/google-chrome-stable"  # Change this if necessary
        options.binary_location = chrome_executable_path

        driver = None
        try:
            # Initialize undetected_chromedriver with options and executable path
            driver = uc.Chrome(options=options, driver_executable_path="/usr/local/bin/chromedriver")  # Specify path to chromedriver if needed
            st.success("WebDriver successfully initialized!")

            # Navigate to LinkedIn Jobs Page
            driver.get(linkedin_jobs_url)
            time.sleep(3)  # Wait for the page to load

            # Example: Find Easy Apply Buttons
            easy_apply_buttons = driver.find_elements("class name", "jobs-apply-button")
            st.write(f"Found {len(easy_apply_buttons)} jobs with Easy Apply!")

            # Simulate applying to jobs
            for i, button in enumerate(easy_apply_buttons[:5]):  # Limit to first 5 jobs
                button.click()
                time.sleep(2)  # Wait for the application modal to load
                st.write(f"Applied to job {i + 1}!")
                driver.back()
                time.sleep(2)

            st.success("Automation completed!")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        finally:
            if driver:
                driver.quit()
