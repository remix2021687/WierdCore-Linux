from scripts.run.run import run

def installpackages():
    print("Install packages...")
    
    packages_group = [
        ("System packages", [
            "base", "linux-zen", "linux-firmware", "intel-ucode", 
            "btrfs-progs", "systemd", "systemd-sysvcompat", "sudo"
        ]),

        ("Hyprland и окружение", [
            "hyprland", "waybar", "wofi", "dunst", "hyprlock", "hyprpaper", 
            "hyprshot", "grim", "slurp", "xdg-desktop-portal-hyprland"
        ]),

        ("Терминал и утилиты", [
            "kitty", "yazi", "fastfetch", "starship", "btop"
        ]),

        ("Звук и мультимедиа", [
            "pipewire", "pipewire-pulse", "wireplumber"
        ]),

        ("Браузер и дополнительное", [
            "firefox"
        ])
    ]


    for group, pkg in packages_group:
        print("=" * 50)
        print(f"Install group {group}")
        print("=" * 50)
        print()

        pkg_list = "".join(pkg)

        run(f"arch-chroot /mnt pacman -Sy --noconfirm {pkg_list}", f"Installed > {pkg_list}")

        print("Group is installed ")

