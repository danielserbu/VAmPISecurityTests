import pytest
import requests
import json

# Change port to 5050 for non vulnerable API.
# 5000 is vulnerable
port = 5000

url = "http://localhost:" + string(port) + "/"
testUser = "testUser"
testUserPassword = "testPassword"
secondTestUser = "secondTestUser"
secondTestUserPassword = "secondTestPassword"
# Default users on the system: name1, name2, admin


### Utils ###
def create_new_db(url=url + "/createdb"):
    """
        Creates new DB. (Can also clean up previous database)
    """
    request = requests.get(url)


def create_new_user(username, password, url=url + "/users/v1/register"):
    contentType = "application/json"
    body = {
        "username": username,
        "password": password,
        "email": username
    }

    request = requests.post(url,
                            data=json.dumps(body),
                            headers={'Content-Type': contentType})
    if "success" in request.text:
        print("User " + username + " created successfully!")
        return "success"
    else:
        return "failure"


def login_with_user(username, password, url=url + "/users/v1/login"):
    contentType = "application/json"
    body = {
        "username": username,
        "password": password
    }

    request = requests.post(url,
                            data=json.dumps(body),
                            headers={'Content-Type': contentType})
    if "success" in request.text:
        print("Logged in successfully with " + username + " account!")
        myToken = json.loads(request.text)["auth_token"]
        return ["success", myToken]
    else:
        return ["failure"]
### Utils ###


### Setup ###
def login_with_test_user(username=testUser, password=testUserPassword):
    """
        Logs in with new USER. (Useful for fetching the auth_token)
    """
    myToken = login_with_user(username, password)
    global testUser_auth_token
    testUser_auth_token = myToken[1]
    print(testUser_auth_token)


def login_with_second_test_user(username=secondTestUser, password=secondTestUserPassword):
    """
        Logs in with secondary test USER. (Useful for fetching the auth_token)
    """
    myToken = login_with_user(username, password)
    global secondTestUser_auth_token
    secondTestUser_auth_token = myToken[1]
    print(secondTestUser_auth_token)


def setup_module():
    create_new_db()
    create_new_user(testUser, testUserPassword)
    create_new_user(secondTestUser, secondTestUserPassword)
### Setup ###


### Tests ###
def test_sql_injection(url=url + "/users/v1/' or 1=1 -- "):
    """
        Tests if getting user functionality is vulnerable to SQLi
    """

    request = requests.get(url)

    assert "name1" not in request.text
    assert "mail1@mail.com" not in request.text


def test_unauthorized_password_change(url=url + "/users/v1/name1/password"):
    """
        Tests if user's "name1" password can be changed
        using our newly created test account's bearer token.
    """
    login_with_test_user()

    contentType = "application/json"
    newPassword = "newTestPassword"

    body = {
        "password": newPassword
    }

    request = requests.put(url,
                           data=json.dumps(body),
                           headers={'Content-Type': contentType,
                                    'Authorization': f"Bearer {testUser_auth_token}"})

    assert request.status_code is not 204

    # Continue in case request.status_code was 204 (vulnerable).
    # Login with name1 user using the newly created password.
    result = login_with_user("name1", newPassword)
    assert result[0] is not "success"

# def test_broken_object_level_authorization():

# def test_mass_assignment():

# def test_excessive_data_exposure():

# def test_user_and_password_enumeration_alongside_rate_limiting():

# def test_regexDOS():
### Tests ###