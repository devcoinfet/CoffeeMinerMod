
# -*- coding: utf-8 -*-
#
import sys
import scapy
from pyroute2.iwutil import IW
from scapy.all import srp
from scapy.all import Ether, ARP, conf
import os
import sys
import subprocess


def system_call(command):
    p = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    return p.stdout.read()


def get_gateway_address(wifi_interface):
    command = "ip route show 0.0.0.0/0 dev " + wifi_interface + "" + " | cut -d\  -f3"
    #print command
    return system_call(command)



def arp_find(iprange):
    target_list = {}
    ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=iprange),timeout=2)
    for s,r in ans:
        #print "{0} is the MAC address for host {1}".format(r.src, r.psrc)
        target_list['Target_IP'] = format(r.psrc) 
        target_list['Target_Mac'] = format(r.src)
    return target_list


def get_iprange(wifi_interface):
    command = "ip -4 addr show " + ''+ wifi_interface +'' + " | grep inet | awk '{ print     $2 }'"
    #print command
    p=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
    data = p.communicate()
    sdata = data[0].split()
    #print(sdata)
    return sdata


def get_wifi_interfaces():
    iw = IW()
    interfaces = {}
    for q in iw.get_interfaces_dump():
        interface_name = q.get_attr('NL80211_ATTR_IFNAME')
        interface_mac = q.get_attr('NL80211_ATTR_MAC')
        interfaces['interface_name'] = interface_name
        interfaces['interface_mac'] = interface_mac
        
    iw.close()
    return interfaces




