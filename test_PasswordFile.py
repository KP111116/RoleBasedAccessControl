from unittest import TestCase

import PasswordFile
import os


class TestPasswordFile(TestCase):
    pf = None

    @classmethod
    def setUpClass(cls) -> None:
        try:
            os.remove('test_passwd.txt')
        except OSError as e:
            print(e)
            pass
        finally:
            cls.pf = PasswordFile.PasswordFile("test_passwd.txt")

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            os.remove('test_passwd.txt')
        except OSError as e:
            print(e)
            pass

    def check_record(self):
        try:
            pass_line = self.pf.retrieve_record("kathan")
        except PasswordFile.BadRequest as e:
            print(e)
            return False
        print("Line retrieved: " + pass_line)
        elements_in_line = pass_line.strip(':').split(':')
        # check for username, role, user_info and user_log_path
        if elements_in_line[0] == "kathan" and elements_in_line[3] == "Admin" and elements_in_line[
            4] == "Kathan Patel, 9898158841" and elements_in_line[5] == "username_role.txt":
            return True
        else:
            return False

    def test_try_password(self):
        try:
            PasswordFile.try_password("Kathan123")
        except PasswordFile.BadRequest as e:
            print(e)
            assert True

    def test_try_SIN(self):
        try:
            PasswordFile.try_password("123-345-908")
        except PasswordFile.BadRequest as e:
            print(e)
            assert True

    def test_try_Date(self):
        try:
            PasswordFile.try_password("22/05/2001")
        except PasswordFile.BadRequest as e:
            print(e)
            assert True

    def test_try_Date_2(self):
        try:
            PasswordFile.try_password("09-93-9033")
        except PasswordFile.BadRequest as e:
            print(e)
            assert True

    def test_try_Date_3(self):
        try:
            PasswordFile.try_password("22-34-54")
        except PasswordFile.BadRequest as e:
            print(e)
            assert True

    def test_try_Date_4(self):
        try:
            PasswordFile.try_password("09-09-09")
        except PasswordFile.BadRequest as e:
            print(e)
            assert True

    def test_number_plate(self):
        try:
            PasswordFile.try_password("ABCD 123")
        except PasswordFile.BadRequest as e:
            print(e)
            assert True

    def test_weak_password(self):
        try:
            PasswordFile.try_password("password")
        except PasswordFile.BadRequest as e:
            print(e)
            assert True

    def test_add_record(self):
        self.pf.add_record("kathan", "Hathan@123", "Admin", "Kathan Patel, 9898158841", "username_role.txt")
        assert self.check_record()

    def test_password_username(self):
        try:
            PasswordFile.try_password_word("Kathan@123", "Kathan@123")
        except PasswordFile.BadRequest as e:
            print(e)
            assert True

    def test_retrieve_record(self):
        with open("test_passwd.txt", 'a') as f:
            f.write("kathan:b'$2b$12$sgkdA35DcHCr1zJGxYPOkO':$2b$12$sgkdA35DcHCr1zJGxYPOkOV5XxEderrsGsovje"
                    "/I6xOLkarethi0q:Admin:Kathan Patel, 9898158841:username_role.txt")
        assert self.check_record()

    def test_wrong_username_retrieve(self):
        self.pf.add_record("athan", "Hetvi@123", "info", "Client", "username.txt")
        try:
            self.pf.retrieve_record("hetvi")
        except PasswordFile.BadRequest as e:
            print(e)
            assert True
            return
        assert False

    def test_authenticate_password(self):
        pass_file = PasswordFile.PasswordFile("test_passwd.txt")
        pass_file.add_record("Kathan", "Hetvi@123", "Client", "info", "kathan.txt")
        assert self.pf.authenticate_user("Kathan", "Hetvi@123")

    def test_authenticate_wrong_password(self):
        pass_file = PasswordFile.PasswordFile("test_passwd.txt")
        pass_file.add_record("Kathan", "Hetvi@123", "Client", "info", "kathan.txt")
        try:
            self.pf.authenticate_user("Kathan", "Hathan@123")
        except PasswordFile.BadRequest as e:
            print(e)
            assert True
