import subprocess
import sys

def run(cmd, description="", live=True):    
    if description:
        print(f"\n[📌 {description} ]")
    print(f"→ {cmd}")

    if live:
        result = subprocess.run(cmd, shell=True, text=True)
    else:
        result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
        if result.stdout:
            print(result.stdout.strip())
        if result.stderr:
            print(f"⚠️  {result.stderr.strip()}")
    
        if result.returncode != 0:
            print(f"Command Error")
            sys.exit(1)

