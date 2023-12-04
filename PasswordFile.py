"""
This class handles the authentication for the user. It is used to file read and write operations.

@Author: KATHAN PATEL (101146368)
@Version: 1.0
@Date: 2023-12-04
"""
import bcrypt
import re
import csv


class BadRequest(Exception):
    pass


'''
This method checks if the password is valid or not. It checks for the following policies:
1. Password length must be greater than 7 characters
2. Password should not match a date format. (eg. mm-dd-yyyy, mm/dd/yyyy, mm-dd-yy, mm/dd/yy)
3. Password should not match a SIN. (eg. 123-456-789)
4. Password should not match an Ontario number plate. (eg. ABCD 123)
5. Password should not be in the list of common passwords. (common_passwords.csv) <- source: kaggle.com
# NOTE: The common_passwords.csv file can be updated to include more passwords.
6. Password cannot contain username (eg Username: Kathan, Password: Kathan@123)
7. The Password must contain at least an Upper Case Alphabet, Lower case Alphabet, 
   numeric character, and a special character !@#$%^&*()_+~=_\\|]}[{\'\"/?.>,<
'''


def try_password_word(password: str, username: str) -> bool:
    # check for password length
    if password.__len__() <= 7:
        raise BadRequest("Password must be longer than 7 characters")

    # check for special formats.

    # date mm-dd-yyyy, mm/dd/yyyy, mm-dd-yy, mm/dd/yy
    date_format = [r'\d{2}-\d{2}-\d{4}', r'\d{2}/\d{2}/\d{4}', r'\d{2}-\d{2}-\d{2}', r'\d{2}/\d{2}/\d{2}']
    for df in date_format:
        if re.search(df, password):
            raise BadRequest("Password should not match a date format. Please guess a stronger password")

    # Social Insurance Number
    if re.search(r'\d{3}-\d{3}-\d{3}', password):
        raise BadRequest("Password should not match a SIN. Please guess a stronger password")

    # License Plate
    if re.search(r'\S{4}\s\d{3}', password):
        raise BadRequest("Password should not match a number plate. Please guess a stronger password")

    # check if the password is found in the list of weak passwords
    with open('resources/common_passwords.csv', 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if password in str(row[0]):
                raise BadRequest("Password is weak, guess again.")

    # check if the password matches the username
    regex = r'(?i)' + username
    if re.search(regex, password):
        raise BadRequest("Password cannot contain username")

    # check if the password consists a capital letter
    (has_capital, has_lower, has_number, has_special) = (False, False, False, False)
    check = [has_capital, has_lower, has_number, has_special]
    password_chars = [x for x in password]
    for c in password_chars:
        if c.isupper():
            check[0] = True
        if c.islower():
            check[1] = True
        if c.isnumeric():
            check[2] = True
        if c in '!@#$%^&*()_+`~=_\\|]}[{\'\"/?.>,<':
            check[3] = True

    for b in check:
        if not b:
            raise BadRequest("The Password must contain at least an Upper Case Alphabet, Lower case Alphabet,\n"
                             "numeric character, and a special character !@#$%^&*()_+~=_\\|]}[{\'\"/?.>,<")
    return True


"""
    This test try_password method is for testing purposes which passes an 
    empty string to the functional try_password method because it will check for all
    other policies, rather than checking if the username is same as password
"""


def try_password(password: str):
    try_password_word(password, " ")


class PasswordFile:
    def __init__(self, *args):
        if len(args) < 1:
            self.file_dest = 'resources/database/passwd'
        else:
            self.file_dest = args[1]
    '''
    This method adds a record to the password file. It takes in the following parameters:
    
    @param username: The username of the user
    @param password: The password of the user
    @param role_name: The role of the user
    @param user_info: The user's information
    
    '''
    def add_record(self, username, password, role_name, user_info, user_log_file_path) -> bool:
        try:
            try_password_word(password, username)
        except BadRequest as e:
            raise BadRequest("Password not accepted")

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        record = f"{username}:{salt}:{hashed_password.decode('utf-8')}:{role_name}:{user_info}:{user_log_file_path}"

        with open(self.file_dest, 'a') as f:
            f.write(record + '\n')
        return True

    '''
    This method authenticates the user.
    '''
    def authenticate_user(self, username, password: str):
        try:
            try_password_word(password, username)
        except BadRequest as e:
            raise e

        record = self.retrieve_record(username)

        # check if the record matched the username and password combo
        record = record.split(":")
        # decrypt password using salt and salted hash
        if bcrypt.checkpw(password.encode('utf-8'), record[2].encode('utf-8')):
            return record
        else:
            raise BadRequest("Username and Password do not match")

    '''
    The method updates the user's role in the password file. This method is accessed only by the admin.
    '''
    def verified_role(self, username, role, user_log_file_path):
        record = self.retrieve_record(username)
        record = record.split(":")
        record[3] = role
        record[5] = user_log_file_path
        record = ":".join(record)
        with open(self.file_dest, 'r') as f:
            lines = f.readlines()
        with open(self.file_dest, 'w') as f:
            for line in lines:
                if line.startswith(username + ':'):
                    f.write(record)
                else:
                    f.write(line)
        return True

    '''
    This method retrieves a record from the password file.
    '''
    def retrieve_record(self, username) -> str:
        with open(self.file_dest, 'r') as f:
            for line in f:
                if line.startswith(username + ':'):
                    return line.strip()
            raise BadRequest("Username not found")

    '''
    This method checks if a user exists in the password file.
    '''
    def check_if_exists(self, username):
        if self.retrieve_record(username):
            return True
        return False
