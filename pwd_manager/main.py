import os
import mp_handler
import key_handler
from menu import PasswordManager

def start():
    if os.path.exists("hashed_mp.txt"):
        master_pwd = input("Enter your master password: ")

        if mp_handler.check_mp(master_pwd):
            master_key = key_handler.generate_master_key(master_pwd, mp_handler.get_salt())
            menu = PasswordManager(master_key)
            menu.get_to_work()
        else:
            print("Master password is incorrect.\n")
            return start()

    else: # First time running program
        print("\nCreating master password.")
        print("This password will be used to login to the password manager.")
        print("Do not misplace or forget this password.")
        master_pwd = mp_handler.set_mp()
        mp_handler.hash_mp(master_pwd)
        print("Master password has been created. Please re-login.")


if __name__ == "__main__":
    start()