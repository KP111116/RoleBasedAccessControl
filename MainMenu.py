"""
This is the main menu for the system. It will be used to interact with the user.
It takes in the user object and displays the menu based on the user's role.
It will also log the user's actions in the user's log file.

@Author: KATHAN PATEL (101146368)
@Version: 1.0
@Date: 2023-12-04
"""
import User


class MainMenu:
    def __init__(self, user: User, permissions: list):
        self.user = user
        self.permissions = permissions
        self.main_menu()

    def main_menu(self):
        # print all the permissions
        print("Please choose an option: ")
        for i in range(len(self.permissions)):
            print(f"{i + 1}. {self.permissions[i]}")
        print(f"{len(self.permissions) + 1}. Log Out")
        # get the user's choice
        try:
            choice = int(input())
            if choice < 1 or choice > len(self.permissions) + 1:
                print("Invalid input. Please try again.")
                self.main_menu()
            else:
                # call the appropriate method based on the choice
                if choice == len(self.permissions) + 1:
                    self.user.logout()
                else:
                    self.call_method(choice)
        except ValueError:
            print("Invalid input. Please try again.")
            self.main_menu()

    def call_method(self, choice: int):
        self.user.call_function(self.permissions[choice - 1])
