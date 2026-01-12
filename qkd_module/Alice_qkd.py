# Alice role for QKD simulation
from QKD import generate_qkd_key

def alice_generate():
    key = generate_qkd_key()
    print("Alice key generated:", key.hex())
    return key
