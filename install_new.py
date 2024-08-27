#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time
import os
import random
import shutil
import socket
import subprocess
import sys
import base64
import io

Version_main = "v1.2.2"
rDownloadURL = f"https://github.com/Vateron-Media/Xtream_main/releases/download/{Version_main}/main_xui.tar.gz"

rPath = os.path.dirname(os.path.realpath(__file__))
rPackages = [
    "cpufrequtils",
    "iproute2",
    "python",
    "net-tools",
    "dirmngr",
    "gpg-agent",
    "software-properties-common",
    "libcurl4",
    "libxslt1-dev",
    "libgeoip-dev",
    "libonig-dev",
    "e2fsprogs",
    "wget",
    "sysstat",
    "alsa-utils",
    "v4l-utils",
    "mcrypt",
    "nscd",
    "htop",
    "iptables-persistent",
    "libjpeg-dev",
    "libpng-dev",
    "php-ssh2",
    "xz-utils",
    "zip",
    "unzip",
    "mc",
    "libpng16-16",
    "libzip5",
    "mariadb-server",
    "rsync",
]
rRemove = ["mysql-server"]
rMySQLCnf = base64.b64decode(
    "IyBYdHJlYW0gQ29kZXMKCltjbGllbnRdCnBvcnQgICAgICAgICAgICA9IDMzMDYKCltteXNxbGRfc2FmZV0KbmljZSAgICAgICAgICAgID0gMAoKW215c3FsZF0KdXNlciAgICAgICAgICAgID0gbXlzcWwKcG9ydCAgICAgICAgICAgID0gNzk5OQpiYXNlZGlyICAgICAgICAgPSAvdXNyCmRhdGFkaXIgICAgICAgICA9IC92YXIvbGliL215c3FsCnRtcGRpciAgICAgICAgICA9IC90bXAKbGMtbWVzc2FnZXMtZGlyID0gL3Vzci9zaGFyZS9teXNxbApza2lwLWV4dGVybmFsLWxvY2tpbmcKc2tpcC1uYW1lLXJlc29sdmU9MQoKYmluZC1hZGRyZXNzICAgICAgICAgICAgPSAqCmtleV9idWZmZXJfc2l6ZSA9IDEyOE0KCm15aXNhbV9zb3J0X2J1ZmZlcl9zaXplID0gNE0KbWF4X2FsbG93ZWRfcGFja2V0ICAgICAgPSA2NE0KbXlpc2FtLXJlY292ZXItb3B0aW9ucyA9IEJBQ0tVUAptYXhfbGVuZ3RoX2Zvcl9zb3J0X2RhdGEgPSA4MTkyCnF1ZXJ5X2NhY2hlX2xpbWl0ICAgICAgID0gNE0KcXVlcnlfY2FjaGVfc2l6ZSAgICAgICAgPSAwCnF1ZXJ5X2NhY2hlX3R5cGUJPSAwCgpleHBpcmVfbG9nc19kYXlzICAgICAgICA9IDEwCm1heF9iaW5sb2dfc2l6ZSAgICAgICAgID0gMTAwTQoKbWF4X2Nvbm5lY3Rpb25zICA9IDIwMDAgI3JlY29tbWVuZGVkIGZvciAxNkdCIHJhbSAKYmFja19sb2cgPSA0MDk2Cm9wZW5fZmlsZXNfbGltaXQgPSAxNjM4NAppbm5vZGJfb3Blbl9maWxlcyA9IDE2Mzg0Cm1heF9jb25uZWN0X2Vycm9ycyA9IDMwNzIKdGFibGVfb3Blbl9jYWNoZSA9IDQwOTYKdGFibGVfZGVmaW5pdGlvbl9jYWNoZSA9IDQwOTYKCgp0bXBfdGFibGVfc2l6ZSA9IDFHCm1heF9oZWFwX3RhYmxlX3NpemUgPSAxRwoKaW5ub2RiX2J1ZmZlcl9wb29sX3NpemUgPSAxMkcgI3JlY29tbWVuZGVkIGZvciAxNkdCIHJhbQppbm5vZGJfYnVmZmVyX3Bvb2xfaW5zdGFuY2VzID0gMQppbm5vZGJfcmVhZF9pb190aHJlYWRzID0gNjQKaW5ub2RiX3dyaXRlX2lvX3RocmVhZHMgPSA2NAppbm5vZGJfdGhyZWFkX2NvbmN1cnJlbmN5ID0gMAppbm5vZGJfZmx1c2hfbG9nX2F0X3RyeF9jb21taXQgPSAwCmlubm9kYl9mbHVzaF9tZXRob2QgPSBPX0RJUkVDVApwZXJmb3JtYW5jZV9zY2hlbWEgPSBPTgppbm5vZGItZmlsZS1wZXItdGFibGUgPSAxCmlubm9kYl9pb19jYXBhY2l0eT0yMDAwMAppbm5vZGJfdGFibGVfbG9ja3MgPSAwCmlubm9kYl9sb2NrX3dhaXRfdGltZW91dCA9IDAKaW5ub2RiX2RlYWRsb2NrX2RldGVjdCA9IDAKaW5ub2RiX2xvZ19maWxlX3NpemUgPSA1MTJNCgpzcWwtbW9kZT0iTk9fRU5HSU5FX1NVQlNUSVRVVElPTiIKCltteXNxbGR1bXBdCnF1aWNrCnF1b3RlLW5hbWVzCm1heF9hbGxvd2VkX3BhY2tldCAgICAgID0gMTZNCgpbbXlzcWxdCgpbaXNhbWNoa10Ka2V5X2J1ZmZlcl9zaXplICAgICAgICAgICAgICA9IDE2TQo="
).decode("utf-8")
rConfig = '; XtreamCodes Configuration\n; -----------------\n; Your username and password will be encrypted and\n; saved to the \'credentials\' file in this folder\n; automatically.\n;\n; To change your username or password, modify BOTH\n; below and XtreamCodes will read and re-encrypt them.\n\n[XtreamCodes]\nhostname    =   "127.0.0.1"\ndatabase    =   "xtream_iptvpro"\nport        =   7999\nserver_id   =   1\n\n[Encrypted]\nusername    =   "%s"\npassword    =   "%s"'
geoliteFiles = ["GeoLite2-City.mmdb", "GeoLite2-Country.mmdb", "GeoLite2-ASN.mmdb"]
rSystemd = "[Unit]\nSourcePath=/home/xtreamcodes/service\nDescription=XtreamCodes Service\nAfter=network.target\nStartLimitIntervalSec=0\n\n[Service]\nType=simple\nUser=root\nRestart=always\nRestartSec=1\nExecStart=/bin/bash /home/xtreamcodes/service start\nExecRestart=/bin/bash /home/xtreamcodes/service restart\nExecStop=/bin/bash /home/xtreamcodes/service stop\n\n[Install]\nWantedBy=multi-user.target"
rSysCtl = "# XtreamCodes\n\nnet.ipv4.tcp_congestion_control = bbr\nnet.core.default_qdisc = fq\nnet.ipv4.tcp_rmem = 8192 87380 134217728\nnet.ipv4.udp_rmem_min = 16384\nnet.core.rmem_default = 262144\nnet.core.rmem_max = 268435456\nnet.ipv4.tcp_wmem = 8192 65536 134217728\nnet.ipv4.udp_wmem_min = 16384\nnet.core.wmem_default = 262144\nnet.core.wmem_max = 268435456\nnet.core.somaxconn = 1000000\nnet.core.netdev_max_backlog = 250000\nnet.core.optmem_max = 65535\nnet.ipv4.tcp_max_tw_buckets = 1440000\nnet.ipv4.tcp_max_orphans = 16384\nnet.ipv4.ip_local_port_range = 2000 65000\nnet.ipv4.tcp_no_metrics_save = 1\nnet.ipv4.tcp_slow_start_after_idle = 0\nnet.ipv4.tcp_fin_timeout = 15\nnet.ipv4.tcp_keepalive_time = 300\nnet.ipv4.tcp_keepalive_probes = 5\nnet.ipv4.tcp_keepalive_intvl = 15\nfs.file-max=20970800\nfs.nr_open=20970800\nfs.aio-max-nr=20970800\nnet.ipv4.tcp_timestamps = 1\nnet.ipv4.tcp_window_scaling = 1\nnet.ipv4.tcp_mtu_probing = 1\nnet.ipv4.route.flush = 1\nnet.ipv6.route.flush = 1"
Choice = "23456789abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ"

