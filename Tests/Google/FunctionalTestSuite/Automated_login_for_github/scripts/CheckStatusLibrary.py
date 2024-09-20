# CheckStatusLibrary.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class CheckStatusLibrary:
    def __init__(self):
        self.driver = None

    def open_browser(self, url):
        """Open a browser and navigate to the given URL."""
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get(url)
        time.sleep(3)  # Wait for the page to load

    def check_status(self):
        """Check the status from the user management dashboard and return the status message."""
        try:
            # Locate the user table (by ID) and all rows inside it
            table = self.driver.find_element(By.ID, "userTable")
            rows = table.find_elements(By.TAG_NAME, "tr")

            # Iterate over the rows (skip the header)
            for row in rows[1:]:  # Start from index 1 to skip the header row
                columns = row.find_elements(By.TAG_NAME, "td")

                if len(columns) > 0:
                    # Get the user ID, username, email, and status from the row
                    user_id = columns[0].text
                    username = columns[1].text
                    email = columns[2].text
                    status = columns[4].text  # Status is in the 5th column

                    # Print out user details
                    print(f"User ID: {user_id}, Username: {username}, Email: {email}, Status: {status}")

                    # Check if the status is 'approved'
                    if "approved" in status.lower():
                        return "Approved"
                    else:
                        return "Not Approved"

        except Exception as e:
            print(f"An error occurred: {e}")
            return "Error"

    def close_browser(self):
        """Close the browser."""
        if self.driver:
            self.driver.quit()
