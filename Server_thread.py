import socketserver
import threading
import time
import datetime

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Timestamp koneksi diterima
        waktu_mulai = datetime.datetime.now()

        # Info basic
        client_address = self.client_address
        thread_name = threading.current_thread().name

        # Log: client terhubung
        print(f"\n[{waktu_mulai.strftime('%H:%M:%S.%f')}] Klien {client_address} terhubung.")
        print(f"[Thread: {thread_name}] Mulai menangani klien.")

        try:
            # Terima pesan dari client
            data = self.request.recv(1024)
            pesan = data.decode()

            print(f"[Thread: {thread_name}] Menerima pesan: '{pesan}'")

            # Simulasi proses
            time.sleep(2)

            # Kirim balasan
            respon = f"[{thread_name}] Pesan diterima: {pesan}".encode()
            self.request.sendall(respon)

        except Exception as e:
            print(f"[ERROR] {thread_name}: {e}")

        finally:
            # Log selesai
            waktu_selesai = datetime.datetime.now()
            durasi = waktu_selesai - waktu_mulai
            print(
                f"[{waktu_selesai.strftime('%H:%M:%S.%f')}] Klien {client_address} "
                f"SELESAI dilayani (Durasi: {durasi.total_seconds():.2f}s)."
            )


# Multi-thread TCP Server
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    pass


if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 9999

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    print(f"Server berjalan pada {HOST}:{PORT}")
    print(f"Server loop berjalan di thread: [{server_thread.name}]")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nServer dihentikan.")
        server.shutdown()
        server.server_close()
