import streamlit as st
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Title of the app
st.title("Workable Easy Apply Bot")

# Collect user details for the application
full_name = st.text_input("Enter your Full Name:")
email = st.text_input("Enter your Email Address:")
phone = st.text_input("Enter your Phone Number:")
uploaded_cv = st.file_uploader("Upload your CV (PDF or DOCX)", type=["pdf", "docx"])

# Workable Jobs Search URL
workable_jobs_url = st.text_input("Enter Workable Jobs Search URL")

# Start Button
if st.button("Start Applying"):
    if not (uploaded_cv and workable_jobs_url and full_name and email and phone):
        st.error("Please fill all required fields and upload your CV!")
    else:
        st.info("Starting automation...")

        # Configure undetected_chromedriver
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Headless mode for cloud
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Automatically download and use the correct chromedriver
        chromedriver_path = ChromeDriverManager(version="120.0.6099.224").install()

        driver = None
        try:
            # Initialize undetected_chromedriver with options
            driver = uc.Chrome(options=options, driver_executable_path=chromedriver_path)
            st.success("WebDriver successfully initialized!")

            # Navigate to Workable Jobs Page
            driver.get(workable_jobs_url)
            time.sleep(3)  # Wait for the page to load

            # Find job listings with "Apply" buttons
            apply_buttons = driver.find_elements(By.XPATH, "//a[contains(text(), 'Apply')]")
            st.write(f"Found {len(apply_buttons)} jobs with Apply buttons!")

            # Simulate applying to jobs
            for i, button in enumerate(apply_buttons[:5]):  # Limit to first 5 jobs
                try:
                    # Open the job application page
                    button.click()
                    time.sleep(3)  # Wait for the application page to load

                    # Fill in the application form fields dynamically
                    st.write(f"Applying to job {i + 1}...")
                    try:
                        # Fill in name
                        name_field = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.NAME, "name"))
                        )
                        name_field.clear()
                        name_field.send_keys(full_name)

                        # Fill in email
                        email_field = driver.find_element(By.NAME, "email")
                        email_field.clear()
                        email_field.send_keys(email)

                        # Fill in phone
                        phone_field = driver.find_element(By.NAME, "phone")
                        phone_field.clear()
                        phone_field.send_keys(phone)

                        # Upload CV
                        cv_field = driver.find_element(By.XPATH, "//input[@type='file']")
                        cv_file_path = "/tmp/uploaded_cv.pdf"  # Temporary path to save uploaded CV
                        with open(cv_file_path, "wb") as f:
                            f.write(uploaded_cv.getbuffer())
                        cv_field.send_keys(cv_file_path)

                        # Submit the form
                        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                        submit_button.click()
                        st.write(f"Successfully applied to job {i + 1}!")
                    except Exception as form_error:
                        st.warning(f"Error filling the form for job {i + 1}: {form_error}")
                    
                    # Navigate back to the job list
                    driver.back()
                    time.sleep(3)
                except Exception as job_error:
                    st.warning(f"Error applying to job {i + 1}: {job_error}")

            st.success("Automation completed!")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        finally:
            if driver:
                driver.quit()
