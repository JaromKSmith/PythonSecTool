import requests
import math

#john the ripper password checker
#rock you wordlist

class password_check:

    def recommendations():
        print()
        print(
            """To create a strong password the more characters used, the better.
        You can try making your password longer, and making sure there are a 
        variety of character types such as uppercase and lowercase letters, 
        numbers, and special characters. A combination of this variety and 
        length will make a strong password. Additionally, some passwords are 
        commonly used such as '123456' or 'password' these types of passwords
        should be avoided."""
        )

    def entropy(password):
        if str(password).isupper() or str(password).islower():
            size = 26
        else:
            size = 52
        for symbol in ('~', '!', '@', '#', '$', '%', '^', '&', '*', '-', '_', '-', '=', '+', ',', '.', '<', '>', '?', ' '):
            if str(password).find(symbol) != -1:
                size = size + 33
                break

        for i in password:
            try:
             int(i)
             size = size + 10
             break
            except:
                continue
        # for num in range(10):
        #     if password.find(num) != "-1":
        #         size = size + 10
        #         break
        length = 0
        for i in password:
            length = length + 1 
        print(f"Length: {length}, charset size: {size}")
        log_size = math.log(size)
        log2 = math.log(2)
        entropy = (length)*(log_size/log2)
        return entropy
        

    def check_strength(password):
        #can do math from crypto class to find bits of entropy and time to brute force
        #then check password against rockyou wordlist to see if it is a common/broken password
        entropy = password_check.entropy(password)
        print()
        print(f"The given password has {entropy} bits of entropy,")

        #assuming 1000 attempts per second
        time =  int((2**entropy)/1000000/60/60/24)
        print(f"It would take {time} days to brute force at 1 Million attempts per second, but some attackers can do much more")
        print(password_check.check_rock_you(password))
        print()
        choice = input("For recommendations on how to create a strong password select 1, or press enter to continue")
        if choice == "1":
            password_check.recommendations()

    def check_rock_you(password):
        with open("1_million_passwords.txt",  errors="ignore") as file:
            contents = file.read()
            search_word = password
            if search_word in contents:
                return "The entered password was found in a list of commonly used passwords, I recommend not using it."
            else:
                return "The entered password was not found in a list of common passwords."
        
    def password_check_menu():

        print("Welcome to the password strength checker tool")

        while True:
            
            choice = input("Please select 1 to check a password or 2 to return to the tool suite: ")
            if choice == "1":
                password = input("Please enter a password to check: ")
                password_check.check_strength(password)
                
            elif choice == "2":
                break

            else:
                print(f"'{choice}' is not a valid option")