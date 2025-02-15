#!/usr/bin/env python3

import subprocess

def start_xtreamcodes():
    """Start the xtreamcodes service."""
    command = ["sudo", "systemctl", "start", "xtreamcodes"]
    subprocess.run(command)
    print("xtreamcodes service started.")

def stop_xtreamcodes():
    """Stop the xtreamcodes service."""
    command = ["sudo", "systemctl", "stop", "xtreamcodes"]
    subprocess.run(command)
    print("xtreamcodes service stopped.")

def restart_xtreamcodes():
    """Restart the xtreamcodes service."""
    command = ["sudo", "systemctl", "restart", "xtreamcodes"]
    subprocess.run(command)
    print("xtreamcodes service restarted.")

def status_xtreamcodes():
    """Get the status of the xtreamcodes service."""
    command = ["sudo", "systemctl", "status", "xtreamcodes.service"]
    subprocess.run(command)

def enable_xtreamcodes():
    """Enable the xtreamcodes service on server boot."""
    command = ["sudo", "systemctl", "enable", "xtreamcodes"]
    subprocess.run(command)
    print("xtreamcodes service enabled on boot.")

def disable_xtreamcodes():
    """Disable the xtreamcodes service on server boot."""
    command = ["sudo", "systemctl", "disable", "xtreamcodes"]
    subprocess.run(command)
    print("xtreamcodes service disabled on boot.")

def print_menu():
    print("\n========   Welcome to   ========")
    print("\n======== XTREAM - TOOLS ========")
    print("1) Start xtreamcodes")
    print("2) Stop xtreamcodes")
    print("3) Restart xtreamcodes")
    print("4) Status of xtreamcodes")
    print("5) Enable xtreamcodes (start on boot)")
    print("6) Disable xtreamcodes (disable on boot)")
    print("7) Exit")
    print("==================================")
    
def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            start_xtreamcodes()
        elif choice == '2':
            stop_xtreamcodes()
        elif choice == '3':
            restart_xtreamcodes()
        elif choice == '4':
            status_xtreamcodes()
        elif choice == '5':
            enable_xtreamcodes()
        elif choice == '6':
            disable_xtreamcodes()
        elif choice == '7':
            print("Exiting XTREAM TOOLS.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
