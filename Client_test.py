import socket
import threading
import time

def client_task(client_id, message):
    try:
        #Menggunakan 'with' untuk memastikan socket ditutup secara otomatis
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(("localhost", 9999)) #terhubung ke server

            sock.sendall(message.encode()) # Kirim pesan

            #Menerima balasan dari server
            response = sock.recv(1024)

            print(f"Client {client_id} menerima balasan: {response.decode()}")
    except ConnectionRefusedError:
        print(f"Client {client_id}: Gagal Terhubung (Server belum menyala).")
    except Exception as e:
        print(f"Client {client_id}: Terjadi Kesalahan: {e}")

if __name__ == "__main__":
    threads = [] 

    #Membuat 5 client yg berjalan serentak
    for i in range (5):
        msg = f"Halo dari client {i+1}"
        t = threading.Thread(target=client_task, args=(i+1, msg))
        threads.append(t)
        t.start() #Menjalankan Thread Klien

    #Menunggu semua client selesai
    for t in threads:
        t.join()

    print("\nSemua Client Selesai.")