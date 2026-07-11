from scripts.run.run import run

def mountdisk(disk):
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

