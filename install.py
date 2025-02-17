#!/usr/bin/python3
import io
import os
import random
import socket
import subprocess
import sys
import time

import requests

# -------------------------------------------------------------------------
#  1) Python Version Check
# -------------------------------------------------------------------------
if sys.version_info.major != 3:
    print("Please run with python3.")
    sys.exit(1)


# -------------------------------------------------------------------------
#  2) GitHub Release Helper
# -------------------------------------------------------------------------
def get_github_releases():
    """
    Gets the latest release and prerelease from GitHub.

    :return: A dictionary with information about the release and prerelease,
             or an error key if something fails.
    """
    base_url = "https://api.github.com/repos/Vateron-Media/Xtream_main/releases"

    try:
        response = requests.get(base_url)
        response.raise_for_status()

        releases = response.json()
        if not releases:
            return {"error": "No releases found"}

        latest_release = next((r for r in releases if not r.get("prerelease")), None)
        latest_prerelease = next((r for r in releases if r.get("prerelease")), None)

        return {
            "latest_release": latest_release["tag_name"] if latest_release else None,
            "latest_prerelease": (
                latest_prerelease["tag_name"] if latest_prerelease else None
            ),
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}


# -------------------------------------------------------------------------
#  3) Gather Release URLs
# -------------------------------------------------------------------------
releases = get_github_releases()
rDownloadURL = (
    f"https://github.com/Vateron-Media/Xtream_main/releases/download/"
    f"{releases.get('latest_release')}/main_xui.tar.gz"
)
bDownloadURL = (
    f"https://github.com/Vateron-Media/Xtream_main/releases/download/"
    f"{releases.get('latest_prerelease')}/main_xui.tar.gz"
)

# -------------------------------------------------------------------------
#  4) Script Paths and Lists
# -------------------------------------------------------------------------
rPath = os.path.dirname(os.path.realpath(__file__))

