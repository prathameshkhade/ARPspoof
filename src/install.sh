#!/bin/bash

# Update apt
printf "[+] Updating apt...\n"
sudo apt update
printf "\n[✓] apt updated."
sleep 1
clear

# install or upgrade python3
printf "[+] Installing python...\n"
apt install python3 -y
printf "\n[✓] python installed."
sleep 1
clear

# Install dependencies
printf "[+] Installing dependencies...\n"
pip3 install scapy
printf "\n[✓] done!"
sleep 1