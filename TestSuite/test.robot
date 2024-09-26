*** Settings ***
Library    ./LoginBot.py  # Adjust the path as necessary
Library    SeleniumLibrary

*** Variables ***
${LOGIN_URL}    http://localhost/portal/frontend/bot_login.html
${DASHBOARD_URL}    http://localhost/portal/frontend/dashboard.php
${USERNAME}    user
${PASSWORD}    pass

*** Test Cases ***
Login and Visit Dashboard
    [Documentation]    Test to log in and visit the dashboard.
    # Step 1: Open the login page
    LoginBot.Open Browser    ${LOGIN_URL}

    # Step 2: Log in with provided credentials
    Login    ${USERNAME}    ${PASSWORD}

    # Step 3: Visit the dashboard
    Visit Dashboard    ${DASHBOARD_URL}

    # Step 4: Close the browser
    LoginBot.Close Browser

*** Keywords ***
Login
    [Arguments]    ${username}    ${password}
    LoginBot.Login    ${username}    ${password}

Visit Dashboard
    [Arguments]    ${dashboard_url}
    LoginBot.Visit Dashboard    ${dashboard_url}
