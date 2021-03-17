from netmiko import ConnectHandler
def main():
    ask_ip_switch = str(input("Enter switches IP address: "))
    ask_username = 'Thanh' #str(input("Enter username: "))
    ask_password = 'cisco'#str(input("Enter password: "))
    ask_secret = 'cisco'#str(input("Enter secret password: "))
    ask_core = str(input("Is it core? (y/n): "))
    ask_cvs_file = str(input("Enter csv file name: "))
    switchDevice = {
        'device_type': 'cisco_ios',
        'ip': ask_ip_switch,
        'username': ask_username,
        'password': ask_password,
        'secret': ask_secret
    }
    ssh_connect = ConnectHandler(**switchDevice)

    ssh_connect.enable()
    output = ssh_connect.send_command('show version')
    print(output)

    config_command = ['hostname test1']
    output = ssh_connect.send_config_set(config_command)
    if ask_core == 'y':
        f1 = open("STNW-core-IP.csv", 'r')
        line = f1.readline()
        while line != '':
            elements = line.split(',')
            if elements[2].split('/')[1].strip() == "24":
                mask = '255.255.255.0'
            elif elements[2].split('/')[1].strip() == "16":
                mask = '255.255.0.0'
            else:
                mask = '255.0.0.0'
            interface_command = "interface vlan " + elements[0]
            ip_address_command = "ip address " + elements[2].split('/')[0] + " " + mask
            vlan_config_commands = [interface_command, ip_address_command, 'no shut']
            output = ssh_connect.send_config_set(vlan_config_commands)
            print(output)
            line = f1.readline()

        f2 = open("STNW-core-dhcp.csv", 'r')
        line = f2.readline()
        while line != '':
            element = line.split(',')
            ip_dhcp_pool_command = "ip dhcp pool " + element[0]
            network_command = "network " + element[1] + " " + element[2]
            default_router = "default-router " + element[3]
            dns_config = "dns-server " + element[4]
            dhcp_commands = [ip_dhcp_pool_command, network_command, default_router, dns_config]
            output = ssh_connect.send_config_set(dhcp_commands)
            print(output)
            line = f2.readline()
    else:
        f3 = open(ask_cvs_file, 'r')
        line = f3.readline()
        element3 = line.split(',')
        ip_switch = "interface " + element3[3]
        swport1_switch = "switchport mode access"
        swport2_switch = "switchport access " + element3[1]
        swport_commands = [ip_switch, swport1_switch, swport2_switch]
        output = ssh_connect.send_config_set(swport_commands)
        print(output)

        ssh_connect.disconnect()

main()
