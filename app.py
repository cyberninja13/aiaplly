import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import os

# Title of the app
st.title("Workable Easy Apply Bot")

# Upload CV
uploaded_cv = st.file_uploader("Upload your CV (PDF, DOC, DOCX, ODT, RTF)", type=["pdf", "doc", "docx", "odt", "rtf"])

# Workable Jobs Link
workable_jobs_url = st.text_input("Enter Workable Jobs URL")

# Additional information
first_name = st.text_input("First Name", "John")
last_name = st.text_input("Last Name", "Doe")
email = st.text_input("Email", "john.doe@example.com")
headline = st.text_input("Headline", "Software Engineer")
phone = st.text_input("Phone", "+966512345678")
address = st.text_input("Address", "Dammam, Saudi Arabia")
current_salary = st.text_input("Current Salary (SAR)", "5000")
notice_period = st.text_input("Notice Period (e.g., 1 month)", "1 month")

# Start Button
if st.button("Start Applying"):
    if not uploaded_cv or not workable_jobs_url:
        st.error("Please upload your CV and provide the Workable jobs link!")
    else:
        st.info("Starting automation...")

        # Configure Chrome Options
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode for cloud
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Initialize WebDriver with Service
        service = Service(ChromeDriverManager().install())
        driver = None

        try:
            driver = webdriver.Chrome(service=service, options=options)
            st.success("WebDriver successfully initialized!")

            # Navigate to Workable Jobs Page
            driver.get(workable_jobs_url)
            time.sleep(3)  # Wait for the page to load

            # Find application links
            job_links = driver.find_elements(By.XPATH, '//a[contains(@href, "apply")]')
            st.write(f"Found {len(job_links)} jobs with Easy Apply!")

            # Automate application submission
            for i, job_link in enumerate(job_links[:5]):  # Limit to first 5 jobs
                st.write(f"Applying to job {i + 1}...")
                job_url = job_link.get_attribute("href")
                driver.get(job_url)
                time.sleep(3)  # Wait for the application page to load

                # Fill in the application form
                try:
                    driver.find_element(By.NAME, "name").send_keys(first_name)
                    driver.find_element(By.NAME, "surname").send_keys(last_name)
                    driver.find_element(By.NAME, "email").send_keys(email)
                    driver.find_element(By.NAME, "headline").send_keys(headline)
                    driver.find_element(By.NAME, "phone").send_keys(phone)
                    driver.find_element(By.NAME, "address").send_keys(address)

                    # Upload Resume
                    cv_path = os.path.abspath(uploaded_cv.name)
                    driver.find_element(By.NAME, "resume").send_keys(cv_path)

                    driver.find_element(By.NAME, "current_salary").send_keys(current_salary)
                    driver.find_element(By.NAME, "notice_period").send_keys(notice_period)

                    # Submit the application
                    submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
                    submit_button.click()
                    st.write(f"Successfully applied to job {i + 1}!")

                except Exception as e:
                    st.error(f"Failed to apply to job {i + 1}: {str(e)}")

                # Go back to the job list
                driver.get(workable_jobs_url)
                time.sleep(2)

            st.success("Automation completed!")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        finally:
            if driver:
                driver.quit()
