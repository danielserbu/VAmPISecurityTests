import pytest
import requests
import json

url = "http://localhost:5000/"
testUser = "testUser"
testUserPassword = "testPassword"


# Default users on the system: name1, name2, admin

def create_new_db(url=url + "/createdb"):
    """
        Creates new DB. (Can also clean up previous database)
    """
    request = requests.get(url)


def create_new_test_user(url=url + "/users/v1/register"):
    """
        Creates new USER. (Useful for fetching the auth_token)
    """
    contentType = "application/json"
    body = {
        "username": testUser,
        "password": testUserPassword,
        "email": "testUser"
    }

    request = requests.post(url,
                            data=json.dumps(body),
                            headers={'Content-Type': contentType})
    if "success" in request.text:
        print("User testUser created successfully!")


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


def login_with_test_user(username=testUser, password=testUserPassword):
    """
        Logs in with new USER. (Useful for fetching the auth_token)
    """
    myToken = login_with_user(username, password)
    global auth_token
    auth_token = myToken[1]
    print(auth_token)


def setup_module():
    create_new_db()
    create_new_test_user()
    login_with_test_user()


def teardown_module():
    print("Teardown here")


def test_unauthorized_password_change(url=url + "/users/v1/name1/password"):
    """
        Tests if user's "name1" password can be changed
        with our created test account's bearer token.
    """
    contentType = "application/json"
    newPassword = "newTestPassword"
    body = {
        "password": newPassword
    }

    request = requests.put(url,
                           data=json.dumps(body),
                           headers={'Content-Type': contentType,
                                    'Authorization': f"Bearer {auth_token}"})
    assert request.status_code is 204

    # Login with name1 user using the newly created password.
    result = login_with_user("name1", newPassword)
    assert result[0] is "success"
