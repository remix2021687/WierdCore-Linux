import subprocess
import sys

def list_disks():
    try:
        result = subprocess.run(
            ["lsblk", "-d", "-o", "NAME,SIZE,TYPE,MODEL"],
            capture_output=True,
            text=True,
            check=True
        )

        print(result.stdout)

    except Exception as err:
        print(f"lsblk isn't completed: {err}")
        sys.exit(1)

def select_disk():
    print("Disk Exits: ")
    list_disks()

    while True:
        disk = input("\n Select exist disk (example: /dev/sda): ").strip()
        
        if not disk.startswith("/dev/"):
            print("Disk start /dev/")
            continue

        if subprocess.run(['test', '-b', disk], capture_output=True).returncode != 0:
            print(f"Disk {disk} not found !")
            continue

        confirm = input(f"WARNING ALL DATA ON DISK GONNA BE DELETED Type Yes(y) or No (n) ! ")

        if confirm.lower() == "yes" or confirm.lower() == 'y':
            print(f'Disk is {disk}')

            return disk

        else:
            print("Install is canceled !")
            sys.exit(0)
            

if __name__ == "__main__":
    select_disk()
