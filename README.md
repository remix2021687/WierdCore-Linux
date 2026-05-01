

## Project scope
This repository defines a custom Arch Linux live ISO profile (`weirdcore`) based on ArchISO, with custom live-root content and a Python-based interactive installer copied into the ISO root filesystem.

Primary source directories:
- `releng/`: ArchISO profile consumed by `mkarchiso`
- `releng/airootfs/`: files copied into the live environment root (`/`)

## Common commands
Run from repository root unless noted otherwise.

- Build ISO (current project script):
  - `sudo ./rebuild.sh`
  - Script behavior: deletes `releng/iso-out/` then runs `mkarchiso -v -r -w ./releng/archiso-work -o ./releng/iso-out ./releng`

- Build ISO (manual equivalent):
  - `sudo mkarchiso -v -r -w ./releng/archiso-work -o ./releng/iso-out ./releng`

- Run installer in live environment (inside booted ISO session):
  - `python /root/install.py`

- Run a single installer module manually (debugging in live environment):
  - `python /root/scripts/selectdisk/select_disk.py`

- Tests / lint:
  - No automated test suite or lint command is currently configured in this repository.
  - There is no “run a single test” command at this time.

## High-level architecture
### 1) ISO build profile layer (`releng/`)
Key files:
- `releng/profiledef.sh`: ISO identity (`iso_name`, label/version), boot modes, permissions, build behavior
- `releng/packages.x86_64`: package set baked into the live ISO
- `releng/pacman.conf`: pacman repo configuration used during build
- `releng/efiboot`, `releng/grub`, `releng/syslinux`: bootloader assets/configs

`mkarchiso` reads this profile and produces output under `releng/iso-out/` using `releng/archiso-work/` as workspace.

### 2) Live root filesystem customization (`releng/airootfs/`)
Everything under `releng/airootfs/` is copied into the live system root. Important customizations include:
- system configuration under `etc/` (hostname, locale, systemd units, pacman hooks, skel files)
- installer and helper scripts under `root/`
- local helper binaries/docs under `usr/local/bin/`

### 3) Installer execution flow (`releng/airootfs/root/`)
Main orchestration happens in `releng/airootfs/root/install.py`:
1. Select target block device via `scripts/selectdisk/select_disk.py`
2. Partition/format/mount target via `scripts/mountdisk/mountdisk.py`
3. Generate fstab + base install (`genfstab`, `pacstrap`)
4. Install additional packages via `scripts/installpackages/installpackages.py`
5. Apply system/user/bootloader config via `scripts/systemsetting/systemsetting.py`

All shell commands are funneled through `scripts/run/run.py::run(...)`, which centralizes command execution/logging.

### 4) Target system provisioning model
- `mountdisk.py` creates GPT with EFI + root partitions and sets up Btrfs subvolumes (`@`, `@home`)
- `systemsetting.py` writes `/mnt/root/setup.sh` and executes it via `arch-chroot`
- chroot script sets locale/hostname/users/sudoers, installs GRUB/network packages, enables services, and writes `/etc/os-release` and GRUB defaults
