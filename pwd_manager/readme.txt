## Outline
Command Line Interface
- Take master password, validate and show/save entries
- Copy generated password to clipboard


## Implementation

## Configure
- Master Password is first inputted while configuring, and hashed to file using bcrypt
- Derive Fernet key using Master Key (PBKDF)
- The Master Key is then used to encrypt/decrypt entries

## Add new entries
Ask for Master Password
Validate Master Password by hashing and checking with existing hash
Input fields: app name, username, password (starting with these for now)
Encrypt username & pwd with Master Key and save fields into the database

## Get entry
- Input the app name to search for
- Display 1/more entries based on app name
Decrypt & display fields 





have yet to implement more security stuff like input validation; error handling is not in place.
only got the basic functionality down



stuff to add in the future:
pwd strength checker
pwd expiry


2fa
pwd sharing?
logging?
rbac


1. secure password generation: strong random password generation based on user preferences
2. encrypted storage
3. autofill & autologin
4. cross platform compatability
5. secure sharing & emergency access
6. 2fa
