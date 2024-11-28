from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import os
import subprocess
import time


class CheckStatusLibrary:
    def __init__(self):
        self.driver = None

    def open_browser(self, url):
        """Open a browser and navigate to the given URL in fullscreen mode."""
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()  # Open browser in fullscreen mode
        self.driver.get(url)

    def check_email(self, email):
        """Check if email is valid using a general email pattern."""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None

    @staticmethod
    def check_password(password):
        special_characters = r'[!@#$%^&*(),.?":{}|<>]'
        print(f"Checking password: {password}")
        result = (len(password) >= 8 and
                  any(c.isupper() for c in password) and
                  any(c.islower() for c in password) and
                  any(c.isdigit() for c in password) and
                  re.search(special_characters, password))

        if not result:
            print(f"Password check failed for: {password}")

        return result

    def check_status_and_validate(self):
        """Check the status, validate email, password, and approve or reject if conditions are met."""
        results = []
        pending_users = []

        while True:
            try:
                table = self.driver.find_element(By.ID, "userTable")
                rows = table.find_elements(By.TAG_NAME, "tr")

                if len(rows) <= 1:
                    print("No pending users found.")
                    break

                for i in range(1, len(rows)):
                    columns = rows[i].find_elements(By.TAG_NAME, "td")

                    if len(columns) > 0:
                        user_id = columns[0].text
                        username = columns[1].text
                        email = columns[2].text.strip()
                        password_plaintext = columns[3].text.strip()
                        status = columns[6].text

                        if "pending" in status.lower():
                            pending_users.append((username, email, password_plaintext))

                if not pending_users:
                    print("No pending users found.")
                    break

                for username, email, password in pending_users:
                    print(f"Evaluating user: {username}")

                    email_valid = self.check_email(email)
                    password_valid = self.check_password(password)

                    if email_valid and password_valid:
                        print(f"User {username} meets all conditions. Approving user...")
                        self.approve_user_by_username(username, results)
                    else:
                        print(f"User {username} does not meet the conditions. Rejecting user...")
                        if not email_valid:
                            print(f"Invalid email: {email}")
                        if not password_valid:
                            print(f"Invalid password: {password}")
                        self.reject_user_by_username(username, results)

                    time.sleep(0)

                self.driver.refresh()
                time.sleep(0.5)

                break

            except Exception as e:
                print(f"Error processing users: {e}")
                break

        return results

    def approve_user_by_username(self, username, results):
        """Approve the user by username."""
        try:
            table = self.driver.find_element(By.ID, "userTable")
            rows = table.find_elements(By.TAG_NAME, "tr")

            for row in rows:
                columns = row.find_elements(By.TAG_NAME, "td")
                if len(columns) > 0 and columns[1].text == username:
                    approve_button = row.find_element(By.XPATH, ".//button[@name='action' and @value='approve']")
                    approve_button.click()
                    WebDriverWait(self.driver, 10).until(EC.staleness_of(approve_button))
                    results.append(f"{username} approved.")
                    break

        except Exception as e:
            print(f"Error approving {username}: {e}")

    def reject_user_by_username(self, username, results):
        """Reject the user by username."""
        try:
            table = self.driver.find_element(By.ID, "userTable")
            rows = table.find_elements(By.TAG_NAME, "tr")

            for row in rows:
                columns = row.find_elements(By.TAG_NAME, "td")
                if len(columns) > 0 and columns[1].text == username:
                    reject_button = row.find_element(By.XPATH, ".//button[@name='action' and @value='reject']")
                    reject_button.click()
                    WebDriverWait(self.driver, 10).until(EC.staleness_of(reject_button))
                    results.append(f"{username} rejected.")
                    break

        except Exception as e:
            print(f"Error rejecting {username}: {e}")
