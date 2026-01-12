# Secure data exchange using hybrid key
from classical_module.aes_encryption import encrypt_data, decrypt_data

def send_secure_message(key, message):
    ciphertext = encrypt_data(key, message)
    print("Message securely sent.")
    return ciphertext

def receive_secure_message(key, ciphertext):
    message = decrypt_data(key, ciphertext)
    print("Message securely received.")
    return message
