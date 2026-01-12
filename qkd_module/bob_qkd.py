# Bob role for QKD simulation
from QKD import generate_qkd_key

def bob_generate():
    key = generate_qkd_key()
    print("Bob key generated:", key.hex())
    return key
