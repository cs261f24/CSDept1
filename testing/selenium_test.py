import pytest
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Steps to run these tests:
# 1. Enter a virtual environment.
# 2. Install Selenium and pytest: `pip install selenium pytest`.
# 3. Start Flask in the command line where Flask is installed: `flask run`.
# 4. Run pytest on python file you would like to test 

# Initialize the Chrome driver
@pytest.fixture(scope="module")
def setup():
    # Sets up the webdriver
    driver = webdriver.Chrome()
    driver.get('http://127.0.0.1:5000')  
    # Allows the driver to run all tests
    yield driver
    # Closes the browser once test is complete 
    driver.quit()

def test_student_login(setup):
    driver = setup
    
    # Go to the registration page
    registration_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Register here"))
    )
    registration_link.click()

    # Fill out the registration form
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'first_name'))).send_keys("Test")  # First Name
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'last_name'))).send_keys("Test")  # Last Name
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys("CSDeptBOT@gmail.com")  # Email
    driver.find_element(By.NAME, "password").send_keys("password")  # Password
    driver.find_element(By.NAME, "confirm_password").send_keys("password")  # Confirm password

    # Select student role
    driver.find_element(By.ID, "student").click()  # Click the student radio button

    # Submit the registration form
    driver.find_element(By.CSS_SELECTOR, ".form-button").click()

    # Wait for a moment to ensure registration is processed
    WebDriverWait(driver, 10).until(EC.url_changes("http://127.0.0.1:5000"))  # Wait for URL change after registration

    # Log in with the registered account
    driver.get("http://127.0.0.1:5000")  # Go back to the login page

    # Fill out the login form
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("CSDeptBOT@gmail.com")  # Email
    driver.find_element(By.NAME, "password").send_keys("password") 

    # Click the login button
    driver.find_element(By.CSS_SELECTOR, ".form-button").click() 

    # Wait for the login to process and verify you're on the right page
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".welcome-message")) 
    )

    # Remove the logout code
    # driver.find_element(By.LINK_TEXT, "Logout").click()  # This line has been removed

    # Optional: Wait to observe the result
    time.sleep(2)  # If you want to see the final state before the test ends


def test_open_events_page(setup):
    driver = setup

    # Go to the Events page
    driver.get("http://127.0.0.1:5000/events")

    # Wait for the input field for the event name to ensure it has loaded
    event_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.NAME, "event_name"))
    )
    
    # Add an event named "Test"
    event_name = "Test"
    event_input.clear()
    event_input.send_keys(event_name)
    
    # Submit the event form
    driver.find_element(By.CSS_SELECTOR, "form[action='/events'] button[type='submit']").click()
    
    # Wait for the event to be added to the list
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, f"//li[contains(text(), '{event_name}')]"))
    )

    # Now remove the event
    remove_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{event_name}')]//following-sibling::form/button"))
    )
    remove_button.click()

    # Wait for the event to be removed from the list
    WebDriverWait(driver, 15).until(
        EC.invisibility_of_element_located((By.XPATH, f"//li[contains(text(), '{event_name}')]"))
    )

    # Optional: Pause to observe the result before closing
    time.sleep(2)
    
def test_filter_reports(setup):
    driver = setup

    # Navigate to the Reports page
    driver.get("http://127.0.0.1:5000/reports")
    
    # Pause to observe the page
    time.sleep(2)


    # Filter by Student Name (e.g., "Dan")
    student_name_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "search"))
    )
    student_name_input.clear()  # Clear any pre-filled value if necessary
    student_name_input.send_keys("Dan")  # Enter the name to filter by

    # Submit the search form
    driver.find_element(By.CSS_SELECTOR, ".search-form button[type='submit']").click()

    # Pause to observe the results for "Dan"
    time.sleep(2)

    # Deselect "Dan" by clearing the input field
    student_name_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "search"))
    )
    student_name_input.clear()  # Clear the name input to deselect "Dan"

    # Submit the search form again to show all results
    driver.find_element(By.CSS_SELECTOR, ".search-form button[type='submit']").click()

    # Pause to confirm all results are displayed
    time.sleep(2) 

    # Now filter by Event Type (specifically for "Club events")
    event_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "event_type"))
    )
    event_dropdown.click()  # Click the dropdown to show options

    # Select "Club" from the dropdown
    club_option = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//option[text()='Club']"))
    )
    club_option.click()

    # Submit the filter form again
    driver.find_element(By.CSS_SELECTOR, ".filter-button").click()

    # Pause to observe the filtered results
    time.sleep(2)


