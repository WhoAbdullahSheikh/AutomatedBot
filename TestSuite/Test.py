from selenium import webdriver
import time

# Initialize the WebDriver
driver = webdriver.Chrome()

# Open the first URL
driver.get("http://example.com")
print("First window title:", driver.title)

# Open a new tab/window and navigate to another URL
driver.execute_script("window.open('http://google.com', '_blank');")
time.sleep(2)  # Wait for the new window to open

# Get the window handles
window_handles = driver.window_handles

# Switch to the second window (Google)
driver.switch_to.window(window_handles[1])
print("Second window title:", driver.title)

# Perform actions in the second window
# Example: Search for something
search_box = driver.find_element("name", "q")
search_box.send_keys("Selenium Python")
search_box.submit()

time.sleep(3)  # Wait for results

# Switch back to the first window
driver.switch_to.window(window_handles[0])
print("Back to first window title:", driver.title)

# Close the driver
driver.quit()
