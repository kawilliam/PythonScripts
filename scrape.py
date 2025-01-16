from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import unquote
import time

# Initialize the browser
driver = webdriver.Chrome()

# Step 1: Log in to eClass
print("Logging into eClass...")
driver.get("https://eclass.yorku.ca/user/index.php?id=125101")

# Fill in login credentials
username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mli")))  # Update ID based on the login page
password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))  # Update ID based on the login page
username_field.send_keys("kawil")
password_field.send_keys("ryhtam-wikZon-3somha")
password_field.send_keys(Keys.RETURN)

# Wait for login to complete
time.sleep(20)

# Step 2: Navigate to the Participants Page
print("Navigating to participants page...")
driver.get("https://eclass.yorku.ca/user/index.php?id=125101")




# Step 3: Visit Each Profile and Extract Emails
emails = []
try:
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Show all 114")]')))
    button.click()
    time.sleep(5)
except Exception as e:
    print("No button.")

print("Scraping current page...")
participant_links = driver.find_elements(By.XPATH, '//td[contains(text(), "Student")]/preceding-sibling::th/a[contains(@href, "/user/view.php?id=")]')  # Adjust the XPath as needed
profile_urls = [link.get_attribute("href") for link in participant_links]
for url in profile_urls:
    driver.get(url)
    time.sleep(0.5)  # Wait for the page to load
    try:
                    # Find the email element on the profile page
        email_element = driver.find_element(By.XPATH, '//dd/a[contains(@href, "mailto:")]')
        email_encoded = email_element.get_attribute("href").replace("mailto:", "")
        email = unquote(email_encoded)
        emails.append(email)
        print(f"Found email: {email}")
    except Exception as e:
        print(f"Email not found on {url}")
    
# Step 4: Save Emails to a File
print("Saving emails to file...")
with open("/Users/kylewilliamson/Library/Mobile Documents/com~apple~CloudDocs/Documents/Python stuff/emails.txt", "w") as f:
    for email in emails:
        f.write(email + "\n")

# Close the browser
driver.quit()