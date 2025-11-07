import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Connect to database
conn = sqlite3.connect("blood_bank.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS donors (
    donor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    blood_group TEXT,
    contact_number TEXT,
    email TEXT,
    disease_history TEXT,
    donation_count INTEGER DEFAULT 0
)''')
conn.commit()

# --- Function to send thank you email ---
def send_thank_you_email(email, name, blood_group):
    sender = "your_email@gmail.com"
    password = "your_email_password"  # use App Password if using Gmail
    
    subject = "Thank You for Your Noble Contribution ❤️"
    message = f"""
    <html>
    <body>
        <h2 style="color:#b30000;">Dear {name},</h2>
        <p>We extend our heartfelt gratitude for your blood donation.</p>
        <p>Your contribution has the power to <b>save lives</b> and bring hope to families.</p>
        <p><b>Blood Group Donated:</b> {blood_group}</p>
        <p style="color:green;">You truly are a hero without a cape! 🦸‍♂️</p>
        <p>Keep shining and inspiring others to donate.</p>
        <br>
        <p>Warm regards,<br><b>Smart Blood Bank Team</b></p>
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
        print(f"✅ Thank you email sent to {email}")
    except Exception as e:
        print("❌ Error sending email:", e)


# --- Add Donor ---
def add_donor():
    name = input("Enter Name: ")
    age = int(input("Enter Age: "))
    blood_group = input("Enter Blood Group: ")
    contact = input("Enter Contact Number: ")
    email = input("Enter Email: ")
    disease = input("Any disease history (Yes/No): ")

    if disease.lower() == "yes":
        print("⚠️ Cannot add donor with disease history.")
        return

    cursor.execute("INSERT INTO donors (name, age, blood_group, contact_number, email, disease_history) VALUES (?, ?, ?, ?, ?, ?)",
                   (name, age, blood_group, contact, email, disease))
    conn.commit()
    print("✅ Donor added successfully.")


# --- View Donors ---
def view_donors():
    cursor.execute("SELECT * FROM donors")
    for row in cursor.fetchall():
        print(row)


# --- Delete Donor ---
def delete_donor():
    donor_id = int(input("Enter Donor ID to delete: "))
    cursor.execute("DELETE FROM donors WHERE donor_id = ?", (donor_id,))
    conn.commit()
    print("🗑️ Donor deleted successfully.")


# --- Update Donor ---
def update_donor():
    donor_id = int(input("Enter Donor ID to update: "))
    field = input("Enter field to update (name, age, contact_number, email, blood_group): ")
    new_value = input(f"Enter new value for {field}: ")
    cursor.execute(f"UPDATE donors SET {field} = ? WHERE donor_id = ?", (new_value, donor_id))
    conn.commit()
    print("✅ Donor updated successfully.")


# --- Record Donation ---
def record_donation():
    donor_id = int(input("Enter Donor ID: "))
    cursor.execute("SELECT name, email, blood_group FROM donors WHERE donor_id = ?", (donor_id,))
    donor = cursor.fetchone()
    if donor:
        name, email, blood_group = donor
        cursor.execute("UPDATE donors SET donation_count = donation_count + 1 WHERE donor_id = ?", (donor_id,))
        conn.commit()
        print("🩸 Donation recorded successfully.")
        send_thank_you_email(email, name, blood_group)
    else:
        print("❌ Donor not found.")


# --- Menu ---
while True:
    print("\n====== Blood Bank Management System ======")
    print("1. Add Donor")
    print("2. View Donors")
    print("3. Update Donor")
    print("4. Delete Donor")
    print("5. Record Donation")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        add_donor()
    elif choice == '2':
        view_donors()
    elif choice == '3':
        update_donor()
    elif choice == '4':
        delete_donor()
    elif choice == '5':
        record_donation()
    elif choice == '6':
        print("👋 Exiting... Stay safe and keep donating!")
        break
    else:
        print("❌ Invalid choice. Try again.")