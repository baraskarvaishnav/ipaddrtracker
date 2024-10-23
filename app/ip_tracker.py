import requests
from app.settings import API_URL

def track_ip(ip_address):
    try:
        response = requests.get(f"{API_URL}/{ip_address}")
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'fail':
                return None
            return data
    except Exception as e:
        print(f"Error tracking IP: {e}")
        return None

