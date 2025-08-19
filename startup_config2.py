#!/usr/bin/env python


import os
import requests
import hashlib
import sys

# Install and boot system (only if checksum matches)
os.system(f"FastCli -p 15 -c 'configure terminal'")
os.system(f"FastCli -p 15 -c 'interface management 1'")
os.system(f"FastCli -p 15 -c 'ip address dhcp'")
os.system(f"FastCli -p 15 -c 'no shut'")
os.system(f"FastCli -p 15 -c 'ip route 0.0.0.0/0 192.168.5.1'")
os.system(f"FastCli -p 15 -c 'write memory'")

print("Downloading EOS now")
os.system(f"FastCli -p 15 -c 'copy tftp://192.168.4.199/vEOS-lab-4.34.2F.swi flash:'")

os.system(f"FastCli -p 15 -c 'install image flash:vEOS-lab-4.34.2F.swi'")
os.system(f"FastCli -p 15 -c 'boot system flash:vEOS-lab-4.34.2F.swi'")
print("EOS image installation and boot system update commands executed.")
os.system(f"FastCli -p 15 -c 'write memory'")

os.system("FastCli -p 15 -c 'reload now'")
