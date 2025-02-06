[POSTMAN Documentation](https://documenter.getpostman.com/view/41851685/2sAYX8GfK3)

# User Guide

## Installation

### 1. Install Required Libraries
Ensure you have the following Python libraries installed:
- `flask`
- `PyJWT`

Use the following command to install them if needed:
```bash
pip install flask PyJWT
```

### 2. Run the Application
Navigate to the directory where your `api.py` file is located:
```bash
cd "path_to_directory"
```
Run the script:
```bash
python api.py
```
For example, you can execute this command in PyCharm or a terminal.

---

## User Roles
- The `users` file contains information on whether a user is an **administrator** or a **regular user**.
- Administrators have full access to all functions.
- Regular users have limited access.

---

## Using Postman

1. Open Postman.
2. Use the `Login_Users` method to retrieve a token.
3. Copy the generated token and include it in your requests.
4. In the `Body -> raw -> JSON` section, enter user credentials.

---

## API Endpoints

### 1. Get Users (`GET`)
Retrieve a list of users.
```bash
GET http://127.0.0.1:5000/api/users
```

### 2. Delete User (`DELETE`)
Remove a user by specifying their ID at the end of the URL.
```bash
DELETE http://127.0.0.1:5000/api/users/{user_id}
```
Example:
```bash
DELETE http://127.0.0.1:5000/api/users/3
```

### 3. Add User (`POST`)
Add a new user by sending a JSON object with user details in the request body.
```bash
POST http://127.0.0.1:5000/api/users
```
JSON Example:
```json
{
    "name": "Olexsandr Ischuk",
    "email": "ishuk.sasha2005@gmail.com"
}
```

### 4. Update User (`PATCH`)
Modify user details by specifying their ID and sending updated data in the request body.
```bash
PATCH http://127.0.0.1:5000/api/users/{user_id}
```
Example:
```bash
PATCH http://127.0.0.1:5000/api/users/4
```
JSON Example:
```json
{
    "name": "Sophias Martinez",
    "email": "sophias.m@example.com"
}
```

