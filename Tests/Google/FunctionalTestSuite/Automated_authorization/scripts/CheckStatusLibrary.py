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

        while True:
            try:
                table = self.driver.find_element(By.ID, "userTable")
                rows = table.find_elements(By.TAG_NAME, "tr")

                if len(rows) <= 1:  # No more users to process
                    print("No pending users found.")
                    break

                processed_any_user = False  # Flag to check if any user was processed this iteration

                for i in range(1, len(rows)):
                    columns = rows[i].find_elements(By.TAG_NAME, "td")

                    if len(columns) > 0:
                        user_id = columns[0].text
                        username = columns[1].text
                        email = columns[2].text
                        password_plaintext = columns[3].text
                        status = columns[6].text

                        print(
                            f"User ID: {user_id}, Username: {username}, Email: {email}, Status: {status}, Password: {password_plaintext}")

                        if "pending" in status.lower():
                            processed_any_user = True
                            if self.check_email(email) and self.check_password(password_plaintext):
                                print(f"User {username} meets all conditions. Approving user...")
                                self.approve_user(rows[i], username, results)
                                self.run_robot_command()  # Run the Robot Framework command after approval
                            else:
                                print(f"User {username} does not meet the conditions. Rejecting user...")
                                self.reject_user(rows[i], username, results)
                                self.run_robot_command()  # Run the Robot Framework command after rejection

                # Wait for a moment for updates to reflect
                WebDriverWait(self.driver, 5).until(EC.staleness_of(rows[1]))

                # If no user was processed in this iteration, break the loop
                if not processed_any_user:
                    print("All users have been processed.")
                    break

            except Exception as e:
                print(f"Error processing users: {e}")
                break

        return results

    def approve_user(self, row, username, results):
        """Approve the user."""
        try:
            approve_button = row.find_element(By.XPATH, ".//button[@name='action' and @value='approve']")
            approve_button.click()
            WebDriverWait(self.driver, 10).until(EC.staleness_of(approve_button))
            results.append(f"{username} approved.")
        except Exception as e:
            print(f"Error approving {username}: {e}")

    def reject_user(self, row, username, results):
        """Reject the user."""
        try:
            reject_button = row.find_element(By.XPATH, ".//button[@name='action' and @value='reject']")
            reject_button.click()
            WebDriverWait(self.driver, 10).until(EC.staleness_of(reject_button))
            results.append(f"{username} rejected.")
        except Exception as e:
            print(f"Error rejecting {username}: {e}")

    def run_robot_command(self):
        """Run the Robot Framework command with a unique output directory."""
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        results_dir = f"Results_Logs/results_{timestamp}"
        os.makedirs(results_dir, exist_ok=True)  # Create a new results directory

        command = ["robot", "-d", results_dir,
                   "Tests/google/functionaltestsuite/automated_authorization/Tasks.robot"]
        try:
            subprocess.run(command, check=True)
            print(f"Robot Framework tests executed. Results stored in '{results_dir}'.")
        except Exception as e:
            print(f"Error running Robot Framework command: {e}")

    def close_browser(self):
        """Close the browser."""
        if self.driver:
            self.driver.quit()
