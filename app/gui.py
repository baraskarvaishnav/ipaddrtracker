import tkinter as tk
from tkinter import messagebox, scrolledtext, Frame, StringVar
from app.ip_tracker import track_ip
from app.utils import log_ip_history
import re
import threading
import time

class IPTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Tracker")
        self.root.geometry("600x750")
        self.root.configure(bg="#2c3e50")  # Dark background for contrast

        # Title Label
        self.title_label = tk.Label(self.root, text="IP Address Tracker", font=("Helvetica", 24, "bold"), bg="#2c3e50", fg="#ecf0f1")
        self.title_label.pack(pady=20)

        self.history = []
        self.create_widgets()

    def create_widgets(self):
        # Main Frame with Rounded Corners
        main_frame = Frame(self.root, bg="#34495e", bd=10, relief=tk.GROOVE)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Frame for Input Section
        input_frame = Frame(main_frame, bg="#34495e")
        input_frame.pack(pady=(10, 20))  # Vertical padding

        tk.Label(input_frame, text="Enter IP Address:", font=("Helvetica", 12), bg="#34495e", fg="#ecf0f1").grid(row=0, column=0, padx=5, sticky='e')
        self.ip_entry = tk.Entry(input_frame, font=("Helvetica", 12), width=25, bd=2, relief=tk.SUNKEN)
        self.ip_entry.grid(row=0, column=1, padx=(0, 10))  # Right padding for better margin

        # Buttons with Increased Padding and Styles
        button_frame = Frame(main_frame, bg="#34495e")
        button_frame.pack(pady=(10, 20))

        self.track_button = tk.Button(button_frame, text="Track IP", command=self.start_tracking, font=("Helvetica", 12), bg="#27ae60", fg="white", relief=tk.RAISED, padx=10, pady=5)
        self.track_button.grid(row=0, column=0, padx=10)

        self.clear_button = tk.Button(button_frame, text="Clear Results", command=self.clear_results, font=("Helvetica", 12), bg="#c0392b", fg="white", relief=tk.RAISED, padx=10, pady=5)
        self.clear_button.grid(row=0, column=1, padx=10)

        self.export_button = tk.Button(button_frame, text="Export History", command=self.export_history, font=("Helvetica", 12), bg="#2980b9", fg="white", relief=tk.RAISED, padx=10, pady=5)
        self.export_button.grid(row=0, column=2, padx=10)

        # Result Display with Padding and Creative Layout
        result_frame = Frame(main_frame, bg="#ecf0f1", bd=2, relief=tk.GROOVE)
        result_frame.pack(pady=(10, 20), fill=tk.BOTH, expand=True)

        result_label = tk.Label(result_frame, text="Results:", font=("Helvetica", 16, "bold"), bg="#ecf0f1", fg="#2c3e50")
        result_label.pack(pady=10)

        self.result_text = scrolledtext.ScrolledText(result_frame, height=10, width=70, font=("Helvetica", 12), bg="#ffffff", wrap=tk.WORD, bd=2, relief=tk.GROOVE)
        self.result_text.pack(pady=(0, 10), padx=10, fill=tk.BOTH, expand=True)

        # History Display with Padding and Creative Layout
        history_frame = Frame(main_frame, bg="#ecf0f1", bd=2, relief=tk.GROOVE)
        history_frame.pack(pady=(10, 20), fill=tk.BOTH, expand=True)

        history_label = tk.Label(history_frame, text="Search History:", font=("Helvetica", 16, "bold"), bg="#ecf0f1", fg="#2c3e50")
        history_label.pack(pady=10)

        self.history_text = scrolledtext.ScrolledText(history_frame, height=8, width=70, font=("Helvetica", 12), bg="#ffffff", wrap=tk.WORD, bd=2, relief=tk.GROOVE)
        self.history_text.pack(pady=(0, 10), padx=10, fill=tk.BOTH, expand=True)
        self.history_text.insert(tk.END, "Search History:\n")

        # Status Bar with Better Margin
        self.status_var = StringVar()
        self.status_var.set("Ready")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bg="#2c3e50", anchor='w', fg="#ecf0f1", font=("Helvetica", 10))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=(5, 20))

    def start_tracking(self):
        ip_address = self.ip_entry.get().strip()
        if not ip_address:
            messagebox.showerror("Error", "Please enter an IP address.")
            return
        
        if not self.validate_ip(ip_address):
            messagebox.showerror("Error", "Please enter a valid IP address.")
            return
        
        self.result_text.delete(1.0, tk.END)
        self.status_var.set("Tracking IP...")
        threading.Thread(target=self.track_ip_with_loading, args=(ip_address,)).start()

    def track_ip_with_loading(self, ip_address):
        time.sleep(1)  # Simulate loading
        try:
            result = track_ip(ip_address)
            if result:
                self.display_results(result)
                log_ip_history(ip_address, result)
                self.update_history(ip_address)
            else:
                messagebox.showwarning("Warning", "No data found for this IP address.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while tracking the IP: {str(e)}")
        finally:
            self.status_var.set("Ready")

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

    def clear_results(self):
        self.result_text.delete(1.0, tk.END)
        self.ip_entry.delete(0, tk.END)

    def validate_ip(self, ip):
        # Regular expression to validate both IPv4 and IPv6 addresses
        ipv4_pattern = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
        ipv6_pattern = r'^[0-9a-fA-F:]{7,39}$'  # Simple regex for IPv6
        return re.match(ipv4_pattern, ip) is not None or re.match(ipv6_pattern, ip) is not None

    def update_history(self, ip_address):
        self.history.append(ip_address)
        self.history_text.insert(tk.END, f"{ip_address}\n")
        self.history_text.yview(tk.END)

    def export_history(self):
        with open("ip_history.txt", "w") as file:
            for ip in self.history:
                file.write(f"{ip}\n")
        messagebox.showinfo("Export History", "History exported to ip_history.txt")

if __name__ == "__main__":
    root = tk.Tk()
    app = IPTrackerApp(root)
    root.mainloop()
