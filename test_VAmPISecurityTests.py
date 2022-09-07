import pytest
import requests
import json

# Change port to 5050 for non vulnerable API.
# 5000 is vulnerable
port = 5000

url = "http://localhost:" + str(port) + "/"
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
    #print(testUser_auth_token)


def login_with_second_test_user(username=secondTestUser, password=secondTestUserPassword):
    """
        Logs in with secondary test USER. (Useful for fetching the auth_token)
    """
    myToken = login_with_user(username, password)
    global secondTestUser_auth_token
    secondTestUser_auth_token = myToken[1]
    #print(secondTestUser_auth_token)


def setup_module():
    create_new_db()
    create_new_user(testUser, testUserPassword)
    create_new_user(secondTestUser, secondTestUserPassword)
### Setup ###


### Tests ###
def test_sql_injection(url=url + "/users/v1/' or 1=1 -- "):
    """
        Tests if getting user functionality is vulnerable to SQLi
        Note: 1=1 technique returns first user in database.
    """

    request = requests.get(url)

    assert "name1" not in request.text
    assert "mail1@mail.com" not in request.text


def test_error_based_sql_injection(url=url + "/users/v1/-1'"):
    """
        Tests if getting user functionality is vulnerable to error based SQLi
        Note: "-1' parameter returns sqlalchemy.exc.OperationalError
    """

    request = requests.get(url)

    assert "SQL: SELECT * FROM users WHERE username = '-1" not in request.text


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


def test_user_and_password_enumeration(url=url + "/users/v1/login"):
    """
        Tests if user's "name1" password can be changed
        using our newly created test account's bearer token.
    """
    contentType = "application/json"

    usernameslist = ["admin", "lackinguser", "someotherfakeuser"]
    passwordslist = ["password123", "greatpasswordx", "someotherfakepassword"]

    for username in usernameslist:
        for password in passwordslist:
            credentials = {"username": username, "password": password}
            body = {
                "username": credentials["username"],
                "password": credentials["password"]
            }

            request = requests.post(url,
                                    data=json.dumps(body),
                                    headers={'Content-Type': contentType})

            assert "Username or Password Incorrect!" in request.text
            assert "Password is not correct for the given username." not in request.text
            assert "Username does not exist" not in request.text


def test_rate_limiting():
    """
        Tests rate limiting by trying to fill up the database with lots of new users
        Observation: not all functions are tested for rate limiting.
        Some other functions might have a rate limit.
    """
    oneThousandUsers = list(range(1000))
    successFailureRate = list()
    for number in oneThousandUsers:
        output = create_new_user(str(number), str(number))
        successFailureRate.append(output)  # which should be success or failure (to create user)
    assert "failure" in successFailureRate


def test_excessive_data_exposure(url=url + "users/v1/"):
    """
        Tests for excessive data exposure in /users/v1/ path.
    """
    potentialPaths = ["options", "pictures", "password", "debug", "_debug"]
    requestOutputs = {}
    for path in potentialPaths:
        request = requests.get(url + path)
        requestOutputs[path] = request.text

    assert "admin" and "password" not in requestOutputs


def test_mass_assignment():
    """
        Tests for mass assignment vulnerability by fuzzing for additional accepted
        parameters inside /register's path body.
    """
    contentType = "application/json"

    fuzzParametersDictionary = {
        "test": "test",
        "administrator": "administrator",
        "root": True,
        "admin": True
    }

    # No duplicate usernames are allowed
    usernames = ["user0", "user1", "user2", "user3"]

    body = {
        "username": "",
        "password": "test",
        "email": "testmail"
    }

    usernameIndex = 0
    for fuzzParameter in fuzzParametersDictionary:
        # Update request body with fuzz parameter
        body[fuzzParameter] = fuzzParametersDictionary[fuzzParameter]

        # Parametrize usernames (No duplicate usernames are allowed)
        body["username"] = usernames[usernameIndex]
        usernameIndex += 1

        request = requests.post(url + "users/v1/register",
                                data=json.dumps(body),
                                headers={'Content-Type': contentType})
        # Cleanup for next loop
        del body[fuzzParameter]

    # Check if any of the fuzzed parameters did tamper the admin value by using the _debug path
    # Otherwise it would be ideal to check directly into DB, but going this way for now.
    usersRequest = requests.get(url + "/users/v1/_debug")
    userRequestOutputDictionary = json.loads(usersRequest.text)

    vulnerable = False

    # Check if any of the users was registered as admin.
    for username in usernames:
        listOfUsers = userRequestOutputDictionary["users"]
        # Get our user's properties
        userDetails = next(item for item in listOfUsers if item["username"] == username)
        # Check if admin field is True
        if userDetails["admin"]:
            # Use username's last number character as index for deciding the vulnerable parameter.
            print("The vulnerable parameter was " +
                  str(list(fuzzParametersDictionary.items())[int(username[-1:])]))
            vulnerable = True
    assert not vulnerable

# Not implemented tests
# def test_broken_object_level_authorization():
# def test_regexDOS():
### Tests ###
