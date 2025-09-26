import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json, os

FILE_NAME = "contacts.json"

def load_contacts():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return {}

def save_contacts():
    with open(FILE_NAME, "w") as f:
        json.dump(contacts, f, indent=4)

def refresh_tree():
    for row in contact_tree.get_children():
        contact_tree.delete(row)
    for name, details in contacts.items():
        contact_tree.insert("", "end", iid=name, values=(details["phone"], details["email"], details["address"]))

def add_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()
    address = address_entry.get().strip()

    if name and phone:
        contacts[name] = {"phone": phone, "email": email, "address": address}
        save_contacts()
        refresh_tree()
        clear_entries()
        messagebox.showinfo("Success", f"Contact '{name}' added.")
    else:
        messagebox.showwarning("Error", "Name and Phone are required.")

def delete_contact():
    selected = contact_tree.selection()
    if not selected:
        messagebox.showwarning("Error", "Select a contact to delete.")
        return
    name = selected[0]
    confirm = messagebox.askyesno("Confirm Delete", f"Delete contact '{name}'?")
    if confirm:
        del contacts[name]
        save_contacts()
        refresh_tree()
        messagebox.showinfo("Deleted", f"Contact '{name}' deleted.")

def search_contact():
    query = simpledialog.askstring("Search", "Enter name or phone:")
    if not query:
        return
    results = [name for name, details in contacts.items()
               if query.lower() in name.lower() or query in details['phone']]
    if results:
        contact_tree.selection_set(results[0])
        contact_tree.see(results[0])
    else:
        messagebox.showinfo("No Results", "No matching contacts found.")

def update_contact():
    selected = contact_tree.selection()
    if not selected:
        messagebox.showwarning("Error", "Select a contact to update.")
        return
    name = selected[0]
    details = contacts[name]
    new_phone = simpledialog.askstring("Update Phone", f"Current: {details['phone']}")
    new_email = simpledialog.askstring("Update Email", f"Current: {details['email']}")
    new_address = simpledialog.askstring("Update Address", f"Current: {details['address']}")
    if new_phone: details['phone'] = new_phone
    if new_email: details['email'] = new_email
    if new_address: details['address'] = new_address
    contacts[name] = details
    save_contacts()
    refresh_tree()
    messagebox.showinfo("Updated", f"Contact '{name}' updated.")

def clear_entries():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

root = tk.Tk()
root.title("📒 Contact Book")
root.geometry("700x500")
root.config(bg="#f8f9fa")

contacts = load_contacts()

style = ttk.Style(root)
style.theme_use("clam")
style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"), background="#495057", foreground="white")
style.configure("Treeview", font=("Helvetica", 10), rowheight=28, background="white", fieldbackground="white")
style.map("Treeview", background=[("selected", "#007bff")], foreground=[("selected", "white")])

top_frame = tk.Frame(root, bg="#f8f9fa")
top_frame.pack(pady=10)

form_frame = tk.LabelFrame(top_frame, text="➕ Add New Contact", padx=10, pady=10, bg="#f8f9fa")
form_frame.pack(side=tk.LEFT, padx=10)

list_frame = tk.Frame(root, bg="#f8f9fa")
list_frame.pack(pady=10)

button_frame = tk.Frame(root, bg="#f8f9fa")
button_frame.pack(pady=10)

tk.Label(form_frame, text="Name:", bg="#f8f9fa").grid(row=0, column=0, sticky="w")
name_entry = tk.Entry(form_frame, width=25)
name_entry.grid(row=0, column=1, pady=5)

tk.Label(form_frame, text="Phone:", bg="#f8f9fa").grid(row=1, column=0, sticky="w")
phone_entry = tk.Entry(form_frame, width=25)
phone_entry.grid(row=1, column=1, pady=5)

tk.Label(form_frame, text="Email:", bg="#f8f9fa").grid(row=2, column=0, sticky="w")
email_entry = tk.Entry(form_frame, width=25)
email_entry.grid(row=2, column=1, pady=5)

tk.Label(form_frame, text="Address:", bg="#f8f9fa").grid(row=3, column=0, sticky="w")
address_entry = tk.Entry(form_frame, width=25)
address_entry.grid(row=3, column=1, pady=5)

ttk.Button(form_frame, text="Add Contact", command=add_contact).grid(row=4, columnspan=2, pady=8)

columns = ("Phone", "Email", "Address")
contact_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)

contact_tree.heading("Phone", text="📞 Phone")
contact_tree.heading("Email", text="📧 Email")
contact_tree.heading("Address", text="🏠 Address")

contact_tree.column("Phone", width=120)
contact_tree.column("Email", width=180)
contact_tree.column("Address", width=220)

scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=contact_tree.yview)
contact_tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
contact_tree.pack()

refresh_tree()

ttk.Button(button_frame, text="🔍 Search", width=15, command=search_contact).grid(row=0, column=0, padx=5)
ttk.Button(button_frame, text="✏ Update", width=15, command=update_contact).grid(row=0, column=1, padx=5)
ttk.Button(button_frame, text="❌ Delete", width=15, command=delete_contact).grid(row=0, column=2, padx=5)

root.mainloop()
