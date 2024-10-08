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

    def check_password(self, password):
        """Check if password meets all security criteria."""
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):  # At least one uppercase letter
            return False
        if not re.search(r'[a-z]', password):  # At least one lowercase letter
            return False
        if not re.search(r'[0-9]', password):  # At least one digit
            return False
        if not re.search(r'[\W_]', password):  # At least one special character
            return False
        return True

    def check_status_and_validate(self):
        """Check the status, validate email, password, and approve or reject if conditions are met."""
        results = []
        pending_users = []

        while True:
            try:
                table = self.driver.find_element(By.ID, "userTable")
                rows = table.find_elements(By.TAG_NAME, "tr")

                if len(rows) <= 1:  # No more users to process
                    print("No pending users found.")
                    break

                # Collect pending users
                for i in range(1, len(rows)):  # Start from 1 to skip the header
                    columns = rows[i].find_elements(By.TAG_NAME, "td")

                    if len(columns) > 0:
                        user_id = columns[0].text
                        username = columns[1].text
                        email = columns[2].text
                        password_plaintext = columns[3].text
                        status = columns[6].text

                        if "pending" in status.lower():
                            pending_users.append((username, email, password_plaintext))

                # Break the loop if no pending users were found
                if not pending_users:
                    print("No pending users found.")
                    break

                # Now process all pending users together
                for username, email, password in pending_users:
                    print(f"Evaluating user: {username}")

                    if self.check_email(email) and self.check_password(password):
                        print(f"User {username} meets all conditions. Approving user...")
                        self.approve_user_by_username(username, results)
                    else:
                        print(f"User {username} does not meet the conditions. Rejecting user...")
                        self.reject_user_by_username(username, results)

                    # Wait for a moment after processing each user
                    time.sleep(0.5)

                # Refresh the table to get the updated user list
                self.driver.refresh()
                time.sleep(1)  # Wait for the page to fully load

                # Optionally, run the Robot Framework command after processing all users
                self.run_robot_command()

                break  # Exit after processing all pending users

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




if __name__ == "__main__":
    url = "http://localhost/portal/frontend/dashboard.php"  # Replace with your actual URL
    check_status = CheckStatusLibrary()
    check_status.open_browser(url)
    results = check_status.check_status_and_validate()
    print(results)
    # Move the browser closing here to close after all users are processed
    check_status.close_browser()
