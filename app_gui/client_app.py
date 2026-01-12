# app_gui/client_app.py
import socket
from classical_module.aes_encryption import encrypt_data, SHARED_SECRET_KEY

SERVER_IP = "127.0.0.1"  # change to server LAN IP for cross-device
PORT = 9090

def start_client():
    print("Initializing SecureShift (Client)...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, PORT))
        print("Connected to SecureShift Server.")

        # Use fixed shared key (same as server)
        hybrid_key = SHARED_SECRET_KEY

        message = input("Enter message to send securely: ")
        ciphertext = encrypt_data(hybrid_key, message)
        s.sendall(ciphertext)
        print("Encrypted message sent successfully.")

if __name__ == "__main__":
    start_client()
