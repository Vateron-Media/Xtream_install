#!/usr/bin/env python3

import subprocess


def start_xc_vm():
    """Start the xc_vm service."""
    command = ["sudo", "systemctl", "start", "xc_vm"]
    subprocess.run(command)
    print("xc_vm service started.")


def stop_xc_vm():
    """Stop the xc_vm service."""
    command = ["sudo", "systemctl", "stop", "xc_vm"]
    subprocess.run(command)
    print("xc_vm service stopped.")


def restart_xc_vm():
    """Restart the xc_vm service."""
    command = ["sudo", "systemctl", "restart", "xc_vm"]
    subprocess.run(command)
    print("xc_vm service restarted.")


def status_xc_vm():
    """Get the status of the xc_vm service."""
    command = ["sudo", "systemctl", "status", "xc_vm.service"]
    subprocess.run(command)


def enable_xc_vm():
    """Enable the xc_vm service on server boot."""
    command = ["sudo", "systemctl", "enable", "xc_vm"]
    subprocess.run(command)
    print("xc_vm service enabled on boot.")


def disable_xc_vm():
    """Disable the xc_vm service on server boot."""
    command = ["sudo", "systemctl", "disable", "xc_vm"]
    subprocess.run(command)
    print("xc_vm service disabled on boot.")


def print_menu():
    print("\n========   Welcome to   ========")
    print("\n======== XTREAM - TOOLS ========")
    print("1) Start xc_vm")
    print("2) Stop xc_vm")
    print("3) Restart xc_vm")
    print("4) Status of xc_vm")
    print("5) Enable xc_vm (start on boot)")
    print("6) Disable xc_vm (disable on boot)")
    print("7) Exit")
    print("==================================")


def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            start_xc_vm()
        elif choice == "2":
            stop_xc_vm()
        elif choice == "3":
            restart_xc_vm()
        elif choice == "4":
            status_xc_vm()
        elif choice == "5":
            enable_xc_vm()
        elif choice == "6":
            disable_xc_vm()
        elif choice == "7":
            print("Exiting XTREAM TOOLS.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
