import bcrypt

# Functions related to master pwd
def set_mp():
    while True:
        master_pwd = input("Enter new master password: ")
        match_pwd = input("Re-enter master password: ")
        if master_pwd == match_pwd:
            return master_pwd
        print("Passwords do not match. Please try again.\n")

def hash_mp(master_pwd):
    salt = bcrypt.gensalt()
    hashed_mp = bcrypt.hashpw(master_pwd.encode("utf-8"), salt)
    with open("hashed_mp.txt", "wb") as file:
        file.write(hashed_mp)

def get_salt():
    with open("hashed_mp.txt", "rb") as file:
        salt = file.read()[7:29]
    return salt

def check_mp(password):
    with open("hashed_mp.txt", "rb") as file:
        hashed_mp = file.read()
    return bcrypt.checkpw(password.encode("utf-8"), hashed_mp)

def change_mp():
    if check_mp(input("Enter current master password: ")):
        print()
        new_mp = set_mp()
        hash_mp(new_mp)
        return new_mp
    else:
        print("Master password is incorrect.")
        return None