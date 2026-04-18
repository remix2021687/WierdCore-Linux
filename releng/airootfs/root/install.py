import getpass
import subprocess
import sys

from scripts.run.run import run
from scripts.selectdisk.select_disk import select_disk
from scripts.installpackages.installpackages import installpackages
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

    print("Setting system... (fstab, bootloader, users)")

    username = input("Write your username: ")
    password = getpass.getpass("Write your password: ")    

    chroot_script = f"""#!/bin/bash
set -e

ln -sf /usr/share/zoneinfo/Europe/Prague /etc/localtime

hwclock --systohc

echo "ru_RU.UTF-8 UTF-8" >> /etc/locale.gen
echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
locale-gen

echo "LANG=ru_RU.UTF-8" > /etc/locale.conf
echo "weirdcore" > /etc/hostname

groupadd -f wheel
groupadd -f audio
groupadd -f video
groupadd -f storage

mkdir -p /etc/sudoers.d/

useradd -m --group wheel,audio,video,storage {username}
echo "{username}:{password}" | chpasswd
echo "{username} ALL=(ALL) ALL" >> /etc/sudoers.d/00_{username}
chmod 440 /etc/sudoers.d/00_{username}

pacman -S --noconfirm grub efibootmgr
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB --recheck 

cat > /etc/default/grub << 'EOF'
GRUB_DEFAULT=0
GRUB_TIMEOUT=3
GRUB_DISTRIBUTOR="WierdCore Linux"
GRUB_CMDLINE_LINUX_DEFAULT="loglevel=3 quiet"
GRUB_CMDLINE_LINUX="rootflags=subvol=@"
GRUB_PRELOAD_MODULES="part_gpt part_msdos"
GRUB_TIMEOUT_STYLE=menu
GRUB_TERMINAL_INPUT=console
GRUB_GFXMODE=auto
GRUB_GFXPAYLOAD_LINUX=keep
GRUB_DISABLE_RECOVERY=true
GRUB_DISABLE_OS_PROBER=true
EOF

cat > /etc/os-release << 'EOF'
NAME="WeirdCore Linux"
PRETTY_NAME="WeirdCore Linux"
ID=wierdcore
ID_LIKE=arch
BUILD_ID=rolling
ANSI_COLOR="38;2;0;255;200"
HOME_URL="https://github.com/remix202687/WierdCore-Linux"
SUPPORT_URL="https://github.com/remix202687/WierdCore-Linux/issues"
BUG_REPORT_URL="https://github.com/remix202687/WierdCore-Linux/issues"
PRIVACY_POLICY_URL="https://github.com/remix202687/WierdCore-Linux/docs/privacy-policy/"
LOGO=wierdcorelogo
IMAGE_ID=wierdcore
IMAGE_VERSION=2026.04
EOF

grub-mkconfig -o /boot/grub/grub.cfg 

echo "WierdCore Linux" > /etc/issue
"""

    with open("/mnt/root/setup.sh", "w") as f:
        f.write(chroot_script)

    run("chmod +x /mnt/root/setup.sh")
    run("arch-chroot /mnt /root/setup.sh", "Setting system chroot")

    print("Copy configs...")
    run(f"mkdir -p /mnt/home/{username}/.config/")
    run(f'cp -r /etc/skel/.bashrc /mnt/home/{username}/ 2> /dev/null || true')
    run(f"cp -r /etc/skel/.config/* /mnt/home/{username}/.config/ 2>/dev/null || true")

    print('Install completed')
    print(f"   DISK {disk}")
    print(f"   USERNAME: {username}")
    print(f"   PASSWORD: {password}")
    is_reboot = input("Reboot system ? ").strip()

    if is_reboot.lower() == "yes" or is_reboot.lower() == "y":
        run("reboot")
    else:
        sys.exit(1)


    



if __name__ == "__main__":
    main()

