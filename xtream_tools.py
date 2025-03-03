#!/usr/bin/env python3

import subprocess
import re


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


def mariadb_memory_fix():
    """Fix mariadb out of memory"""
    try:
        # Get total memory
        with open("/proc/meminfo", "r") as f:
            meminfo = f.read()

        total_mem_kb = int(re.search(r"MemTotal:\s+(\d+) kB", meminfo).group(1))
        total_mem_mb = total_mem_kb // 1024  # Convert to megabytes

        # Calculate 70% of the available memory in MB
        buffer_pool_mb = int(total_mem_mb * 0.7)

        # Define the format of the value
        if buffer_pool_mb >= 1024 and (buffer_pool_mb % 1024 == 0):
            # If it is a multiple of 1024, we use gigabytes
            buffer_size = f"{buffer_pool_mb // 1024}G"
        else:
            # In all other cases, megabytes
            buffer_size = f"{buffer_pool_mb}M"

        # Update config file
        config_path = "/etc/mysql/my.cnf"

        with open(config_path, "r") as f:
            config = f.readlines()

        updated = False
        for i, line in enumerate(config):
            if line.strip().startswith("innodb_buffer_pool_size"):
                config[i] = f"innodb_buffer_pool_size = {buffer_size}\n"
                updated = True
                break

        if not updated:
            for i, line in enumerate(config):
                if line.strip().startswith("[mysqld]"):
                    config.insert(i + 1, f"innodb_buffer_pool_size = {buffer_size}\n")
                    break

        with open(config_path, "w") as f:
            f.writelines(config)

        print(f"Set: innodb_buffer_pool_size = {buffer_size}")
        print("Restarting MariaDB")
        subprocess.run(["sudo", "systemctl", "restart", "mariadb"])

    except Exception as e:
        print(f"Ошибка: {str(e)}")
        exit(1)

    print("mariadb out of memory fixed.")


def print_menu():
    print("\n========   Welcome to   ========")
    print("\n======== XTREAM - TOOLS ========")
    print("1) Start xc_vm")
    print("2) Stop xc_vm")
    print("3) Restart xc_vm")
    print("4) Status of xc_vm")
    print("5) Enable xc_vm (start on boot)")
    print("6) Disable xc_vm (disable on boot)")
    print("7) Fix mariadb out of memory")
    print("8) Exit")
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
            mariadb_memory_fix()
        elif choice == "8":
            print("Exiting XTREAM TOOLS.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
