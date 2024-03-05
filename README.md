# 🫣 ARPspoof

This is a simple python script which sends the malicious spoofed ARP packets to the target IP address. 

It continuously sends ARP requests to the victim IP and Router. Simply, it generates packets with your MAC address as a source and sends these packets to the victim and router. So, the victim thinks that you are the router and the router thinks that you are the victim. i.e., you are sniffing the data packets that the victim sends to the router and vice versa. 

Then you can use the `dsniff` for capturing any username and password for unencrypted data packets. Further you can use the `dnsspoof` tool for modifying dns queries. 


## 💻 Installation 

1. Clone the repository: 
```sh
git clone https://github.com/prathameshkhade/ARPspoof
```
2. Change your current working directory:
```sh
cd ARPspoof/src/
```
3. Install scapy library required for creating and sending packets in requirements.txt:
```sh
pip3 install -r requirements.txt
``` 
- Or use the script for installing python and scapy library:
```bash
chmod 744 install.sh && ./install.sh
```

## 🪴 Usage

```sh
sudo arpspoof.py -v <VICTIM IP> -r <ROUTER/GATEWAY IP> -i <INTERFACE>
``` 

## 🤹‍♀️ Options

| Arguments |Alternative Arguments| Description |
|:---------:|:-------------------:| :----------:|
|-v          |  --victim  | IP address of the victim |
|-r          | --router | IP address of the Router or Gateway|
|-i          |  --interface  | Interface to be used for sending ARP packets |
|-h        | --help   |  Disaply the help menu|
