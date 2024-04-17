#!/usr/bin/env python3
#networkFileRW.py
#Javaris Snell
#Thursday, March 3, 2022
#Update routers and switches;
#read equipment from a file, write updates & errors to file

import json

##---->>>> Create file constants for the file names; file constants can be reused
##         There are 2 files to read this program: equip_r.txt and equip_s.txt
##         There are 2 files to write in this program: updated.txt and errors.txt
    
EQUIP_R = "equip_r.txt"
EQUIP_S = "equip_s.txt"
UPDATED_FILE = "updated.txt"
ERRORS_FILE = "invalid.txt"

#prompt constants
UPDATE = "\nWhich device would you like to update "
QUIT = "(enter x to quit)? "
NEW_IP = "What is the new IP address (111.111.111.111) "
SORRY = "Sorry, that is not a valid IP address\n"

#function to get valid device
def getValidDevice(routers, switches):
    validDevice = False
    while not validDevice:
        #prompt for device to update
        device = input(UPDATE + QUIT).lower()
        if device in routers.keys():
            return device
        elif device in switches.keys():
            return device
        elif device == 'x':
            return device  
        else:
            print("That device is not in the network inventory.")

#function to get valid IP address
def getValidIP(invalidIPCount, invalidIPAddresses):
    validIP = False
    while not validIP:
        ipAddress = input(NEW_IP)
        if ipAddress.lower() == 'x':
            return ipAddress, invalidIPCount  # Return 'x' if user wants to quit
        octets = ipAddress.split('.')
        if len(octets) != 4:  # Check if there are four parts in the IP address
            invalidIPCount += 1
            invalidIPAddresses.append(ipAddress)
            print(SORRY)
            continue
        validOctets = True
        for byte in octets:
            try:
                byte = int(byte)
                if byte < 0 or byte > 255:
                    validOctets = False
                    break
            except ValueError:
                validOctets = False
                break
        if validOctets:
            return ipAddress, invalidIPCount
        else:
            invalidIPCount += 1
            invalidIPAddresses.append(ipAddress)
            print(SORRY)

def main():
    try:
        #open files here
        with open(EQUIP_R, 'r') as file:
            routers = json.load(file)
        with open(EQUIP_S, 'r') as file:
            switches = json.load(file)
    except FileNotFoundError:
        print("Error: Equipment files not found.")
        return

    #the updated dictionary holds the device name and new ip address
    updated = {}

    #list of bad addresses entered by the user
    invalidIPAddresses = []

    #accumulator variables
    devicesUpdatedCount = 0
    invalidIPCount = 0

    #flags and sentinels
    quitNow = False
    validIP = False

    print("Network Equipment Inventory\n")
    print("\tequipment name\tIP address")
    for router, ipa in routers.items(): 
        print("\t" + router + "\t\t" + ipa)
    for switch, ipa in switches.items():
        print("\t" + switch + "\t\t" + ipa)

    while not quitNow:
        #function call to get valid device
        device = getValidDevice(routers, switches)
        
        if device == 'x':
            quitNow = True
            break
        
        #function call to get valid IP address
        #python lets you return two or more values at one time
        ipAddress, invalidIPCount = getValidIP(invalidIPCount, invalidIPAddresses)
  
        #update device
        if 'r' in device:
            #modify the value associated with the key
            routers[device] = ipAddress 
        else:
            switches[device] = ipAddress

        devicesUpdatedCount += 1
        #add the device and ipAddress to the dictionary
        updated[device] = ipAddress

        print(device, "was updated; the new IP address is", ipAddress)
        #loop back to the beginning

    #user finished updating devices
    print("\nSummary:")
    print()
    print("Number of devices updated:", devicesUpdatedCount)

    #write the updated equipment dictionary to a file
    with open(UPDATED_FILE, 'w') as file:
        json.dump(updated, file)
    print("Updated equipment written to file 'updated.txt'")

    #write the list of invalid addresses to a file
    with open(ERRORS_FILE, 'w') as file:
        for ip in invalidIPAddresses:
            file.write(ip + '\n')
    print("List of invalid addresses written to file 'invalid.txt'")
    
#top-level scope check
if __name__ == "__main__":
    main()
