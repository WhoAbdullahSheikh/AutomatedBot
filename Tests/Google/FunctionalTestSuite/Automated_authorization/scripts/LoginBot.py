import requests


def login(username, password):
    url = "http://localhost/portal/frontend/bot_login.php"  # Adjust to your actual URL
    payload = {
        'username': username,
        'password': password
    }
    response = requests.post(url, data=payload)

    if "Invalid username or password" in response.text:
        print("Login failed!")
    else:
        print("Login successful!")


if __name__ == "__main__":
    login("user", "pass")  # Replace with valid credentials
