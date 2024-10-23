import tkinter as tk
from tkinter import messagebox
from app.ip_tracker import track_ip
from app.utils import log_ip_history

class IPTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Tracker")
        self.root.geometry("400x300")
        
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Enter IP Address:", font=("Helvetica", 12)).pack(pady=10)

        self.ip_entry = tk.Entry(self.root, font=("Helvetica", 12), width=25)
        self.ip_entry.pack(pady=5)

        self.track_button = tk.Button(self.root, text="Track IP", command=self.track_ip, font=("Helvetica", 12))
        self.track_button.pack(pady=20)

        self.result_text = tk.Text(self.root, height=8, width=50, font=("Helvetica", 10))
        self.result_text.pack(pady=5)

    def track_ip(self):
        ip_address = self.ip_entry.get()
        if not ip_address:
            messagebox.showerror("Error", "Please enter an IP address.")
            return
        
        result = track_ip(ip_address)
        if result:
            self.display_results(result)
            log_ip_history(ip_address, result)

    def display_results(self, data):
        self.result_text.delete(1.0, tk.END)
        result = (
            f"IP: {data['query']}\n"
            f"Country: {data['country']}\n"
            f"Region: {data['regionName']}\n"
            f"City: {data['city']}\n"
            f"ZIP: {data['zip']}\n"
            f"Latitude: {data['lat']}\n"
            f"Longitude: {data['lon']}\n"
            f"ISP: {data['isp']}\n"
        )
        self.result_text.insert(tk.END, result)

if __name__ == "__main__":
    root = tk.Tk()
    app = IPTrackerApp(root)
    root.mainloop()

