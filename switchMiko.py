
from netmiko import ConnectHandler

#netmiko is a ssh library designed for network automation

switchInfo = {
    "device_type": "cisco_ios",
    "ip": "192.168.60.141",
    "username": "cisco",
    "password": "cisco"
}


connectToDevice = ConnectHandler(**switchInfo)  
output = connectToDevice.send_command("show ip int br")
print(output)

interfaceName = "int gigabit "


#this function is when you want to configure a group of interfaces
def loopCommand(interfaceSlot, rangeFrom, rangeTo, commands):
    for i in range(rangeFrom, rangeTo):
        currentInterface = f"{interfaceName}{interfaceSlot}/{str(i)}"
        print("Configuring ", currentInterface)
        myCommands = [currentInterface, *commands]
        sendCommand = connectToDevice.send_config_set(myCommands)
        print(sendCommand)

def configEtherChannel():
    commandList = ["switchport trunk encapsulation dot1q",
                   "switchport mode trunk", "channel-group 1 mode auto"]
    loopCommand("1", 0, 4, commandList) #my switch slots went up to 3 


def configSwitchPortSecurity():
    commandList = ["switchport mode access", "switchport port-security",
                   "switchport port-security violation restrict"]
    loopCommand("2", 0, 3, commandList)  


def main():
    configEtherChannel()
    configSwitchPortSecurity()


""" This Script Configures
Interfaces Gigabit 1/0 - 1/3 with etherchannel
Interfaces Gigabit 2/0 - 1/2 with port security
""" 

if __name__ == "__main__":
    main()
