import customtkinter as ctk
from tkinter import ttk, messagebox
from pymongo import MongoClient
from bson.objectid import ObjectId

# ------------------ MongoDB Connection ------------------
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["car_db"]
    collection = db["cars"]
except Exception as e:
    print("Error connecting to MongoDB:", e)
    exit()

# ------------------ CRUD Functions ------------------
def insert_data():
    brand = entry_brand.get().strip()
    model = entry_model.get().strip()
    year = entry_year.get().strip()

    if brand and model and year.isdigit():
        try:
            collection.insert_one({"brand": brand, "model": model, "year": int(year)})
            messagebox.showinfo("Success", "Car record inserted successfully!")
            clear_fields()
            fetch_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Input Error", "Please enter valid Brand, Model, and Year (number).")

def fetch_data():
    for row in tree.get_children():
        tree.delete(row)
    for doc in collection.find().sort("_id", 1):  # Show oldest first
        tree.insert("", "end", iid=str(doc["_id"]), values=(doc["brand"], doc["model"], doc["year"]))

def update_data():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a record to update.")
        return

    record_id = ObjectId(selected[0])
    brand = entry_brand.get().strip()
    model = entry_model.get().strip()
    year = entry_year.get().strip()

    if brand and model and year.isdigit():
        try:
            collection.update_one({"_id": record_id}, {"$set": {"brand": brand, "model": model, "year": int(year)}})
            messagebox.showinfo("Success", "Car record updated successfully!")
            clear_fields()
            fetch_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Input Error", "Please enter valid Brand, Model, and Year (number).")

def delete_data():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a record to delete.")
        return

    record_id = ObjectId(selected[0])
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
    if confirm:
        try:
            collection.delete_one({"_id": record_id})
            messagebox.showinfo("Success", "Car record deleted successfully!")
            fetch_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))

def clear_fields():
    entry_brand.delete(0, "end")
    entry_model.delete(0, "end")
    entry_year.delete(0, "end")

def select_record(event):
    selected = tree.selection()
    if selected:
        record = collection.find_one({"_id": ObjectId(selected[0])})
        if record:
            clear_fields()
            entry_brand.insert(0, record["brand"])
            entry_model.insert(0, record["model"])
            entry_year.insert(0, str(record["year"]))

# ------------------ CustomTkinter Setup ------------------
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("🚗 Car Management System")
root.geometry("800x550")

# Title
title_label = ctk.CTkLabel(root, text="🚗 Car Management System", font=ctk.CTkFont(size=22, weight="bold"))
title_label.pack(pady=15)

# Form Frame
form_frame = ctk.CTkFrame(root)
form_frame.pack(pady=10, padx=20, fill="x")

entry_brand = ctk.CTkEntry(form_frame, placeholder_text="Enter Brand", width=200)
entry_brand.grid(row=0, column=0, padx=10, pady=10)

entry_model = ctk.CTkEntry(form_frame, placeholder_text="Enter Model", width=200)
entry_model.grid(row=0, column=1, padx=10, pady=10)

entry_year = ctk.CTkEntry(form_frame, placeholder_text="Enter Year", width=100)
entry_year.grid(row=0, column=2, padx=10, pady=10)

# Buttons
btn_frame = ctk.CTkFrame(root)
btn_frame.pack(pady=5)

ctk.CTkButton(btn_frame, text="Add", command=insert_data, fg_color="green").grid(row=0, column=0, padx=10, pady=5)
ctk.CTkButton(btn_frame, text="Update", command=update_data, fg_color="blue").grid(row=0, column=1, padx=10, pady=5)
ctk.CTkButton(btn_frame, text="Delete", command=delete_data, fg_color="red").grid(row=0, column=2, padx=10, pady=5)
ctk.CTkButton(btn_frame, text="Read", command=fetch_data, fg_color="orange").grid(row=0, column=3, padx=10, pady=5)
ctk.CTkButton(btn_frame, text="Clear", command=clear_fields, fg_color="gray").grid(row=0, column=4, padx=10, pady=5)

# Table
tree_frame = ctk.CTkFrame(root)
tree_frame.pack(pady=10, padx=20, fill="both", expand=True)

columns = ("Brand", "Model", "Year")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=200)
tree.pack(fill="both", expand=True)

tree.bind("<<TreeviewSelect>>", select_record)

# Fetch initial data
fetch_data()

root.mainloop()
