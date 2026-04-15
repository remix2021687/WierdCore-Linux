import subprocess
import sys

from scripts.selectdisk.select_disk import select_disk

def run(cmd, description=""):    
    if description:
        print(f"\n[📌 {description}]")
    print(f"→ {cmd}")
    
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(f"⚠️  {result.stderr.strip()}")
    
    if result.returncode != 0:
        print(f"Command Error")
        sys.exit(1)
    
    print("✓ Completed")
    return result.stdout.strip()

def main():
    subprocess.run(['clear'], shell=True)
    print("-" * 50)
    print()
    print("Wierd Core Insall Script")
    print()
    print("-" * 50)
    print()

    disk = select_disk()

    run("mount -o remount,size=4G /run/archiso/cowspace")

    run(f"sgdisk -Z {disk}", "Formatation disk")
    run(f"sgdisk -n=1:0:+512M -t=1:EF00 {disk}", "Create EFI partition")
    run(f"sgdisk -n=2:0:0 -t=2:8300 {disk}", "Create root pratition")

    efi_part = f"{disk}p1" if "nvme" in disk else f"{disk}1"
    root_part = f"{disk}p2" if "nvme" in disk else f"{disk}2"

    run(f"umount -f {efi_part} 2>/dev/null || true", "Over umount EFI")
    run(f"umount -f {root_part} 2>/dev/null || true", "Over umount root")

    print("Formating disk...")
    run(f"mkfs.fat -F32 {efi_part}")
    run(f"mkfs.btrfs -f -L root {root_part}")

    print("Create btrfs partition...")
    run(f"mount {root_part} /mnt")
    run(f"btrfs subvolume create /mnt/@")
    run(f"btrfs subvolume create /mnt/@home")
    run(f"umount /mnt")

    run(f"mount -o noatime,compress=zstd,subvol=@ {root_part} /mnt")

    run("mkdir -p /mnt/home /mnt/boot /mnt/etc")

    run(f"mount {efi_part} /mnt/boot")
    run(f"mount -o noatime,compress=zstd,subvol=@ {root_part} /mnt/home")

    print("Mount completed")
    
    run("mkdir -p /mnt/etc /mnt/proc /mnt/sys /mnt/dev /mnt/run /mnt/run/lock /mnt/boot", "Create base dir")
    
    run("mount --types proc /proc /mnt/proc", "Mount /proc")
    run("mount --rbind /sys /mnt/sys", "Mount/sys")
    run("mount --make-rslave /mnt/sys", "setup /sys")
    run("mount --rbind /dev /mnt/dev", "mount /dev")
    run("mount --make-rslave /mnt/dev", "setup /dev")
    run("mount --types tmpfs tmpfs /mnt/run", "Mount /run")
    run("mkdir -p /mnt/run/lock", "Create /run/lock")

    run("genfstab -U /mnt >> /mnt/etc/fstab")

    run("pacstrap -K /mnt base linux-zen linux-firmware intel-ucode btrfs-progs systemd systemd-sysvcompat")
    
    print("Install packages...")
    
    packages = [
        "base", "linux-zen", "linux-firmware", "intel-ucode", "btrfs-progs",
        "systemd", "systemd-sysvcompat",
        "hyprland", "waybar", "wofi", "dunst", "hyprlock", "hyprpaper", "hyprshot",
        "grim", "slurp", "kitty", "firefox", "yazi", "fastfetch", "starship", "btop",
        "pipewire", "pipewire-pulse", "wireplumber", "xdg-desktop-portal-hyprland"
    ]


    total = len(packages)
    for i, pkg in enumerate(packages, 1):
        procent = int((i / total) * 100)
        print(f"\n\033[1;36m[{i:2d}/{total}] [{procent:3d}%] Installed: {pkg}\033[0m")

        run(f"arch-chroot /mnt pacman -Sy --noconfirm {pkg}", f"Installed > {pkg}")



    print("Setting system... (fstab, bootloader, users)")

    chroot_script = f"""
    #!/bin/bash

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
    groupadd -f weird

    mkdir -p /etc/sudoers.d/

    useradd -m -G wheel,audio,video,storage weird
    echo "weird:weird" | chpasswd
    echo "%wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/weird
    chmod 440 /etc/sudoers.d/weird

    bootctl --path=/boot install

    cat > /boot/loader/loader.conf << EOC
    defualt weirdcore
    timout 3
    EOC

    cat > /boot/loader/entries/wierdcore.conf << EOC
    title   WierdCore Linux
    linux   /vmlinuz-linux-zen
    initrd  /intel-ucode.img
    initrd  /initramfs-linux-zen.img
    options root=UUID=$(blkid -s UUID -o value {root_part}) rootflags=subvol=@ rw
    EOC

    mkinitcpio -P

    """

    with open("/mnt/root/setup.sh", "w") as f:
        f.write(chroot_script)

    run("chmod +x /mnt/root/setup.sh")
    run("arch-chroot /mnt /root/setup.sh")

    print("Copy configs...")
    run(f"mkdir -p /mnt/home/weird/.config/")
    run(f"cp -r /etc/skel/.config/* /mnt/home/weird/.config/ 2>/dev/null || true")
    run(f"chown -R weird:weird /mnt/home/weird/.config")

    print('Install completed')
    print(f"   DISK {disk}")
    print(f"   USERNAME: weird")
    print(f"   PASSWORD: weird")
    is_reboot = input("Reboot system ? ")

    if is_reboot.lower() == "yes" or is_reboot.lower() == "y":
        run("reboot")
    else:
        sys.exit(1)


    



if __name__ == "__main__":
    main()

