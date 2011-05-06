#!/bin/sh

# Run in the computer want to access but is not connected to the Internets
# Root powers needed

ifconfig eth0 192.168.5.2
route add default gw 192.168.5.1
echo "nameserver 8.8.8.8" >> /etc/resolv.conf
