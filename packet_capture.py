from scapy.all import sniff
import pandas as pd

def packet_callback(packet):
    if packet.haslayer('IP'):
        new_entry = {
            'ip_address': packet['IP'].src,
            'bytes_sent': len(packet),
            'bytes_received': 0,
            'connections': 1
        }
        df = pd.DataFrame([new_entry])
        df.to_csv('data/network_logs.csv', mode='a', header=False, index=False)

def start_capture():
    sniff(prn=packet_callback, store=0)
