import socket
import json
import ipaddress
import os

class network_scanner:
#this method checks if the provided IP is valid
    def check_ip(ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except:
            return False

    #method to scan the IP address and port combination provided
    def scan(ip, port):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((ip, port))
            sock.close()
            if result == 0:
                readable_result = "Open"
            else:
                readable_result = "Closed"
            

            scan_result = ("Target IP: " + ip,"Port: " + str(port),"Result: " + readable_result)
            
            return scan_result

    #this method dumps the nested list of the scan results into a json file named by the user
    def save_scan(results):
        filename = input("Please enter a name for this scan: ")
        if filename.endswith(".json") is False:
            filename = filename +".json"
        network_scanner.scan_folder()
        os.chdir('./scan_results')
        with open(filename, 'w') as file:
            json.dump(results, file)
            print(f"Results saved as: {filename}")
        os.chdir('../')

    #this method returns the contents of a json file(used later to populate the scan_results nested list if you want to view the results)
    def get_scan(filename):
        try: 
            with open(filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError: 
            return{}
        
    #method to check if there is already a folder with scan results and create one if not
    def scan_folder():
        if os.path.exists('./scan_results'):
            return
        else:
            os.mkdir('./scan_results')

    #main method
    def main():
        scan_results = []
        scan_bool = False
        while True:
            print()
            print("Welcome to the network scanner tool:")
            print("Main Menu:")
            print("1. Scan a target")
            print("2. Print most recent scan results")
            print("3. Retrieve saved scan results")
            print("4. Save recent scan")
            print("5. Retrun to tool suite")
            choice = input("Enter your choice (1/2/3/4/5): ")
            if choice == "1":
                target = input("Enter a target (e.g., www.example.com, IP address, or for a list of IP addresses, enter the starting and ending IP separated by commas): ")

                #loops and operators to make sure the IPs entered are valid, and the starting IP does not come after the ending IP
                if target.startswith("www."):
                    continue
                elif target.find(", ") == -1:
                    while True:
                        if network_scanner.check_ip(target):
                            print("valid IP")
                            ip_range = [target]
                            break
                        else:
                            print("An invalid IP address has been entered")
                            target = input("Please enter a valid IP")
                #this checks if there is a ", " in the input provided which would mean the starting and ending IP for the range
                elif target.find(", ") != -1: 
                    while True:
                        #this splits the user input into separate IP addresses and then checks to make sure they are both valid and in correct order
                        target.replace(" ", "")
                        start_end = [ip for ip in target.split(",")]
                        print(start_end)
                        ip1 = str(start_end[0])
                        ip2 = str(start_end[1])
                        start_octets = [int(oc) for oc in start_end[0].split(".")]
                        end_octets = [int(oc) for oc in start_end[1].split(".")]
                        if start_octets[0] > end_octets[0]:
                            print("An invalid format for IP ranges has been entered, please ensure the starting IP comes before the ending IP")
                            target = input("Please enter a valid starting and ending IP separated by commas")
                        if start_octets[0] == end_octets[0] and start_octets[1] > end_octets[1]:
                            print("An invalid format for IP ranges has been entered, please ensure the starting IP comes before the ending IP")
                            target = input("Please enter a valid starting and ending IP separated by commas")
                        if start_octets[0] == end_octets[0] and start_octets[1] == end_octets[1] and start_octets[2] > end_octets[2]:
                            print("An invalid format for IP ranges has been entered, please ensure the starting IP comes before the ending IP")
                            target = input("Please enter a valid starting and ending IP separated by commas")
                        if start_octets[0] == end_octets[0] and start_octets[1] > end_octets[1] and start_octets[2] == end_octets[2] and start_octets[3] > end_octets[3]:
                            print("An invalid format for IP ranges has been entered, please ensure the starting IP comes before the ending IP")
                            target = input("Please enter a valid starting and ending IP separated by commas")
                        if network_scanner.check_ip(ip1) is False or network_scanner.check_ip(ip2) is False:
                            print("An invalid IP address has been entered")
                            target = input("Please enter a valid starting and ending IP separated by commas")
                        else:
                            break

                    #separating the starting and ending IP address into octets to iterate through all possible IPs and creating the ip_range list to be used later
                    start_octets = [int(oc) for oc in start_end[0].split(".")]
                    end_octets = [int(oc) for oc in start_end[1].split(".")]
                    ip_range = []

                    #while loop to iterate through the range of possible IP address and add them to a list until the ending Ip is reached
                    while True:
                        ip_range.append(f"{start_octets[0]}.{start_octets[1]}.{start_octets[2]}.{start_octets[3]}")
                        print(start_octets)
                        if start_octets == end_octets:
                            break
                        #check if the fourth octet has hit 255, and if it has to add 1 to the third octet and reset the fourth octet to zero
                        elif start_octets[3] == 255 and start_octets[2] < end_octets[2] or start_octets[1] < end_octets[1] or start_octets[0] < end_octets[0]:
                            start_octets[3] = 0
                            start_octets[2] = start_octets[2] + 1
                            continue
                        #check if the third octet has hit 255, and if it has to add 1 to the second octet and reset the third octet to zero
                        elif start_octets[2] == 255 and (start_octets[1] < end_octets[1] or start_octets[0] < end_octets[0]):
                            start_octets[2] = 0
                            start_octets[1] = start_octets[1] + 1
                            continue
                        #check if the second octet has hit 255, and if it has to add 1 to the first octet and reset the second octet to zero
                        elif start_octets[1] == 255 and  start_octets[0] < end_octets[0]:
                            start_octets[1] = 0
                            start_octets[0] = start_octets[0] + 1
                        #add one to the fourth octet
                        else:
                            start_octets[3] = start_octets[3] + 1 
                            continue
        
                #get target ports from user and split beginning and ending port if multiple are entered
                while True:
                    ports = input("Enter ports (e.g., 80, 443, or a starting and ending port separated by a comma): ")
                    ports.replace(" ", "")
                    port_start_end = [port for port in ports.split(",")]

                    port_count = 0
                    #this counts how many ports were entered by the user
                    for port in port_start_end:
                        port_count = port_count + 1
                    #if there were only two, that would be the correct format for a range and port_range is filled for the range
                    if port_count == 2:
                        start_port = port_start_end[0]
                        end_port = port_start_end[1]
                        port_range = [port for port in range(int(start_port), int(end_port)+1)]
                        for target_ip in ip_range:
                            for target_port in port_range:
                                scan_results.append(network_scanner.scan(target_ip, target_port))
                        scan_bool = True
                        break
                    #if there is only one port provided we just scan that port 
                    elif port_count == 1:
                        port_range = [int(ports)]
                        for ip in ip_range:
                            for port in port_range:
                                scan_results.append(network_scanner.scan(ip, port))
                        scan_bool = True
                        break
                    else:
                        print("Invalid format for target ports")
                        continue
                print("Scan complete")
                

            elif choice == "3":
                #checking if the scan results directory is present and moving to that directory if it is
                try:
                    os.chdir('./scan_results')
                    os.chdir('../')
                except:
                    print("There are no saved scans on this drive, please conduct a scan")
                    continue
                

                while True:
                    os.chdir('./scan_results')
                    print("Saved scan files: ")
                    print(os.listdir('./'))
                    select = input("Please enter the name of the file you want to view or press enter to return to the main menu: ")
                    if select == "":
                        os.chdir('../')
                        break
                    else:
                        if select.endswith(".json") is False: #adding the .json filename extension if the esure didn't include it
                            select = select +".json"
                        if os.path.exists(f"./{select}"):
                            scan_results = network_scanner.get_scan(select)
                            for item in scan_results:
                                print()
                                for detail in item:
                                    print(detail)
                            os.chdir('../')
                            break
                        else:
                            print("The filename entered does not exist in the current directory")
                            os.chdir('../')
                            continue
                    

            elif choice == "4":    
                network_scanner.save_scan(scan_results)


            elif choice == "5":
                print("Exiting")
                break

            elif choice == "2":
                print()
                if scan_bool is False:
                    print("There has not been a scan conducted in this session\nPlease conduct a scan, or retrieve saved results")
                else:
                    for item in scan_results:
                        print()
                        for detail in item:
                            print(detail)
            else:
                print("An invalid option was selected, please try again.")

if __name__ == "__main__":
    network_scanner.main()
