from password_check import password_check
from crypto_tool import crypto_tool
from scanner import network_scanner
from url_check import UrlCheckApp
import tkinter as tk

def main():
    while True:
        print()
        print("Welcome to my integrated security tool suite")
        print("Available tools:")
        print("Password Strength/common password list: 1")
        print("Encrypt/Decrypt files: 2")
        print("Socket Network Scanner: 3")
        print("URL security scanner: 4")

        choice = input("Please select an option(1/2/3/4 or exit to quit)")

        if choice == "1":
            password_check.password_check_menu()
        
        elif choice == "2":
            crypto_tool.crypto_tool_menu()

        elif choice == "3":
            network_scanner.main()
        
        elif choice == "4":
            root = tk.Tk()
            app = UrlCheckApp(root)
            root.mainloop()

        elif choice == "exit": 

            break
        else:
            print(f"{choice} is not a valid option, please try again.")

if __name__ == "__main__":
    main()
