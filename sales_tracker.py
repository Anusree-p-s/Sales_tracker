import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
class SalesTracker:
    def __init__(self, master):
        self.master = master
        self.master.title("Monthly Sales Tracker")
        self.master.geometry("400x550")
        self.products = [
            "Smart Devices", "Home & Kitchen", "Personal Care",
            "Fitness", "Fashion", "Grocery"
        ]
        self.entries = {}
        tk.Label(master, text="Enter Monthly Sales", font=("Arial", 14, "bold")).pack(pady=10)
        for product in self.products:
            tk.Label(master, text=product).pack()
            entry = tk.Entry(master)
            entry.pack()
            self.entries[product] = entry
        tk.Button(master, text="Submit", command=self.save_sales).pack(pady=10)
        tk.Button(master, text="View Chart", command=self.show_chart).pack()
    def save_sales(self):
        month = datetime.now().strftime("%B")
        sales = {"Month": month}
        for product, entry in self.entries.items():
            try:
                sales[product] = int(entry.get())
            except ValueError:
                messagebox.showerror("Invalid Input", f"Enter a number for '{product}'")
                return
        filename = "sales_data.csv"
        new_file = not os.path.exists(filename) or os.stat(filename).st_size == 0
        with open(filename, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["Month"] + self.products)
            if new_file:
                writer.writeheader()
            writer.writerow(sales)
        messagebox.showinfo("Success", "Sales saved successfully!")
        for entry in self.entries.values():
            entry.delete(0, tk.END)
    def show_chart(self):
        month = datetime.now().strftime("%B")
        try:
            df = pd.read_csv("sales_data.csv")
        except:
            messagebox.showerror("Sales data not found.")
            return
        if "Month" not in df.columns or month not in df["Month"].values:
            messagebox.showinfo("Info", f"No data found for {month}.")
            return
        latest = df[df["Month"] == month].iloc[-1]
        sales = latest[self.products]
        plt.figure(figsize=(8, 5))
        sales.plot(kind="bar")
        plt.title(f"Sales Report - {month}")
        plt.ylabel("Units Sold")
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.show()
if __name__ == "__main__":
    root = tk.Tk()
    app = SalesTracker(root)
    root.mainloop()
