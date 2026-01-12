# Combines QKD + PQC keys
import hashlib

def combine_keys(qkd_key, pqc_key):
    hybrid = hashlib.sha256(qkd_key + pqc_key).digest()
    print("Hybrid key (QKD + PQC) generated successfully.")
    return hybrid
