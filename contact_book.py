"""
Contact Book App (Python + tkinter)
Run with: python contact_book.py
Contacts are saved to contacts.json so they persist between runs.
"""

import json
import os
import tkinter as tk
from tkinter import messagebox

CONTACTS_FILE = "contacts.json"

# ---- Colors (same theme as the calculator app) ----
BG_COLOR = "#1e1e1e"
PANEL_BG = "#2d2d2d"
FG_COLOR = "#ffffff"
ENTRY_BG = "#3a3a3a"
ACCENT = "#ff9500"
DELETE_BG = "#d9534f"


def load_contacts():
    """Load contacts from the JSON file. Returns an empty list if it doesn't exist yet."""
    if not os.path.exists(CONTACTS_FILE):
        return []
    with open(CONTACTS_FILE, "r") as f:
        return json.load(f)


def save_contacts(contacts):
    """Write the current list of contacts to the JSON file."""
    with open(CONTACTS_FILE, "w") as f:
        json.dump(contacts, f, indent=2)


class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.configure(bg=BG_COLOR)
        self.root.geometry("650x420")
        self.root.minsize(600, 400)

        self.contacts = load_contacts()
        self.filtered = list(self.contacts)  # what's currently shown in the listbox
        self.selected_index = None  # index in self.contacts of the currently selected contact

        self.build_left_panel()
        self.build_right_panel()
        self.refresh_list()

    # ---------- UI BUILDING ----------

    def build_left_panel(self):
        left = tk.Frame(self.root, bg=BG_COLOR)
        left.pack(side="left", fill="both", expand=True, padx=(15, 8), pady=15)

        # Search bar
        search_frame = tk.Frame(left, bg=BG_COLOR)
        search_frame.pack(fill="x", pady=(0, 8))

        tk.Label(search_frame, text="Search:", bg=BG_COLOR, fg="#aaaaaa",
                 font=("Segoe UI", 10)).pack(side="left", padx=(0, 6))

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame, textvariable=self.search_var,
            font=("Segoe UI", 12), bg=ENTRY_BG, fg=FG_COLOR, bd=0, insertbackground=FG_COLOR
        )
        search_entry.pack(side="left", fill="x", expand=True, ipady=6)
        search_entry.bind("<KeyRelease>", lambda e: self.refresh_list())

        # Contact list (shows name + phone for every saved contact)
        self.listbox = tk.Listbox(
            left, bg=PANEL_BG, fg=FG_COLOR, font=("Segoe UI", 12),
            bd=0, highlightthickness=0, selectbackground=ACCENT, activestyle="none"
        )
        self.listbox.pack(fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        tk.Button(
            left, text="+ New Contact", command=self.clear_form,
            bg=ACCENT, fg="#ffffff", bd=0, font=("Segoe UI", 11), pady=8
        ).pack(fill="x", pady=(8, 0))

    def build_right_panel(self):
        right = tk.Frame(self.root, bg=BG_COLOR)
        right.pack(side="right", fill="both", padx=(8, 15), pady=15)

        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()

        self.build_field(right, "Name", self.name_var)
        self.build_field(right, "Phone", self.phone_var)
        self.build_field(right, "Email", self.email_var)
        self.build_field(right, "Address", self.address_var)

        btn_frame = tk.Frame(right, bg=BG_COLOR)
        btn_frame.pack(fill="x", pady=(15, 0))

        # Save doubles as both "Add" (nothing selected) and "Update" (a contact is selected)
        tk.Button(
            btn_frame, text="Save", command=self.save_contact,
            bg=ACCENT, fg="#ffffff", bd=0, font=("Segoe UI", 11), pady=8
        ).pack(fill="x", pady=(0, 6))

        tk.Button(
            btn_frame, text="Delete", command=self.delete_contact,
            bg=DELETE_BG, fg="#ffffff", bd=0, font=("Segoe UI", 11), pady=8
        ).pack(fill="x")

    def build_field(self, parent, label, var):
        tk.Label(parent, text=label, bg=BG_COLOR, fg="#aaaaaa", font=("Segoe UI", 10)).pack(
            anchor="w", pady=(8, 2)
        )
        entry = tk.Entry(
            parent, textvariable=var, font=("Segoe UI", 12),
            bg=ENTRY_BG, fg=FG_COLOR, bd=0, insertbackground=FG_COLOR, width=28
        )
        entry.pack(fill="x", ipady=6)

    # ---------- LOGIC ----------

    def refresh_list(self):
        """Redraws the listbox based on the current search text."""
        query = self.search_var.get().strip().lower()
        self.listbox.delete(0, "end")

        if query:
            self.filtered = [
                c for c in self.contacts
                if query in c["name"].lower() or query in c["phone"].lower()
            ]
        else:
            self.filtered = list(self.contacts)

        for c in self.filtered:
            self.listbox.insert("end", f"{c['name']}  —  {c['phone']}")

    def on_select(self, event):
        """When a contact is clicked in the list, load its details into the form."""
        selection = self.listbox.curselection()
        if not selection:
            return
        contact = self.filtered[selection[0]]
        self.selected_index = self.contacts.index(contact)

        self.name_var.set(contact["name"])
        self.phone_var.set(contact["phone"])
        self.email_var.set(contact["email"])
        self.address_var.set(contact["address"])

    def clear_form(self):
        """Clears the form and deselects, ready to add a brand new contact."""
        self.selected_index = None
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.address_var.set("")
        self.listbox.selection_clear(0, "end")

    def save_contact(self):
        """Adds a new contact, or updates the selected one if editing."""
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        address = self.address_var.get().strip()

        if not name or not phone:
            messagebox.showwarning("Missing info", "Name and phone are required.")
            return

        contact = {"name": name, "phone": phone, "email": email, "address": address}

        if self.selected_index is None:
            self.contacts.append(contact)
        else:
            self.contacts[self.selected_index] = contact

        save_contacts(self.contacts)
        self.refresh_list()
        self.clear_form()

    def delete_contact(self):
        if self.selected_index is None:
            messagebox.showinfo("No selection", "Select a contact from the list first.")
            return
        if messagebox.askyesno("Delete contact", "Delete this contact?"):
            del self.contacts[self.selected_index]
            save_contacts(self.contacts)
            self.refresh_list()
            self.clear_form()


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()