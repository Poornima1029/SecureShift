# QKD.py – BB84 Quantum Key Distribution Protocol (Simulation)

import numpy as np
import random
import hashlib

def prepare_bits(num_bits=128):
    bits = np.random.randint(0, 2, num_bits)
    bases = np.random.randint(0, 2, num_bits)
    return bits, bases

def measure_bits(bits, send_bases, recv_bases):
    results = []
    for b, sb, rb in zip(bits, send_bases, recv_bases):
        results.append(b if sb == rb else random.randint(0, 1))
    return np.array(results)

def sift_keys(alice_bases, bob_bases, alice_bits, bob_bits):
    indices = np.where(alice_bases == bob_bases)
    sifted_a = alice_bits[indices]
    sifted_b = bob_bits[indices]
    return sifted_a, sifted_b

def detect_eavesdrop(sifted_a, sifted_b):
    test_len = len(sifted_a) // 4
    sample_a = sifted_a[:test_len]
    sample_b = sifted_b[:test_len]
    error_rate = np.mean(sample_a != sample_b) * 100
    return error_rate

def generate_qkd_key(num_bits=128):
    a_bits, a_bases = prepare_bits(num_bits)
    b_bases = np.random.randint(0, 2, num_bits)
    b_bits = measure_bits(a_bits, a_bases, b_bases)

    sifted_a, sifted_b = sift_keys(a_bases, b_bases, a_bits, b_bits)
    error = detect_eavesdrop(sifted_a, sifted_b)

    key = hashlib.sha256(sifted_a.tobytes()).digest()
    print(f"QKD completed. Eavesdrop error: {error:.2f}%")
    return key
