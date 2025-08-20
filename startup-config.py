configuration terminal
interface management 1
ip address dhcp
no shutdown
ip route 0.0.0.0/0 192.168.5.1
boot system flash: vEOS-lab-4.34.2F.swi
write memory
