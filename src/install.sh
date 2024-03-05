#!/bin/bash

# Update apt
printf "[+] Updating apt...\n"
sudo apt update

if [[$? -eq 0]] then
	printf "\n[✓] apt updated."
else 
	printf "\n[!] apt not updated!"
fi

sleep 1
clear

# install or upgrade python3
printf "[+] Installing python...\n"
apt install python3 -y

if [[$? -eq 0]] then
	printf "\n[✓] python3 installed."
else
	printf "\n[!] python3 not installed!"
fi

sleep 1
clear

# Install dependencies
printf "[+] Installing dependencies...\n"
pip3 install -r requirements.txt

if [[$? -eq 0]] then
	printf "\n[✓] done!"
else
	printf "\n[!] dependencies not installed!"
fi

sleep 1