rVersions = {
    "14.04": "trusty",
    "16.04": "xenial",
    "18.04": "bionic",
    "20.04": "focal",
    "20.10": "groovy",
    "21.04": "hirsute",
    "21.10": "impish",
}


class col:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    YELLOW = "\033[33m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def generate(length=32):
    return "".join(random.choice(Choice) for i in range(length))


def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def getVersion():
    try:
        return subprocess.check_output("lsb_release -d".split()).split(":")[-1].strip()
    except:
        return ""


def printc(rText, rColour=col.OKBLUE, rPadding=0):
    rLeft = int(30 - (len(rText) / 2))
    rRight = 60 - rLeft - len(rText)
    print(
        "%s |--------------------------------------------------------------| %s"
        % (rColour, col.ENDC)
    )
    for i in range(rPadding):
        print(
            "%s |                                                              | %s"
            % (rColour, col.ENDC)
        )
    print("%s | %s%s%s | %s" % (rColour, " " * rLeft, rText, " " * rRight, col.ENDC))
    for i in range(rPadding):
        print(
            "%s |                                                              | %s"
            % (rColour, col.ENDC)
        )
    print(
        "%s |--------------------------------------------------------------| %s"
        % (rColour, col.ENDC)
    )
    print(" ")


if __name__ == "__main__":
    ##################################################
    # START                                          #
    ##################################################
    try:
        rVersion = os.popen("lsb_release -sr").read().strip()
    except:
        rVersion = None
    # if rVersion not in rVersions:
    #     printc("Unsupported Operating System")
    #     sys.exit(1)

    printc("XtreamUI Ubuntu 20.04 - Moded Divarion-D", col.OKGREEN, 2)
    rHost = "127.0.0.1"
    rServerID = 1
    rUsername = "user_iptvpro"
    rPassword = generate()
    rDatabase = "xtream_iptvpro"
    rPort = 7999

    if os.path.exists("/home/xtreamcodes/"):
        printc("XtreamCodes Directory Exists!")
        while True:
            rAnswer = input("Continue and overwrite? (Y / N) : ")
            if rAnswer.upper() in ["Y", "N"]:
                break
        if rAnswer == "N":
            sys.exit(1)

    ##################################################
    # UPGRADE                                        #
    ##################################################

    printc("Preparing Installation")
    for rFile in [
        "/var/lib/dpkg/lock-frontend",
        "/var/cache/apt/archives/lock",
        "/var/lib/dpkg/lock",
    ]:
        if os.path.exists(rFile):
            try:
                os.remove(rFile)
            except:
                pass

    if os.path.isfile("/home/xtreamcodes/config"):
        shutil.copyfile("/home/xtreamcodes/config", "/tmp/config.xtmp")
    # for geoliteFile in geoliteFiles:
    #     if os.path.isfile(f"/home/xtreamcodes/bin/maxmind/{geoliteFile}"):
    #         os.system(
    #             f"chattr -i /home/xtreamcodes/bin/maxmind/{geoliteFile} > /dev/null"
    #         )

    printc("Updating system")

    os.system("apt-get update > /dev/null")
    os.system("apt-get -y full-upgrade > /dev/null")
    os.system(
        "sudo DEBIAN_FRONTEND=noninteractive apt-get -yq install software-properties-common"
    )
    if rVersion in rVersions:
        printc("Adding repo: Ubuntu %s" % rVersion)
        os.system(
            "sudo apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xF1656F24C74CD1D8"
        )
        os.system(
            "sudo add-apt-repository -y 'deb [arch=amd64,arm64,ppc64el] http://ams2.mirrors.digitalocean.com/mariadb/repo/10.6/ubuntu %s main'"
            % rVersions[rVersion]
        )
    os.system("apt-get update > /dev/null")
    for rPackage in rRemove:
        printc("Removing %s" % rPackage)
        os.system("sudo apt-get remove %s -y" % rPackage)

    for rPackage in rPackages:
        printc("Installing %s" % rPackage)
        os.system(
            "sudo DEBIAN_FRONTEND=noninteractive apt-get -yq install %s" % rPackage
        )
    printc("Installing pip3")
    os.system(
        "add-apt-repository universe > /dev/null 2>&1 && curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py > /dev/null 2>&1 && python3 get-pip.py > /dev/null 2>&1"
    )
    printc("Installing pip modules")
    os.system(
        "pip3 install ndg-httpsclient > /dev/null 2>&1 && pip3 install pyopenssl > /dev/null 2>&1 && pip3 install pyasn1 > /dev/null 2>&1"
    )

    try:
        subprocess.check_output("getent passwd xtreamcodes > /dev/null".split())
    except:
        # Create User
        printc("Creating user xtreamcodes")
        os.system(
            "adduser --system --shell /bin/false --group --disabled-login xtreamcodes > /dev/null"
        )

    if not os.path.exists("/home/xtreamcodes"):
        os.mkdir("/home/xtreamcodes")

    ##################################################
    # INSTALL                                        #
    ##################################################

    printc("Downloading Software")
    os.system('wget -q -O "/tmp/xtreamcodes.tar.gz" "%s"' % rDownloadURL)
    if os.path.exists("/tmp/xtreamcodes.tar.gz"):
        printc("Installing Software")
        os.system(
            'tar -xvf "/tmp/xtreamcodes.tar.gz" -C "/home/xtreamcodes/" > /dev/null'
        )
        try:
            os.remove("/tmp/xtreamcodes.tar.gz")
        except:
            pass
        if not os.path.exists("/home/xtreamcodes/status"):
            printc("Failed to extract! Exiting")
            sys.exit(1)
    else:
        printc("Download failed", col.FAIL)
        sys.exit(1)

    ##################################################
    # MYSQL                                          #
    ##################################################

    printc("Configuring MySQL")
    rCreate = True
    if os.path.exists("/etc/mysql/my.cnf"):
        if open("/etc/mysql/my.cnf", "r").read(14) == "# Xtream Codes":
            rCreate = False
    if rCreate:
        shutil.copy("/etc/mysql/my.cnf", "/etc/mysql/my.cnf.xc")
        rFile = open("/etc/mysql/my.cnf", "w")
        rFile.write(rMySQLCnf)
        rFile.close()
        os.system("sudo service mariadb restart")

    rExtra = ""
    rRet = os.system('mysql -u root -e "SELECT VERSION();"')
    if rRet != 0:
        while True:
            rExtra = " -p%s" % input("Root MySQL Password: ")
            rRet = os.system('mysql -u root%s -e "SELECT VERSION();"' % rExtra)
            if rRet == 0:
                break
            else:
                printc("Invalid password! Please try again.")

    os.system(
        'sudo mysql -u root%s -e "DROP DATABASE IF EXISTS xtream_iptvpro; CREATE DATABASE IF NOT EXISTS xtream_iptvpro;"'
        % rExtra
    )
    os.system(
        'sudo mysql -u root%s xtream_iptvpro < "/home/xtreamcodes/database.sql"'
        % rExtra
    )
    os.system(
        "sudo mysql -u root%s -e \"USE xtream_iptvpro; REPLACE INTO reg_users (id, username, password, email, member_group_id, verified, status) VALUES (1, 'admin', '\$6\$rounds=20000\$xtreamcodes\$XThC5OwfuS0YwS4ahiifzF14vkGbGsFF1w7ETL4sRRC5sOrAWCjWvQJDromZUQoQuwbAXAFdX3h3Cp3vqulpS0', 'admin@website.com', 1, 1, 1);\" > /dev/null"
        % rExtra
    )
    os.system(
        "sudo mysql -u root%s -e \"USE xtream_iptvpro; CREATE TABLE IF NOT EXISTS dashboard_statistics (id int(11) NOT NULL AUTO_INCREMENT, type varchar(16) NOT NULL DEFAULT '', time int(16) NOT NULL DEFAULT '0', count int(16) NOT NULL DEFAULT '0', PRIMARY KEY (id)) ENGINE=InnoDB DEFAULT CHARSET=latin1; INSERT INTO dashboard_statistics (type, time, count) VALUES('conns', UNIX_TIMESTAMP(), 0),('users', UNIX_TIMESTAMP(), 0);\" > /dev/null"
        % rExtra
    )
    os.system(
        "sudo mysql -u root%s -e \"CREATE USER '%s'@'localhost' IDENTIFIED BY '%s';\""
        % (rExtra, rUsername, rPassword)
    )
    os.system(
        "sudo mysql -u root%s -e \"GRANT ALL PRIVILEGES ON xtream_iptvpro.* TO '%s'@'localhost';\""
        % (rExtra, rUsername)
    )
    os.system(
        "sudo mysql -u root%s -e \"GRANT ALL PRIVILEGES ON mysql.* TO '%s'@'localhost';\""
        % (rExtra, rUsername)
    )
    os.system(
        "sudo mysql -u root%s -e \"GRANT GRANT OPTION ON xtream_iptvpro.* TO '%s'@'localhost';\""
        % (rExtra, rUsername)
    )
    os.system(
        "sudo mysql -u root%s -e \"CREATE USER '%s'@'127.0.0.1' IDENTIFIED BY '%s';\""
        % (rExtra, rUsername, rPassword)
    )
    os.system(
        "sudo mysql -u root%s -e \"GRANT ALL PRIVILEGES ON xtream_iptvpro.* TO '%s'@'127.0.0.1';\""
        % (rExtra, rUsername)
    )

    os.system(
        "sudo mysql -u root%s -e \"GRANT ALL PRIVILEGES ON mysql.* TO '%s'@'127.0.0.1';\""
        % (rExtra, rUsername)
    )
    os.system(
        "sudo mysql -u root%s -e \"GRANT GRANT OPTION ON xtream_iptvpro.* TO '%s'@'127.0.0.1';\""
        % (rExtra, rUsername)
    )
    os.remove("/home/xtreamcodes/database.sql")

    # if not folder config
    if not os.path.exists("/home/xtreamcodes/config"):
        os.mkdir("/home/xtreamcodes/config")
    rConfigData = rConfig % (rUsername, rPassword)
    rFile = io.open("/home/xtreamcodes/config/config.ini", "w", encoding="utf-8")
    rFile.write(rConfigData)
    rFile.close()

    ##################################################
    # CONFIGURE                                      #
    ##################################################

    printc("Configuring System")
    if not "/home/xtreamcodes/" in open("/etc/fstab").read():
        rFile = io.open("/etc/fstab", "a", encoding="utf-8")
        rFile.write(
            "tmpfs /home/xtreamcodes/content/streams tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=90% 0 0\ntmpfs /home/xtreamcodes/tmp tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=2G 0 0"
        )
        rFile.close()
    if not "xtreamcodes" in open("/etc/sudoers").read():
        os.system(
            'echo "xtreamcodes ALL = (root) NOPASSWD: /sbin/iptables, /usr/bin/chattr, /usr/bin/python3, /usr/bin/python" >> /etc/sudoers'
        )
    if os.path.exists("/etc/init.d/xtreamcodes"):
        os.remove("/etc/init.d/xtreamcodes")

    if not os.path.exists("/etc/systemd/system/xtreamcodes.service"):
        rFile = io.open(
            "/etc/systemd/system/xtreamcodes.service", "w", encoding="utf-8"
        )
        rFile.write(rSystemd)
        rFile.close()
        os.system("sudo chmod +x /etc/systemd/system/xtreamcodes.service")
        os.system("sudo systemctl daemon-reload")
        os.system("sudo systemctl enable xtreamcodes")
    print(
        "Custom sysctl.conf - If you have your own custom sysctl.conf, type N or it will be overwritten. If you don't know what a sysctl configuration is, type Y as it will correctly set your TCP settings and open file limits."
    )
    print(" ")
    while True:
        rAnswer = input("Overwrite sysctl configuration? Recommended! (Y / N): ")
        if rAnswer.upper() in ["Y", "N"]:
            break
    if rAnswer.upper() == "Y":
        try:
            os.system("sudo modprobe ip_conntrack")
        except:
            pass
        try:
            rFile = io.open("/etc/sysctl.conf", "w", encoding="utf-8")
            rFile.write(rSysCtl)
            rFile.close()
            os.system("sudo sysctl -p >/dev/null 2>&1")
            rFile = open("/home/xtreamcodes/config/sysctl.on", "w")
            rFile.close()
        except:
            print("Failed to write to sysctl file.")
    else:
        if os.path.exists("/home/xtreamcodes/config/sysctl.on"):
            os.remove("/home/xtreamcodes/config/sysctl.on")
    if not "DefaultLimitNOFILE=655350" in open("/etc/systemd/system.conf").read():
        os.system(
            'sudo echo "\nDefaultLimitNOFILE=655350" >> "/etc/systemd/system.conf"'
        )
        os.system('sudo echo "\nDefaultLimitNOFILE=655350" >> "/etc/systemd/user.conf"')

    ##################################################
    # FINISHED                                       #
    ##################################################

    if not os.path.exists("/home/xtreamcodes/tmp"):
        os.mkdir("/home/xtreamcodes/tmp")
    
    if not os.path.exists("/home/xtreamcodes/logs"):
        os.mkdir("/home/xtreamcodes/logs")


    if not os.path.exists("/home/xtreamcodes/content"):
        os.mkdir("/home/xtreamcodes/content")

    if not os.path.exists("/home/xtreamcodes/content/streams"):
        os.mkdir("/home/xtreamcodes/content/streams")

    os.system("sudo mount -a  >/dev/null 2>&1")
    os.system(
        "sudo chown xtreamcodes:xtreamcodes -R /home/xtreamcodes > /dev/null 2>&1"
    )
    os.system("sleep 2 && sudo /home/xtreamcodes/permissions.sh > /dev/null")
    os.system("sudo systemctl daemon-reload")
    os.system("sudo systemctl start xtreamcodes")

    time.sleep(10)
    os.system("sudo /home/xtreamcodes/status 1")
    os.system(
        "sudo /home/xtreamcodes/bin/php/bin/php /home/xtreamcodes/tools/startup.php >/dev/null 2>&1"
    )
    # for geoliteFile in geoliteFiles:
    #     if os.path.isfile(f"/home/xtreamcodes/bin/maxmind/{geoliteFile}"):
    #         os.system(
    #             f"chattr +i /home/xtreamcodes/bin/maxmind/{geoliteFile} > /dev/null"
    #         )

    rFile = io.open(rPath + "/credentials.txt", "w", encoding="utf-8")
    rFile.write("MySQL Username: %s\nMySQL Password: %s" % (rUsername, rPassword))
    rFile.close()

    printc("Installation completed!", col.OKGREEN, 2)
    print(" ")
    printc("Your mysql credentials have been saved to:")
    printc(rPath + "/credentials.txt")
    print(" ")
    printc("Please move this file somewhere safe!")
    print(" ")
    printc("Admin UI: http://%s:25500" % getIP())
    printc("Admin UI default login is admin/admin")
