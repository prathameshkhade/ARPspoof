from scapy.all import Ether, ARP, send 
from argparse import ArgumentParser
from sys import argv
from os import getuid

parser = ArgumentParser(argv)

def main():
    if(getuid() == 0):
        print("[*] Your are root!!!")
    else:
        print("[*] Your not a root user, please run the script with the root user.....")
        print("[*] Exiting")
        # return exit(-1)
    
main()