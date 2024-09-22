*** Settings ***
Library    SeleniumLibrary
Library    ./scripts/CheckStatusLibrary.py  # Import the custom Python library
Suite Teardown    No Operation    # Prevents automatic browser closure in teardown
Test Teardown     No Operation    # Ensures no operation on test completion

*** Variables ***
${URL}    http://localhost/portal/frontend/dashboard.php
${BROWSER}    chrome

*** Test Cases ***
Open Browser, Visit Dashboard, and Check Status and Conditions
    [Documentation]    Open browser, visit dashboard, check user status and validate email/password.

    # Step 1: Open browser using the custom Python library
    Open Browser Using Library    ${URL}

    # Step 2: Check the user status, validate conditions, and approve if all conditions are met
    ${result}=    Check Status and Validate Using Library

    # Step 3: Log the result in the terminal
    Log To Console    The result is: ${result}

*** Keywords ***
Open Browser Using Library
    [Arguments]    ${url}
    CheckStatusLibrary.Open Browser    ${url}

Check Status and Validate Using Library
    ${result}=    CheckStatusLibrary.Check Status and Validate
    RETURN    ${result}

Close Browser Using Library
    CheckStatusLibrary.Close Browser
