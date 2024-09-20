*** Settings ***
Library    SeleniumLibrary
Library    ./scripts/CheckStatusLibrary.py  # Import the custom Python library
Suite Teardown    No Operation    # Prevents automatic browser closure in teardown
Test Teardown     No Operation    # Ensures no operation on test completion

*** Variables ***
${URL}    http://localhost/portal/frontend/dashboard.php
${BROWSER}    chrome

*** Test Cases ***
Open Browser, Visit Dashboard, and Check Status
    [Documentation]    Open browser, visit dashboard, and use the custom Python library to check the status.

    # Step 1: Open browser using the custom Python library
    Open Browser Using Library    ${URL}

    # Step 2: Check the user status using the custom Python library
    ${status}=    Check Status Using Library

    # Step 3: Print the status in the terminal
    Log To Console    The status is: ${status}

    # (Optional) You can keep the browser open or close it as needed
    # Close Browser Using Library

*** Keywords ***
Open Browser Using Library
    [Arguments]    ${url}
    CheckStatusLibrary.Open Browser    ${url}

Check Status Using Library
    ${status}=    CheckStatusLibrary.Check Status
    RETURN    ${status}

Close Browser Using Library
    CheckStatusLibrary.Close Browser
