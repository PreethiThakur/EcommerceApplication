from products import *
import os
import uuid
import re
import pandas as pd
from past.builtins import raw_input
import csv
import sys
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type

# Hardcoding admin credentials. There is only one admin
admin_email = "admin@test.com"
admin_password = "admin"


# New Registration
class RegistrationProcess:
    """Class to register new users"""
    user_id = uuid.uuid4()
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    # Constructor
    def __init__(self):
        self

    # Registration process begins
    def register(self):
        # reading data from csv and storing in into variable df. variable is used to check if email exists already
        df = pd.read_csv('users.csv')

        # email id validation
        self.email = input("Please enter your email id : ")
        if not re.search(__class__.regex, self.email):
            self.email = raw_input("Invalid email address, re-enter email id: ")
        if self.email in df['Email'].values:
            self.email = input("Email already registered! Please enter new email : ")

        # password validation
        password = input("Please enter password : ")
        while len(password) < 6:  # assigning length to the password
            password = raw_input("Password should have atleast 6 characters : ")
        conf_password = input("Please confirm password : ")
        while conf_password != password:  # comparing passwords match or not
            conf_password = raw_input('Passwords dont match enter password again : ')

        # name validation
        name = input("Please enter your name : ")
        if len(name) < 1:
            name = raw_input("Name cannot be empty. Try again : ")

        # phone number validation - limit numbers - TBD
        phone = raw_input("Please enter phone number : ")
        rule = re.compile("(0|91)?[0-9][0-9]{9}")
        while not rule.match(phone):
            phone = raw_input("Mobile number should have 10 digits only : ")

        # address validation
        address = input("Please enter your full address : ")
        if len(address) < 1:
            address = raw_input("Address cannot be empty. Try again : ")

        # creating a dataframe to add new row to import the user information into users csv file
        new_row = {'UserID': str(__class__.user_id), 'Name': [name], 'Email': [self.email],
                   'Password': [password], 'Address': [address], 'Phone': [phone]}
        usersdf = pd.DataFrame(new_row)

        # Checking if the users file already exists to prevent header from repeating
        file_exists = os.path.exists('users.csv')
        while file_exists:
            # Importing the dataframe to a csv file without header
            usersdf.to_csv('users.csv', mode='a', index=False, header=False)
            print("Thank you for registering")
            break
        else:
            # Importing the dataframe to a csv file with header
            usersdf.to_csv('users.csv', mode='a', index=False, header=True)
            print("Thank you for registering!")
            LoginAction.membertype(self)


# Logout
class LogoutAction:
    """Class to log the user out of the application"""

    def __init__(self):
        self

    # logout method based on user input
    def logout(self):
        logout_choice = input()
        while True:
            if logout_choice == 'Y':
                print("Logged out!")
                sys.exit()
            elif logout_choice == 'N':
                return False
            else:
                print("Expecting Y or N to logout")
                break


# Login
class LoginAction(RegistrationProcess, LogoutAction):
    """Class to let users login into the application.
        Check if account already exists.
        Check type of login.
        This class inherits properties of classes
        RegistrationProcess and LogoutAction."""

    # class attribute to validate the login type(customer, guest, admin)
    member_status = ""

    # Constructor
    def __init__(self):
        super().__init__()

    # login functionality to let users login into the application
    def login(self):
        # While logging in, validating if user credentials are already registered
        try:
            df = pd.read_csv('users.csv')
            self.email = input("Please enter email: ")
            self.password = input("Please enter password : ")

            # validation for empty input
            if self.email == "" or self.password == "":
                raise ValueError("You cannot give empty value. Try again")

            # validation if user credentials are registered before letting user login into the application
            if (self.email in df['Email'].values) & (self.password in df['Password'].values):

                # initializing a variable useful to determine who the user is in membertype() method to
                # display respective page
                __class__.member_status = 'Customer'

                print("Welcome back!")  # displaying message

                # letting user start shopping
                LoginAction.membertype(self)

            # validation to check if user trying to login is admin
            elif (self.email == admin_email) & (self.password == admin_password):

                # initializing a variable useful to determine who the user is in membertype() method to
                # display respective page
                __class__.member_status = 'Admin'

                print("Welcome Admin")  # displaying message

                # letting admin start modifying the inventory
                LoginAction.membertype(self)

            # letting user try logging in again if credentials provided are invalid
            else:
                print("Account doesn't exist, try again!")
                LoginAction.login(self)

        except ValueError as e:
            print(e)
            LoginAction.login(self)

    # validating type of login (Customer, Guest, Admin) to display respective page
    def membertype(self):
        while True:
            # Letting admin add, remove, update items in the inventory
            if self.member_status == 'Admin':
                adminobj = AdminAccess()
                adminobj.view_inventory()  # view items from inventory
                try:
                    while True:
                        admin_choice = input("Add or remove from inventory? View or Add or Remove or Update : ")
                        if admin_choice == "Add":
                            adminobj.add_to_inventory()         # add items to inventory
                            break
                        elif admin_choice == "Remove":
                            adminobj.remove_from_inventory()    # remove items from inventory
                            break
                        elif admin_choice == "View":
                            adminobj.view_inventory()           # view items from inventory
                            break
                        elif admin_choice == "Update":
                            adminobj.update_inventory()         # update items from inventory
                            break
                        else:
                            print("Invalid entry, Try again")
                except ValueError:
                    print("Invalid entry")

                # letting admin logout
                print("Want to logout? : ", end="")
                if LogoutAction.logout(self):
                    break

            # Letting user shop for login type is customer or guest
            elif self.member_status == 'Customer' or self.member_status == 'Guest':
                custobj = ShoppingCart()
                custobj.product_catalog()
                custobj.add_item_to_cart()
                custobj.view_cart()
                while True:
                    cust_choice = input("Do you want to remove something from cart? Y or N : ")
                    if cust_choice == "Y":
                        custobj.remove_item_from_cart()
                        custobj.view_cart()
                        custobj.checkout()
                        break
                    elif cust_choice == "N":
                        custobj.checkout()
                        break
                    else:
                        print("Expecting Y or N")
                        break

            # letting user logout
            print("Want to logout? : ", end="")
            if LogoutAction.logout(self):
                break

    # Checking if user has an existing account, if not taking them either to registration process or making them
    # guests as per the user choice
    def status_check(self):
        try:
            userstatus = input("Do you want have an account? Y or N : ")
            if userstatus == "Y":
                LoginAction.login(self)
            elif userstatus == "N":
                reg_choice = input("Do you want to register? Y or N : ")
                if reg_choice == 'Y':
                    RegistrationProcess.register(self)
                    __class__.member_status = 'Customer'
                    LoginAction.membertype(self)
                elif reg_choice == 'N':
                    print("Welcome guest")
                    __class__.member_status = 'Guest'
                    LoginAction.membertype(self)
                else:
                    print("Invalid input")
                    LoginAction.status_check(self)
            else:
                print("Invalid input")
                LoginAction.status_check(self)
        except ValueError:
            print("Invalid input")
            LoginAction.status_check(self)
