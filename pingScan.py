import subprocess
import threading
import platform
import argparse

BASE = "192.168"
OUTPUT_FILE = "ping.txt"
MAX_THREADS = 100
lock = threading.Lock()

def ping_ip(ip):
    try:
        if platform.system() == "Windows":
            cmd = ["ping", "-n", "1", "-w", "500", ip]
        else:
            cmd = ["ping", "-c", "1", "-W", "1", ip]

        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if result.returncode == 0:
            with lock:
                with open(OUTPUT_FILE, 'a') as f:
                    f.write(ip + '\n')
                print(f"{ip} respondió")
    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser(description="Scan network for responsive IPs")
    parser.add_argument('-b', '--base', default=BASE, help='Base network prefix, e.g. 192.168')
    args = parser.parse_args()

    base = args.base

    with open(OUTPUT_FILE, 'w') as f:
        f.write('')
    threads = []

    for i in range(256):
        for j in range(256):
            ip = f"{base}.{i}.{j}"
            t = threading.Thread(target=ping_ip, args=(ip,))
            t.start()
            threads.append(t)

            if len(threads) == MAX_THREADS:
                for t in threads:
                    t.join()
                threads = []

    for t in threads:
        t.join()

    print(f"Script finalizado. Las IPs que respondieron se han guardado en {OUTPUT_FILE}.")

if __name__ == "__main__":
    main()
