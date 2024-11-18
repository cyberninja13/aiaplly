import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

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

        # Configure Selenium WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Headless mode for cloud deployment
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # Start WebDriver
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            st.success("WebDriver successfully initialized!")
            
            # Navigate to LinkedIn Jobs Page
            driver.get(linkedin_jobs_url)
            time.sleep(3)  # Wait for page to load
            
            # Example: Find Easy Apply Buttons
            easy_apply_buttons = driver.find_elements(By.CLASS_NAME, "jobs-apply-button")
            st.write(f"Found {len(easy_apply_buttons)} jobs with Easy Apply!")

            # Simulate applying to jobs (this is just a placeholder logic)
            for i, button in enumerate(easy_apply_buttons[:5]):  # Limit to first 5 jobs
                button.click()
                time.sleep(2)  # Wait for the application modal to load
                st.write(f"Applied to job {i + 1}!")
                # Add more detailed logic here if needed
                driver.back()
                time.sleep(2)

            st.success("Automation completed!")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        finally:
            driver.quit()
