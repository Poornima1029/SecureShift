import socket
import threading
import time
from collections import defaultdict
from datetime import datetime
import json
import base64

HOST = "0.0.0.0"
BASE_PORT = 9000
MAX_PORTS = 10
STATS_PORT = 9009

# REAL MESSAGE STORAGE + STATS
port_messages = defaultdict(list)  # {port: [{'key': '...', 'ciphertext': '...'}]}
stats = {'total_messages': 0, 'active_ports': 0}

def get_stats():
    stats['active_ports'] = len([p for p in port_messages if port_messages[p]])
    stats['total_messages'] = sum(len(msgs) for msgs in port_messages.values())
    return stats

def handle_client(conn, addr, port):
    try:
        data = conn.recv(16384)  # Bigger buffer
        if not data: return
            
        if data.startswith(b"ALICE:"):
            # Parse: ALICE:key:ciphertext_b64:ttl:priority
            msg_data = data[6:].decode(errors='ignore')
            parts = msg_data.split(":", 4)
            
            if len(parts) >= 2:
                key_hex = parts[0]
                ciphertext_b64 = parts[1]
                
                # STORE REAL CIPHERTEXT
                port_messages[port].append({
                    'key_hex': key_hex,
                    'ciphertext_b64': ciphertext_b64,
                    'sender': f"{addr[0]}:{addr[1]}",
                    'time': datetime.now().strftime("%H:%M:%S")
                })
                
                print(f"📨 Port {port}: Stored encrypted msg #{len(port_messages[port])}")
                conn.send(b"DELIVERED")
                
        elif data.startswith(b"BOB:"):
            # Bob retrieves - SEND ALL MESSAGES FOR THIS PORT
            messages = port_messages[port]
            if messages:
                msg_list = []
                for msg in messages[-3:]:  # Last 3 messages
                    msg_list.append(f"{msg['key_hex']}|{msg['ciphertext_b64']}")
                response = f"FOUND:{len(messages)}:" + ";".join(msg_list)
                conn.send(response.encode())
                print(f"👀 Port {port}: Bob retrieved {len(messages)} msgs")
            else:
                conn.send(b"EMPTY")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

def start_port_server(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, port))
    s.listen(5)
    print(f"📡 Port {port} READY")
    
    while True:
        try:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr, port), daemon=True)
            t.start()
        except:
            break

def stats_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", STATS_PORT))
    s.listen(5)
    print(f"📊 Stats: {STATS_PORT}")
    
    while True:
        try:
            conn, _ = s.accept()
            conn.send(json.dumps(get_stats()).encode())
            conn.close()
        except:
            break

if __name__ == "__main__":
    print("🚀 SecureShift Server v8.0 - FULL MESSAGE STORAGE")
    
    # Start servers
    threads = []
    for port in range(BASE_PORT, BASE_PORT + MAX_PORTS):
        t = threading.Thread(target=start_port_server, args=(port,), daemon=True)
        t.start()
        threads.append(t)
    
    stats_t = threading.Thread(target=stats_server, daemon=True)
    stats_t.start()
    
    print("✅ ALL PORTS LIVE - Ctrl+C to stop")
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
