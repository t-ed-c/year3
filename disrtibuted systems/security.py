# Dictionary storing user credentials and their roles
users = {
    "alice": {"password": "1234", "role": "admin"},
    "bob": {"password": "abcd", "role": "user"},
}

# Permissions assigned to each role
permissions = {
    "admin": ["read", "write", "delete"],  # Admins can read, write, and delete
    "user": ["read"]                       # Regular users can only read
}

def login(username, password):
    # Check if username exists and password matches
    if username in users and users[username]["password"] == password:
        return users[username]["role"]  # Return the role on successful login
    return None  # Return None if login fails

def check_access(role, action):
    # Check if the given role has permission to perform the action
    return action in permissions.get(role, [])

# --- Simulate a user login and permission check ---
username = "bob"
password = "abcd"
action = "delete"

role = login(username, password)  # Attempt to login

if role:
    if check_access(role, action):
        print(f"Access granted for {action}")
    else:
        print(f"Access denied for {action}")
else:
    print("Invalid login")
