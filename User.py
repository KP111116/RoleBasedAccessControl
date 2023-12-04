"""
This class is a model for any user in the system.
It has all the functions a user can use.
It will also provide only the functions that the user has access to.

@Author: KATHAN PATEL (101146368)
@Version: 1.0
@Date: 2023-12-04
"""
import os
import re
import PasswordFile
import System_UI
from MainMenu import MainMenu
from PasswordFile import BadRequest
from datetime import datetime


class User:
    # init
    def __init__(self, roles_controller):
        self.roles_controller = roles_controller
        self.username = None
        self.user_log_file = None
        self.role = None
        self.user_info = None


    '''
        This method will show the admin the list of requested roles.
        It will ask the admin to verify the role of a user.
        If the admin verifies the role, the user will be able to use the system.
        If the admin denies the role, the user will not be able to call any functions in the system
    '''
    def show_requested_roles(self):
        # if empty show message
        with open('resources/database/requested_roles', 'r') as f:
            if f.readline() == '':
                print("No requested roles.")
                return
        with open('resources/database/requested_roles', 'r+') as f:
            for line in f:
                print(line)
                self.verify_role(line)

    '''
        This method will verify the role of a user.
    '''
    def verify_role(self, line):
        pf = PasswordFile.PasswordFile()
        line = line.split(':')
        username, role, user_log_file = line[0], line[1], line[3]
        print(f"Would you like to verify the role of {username} as {role}? (y/n)")
        choice = input()
        if choice == 'y':
            pf.verified_role(username, role, user_log_file)
        elif choice == 'n':
            pf.verified_role(username, 'rejected', user_log_file)
        else:
            print("Invalid input. Please try again.")
            self.verify_role(line)
        with open(self.user_log_file, "a") as f:
            f.write(f"{datetime.now()}: Verified role of {username} as {role}\n")
        with open('resources/database/requested_roles', 'r+') as f:
            lines = f.readlines()
        with open('resources/database/requested_roles', 'w') as f:
            for line in lines:
                if line.startswith(username + ':'):
                    line.replace(line, '')

    '''
    This method will register a user.
    It will ask the user to choose a username, password, role and provide user info(email)
    which can be used to contact the user and send user logs to notify the user of any changes.
    The logging and notifying can be implemented in the future.
    After the registration, the user will be redirected to the start up screen.
    '''
    def register(self):
        print("Please choose a username: ")
        username = self.get_username()
        print("Please choose a password: ")
        password = self.get_password(username)
        role = self.match_role()
        user_info = self.get_user_info()
        self.add_record(username, password, role, user_info, f'resources/database/{username}/{username}')

    '''
    This method will request a role for a user from the admin
    '''
    def request_role(self, username, role, user_info, user_log_file):
        # this method will be called when a user registers
        # it will send a request to the admin to approve the role
        # the admin will be able to see the request in the logs
        # the admin will be able to approve the request
        # the admin will be able to deny the request
        with open("resources/database/requested_roles", "a") as f:
            f.write(f"{username}:{role}:{user_info}:{user_log_file}\n")

    '''
    This method will login a user. It will ask for username and the password set up by the user.
    '''
    def login(self):
        print("Provide your username: ")
        username = input()
        print("Provide your password: ")
        password = input()
        try:
            user_record = PasswordFile.PasswordFile().authenticate_user(username, password)
            self.username = user_record[0]
            self.role = user_record[3]
            self.user_info = user_record[4]
            self.user_log_file = user_record[5]
            print("Login successful!")
            path = f'resources/database/{username}'
            if os.path.exists(path):
                with open(self.user_log_file, "a") as f:
                    f.write(f"{datetime.now()}: Logged in\n")
            else:
                os.mkdir(path)
                with open(self.user_log_file, "a") as f:
                    f.write(f"{datetime.now()}: Logged in\n")
            while True:
                self.main_menu()
        except BadRequest as e:
            print(e)
            self.login()

    '''
    After the user has successfully logged in, this method will be called. To display the main menu.
    The main menu has only the required functions for the user based on the user's role.
    '''
    def main_menu(self):
        # this method will clear the screen
        # it will display the main menu
        # it will ask the user to choose an option
        # it will call the appropriate method based on the option chosen
        # it will call the main menu again
        # it will exit the system if the user chooses to exit
        print(f"Welcome {self.username}!\nYou can view your log at {self.user_log_file}\nAs a {self.role} you have "
              f"the following permissions: " )
        print("Main Menu")
        # get the permissions for the user
        permissions = self.roles_controller.get_permissions(self.role)
        MainMenu(self, permissions)

    '''
    This method handles the logout procedure for the system.
    When a user logs out, it will be logged in the user's log file.
    And the user will be redirected to the start up screen. Where another user can login or register.
    '''
    def logout(self):
        # this method will log the user out
        # it will call the login method
        with open(self.user_log_file, "a") as f:
            f.write(f"{datetime.now()}: Logged out\n")
        self.username = None
        self.user_log_file = None
        self.role = None
        self.user_info = None
        exit(0)

    '''
    This method handles the registration procedure for the system.
    When a user registers, it will be logged in the user's log file.
    The information is saved securely in the passwd.txt file.
    '''
    def add_record(self, username, password, role, user_info, user_log):
        pf = PasswordFile.PasswordFile()
        try:
            pf.add_record(username, password, 'requested', user_info, user_log)
        except BadRequest as e:
            print(e)
        self.username = username
        self.user_log_file = user_log
        self.role = 'requested'
        self.user_info = user_info
        os.mkdir(f'resources/database/{username}')
        with open(self.user_log_file, "a") as f:
            f.write(f"{datetime.now()}: Registered\n")
        self.request_role(username, role, user_info, user_log)

    '''
    This is a helper method to verify each username is unique.
    '''
    def get_username(self):
        username = input()
        try:
            PasswordFile.PasswordFile().check_if_exists(username)
        except BadRequest as e:
            return username
        print("Username already exists. Please try again.")
        self.get_username()

    '''
    This is a helper method to verify each password is valid.
    '''
    def get_password(self, username) -> str:
        password = input()
        try:
            PasswordFile.try_password_word(password, username)
        except BadRequest as e:
            print(e)
            return self.get_password(username)

        print("Please re-enter you password: ")
        password2 = input()

        if password != password2:
            print("Passwords do not match. Please try again.")
            return self.get_password(username)
        else:
            return password

    '''
    This is a helper method to verify each email is valid.
    '''
    def get_user_info(self):
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        # get email
        print("Please enter your email: ")
        try:
            email = input()
            if re.fullmatch(regex, email):
                return email
            else:
                print("Invalid email format. Please try again.")
                return self.get_user_info()
        except ValueError:
            print("Invalid input. Please try again.")
            return self.get_user_info()

    '''
    This is a helper method to match each role to the user.
    '''
    def match_role(self):
        print("Please choose a role: ")
        print("1. Client\n2. Premium Client\n3. Financial Advisor\n4. Investment Analyst\n5. Financial Planner\n"
              "6. Technical Support\n7. Teller\n8. Compliance Officer\n"
              "The role you choose shall be 'requested' to the admin until approved.")

        role = input()
        if role == '1':
            return 'client'
        elif role == '2':
            return 'premium_client'
        elif role == '3':
            return 'financial_advisor'
        elif role == '4':
            return 'investment_analyst'
        elif role == '5':
            return 'financial_planner'
        elif role == '6':
            return 'technical_support'
        elif role == '7':
            return 'teller'
        elif role == '8':
            return 'compliance_officer'
        else:
            print("Invalid input. Please try again.")
            self.match_role()

    '''
    This method is used to call the appropriate method based on the user's choice.
    '''
    def call_function(self, function):
        if function == 'view_balance':
            self.view_balance()
        elif function == 'view_investment_portfolio':
            self.view_investment_portfolio()
        elif function == 'modify_portfolio':
            self.modify_portfolio()
        elif function == 'view_consumer_instruments':
            self.view_consumer_instruments()
        elif function == 'view_money_market_instruments':
            self.view_money_market_instruments()
        elif function == 'view_derivatives_trading':
            self.view_derivatives_trading()
        elif function == 'view_interest_instruments':
            self.view_interest_instruments()
        elif function == 'view_client_information':
            self.view_client_information()
        elif function == 'request_client_access':
            self.request_client_access()
        elif function == 'validate_investment_mods':
            self.validate_investment_mods()
        elif function == 'verify_user_role':
            self.verify_user_role()
        elif function == 'view_logs':
            self.view_logs()
        elif function == 'static_role':
            print("Static Role")

    '''
    The following is the suite of methods that will be called based on the user's role.
    Each method checks if the user has the permission to call the method.
    If the user has the permission, the method will be called.
    '''
    # NOTE: The following methods are just placeholders for the actual methods that will be implemented in the future.
    def view_balance(self):
        if self.roles_controller.has_permission(self.role, 'view_balance'):
            # Limitations: 8:59 < t < 17:01 : t = time of day, on business working days if the user is a teller:
            if self.role == 'teller' and (datetime.now().hour < 9 or datetime.now().hour > 17):
                print("You are a teller. You can only view balance between 9:00 AM and 5:00 PM on business days.")
                return
            print("View Balance")
        else:
            print("You do not have permission to view balance.")

    def view_investment_portfolio(self):
        if self.roles_controller.has_permission(self.role, 'view_investment_portfolio'):
            # Limitations: 8:59 < t < 17:01 : t = time of day, on business working days
            if (datetime.now().hour < 9 or datetime.now().hour > 17) and self.role == 'telller':
                print("You can only view investment portfolio between 9:00 AM and 5:00 PM on business days.")
                return
            print("View Investment Portfolio")
        else:
            print("You do not have permission to view investment portfolio.")

    def modify_portfolio(self):
        if self.roles_controller.has_permission(self.role, 'modify_portfolio'):
            print("Modify Portfolio")
        else:
            print("You do not have permission to modify portfolio.")

    def view_consumer_instruments(self):
        if self.roles_controller.has_permission(self.role, 'view_consumer_instruments'):
            print("View Consumer Instruments")
        else:
            print("You do not have permission to view consumer instruments.")

    def view_money_market_instruments(self):
        if self.roles_controller.has_permission(self.role, 'view_money_market_instruments'):
            print("View Money Market Instruments")
        else:
            print("You do not have permission to view money market instruments.")

    def view_derivatives_trading(self):
        if self.roles_controller.has_permission(self.role, 'view_derivatives_trading'):
            print("View Derivatives Trading")
        else:
            print("You do not have permission to view derivatives trading.")

    def view_interest_instruments(self):
        if self.roles_controller.has_permission(self.role, 'view_interest_instruments'):
            print("View Interest Instruments")
        else:
            print("You do not have permission to view interest instruments.")

    def view_client_information(self):
        if self.roles_controller.has_permission(self.role, 'view_client_information'):
            print("View Client Information")
        else:
            print("You do not have permission to view client information.")

    def request_client_access(self):
        if self.roles_controller.has_permission(self.role, 'request_client_access'):
            print("Request Client Access")
        else:
            print("You do not have permission to request client access.")

    def validate_investment_mods(self):
        if self.roles_controller.has_permission(self.role, 'validate_investment_mods'):
            print("Validate Investment Mods")
        else:
            print("You do not have permission to validate investment mods.")

    def verify_user_role(self):
        # This method helps to verify the role of a user
        # It will be used by the admin to verify the role of a user
        # show the admin the list of requested roles
        # ask the admin to verify the role of a user
        # if the admin verifies the role, the user will be able to use the system
        # if the admin denies the role, the user will not be able to use the system
        # if the admin does not verify the role, the user will only be able to see their log
        if self.roles_controller.has_permission(self.role, 'verify_user_role'):
            self.show_requested_roles()
        else:
            print("You do not have permission to verify user roles.")

    def view_logs(self):
        if self.roles_controller.has_permission(self.role, 'view_logs'):
            print("View Logs")
        else:
            print("You do not have permission to view logs.")

