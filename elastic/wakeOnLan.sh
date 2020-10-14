#!/bin/bash

# MAC Addresses are defined here
dev1=e4:54:e8:81:33:f8
dev2=e4:54:e8:81:33:f8
dev3=e4:54:e8:81:33:f8
dev4=e4:54:e8:81:33:f8
dev5=e4:54:e8:81:33:f8
dev6=e4:54:e8:81:33:f8

# wake up all the devices
echo "Sending packets to wake up devices..."
/usr/bin/wol $dev1
/usr/bin/wol $dev2
/usr/bin/wol $dev3
/usr/bin/wol $dev4
/usr/bin/wol $dev5
/usr/bin/wol $dev6
echo "Sent."
