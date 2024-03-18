import requests
import json
import tkinter as tk
from tkinter import messagebox
import time

class UrlCheckApp:



    def __init__(self, root):
        self.root = root
        self.root.title("URL Check Tool")

        self.url_label = tk.Label(root, text="Enter URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack()

        self.submit_button = tk.Button(root, text="Submit", command=self.check_url)
        self.submit_button.pack()

        self.result_text = tk.Text(root, height=10, width=60)
        self.result_text.pack()

        self.root.bind("<Return>", lambda event: self.check_url())
    def check_url(self):
        url_choice = self.url_entry.get()
        if not url_choice:
            messagebox.showwarning("Warning", "Please enter a URL.")
            return

        url = "https://www.virustotal.com/api/v3/urls"
        payload = {"url": url_choice}
        headers = {
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded",
            "X-Apikey": "b21ef2cf6ade30bdd9f871228b7b411f70dafe3103c136ad1c4025b715a0efc7",
            }

        response = requests.post(url, data=payload, headers=headers)

        data = json.loads(response.text)
        info = data["data"]
        url_id = info["id"]

        url = f"https://www.virustotal.com/api/v3/analyses/{url_id}"
        headers = {
            "accept": "application/json",
            "x-apikey": "b21ef2cf6ade30bdd9f871228b7b411f70dafe3103c136ad1c4025b715a0efc7",
        }

        self.check_status(url, headers)

    def check_status(self, url, headers):
        response = requests.get(url, headers=headers)
        stats = json.loads(response.text)
        data = stats["data"]
        attributes = data["attributes"]
        status = attributes["status"]
        stats = attributes["stats"]

        if status == "queued":
            result_message = f"\nStatus of the scan: {status}\nPlease standby"
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, result_message)

            # Schedule the next check after 5000 milliseconds (5 seconds)
            self.root.after(5000, lambda: self.check_status(url, headers))
        else:
            result_message = f"\nStatus of the scan: {status}\nScans were completed with 90 tools, here are the totals for the results:\n"

            for value in stats:
                result_message += f"{value}: {stats[value]}\n"

            self.result_text.delete("1.0", tk.END)  # Clear previous results
            self.result_text.insert(tk.END, result_message)

if __name__ == "__main__":
    root = tk.Tk()
    app = UrlCheckApp(root)
    root.mainloop()