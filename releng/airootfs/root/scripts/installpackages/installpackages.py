from scripts.run.run import run

def installpackages():
    print("Install packages...")
    
    packages = [
        "base", "linux-zen", "linux-firmware", "intel-ucode", "btrfs-progs",
        "systemd", "systemd-sysvcompat", "grub", "efibootmgr", "sudo",
        "hyprland", "waybar", "wofi", "dunst", "hyprlock", "hyprpaper", "hyprshot",
        "grim", "slurp", "kitty", "firefox", "yazi", "fastfetch", "iwd", "dhcpcd", "starship", "python-pip" "btop",
        "pipewire", "pipewire-pulse", "wireplumber", "xdg-desktop-portal-hyprland"
    ]


    total = len(packages)
    for i, pkg in enumerate(packages, 1):
        procent = int((i / total) * 100)
        print(f"\n\033[1;36m[{i:2d}/{total}] [{procent:3d}%] Installed: {pkg}\033[0m")

        run(f"arch-chroot /mnt pacman -Sy --noconfirm {pkg}", f"Installed > {pkg}")

