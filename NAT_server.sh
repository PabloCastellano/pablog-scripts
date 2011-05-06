#!/bin/sh

# Run in the computer that is connected to the Internets
# Root powers needed

echo 1 > /proc/sys/net/ipv4/ip_forward

iptables -F -t nat
iptables -P FORWARD ACCEPT
iptables -t nat -A POSTROUTING -o wlan3 -s 192.168.5.0/255.255.255.0 -j MASQUERADE

ifconfig eth0 192.168.5.1
