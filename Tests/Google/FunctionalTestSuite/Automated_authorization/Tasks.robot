*** Settings ***
Library           SeleniumLibrary
Library           ./scripts/CheckStatusLibrary.py
Suite Teardown    No Operation
Test Teardown     No Operation

*** Variables ***
${URL}            http://localhost/portal/frontend/dashboard.php
${BROWSER}        chrome

*** Test Cases ***
Open Browser, Visit Dashboard, and Check Status and Conditions
    [Documentation]    Open browser, visit dashboard, check user status and validate email/password.

    Open Browser Using Library    ${URL}

    ${result}=    Check Status and Validate Using Library

    Log To Console    The result is: ${result}

*** Keywords ***
Open Browser Using Library
    [Arguments]    ${url}
    CheckStatusLibrary.Open Browser    ${url}

Check Status and Validate Using Library
    ${result}=    CheckStatusLibrary.check_status_and_validate
    RETURN    ${result}

Close Browser Using Library
    CheckStatusLibrary.Close Browser
