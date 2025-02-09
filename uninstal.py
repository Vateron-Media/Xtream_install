#!/usr/bin/python3
import os
import shutil


# Color output in the terminal
class col:
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"


def printc(message, color=col.OKGREEN):
    print(f"{color}{message}{col.ENDC}")


def run_command(command):
    """Run the command in the terminal"""
    return os.system(command)


def remove_directory(path):
    """Safely delete a directory"""
    if os.path.exists(path):
        printc(f"Удаление {path} ...", col.WARNING)
        shutil.rmtree(path, ignore_errors=True)


def remove_file(path):
    """Safely delete a file"""
    if os.path.exists(path):
        printc(f"Удаление {path} ...", col.WARNING)
        os.remove(path)


def stop_services():
    """Stop and disable the systemd service Xtream Codes"""
    printc("Stopping Xtream Codes services...", col.WARNING)
    run_command("sudo systemctl stop xtreamcodes")
    run_command("sudo systemctl disable xtreamcodes")
    run_command("sudo systemctl daemon-reload")


def remove_systemd():
    """Delete the systemd unit file Xtream Codes"""
    printc("Deleting the systemd configuration...", col.WARNING)
    remove_file("/etc/systemd/system/xtreamcodes.service")
    run_command("sudo systemctl daemon-reload")


def remove_cronjobs():
    """Delete cron jobs related to Xtream Codes"""
    printc("Deleting cron tasks...", col.WARNING)
    run_command("sudo crontab -u xtreamcodes -r")
    run_command("sudo rm -f /etc/cron.d/xtreamcodes")


def remove_fstab_entries():
    """Remove temporary file systems associated with Xtream Codes"""
    printc("Deleting the fstab configuration...", col.WARNING)
    fstab_path = "/etc/fstab"
    if os.path.exists(fstab_path):
        with open(fstab_path, "r") as fstab_file:
            lines = fstab_file.readlines()
        with open(fstab_path, "w") as fstab_file:
            for line in lines:
                if "xtreamcodes" not in line:
                    fstab_file.write(line)
    run_command("sudo mount -a")


def remove_iptables_rules():
    """Remove iptables rules if they have been added"""
    printc("Clearing iptables from Xtream Codes rules...", col.WARNING)
    run_command("sudo iptables -F")
    run_command("sudo iptables -X")
    run_command("sudo iptables-save > /etc/iptables/rules.v4")


def remove_redis():
    """Stop and uninstall Redis if it was installed for Xtream Codes"""
    printc("Deleting a Redis configuration...", col.WARNING)
    run_command("sudo systemctl stop redis-server")
    remove_file("/etc/systemd/system/redis.service")
    remove_directory("/home/xtreamcodes/bin/redis")


def remove_mysql():
    """Delete databases and MySQL user if they were created by Xtream Codes"""
    printc("Deleting the Xtream Codes database...", col.WARNING)
    mysql_commands = [
        "DROP DATABASE IF EXISTS xc_vm;",
        "DROP DATABASE IF EXISTS xc_vm_migrate;",
        "DROP USER IF EXISTS 'xtreamcodes'@'localhost';",
        "DROP USER IF EXISTS 'xtreamcodes'@'127.0.0.1';",
        "FLUSH PRIVILEGES;",
    ]
    for cmd in mysql_commands:
        run_command(f'sudo mysql -u root -e "{cmd}"')


def remove_dependencies():
    """Uninstalling packages if they are not used by other programs"""
    printc("Removing dependencies...", col.WARNING)
    packages = [
        "cpufrequtils",
        "iproute2",
        "net-tools",
        "dirmngr",
        "gpg-agent",
        "software-properties-common",
        "libmaxminddb0",
        "libmaxminddb-dev",
        "mmdb-bin",
        "libcurl4",
        "libgeoip-dev",
        "libxslt1-dev",
        "libonig-dev",
        "e2fsprogs",
        "wget",
        "mariadb-server",
        "sysstat",
        "alsa-utils",
        "v4l-utils",
        "mcrypt",
        "certbot",
        "iptables-persistent",
        "libjpeg-dev",
        "libpng-dev",
        "php-ssh2",
        "xz-utils",
        "zip",
        "unzip",
    ]
    run_command(f"sudo apt-get remove --purge -y {' '.join(packages)}")
    run_command("sudo apt-get autoremove -y")
    run_command("sudo apt-get clean")


def remove_xtreamcodes_files():
    """Delete Xtream Codes folders and files"""
    remove_directory("/home/xtreamcodes")
    remove_directory("/var/log/xtreamcodes")
    remove_directory("/etc/nginx/sites-enabled/xtreamcodes.conf")
    remove_file("/etc/systemd/system/xtreamcodes.service")


def remove_user():
    """Remove the Xtream Codes system user"""
    printc("Deleting the xtreamcodes system user...", col.WARNING)
    run_command("sudo userdel -r xtreamcodes")


def final_cleanup():
    """Final system cleanup"""
    printc("Final system cleanup...", col.WARNING)
    run_command("sudo systemctl daemon-reload")
    run_command("sudo systemctl reset-failed")
    run_command("sudo systemctl restart networking")


# Запуск скрипта
if __name__ == "__main__":
    printc("The removal of Xtream Codes has begun...", col.OKGREEN)

    stop_services()
    remove_systemd()
    remove_cronjobs()
    remove_fstab_entries()
    remove_iptables_rules()
    remove_redis()
    remove_mysql()
    remove_xtreamcodes_files()
    remove_user()
    remove_dependencies()
    final_cleanup()

    printc("Xtream Codes успешно удалён!", col.OKGREEN)
