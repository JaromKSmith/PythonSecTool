import os
from cryptography.fernet import Fernet


class crypto_tool:

    def read_file(filename):
         return open(filename, "rb").read()
    
    def write_file(filename, content):
         with open(filename, "wb") as file:
              file.write(content)

    def new_key():
        key = Fernet.generate_key()
        os.chdir('./keys')
        name = input("Please enter a name for the key: ")
        if name.endswith(".key") is False:
             name = name +".key"
        with open(name, "wb") as key_file:
            key_file.write(key)
        os.chdir('../')
        return key
        

    def select_key():
         while True:
            os.chdir('./keys')
            print()
            print("---Keys---")
            print(os.listdir('./'))
            print("Please note: using the wrong key may result in unrecoverable files")
            key_choice = input("Please select the correct key for the selected file, type new to create a new key, or press enter to cancel")
            if key_choice == "new":
                os.chdir('../')
                key = crypto_tool.new_key()
                return key
            elif key_choice == "":
                os.chdir('../')
                break
            else:
                if key_choice.endswith(".key") is False:
                    key_choice = key_choice +".key"
                    if os.path.exists(f"./{key_choice}"):
                        print()
                        key = crypto_tool.read_file(key_choice)
                        os.chdir('../')
                        return key
                    else:
                        print("The filename entered does not exist in the current directory")
                        os.chdir('../')
                        continue



    def check_folder():
        if os.path.exists('./txt_files'):
            return
        else:
            os.mkdir('./txt_files')
                

    def encrypt_file(filename, fernet):
        content = crypto_tool.read_file(filename)
        encrypted_content = fernet.encrypt(content)
        crypto_tool.write_file(filename, encrypted_content)
        pass

    def encrypt_text(content, fernet):
        encrypted_content = fernet.encrypt(content)
        crypto_tool.save_new_file(encrypted_content)
        pass
    
    def decrypt_file(filename, fernet):
        content = crypto_tool.read_file(filename)
        decrypted_content = fernet.decrypt(content)
        crypto_tool.write_file(filename, decrypted_content)
        pass
    
    def load_key():
        return open("secret.key", "rb").read()

         

    def encrypt_decrypt(filename, fernet):
         while True:
            print("Please check if the selected file is already encrypted or not to avoid confusion")
            choice = input("Select 1 to encrypt, 2 to decrypt, or press enter to cancel")
            if choice == "1":
                crypto_tool.encrypt_file(filename, fernet)
                break
            elif choice == "2":
                crypto_tool.decrypt_file(filename, fernet)
                break
            elif choice == "":
                break
            else: 
                 print(f"{choice} is not a valid input, please select a valid option")
            

    def save_new_file(text):
        filename = input("Please enter a name for the new file: ")
        if filename.endswith(".txt") is False:
            filename = filename +".txt"
        with open(filename, 'wb') as file:
                        file.write(text)
        



    def crypto_tool_menu():

        crypto_tool.check_folder()
        while True:
            print()
            print("Welcome to the Cryptography tool")
            
            print("Encrypt or Decrypt an existing or create a new text file: 1")
            print("Return to the tool suite: 2")
            choice = input("Please select an option (1/2): ")

            if choice == "1":

                # key = crypto_tool.load_key()
                # fernet = Fernet(key)
            
                while True:
                    os.chdir('./txt_files')
                    print()
                    print("Files: ") 
                    print(os.listdir('./'))
                    choice2 = input("Enter the name of the file you want to edit, type new to create a new file, or press enter to cancel: ")

                    if choice2 == "":
                        os.chdir('../')
                        break
                    elif choice2 == "new":
                        content = input("Please enter the text you would like to encrypt and save: ")
                        bytes_content = bytes(content, 'utf-8')
                        os.chdir('../') 
                        fernet = Fernet(crypto_tool.select_key())
                        os.chdir('./txt_files')
                        crypto_tool.encrypt_text(bytes_content, fernet)
                        os.chdir('../')
                        break
                    else:
                        if choice2.endswith(".txt") is False: #adding the .txt filename extension if the esure didn't include it
                            choice2 = choice2 +".txt"
                        if os.path.exists(f"./{choice2}"):
                            print()
                            os.chdir('../')
                            fernet = Fernet(crypto_tool.select_key())
                            
                            os.chdir('./txt_files')
                            crypto_tool.encrypt_decrypt(choice2, fernet)
                            os.chdir('../')
                            break
                        else:
                            print("The filename entered does not exist in the current directory")
                            os.chdir('../')
                            continue

                
            elif choice == "2":
                break
            else:
                print(f"{choice} is not a valid input, please select a valid option")