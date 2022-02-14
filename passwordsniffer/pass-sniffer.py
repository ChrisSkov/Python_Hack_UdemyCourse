from scapy.all import *
from urllib import parse
import re

iface = "eth0"

def get_login_pass():


def pkt_parser(packet):


try:
    sniff(iface=iface, prn=pkt_parser, store=0)
except KeyboardInterrupt:
    print('Exiting')
    exit(0)