"""
This class is the UI for the system. It will be used to interact with the user.

@Author: KATHAN PATEL (101146368)
@Version: 1.0
@Date: 2023-12-04
"""
import User
from RolesController import RolesController


class SystemUI:

    # init
    def __init__(self):
        self.user = None
        self.roles_controller = RolesController()
        self.roles_controller.connect_to_db()
        self.roles_controller.create_roles_table()
        self.start_up()
        self.roles_controller.close_connection()

    def start_up(self):
        print("Welcome to Finvest!")
        # ask if already a user or need to register
        print("Are you already a user? (y/n)")
        try:
            user = input()
            if user == 'y':
                self.login()
            elif user == 'n':
                self.register()
            else:
                print("Invalid input. Please try again.")
                self.start_up()
        # except keyboard interrupt
        except KeyboardInterrupt:
            if self.user.user_log_file is not None:
                self.logout()
            else:
                print("Thank you for using Finvest!")
        self.start_up()

    def login(self):
        self.user = User.User(self.roles_controller)
        self.user.login()

    def register(self):
        self.user = User.User(self.roles_controller)
        self.user.register()

    def logout(self):
        self.user.logout()
        self.user = None
        print("Thank you for using Finvest!")
        exit(0)
