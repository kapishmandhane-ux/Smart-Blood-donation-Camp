import mysql.connector
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox

# ---------- DATABASE CONNECTION ----------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",               # your MySQL username
        password="Aurojyoti@10",  # your MySQL password
        database="blood_donation_camp"   # your MySQL database name
    )

# ---------- ELIGIBILITY CHECK ----------
def check_eligibility(age, last_donation_date):
    if age < 18:
        messagebox.showwarning("Ineligible", "🚫 Underage! Donor must be at least 18 years old.")
        return False

    if last_donation_date:
        last_date = datetime.strptime(str(last_donation_date), "%Y-%m-%d")
        next_eligible_date = last_date + timedelta(days=90)
        today = datetime.today()

        if today < next_eligible_date:
            remaining = next_eligible_date - today
            months_left = remaining.days // 30
            days_left = remaining.days % 30
            messagebox.showinfo(
                "Not Eligible",
                f"🩸 Donor cannot donate yet.\nWait for {months_left} month(s) and {days_left} day(s).\n"
                f"Next eligible date: {next_eligible_date.date()}"
            )
            return False
    return True

# ---------- ADD / UPDATE DONOR ----------
def add_update_donor():
    name = name_entry.get().strip()
    contact = contact_entry.get().strip()
    age_text = age_entry.get().strip()
    blood_group = bg_entry.get().strip().upper()
    donation_date = datetime.now().strftime("%Y-%m-%d")  # auto date

    if not (name and contact and age_text and blood_group):
        messagebox.showerror("Error", "Please fill all fields.")
        return

    try:
        age = int(age_text)
    except ValueError:
        messagebox.showerror("Error", "Age must be a number.")
        return

    db = connect_db()
    cursor = db.cursor()

    # Check for existing donor using Name + Contact only
    cursor.execute("""
        SELECT UID, Donation_Date, Age FROM donors 
        WHERE Name=%s AND Contact_No=%s
    """, (name, contact))
    result = cursor.fetchone()

    if result:
        uid, last_donation_date, old_age = result
        if check_eligibility(age, last_donation_date):
            cursor.execute("""
                UPDATE donors 
                SET Age=%s, Blood_Group=%s, Donation_Date=%s 
                WHERE UID=%s
            """, (age, blood_group, donation_date, uid))
            db.commit()
            messagebox.showinfo("Updated", f"✅ Donation record updated for {name} ({donation_date})")
    else:
        if check_eligibility(age, None):
            cursor.execute("""
                INSERT INTO donors (Name, Contact_No, Age, Blood_Group, Donation_Date)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, contact, age, blood_group, donation_date))
            db.commit()
            messagebox.showinfo("Added", f"✅ Donor {name} added successfully on {donation_date}")

    db.close()
    view_donors()

# ---------- VIEW DONORS ----------
def view_donors():
    for row in donor_table.get_children():
        donor_table.delete(row)
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM donors")
    for row in cursor.fetchall():
        donor_table.insert("", tk.END, values=row)
    db.close()

# ---------- UPDATE INFO ----------
def update_info():
    selected = donor_table.focus()
    if not selected:
        messagebox.showerror("Error", "Please select a donor to update.")
        return
    values = donor_table.item(selected, 'values')
    uid = values[0]
    new_contact = contact_entry.get().strip()
    new_age = age_entry.get().strip()
    new_bg = bg_entry.get().strip().upper()

    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE donors SET Contact_No=%s, Age=%s, Blood_Group=%s WHERE UID=%s
    """, (new_contact, new_age, new_bg, uid))
    db.commit()
    db.close()
    messagebox.showinfo("Updated", "✅ Donor information updated successfully.")
    view_donors()

# ---------- DELETE DONOR ----------
def delete_donor():
    selected = donor_table.focus()
    if not selected:
        messagebox.showerror("Error", "Please select a donor to delete.")
        return
    values = donor_table.item(selected, 'values')
    uid = values[0]
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM donors WHERE UID=%s", (uid,))
    db.commit()
    db.close()
    messagebox.showinfo("Deleted", "🗑️ Donor deleted successfully.")
    view_donors()

# ---------- GUI ----------
root = tk.Tk()
root.title("🩸 Blood Donation Management System")
root.geometry("1000x600")
root.configure(bg="#1e1e2f")

root.columnconfigure((0, 1, 2), weight=1)
root.rowconfigure(6, weight=1)

# ---------- STYLE ----------
style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview",
                background="#2c2c3e",
                foreground="white",
                rowheight=25,
                fieldbackground="#2c2c3e")
style.configure("Treeview.Heading",
                background="#ff4c4c",
                foreground="white",
                font=("Helvetica", 10, "bold"))
style.map("Treeview", background=[("selected", "#ffeb3b")])

label_fg = "#f5f5f5"
entry_bg = "#3c3c50"
entry_fg = "white"
btn_font = ("Helvetica", 10, "bold")
btn_bg = "#ffeb3b"
btn_fg = "black"

# ---------- FORM ----------
tk.Label(root, text="Name:", bg="#1e1e2f", fg=label_fg).grid(row=0, column=0, padx=10, pady=5, sticky="w")
name_entry = tk.Entry(root, bg=entry_bg, fg=entry_fg, insertbackground="white")
name_entry.grid(row=0, column=1, pady=5, sticky="ew")

tk.Label(root, text="Contact No:", bg="#1e1e2f", fg=label_fg).grid(row=1, column=0, padx=10, pady=5, sticky="w")
contact_entry = tk.Entry(root, bg=entry_bg, fg=entry_fg, insertbackground="white")
contact_entry.grid(row=1, column=1, pady=5, sticky="ew")

tk.Label(root, text="Age:", bg="#1e1e2f", fg=label_fg).grid(row=2, column=0, padx=10, pady=5, sticky="w")
age_entry = tk.Entry(root, bg=entry_bg, fg=entry_fg, insertbackground="white")
age_entry.grid(row=2, column=1, pady=5, sticky="ew")

tk.Label(root, text="Blood Group:", bg="#1e1e2f", fg=label_fg).grid(row=3, column=0, padx=10, pady=5, sticky="w")
bg_entry = tk.Entry(root, bg=entry_bg, fg=entry_fg, insertbackground="white")
bg_entry.grid(row=3, column=1, pady=5, sticky="ew")

# ---------- BUTTONS ----------
tk.Button(root, text="Add / Update Donation", command=add_update_donor,
          bg=btn_bg, fg=btn_fg, font=btn_font, relief="raised", borderwidth=3,
          activebackground="#fff176").grid(row=5, column=0, pady=10, padx=10, sticky="ew")

tk.Button(root, text="Update Info", command=update_info,
          bg=btn_bg, fg=btn_fg, font=btn_font, relief="raised", borderwidth=3,
          activebackground="#fff176").grid(row=5, column=1, pady=10, padx=10, sticky="ew")

tk.Button(root, text="Delete Donor", command=delete_donor,
          bg=btn_bg, fg=btn_fg, font=btn_font, relief="raised", borderwidth=3,
          activebackground="#fff176").grid(row=5, column=2, pady=10, padx=10, sticky="ew")

# ---------- TABLE ----------
columns = ("UID", "Name", "Contact No", "Age", "Blood Group", "Donation Date")
donor_table = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    donor_table.heading(col, text=col)
    donor_table.column(col, width=150)
donor_table.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

scroll = ttk.Scrollbar(root, orient="vertical", command=donor_table.yview)
scroll.grid(row=6, column=3, sticky="ns")
donor_table.configure(yscrollcommand=scroll.set)

view_donors()
root.mainloop()
