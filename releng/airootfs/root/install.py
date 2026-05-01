import getpass
import subprocess
import sys

from scripts.run.run import run
from scripts.selectdisk.select_disk import select_disk
from scripts.installpackages.installpackages import installpackages
from scripts.systemsetting.systemsetting import systemsetting
from scripts.mountdisk.mountdisk import mountdisk



def main():
    subprocess.run(['clear'], shell=True)
    print("-" * 50)
    print()
    print("Wierd Core Insall Script")
    print()
    print("-" * 50)
    print()

    disk = select_disk()

    mountdisk(disk)

    run("genfstab -U /mnt >> /mnt/etc/fstab")

    run("pacstrap -K /mnt base linux-zen linux-firmware intel-ucode btrfs-progs systemd systemd-sysvcompat sudo")
    
    installpackages()

    username = input("Write your username: ")
    password = getpass.getpass("Write your password: ")

    systemsetting(username, password)

    print("Copy configs...")
    run(f"mkdir -p /mnt/home/{username}/.config/")
    run(f'cp -r /etc/skel/.bashrc /mnt/home/{username}/ 2> /dev/null || true')
    run(f"cp -r /etc/skel/.config/* /mnt/home/{username}/.config/ 2>/dev/null || true")
    run(f"cp -r /usr/share/pixmaps/weirdcore.png /mnt/usr/share/pixmaps/ 2> /dev/null || true")
    run("chmod 664 /usr/share/pixmaps/weirdcore.png")
    
    # cp /root/logo/weirdcore.png /usr/share/pixmaps/
    # chmod 664 /usr/share/pixmaps/weirdcore.png

    print('Install completed')
    print(f"   DISK {disk}")
    print(f"   USERNAME: {username}")
    print(f"   PASSWORD: {password}")

    while True:
        is_reboot = input("Reboot system ? ").strip()

        if not is_reboot:
            print("Please write yes (y) or No (n)")
            continue
        
        if is_reboot.lower() == "yes" or is_reboot.lower() == "y":
            run("reboot")
        else:
            sys.exit(1)
            
if __name__ == "__main__":
    main()

