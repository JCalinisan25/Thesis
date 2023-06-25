import os, json
# Create a global variable to track the login state and store the current user
logged_in = False
current_user = None

# Function to handle exit
def exit_application():
    global logged_in
    # Perform any necessary cleanup or save operations here
    # Set logged_in to False to indicate the user is no longer logged in
    logged_in = False
    # Show the login screen
    os.system('Login.py')

# Function to handle logout
def logout():
    global logged_in, current_user
    # Perform any necessary cleanup or save operations here
    # Set logged_in to False to indicate the user is no longer logged in
    logged_in = False
    current_user = None
    # Show the login screen
    os.system('Login.py')

# Function to handle successful login
def handle_login(user):
    global logged_in, current_user
    # Set logged_in to True to indicate the user is logged in
    logged_in = True
    current_user = user
    # Show the dashboard
    os.system('Dashboard.py')

# Check if the user is logged in
try:
    with open('user.json', 'r') as file:
        user_info = json.load(file)
    if 'email' in user_info:
        email = user_info['email']
    else:
        email = ""
except FileNotFoundError:
    email = ""

if email:
    logged_in = True
    current_user = email
    os.system('Dashboard.py')
else:
    os.system('Login.py')

