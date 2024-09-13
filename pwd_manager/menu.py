import os
import sys
import string
import random
import pickle
import pyperclip
import mp_handler
import key_handler
from datetime import datetime

class PasswordManager:
    def __init__(self, master_key):
        self.master_key = master_key
        self.pwds = {}
        self.load_passwords()

    def load_passwords(self):
        if os.path.exists("pwds.txt"):
            with open("pwds.txt", "rb") as file:
                self.pwds = pickle.load(file)

    def save_passwords(self):
        with open("pwds.txt", "wb") as file:
            pickle.dump(self.pwds, file)

    def get_pwd(self, master_key, app_name):
        username = key_handler.decrypt_msg(master_key, self.pwds[app_name][0])
        password = key_handler.decrypt_msg(master_key, self.pwds[app_name][1])
        last_modified = self.pwds[app_name][2]
        return username, password, last_modified

    def generate_password(self, length):
        chars = string.ascii_letters + string.digits + string.punctuation
        password = ""
        for i in range(length):
            password += random.choice(chars)
        return password
    
    def get_generated_password(self, length):
        random_pwd = self.generate_password(length)
        print("\nRandom password:", random_pwd)
        check = input("Generate new password? (y/n): ")
        if check.lower() == "y":
            return self.get_generated_password(length)
        else:
            return random_pwd

    def add_password(self, app_name, username, password):
        enc_username = key_handler.encrypt_msg(self.master_key, username)
        enc_password = key_handler.encrypt_msg(self.master_key, password)
        self.pwds[app_name] = [enc_username, enc_password, datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        self.save_passwords()

    def remove_password(self, app_name):
        if app_name in self.pwds:
            check = input("Confirm delete? (y/n): ")
            if check == "y":
                del self.pwds[app_name]
                self.save_passwords()
        else:
            print("Password has not been saved.")

    def search_password(self, app_name):
        if app_name in self.pwds:
            username, password, last_modified = self.get_pwd(self.master_key, app_name)
            print("Username:", username)
            print("Password:", password)
            print("Last modified:", last_modified)
            pyperclip.copy(password)
        else:
            print(f"Password for {app_name} has not been saved.")

    def display_all_apps(self):
        if not self.pwds:
            print("No passwords currently saved.")
        else:
            for app_name in self.pwds:
                print()
                username = self.get_pwd(self.master_key, app_name)[0]
                print(app_name)
                print("Username:", username)
                

    def find_vuln_pwds(self):
        is_vuln = 0
        if not self.pwds:
            print("No passwords currently saved.")
        else:
            for app_name in self.pwds:
                last_modified = self.get_pwd(self.master_key, app_name)[2]
                last_modified = datetime.strptime(last_modified, '%Y-%m-%d %H:%M:%S')

                if (datetime.now().day-last_modified.day)>365:
                    print(f'{app_name}\'s password has not been changed since {last_modified}.')
                    is_vuln = 1

        if is_vuln==0: 
            print("All passwords are up-to-date.")

                


    def change_master_password(self):
        check = input("Are you sure you want to change the master password? (y/n): ")
        if check.lower() == "y":
            new_mp = mp_handler.change_mp()
            if new_mp is not None:
                new_mk = key_handler.generate_master_key(new_mp, mp_handler.get_salt())
                for app_name in self.pwds:
                    for i in range(len(self.pwds[app_name])):
                        self.pwds[app_name][i] = key_handler.rotate_keys(self.master_key, new_mk, self.pwds[app_name][i])
                self.save_passwords()
                print("Password successfully changed. Please re-login.")
                sys.exit()
        else:
            print("Master password change cancelled")

    def get_to_work(self):
        choice = self.prompt()

        if choice == "1":
            length = int(input("Enter the desired length of the password: "))
            random_pwd = self.get_generated_password(length)
            pyperclip.copy(random_pwd)
            print("Password copied.")

        elif choice == "2":
            app_name = input("Please enter site/app name: ")
            if app_name not in self.pwds:
                username = input("Please enter username: ")
                password = input("Please enter password: ")
                self.add_password(app_name, username, password)
            else:
                print(f"Password for {app_name} has already been saved.")

        elif choice == "3":
            app_name = input("Please enter site/app name: ")
            self.remove_password(app_name)

        elif choice == "4":
            app_name = input("Please enter site/app name: ")
            self.search_password(app_name)

        elif choice == "5":
            self.display_all_apps()

        elif choice == "6":
            self.find_vuln_pwds()

        elif choice == "7":
            self.change_master_password()

        elif choice == "q":
            sys.exit()

        else:
            print("Please enter a valid option.")
            
        self.get_to_work()

    def prompt(self):
        print("\nMenu")
        print("(1) Generate password")
        print("(2) Add password")
        print("(3) Remove password")
        print("(4) Search by app name")
        print("(5) Get all saved apps")
        print("(6) Find expired passwords")
        print("(7) Change master password")
        print("(q) Quit")
        choice = input(">> ")
        return choice