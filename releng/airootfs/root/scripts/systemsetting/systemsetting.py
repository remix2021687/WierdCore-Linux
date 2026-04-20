from scripts.run.run import run

def systemsetting(username, password):
    print("Setting system... (fstab, bootloader, users)")
    
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

# cp /root/logo/weirdcore.png /usr/share/pixmaps/
# chmod 664 /usr/share/pixmaps/weirdcore.png

useradd -m --group wheel,audio,video,storage {username}
echo "{username}:{password}" | chpasswd
echo "{username} ALL=(ALL) ALL" >> /etc/sudoers.d/00_{username}
chmod 440 /etc/sudoers.d/00_{username}

pacman -S --noconfirm grub efibootmgr iwd dhcpcd
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB --recheck 

systemctl enable iwd
systemctl enable  dhcpcd

cat > /etc/default/grub << 'EOF'
GRUB_DEFAULT=0
GRUB_TIMEOUT=3
GRUB_DISTRIBUTOR="WierdCore"
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
NAME="WeirdCore"
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

echo "WeirdCore Linux" > /etc/issue
"""

    with open("/mnt/root/setup.sh", "w") as f:
        f.write(chroot_script)

    run("chmod +x /mnt/root/setup.sh")
    run("arch-chroot /mnt /root/setup.sh", "Setting system chroot") 


