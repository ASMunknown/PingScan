import subprocess
import threading

BASE = "192.168"
OUTPUT_FILE = "ping.txt"
MAX_THREADS = 100
lock = threading.Lock()

def ping_ip(ip):
    try:
        output = subprocess.check_output("ping -n 1 -w 500 " + ip, shell=True).decode("utf-8", errors="ignore")
        
        # CAMBIAR LA SIGUIENTE LÍNEA CON EL MENSAJE CORRECTO DE TU SISTEMA
        success_msg = "Respuesta desde"  # Por ejemplo: "Reply from"
        
        if success_msg in output:
            with lock:
                with open(OUTPUT_FILE, 'a') as f:
                    f.write(ip + '\n')
                print(f"{ip} respondió")
    except subprocess.CalledProcessError:
        pass

def main():
    with open(OUTPUT_FILE, 'w') as f:
        f.write('')
    threads = []

    for i in range(256):
        for j in range(256):
            ip = f"{BASE}.{i}.{j}"
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