rPackages = [
    "cpufrequtils",
    "iproute2",
    "python",  # or python-is-python3 in some OS versions
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

rRemove = ["mysql-server"]

geoliteFiles = ["GeoLite2-City.mmdb", "GeoLite2-Country.mmdb", "GeoLite2-ASN.mmdb"]

rMySQLCnf = """# XC_VM
[client]
port                            = 3306

[mysqld_safe]
nice                            = 0

[mysqld]
user                            = mysql
port                            = 7999
basedir                         = /usr
datadir                         = /var/lib/mysql
tmpdir                          = /tmp
lc-messages-dir                 = /usr/share/mysql
skip-external-locking
skip-name-resolve
bind-address                    = *

key_buffer_size                 = 128M
myisam_sort_buffer_size         = 4M
max_allowed_packet              = 64M
myisam-recover-options          = BACKUP
max_length_for_sort_data        = 8192
query_cache_limit               = 0
query_cache_size                = 0
query_cache_type                = 0
expire_logs_days                = 10
max_binlog_size                 = 100M
max_connections                 = 8192
back_log                        = 4096
open_files_limit                = 20240
innodb_open_files               = 20240
max_connect_errors              = 3072
table_open_cache                = 4096
table_definition_cache          = 4096
tmp_table_size                  = 1G
max_heap_table_size             = 1G

innodb_buffer_pool_size         = 10G
innodb_buffer_pool_instances    = 10
innodb_read_io_threads          = 64
innodb_write_io_threads         = 64
innodb_thread_concurrency       = 0
innodb_flush_log_at_trx_commit  = 0
innodb_flush_method             = O_DIRECT
performance_schema              = 0
innodb-file-per-table           = 1
innodb_io_capacity              = 20000
innodb_table_locks              = 0
innodb_lock_wait_timeout        = 0

sql_mode                        = "NO_ENGINE_SUBSTITUTION"

[mariadb]

thread_cache_size               = 8192
thread_handling                 = pool-of-threads
thread_pool_size                = 12
thread_pool_idle_timeout        = 20
thread_pool_max_threads         = 1024

[mysqldump]
quick
quote-names
max_allowed_packet              = 16M

[mysql]

[isamchk]
key_buffer_size                 = 16M
"""

rConfig = """; XC_VM Configuration
; -----------------
; Your username and password will be encrypted and
; saved to the 'credentials' file in this folder
; automatically.
;
; To change your username or password, modify BOTH
; below and XC_VM will read and re-encrypt them.

[XC_VM]
hostname    =   "127.0.0.1"
database    =   "xc_vm"
port        =   7999
server_id   =   1

[Encrypted]
username    =   "%s"
password    =   "%s"
"""

rSystemd = """[Unit]
SourcePath=/home/xtreamcodes/service
Description=XC_VM Service
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
User=root
Restart=always
RestartSec=1
ExecStart=/bin/bash /home/xtreamcodes/service start
ExecReload=/bin/bash /home/xtreamcodes/service restart
ExecStop=/bin/bash /home/xtreamcodes/service stop

[Install]
WantedBy=multi-user.target
"""

rRedisConfig = """bind *
protected-mode yes
port 6379
tcp-backlog 511
timeout 0
tcp-keepalive 300
daemonize yes
supervised no
pidfile /home/xtreamcodes/bin/redis/redis-server.pid
loglevel warning
logfile /home/xtreamcodes/bin/redis/redis-server.log
databases 1
always-show-logo yes
stop-writes-on-bgsave-error no
rdbcompression no
rdbchecksum no
dbfilename dump.rdb
dir /home/xtreamcodes/bin/redis/
slave-serve-stale-data yes
slave-read-only yes
repl-diskless-sync no
repl-diskless-sync-delay 5
repl-disable-tcp-nodelay no
slave-priority 100
requirepass #PASSWORD#
maxclients 655350
lazyfree-lazy-eviction no
lazyfree-lazy-expire no
lazyfree-lazy-server-del no
slave-lazy-flush no
appendonly no
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-load-truncated yes
aof-use-rdb-preamble no
lua-time-limit 5000
slowlog-log-slower-than 10000
slowlog-max-len 128
latency-monitor-threshold 0
notify-keyspace-events ""
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-size -2
list-compress-depth 0
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64
hll-sparse-max-bytes 3000
activerehashing yes
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit slave 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
hz 10
aof-rewrite-incremental-fsync yes
save 60 1000
server-threads 4
server-thread-affinity true
"""

rSysCtl = """# XC_VM

net.ipv4.tcp_congestion_control = bbr
net.core.default_qdisc = fq
net.ipv4.tcp_rmem = 8192 87380 134217728
net.ipv4.udp_rmem_min = 16384
net.core.rmem_default = 262144
net.core.rmem_max = 268435456
net.ipv4.tcp_wmem = 8192 65536 134217728
net.ipv4.udp_wmem_min = 16384
net.core.wmem_default = 262144
net.core.wmem_max = 268435456
net.core.somaxconn = 1000000
net.core.netdev_max_backlog = 250000
net.core.optmem_max = 65535
net.ipv4.tcp_max_tw_buckets = 1440000
net.ipv4.tcp_max_orphans = 16384
net.ipv4.ip_local_port_range = 2000 65000
net.ipv4.tcp_no_metrics_save = 1
net.ipv4.tcp_slow_start_after_idle = 0
net.ipv4.tcp_fin_timeout = 15
net.ipv4.tcp_keepalive_time = 300
net.ipv4.tcp_keepalive_probes = 5
net.ipv4.tcp_keepalive_intvl = 15
fs.file-max=20970800
fs.nr_open=20970800
fs.aio-max-nr=20970800
net.ipv4.tcp_timestamps = 1
net.ipv4.tcp_window_scaling = 1
net.ipv4.tcp_mtu_probing = 1
net.ipv4.route.flush = 1
net.ipv6.route.flush = 1
"""

rVersions = {
    "18.04": "bionic",
    "20.04": "focal",
    "20.10": "groovy",
    "21.04": "hirsute",
    "21.10": "impish",
    # Add more if needed
}

Choice = "23456789abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ"


class col:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def generate(length=32):
    return "".join(random.choice(Choice) for _ in range(length))


def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def printc(rText, rColour=col.OKBLUE, rPadding=0):
    rLeft = int(30 - (len(rText) / 2))
    rRight = 60 - rLeft - len(rText)
    print(f"{rColour} |{'-'*62}| {col.ENDC}")
    for _ in range(rPadding):
        print(f"{rColour} |{' ' * 62}| {col.ENDC}")
    print(f"{rColour} | {' ' * rLeft}{rText}{' ' * rRight} | {col.ENDC}")
    for _ in range(rPadding):
        print(f"{rColour} |{' ' * 62}| {col.ENDC}")
    print(f"{rColour} |{'-'*62}| {col.ENDC}\n")


if __name__ == "__main__":

    # ---------------------------------------------------------------------
    #  1) Prompt: Stable or Beta?
    # ---------------------------------------------------------------------
    printc("Please select the version")
    printc(
        f"Stable version: {releases.get('latest_release')}  "
        f"Beta version: {releases.get('latest_prerelease')}"
    )
    while True:
        rAnswer = input("Install Stable or Beta? (S / B) : ")
        if rAnswer.upper() in ["S", "B"]:
            break

    if rAnswer.upper() == "B":
        ReleaseURL = bDownloadURL
    else:
        ReleaseURL = rDownloadURL

    # ---------------------------------------------------------------------
    #  2) Check OS Version
    # ---------------------------------------------------------------------
    try:
        rVersion = os.popen("lsb_release -sr").read().strip()
    except:
        rVersion = None

    if rVersion not in rVersions:
        printc("Unsupported Operating System", col.FAIL)
        sys.exit(1)

    # ---------------------------------------------------------------------
    #  3) Insert libzip if Ubuntu 20.04 or 18.04
    # ---------------------------------------------------------------------
    if rVersion == "20.04":
        rPackages.append("libzip5")
    elif rVersion == "18.04":
        rPackages.append("libzip4")
    else:
        rPackages.append("libzip5")

    # ---------------------------------------------------------------------
    #  4) Banner
    # ---------------------------------------------------------------------
    printc("XC_VM", col.OKGREEN, 2)
    rHost = "127.0.0.1"
    rServerID = 1
    rUsername = generate()
    rPassword = generate()
    rDatabase = "xc_vm"
    rPort = 7999

    # ---------------------------------------------------------------------
    #  5) Check if /home/xtreamcodes/ exists
    # ---------------------------------------------------------------------
    if os.path.exists("/home/xtreamcodes/"):
        printc("XC_VM Directory Exists!")
        while True:
            rAnswer = input("Continue and overwrite? (Y / N) : ")
            if rAnswer.upper() in ["Y", "N"]:
                break
        if rAnswer.upper() == "N":
            sys.exit(1)

    # ---------------------------------------------------------------------
    #  6) System Update & Package Install
    # ---------------------------------------------------------------------
    printc("Preparing Installation")
    for rFile in [
        "/var/lib/dpkg/lock-frontend",
        "/var/cache/apt/archives/lock",
        "/var/lib/dpkg/lock",
        "/var/lib/apt/lists/lock",
    ]:
        if os.path.exists(rFile):
            try:
                os.remove(rFile)
            except:
                pass

    printc("Updating system")
    os.system("sudo apt-get update")
    os.system("sudo apt-get -y full-upgrade")
    os.system(
        "sudo DEBIAN_FRONTEND=noninteractive apt-get -yq install software-properties-common"
    )

    # 6.a) Add correct MariaDB repo
    if rVersion in rVersions:
        printc(f"Adding repo: Ubuntu {rVersion}")
        os.system(
            "sudo apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xF1656F24C74CD1D8"
        )
        os.system(
            f"sudo add-apt-repository -y 'deb [arch=amd64,arm64,ppc64el] "
            f"http://ams2.mirrors.digitalocean.com/mariadb/repo/10.6/ubuntu {rVersions[rVersion]} main'"
        )

    os.system("sudo apt-get update")

    # 6.b) Remove conflicting packages
    for pkg in rRemove:
        printc(f"Removing {pkg}")
        os.system(f"sudo apt-get remove {pkg} -y")

    # 6.c) Install all required packages
    for pkg in rPackages:
        printc(f"Installing {pkg}")
        os.system(f"sudo DEBIAN_FRONTEND=noninteractive apt-get -yq install {pkg}")

    os.system("sudo ldconfig")

    # ---------------------------------------------------------------------
    #  7) Create xtreamcodes user
    # ---------------------------------------------------------------------
    try:
        subprocess.check_output("getent passwd xtreamcodes".split())
    except:
        printc("Creating user")
        os.system(
            "sudo adduser --system --shell /bin/false --group --disabled-login xtreamcodes"
        )

    if not os.path.exists("/home/xtreamcodes"):
        os.mkdir("/home/xtreamcodes")

    # ---------------------------------------------------------------------
    #  8) Download & Extract
    # ---------------------------------------------------------------------
    printc("Downloading Software")
    os.system(f'wget -q -O "/tmp/xtreamcodes.tar.gz" "{ReleaseURL}"')
    if os.path.exists("/tmp/xtreamcodes.tar.gz"):
        printc("Installing XC_VM")
        os.system('sudo tar -zxvf "/tmp/xtreamcodes.tar.gz" -C "/home/xtreamcodes/"')
        if not os.path.exists("/home/xtreamcodes/status"):
            printc("Failed to extract! Exiting", col.FAIL)
            sys.exit(1)
    else:
        printc("Download failed", col.FAIL)
        sys.exit(1)

    # ---------------------------------------------------------------------
    #  9) Configure MySQL (MariaDB)
    # ---------------------------------------------------------------------
    printc("Configuring MySQL")
    rCreate = True
    if os.path.exists("/etc/mysql/my.cnf"):
        if open("/etc/mysql/my.cnf", "r").read(5) == "# XC_VM":
            rCreate = False

    if rCreate:
        with io.open("/etc/mysql/my.cnf", "w", encoding="utf-8") as f:
            f.write(rMySQLCnf)
        os.system("sudo service mariadb restart")

    # 9.a) Check if root has a password
    rExtra = ""
    rRet = os.system('mysql -u root -e "SELECT VERSION();"')
    if rRet != 0:
        while True:
            rRootPass = input("Root MySQL Password: ")
            rExtra = f" -p{rRootPass}"
            rRet = os.system(f'mysql -u root{rExtra} -e "SELECT VERSION();"')
            if rRet == 0:
                break
            else:
                printc("Invalid password! Please try again.")

    # 9.b) Create DB and user
    os.system(
        f'sudo mysql -u root{rExtra} -e "DROP DATABASE IF EXISTS xc_vm; CREATE DATABASE IF NOT EXISTS xc_vm;"'
    )
    os.system(
        f'sudo mysql -u root{rExtra} -e "DROP DATABASE IF EXISTS xc_vm_migrate; CREATE DATABASE IF NOT EXISTS xc_vm_migrate;"'
    )

    os.system(
        f'sudo mysql -u root{rExtra} xc_vm < "/home/xtreamcodes/bin/install/database.sql"'
    )

    os.system(
        f"sudo mysql -u root{rExtra} -e \"CREATE USER '{rUsername}'@'localhost' IDENTIFIED BY '{rPassword}';\""
    )
    os.system(
        f"sudo mysql -u root{rExtra} -e \"GRANT ALL PRIVILEGES ON xc_vm.* TO '{rUsername}'@'localhost';\""
    )
    os.system(
        f"sudo mysql -u root{rExtra} -e \"GRANT ALL PRIVILEGES ON xc_vm_migrate.* TO '{rUsername}'@'localhost';\""
    )
    os.system(
        f"sudo mysql -u root{rExtra} -e \"GRANT ALL PRIVILEGES ON mysql.* TO '{rUsername}'@'localhost';\""
    )
    os.system(
        f"sudo mysql -u root{rExtra} -e \"GRANT GRANT OPTION ON xc_vm.* TO '{rUsername}'@'localhost';\""
    )

    os.system(
        f"sudo mysql -u root{rExtra} -e \"CREATE USER '{rUsername}'@'127.0.0.1' IDENTIFIED BY '{rPassword}';\""
    )
    os.system(
        f"sudo mysql -u root{rExtra} -e \"GRANT ALL PRIVILEGES ON xc_vm.* TO '{rUsername}'@'127.0.0.1';\""
    )
    os.system(
        f"sudo mysql -u root{rExtra} -e \"GRANT ALL PRIVILEGES ON xc_vm_migrate.* TO '{rUsername}'@'127.0.0.1';\""
    )
    os.system(
        f"sudo mysql -u root{rExtra} -e \"GRANT ALL PRIVILEGES ON mysql.* TO '{rUsername}'@'127.0.0.1';\""
    )
    os.system(
        f"sudo mysql -u root{rExtra} -e \"GRANT GRANT OPTION ON xc_vm.* TO '{rUsername}'@'127.0.0.1';\""
    )

    os.system(
        f"sudo mysql -u root{rExtra} -e \"GRANT RELOAD ON *.* TO '{rUsername}'@'localhost';\""
    )

    os.system(f'sudo mysql -u root{rExtra} -e "FLUSH PRIVILEGES;"')

    # 9.c) Write config.ini
    rConfigData = rConfig % (rUsername, rPassword)
    with io.open("/home/xtreamcodes/config/config.ini", "w", encoding="utf-8") as f:
        f.write(rConfigData)

    # ---------------------------------------------------------------------
    # 10) System Configurations
    # ---------------------------------------------------------------------
    printc("Configuring System")

    # 10.a) FSTAB for ram-disks
    if "/home/xtreamcodes/" not in open("/etc/fstab").read():
        with io.open("/etc/fstab", "a", encoding="utf-8") as f:
            f.write(
                "\ntmpfs /home/xtreamcodes/content/streams tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=90% 0 0"
            )
            f.write(
                "\ntmpfs /home/xtreamcodes/tmp tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=6G 0 0"
            )

    # 10.b) Systemd service file
    if os.path.exists("/etc/init.d/xtreamcodes"):
        os.remove("/etc/init.d/xtreamcodes")
    if os.path.exists("/etc/systemd/system/xtreamcodes.service"):
        os.remove("/etc/systemd/system/xtreamcodes.service")

    if not os.path.exists("/etc/systemd/system/xtreamcodes.service"):
        with io.open(
            "/etc/systemd/system/xtreamcodes.service", "w", encoding="utf-8"
        ) as f:
            f.write(rSystemd)
        os.system("sudo chmod +x /etc/systemd/system/xtreamcodes.service")
        os.system("sudo systemctl daemon-reload")
        os.system("sudo systemctl enable xtreamcodes")

    # 10.c) sysctl
    print(
        "Custom sysctl.conf - If you have your own custom sysctl.conf, type N "
        "or it will be overwritten. If you don't know what a sysctl configuration is, "
        "type Y as it will correctly set your TCP settings and open file limits."
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
            with io.open("/etc/sysctl.conf", "w", encoding="utf-8") as f:
                f.write(rSysCtl)
            os.system("sudo sysctl -p >/dev/null 2>&1")
            with open("/home/xtreamcodes/config/sysctl.on", "w") as f:
                f.write("")
        except:
            print("Failed to write to sysctl file.")
    else:
        if os.path.exists("/home/xtreamcodes/config/sysctl.on"):
            os.remove("/home/xtreamcodes/config/sysctl.on")

    # 10.d) Increase systemd open-files limit
    systemd_sysconf = "/etc/systemd/system.conf"
    if "DefaultLimitNOFILE=655350" not in open(systemd_sysconf).read():
        os.system(
            'sudo echo "\nDefaultLimitNOFILE=655350" >> "/etc/systemd/system.conf"'
        )
        os.system('sudo echo "\nDefaultLimitNOFILE=655350" >> "/etc/systemd/user.conf"')

    # 10.e) Redis config if not exists
    redis_conf = "/home/xtreamcodes/bin/redis/redis.conf"
    if not os.path.exists(redis_conf):
        with io.open(redis_conf, "w", encoding="utf-8") as f:
            f.write(rRedisConfig)

    # ---------------------------------------------------------------------
    # 11) Final Steps
    # ---------------------------------------------------------------------
    os.system("sleep 2 && sudo mount -a  >/dev/null 2>&1")
    os.system("sudo chown xtreamcodes:xtreamcodes -R /home/xtreamcodes > /dev/null 2>&1")
    
    # Reload systemd just in case
    os.system("sudo systemctl daemon-reload")
    os.system("sudo systemctl start xtreamcodes")

    # Give it a moment to spin up
    time.sleep(10)

    # Start additional processes
    os.system("sudo /home/xtreamcodes/status 1")
    os.system(
        "sudo /home/xtreamcodes/bin/php/bin/php /home/xtreamcodes/includes/cli_tool/startup.php >/dev/null 2>&1"
    )

    # Save credentials for reference
    with io.open(os.path.join(rPath, "credentials.txt"), "w", encoding="utf-8") as f:
        f.write(f"MySQL Username: {rUsername}\nMySQL Password: {rPassword}")

    # ---------------------------------------------------------------------
    # 12) Done
    # ---------------------------------------------------------------------
    printc("Installation completed!", col.OKGREEN, 2)
    printc(f"Continue Setup: http://{getIP()}:25500")

    print(" ")
    printc("Your mysql credentials have been saved to:")
    printc(os.path.join(rPath, "credentials.txt"))

    print(" ")
    printc("Please move this file somewhere safe!")
