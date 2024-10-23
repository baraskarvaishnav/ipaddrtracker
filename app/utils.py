import csv
from datetime import datetime

def log_ip_history(ip_address, data):
    log_entry = {
        'IP': data['query'],
        'Country': data['country'],
        'Region': data['regionName'],
        'City': data['city'],
        'ZIP': data['zip'],
        'Latitude': data['lat'],
        'Longitude': data['lon'],
        'ISP': data['isp'],
        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Write to CSV
    with open('data/ip_history.csv', mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=log_entry.keys())
        if file.tell() == 0:  # Check if the file is empty to write the header
            writer.writeheader()
        writer.writerow(log_entry)

