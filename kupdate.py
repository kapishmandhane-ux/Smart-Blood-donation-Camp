import sqlite3
from colorama import init, Fore, Style

init(autoreset=True)

conn = sqlite3.connect("blood_donation.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS donors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    blood_group TEXT,
    contact TEXT,
    emergency_contact TEXT
)
""")
conn.commit()

def print_header():
    print(Fore.RED + Style.BRIGHT + "\n🩸 Welcome to Blood Donation Camp 🩸")
    print(Fore.YELLOW + "-" * 40)

def add_donor():
    print(Fore.CYAN + "\n➕ Add New Donor")
    name = input("👤 Name: ")
    age = input("🎂 Age: ")
    blood_group = input("🧬 Blood Group: ")
    contact = input("📱 Contact Number: ")
    emergency_contact = input("📞 Emergency Contact: ")

    if not age.isdigit():
        print(Fore.RED + "❌ Age must be a number.")
        return

    cursor.execute("INSERT INTO donors (name, age, blood_group, contact, emergency_contact) VALUES (?, ?, ?, ?, ?)",
                   (name, int(age), blood_group.upper(), contact, emergency_contact))
    conn.commit()
    print(Fore.GREEN + "✅ Donor added successfully!")

def delete_donor():
    print(Fore.CYAN + "\n🗑️ Delete Donor")
    donor_id = input("Enter donor ID to delete: ")
    cursor.execute("DELETE FROM donors WHERE id = ?", (donor_id,))
    conn.commit()
    print(Fore.GREEN + "✅ Donor deleted.")

def view_donors():
    print(Fore.CYAN + "\n📋 All Donors")
    cursor.execute("SELECT * FROM donors")
    donors = cursor.fetchall()
    if donors:
        for d in donors:
            print(Fore.YELLOW + f"ID: {d[0]}, Name: {d[1]}, Age: {d[2]}, Blood Group: {d[3]}, Contact: {d[4]}, Emergency: {d[5]}")
    else:
        print(Fore.RED + "No donors found.")

def search_by_blood_group():
    print(Fore.CYAN + "\n🔍 Search by Blood Group")
    group = input("Enter blood group: ").upper()
    cursor.execute("SELECT * FROM donors WHERE blood_group = ?", (group,))
    results = cursor.fetchall()
    if results:
        for d in results:
            print(Fore.YELLOW + f"ID: {d[0]}, Name: {d[1]}, Age: {d[2]}, Contact: {d[4]}")
    else:
        print(Fore.RED + "No donors found with that blood group.")

def update_donor():
    print(Fore.CYAN + "\n✏️ Update Donor Info")
    donor_id = input("Enter donor ID to update: ")
    cursor.execute("SELECT * FROM donors WHERE id = ?", (donor_id,))
    donor = cursor.fetchone()
    if not donor:
        print(Fore.RED + "Donor not found.")
        return

    print("Leave blank to keep current value.")
    name = input(f"New name ({donor[1]}): ") or donor[1]
    age = input(f"New age ({donor[2]}): ") or donor[2]
    blood_group = input(f"New blood group ({donor[3]}): ") or donor[3]
    contact = input(f"New contact ({donor[4]}): ") or donor[4]
    emergency_contact = input(f"New emergency contact ({donor[5]}): ") or donor[5]

    cursor.execute("""
    UPDATE donors SET name = ?, age = ?, blood_group = ?, contact = ?, emergency_contact = ? WHERE id = ?
    """, (name, int(age), blood_group.upper(), contact, emergency_contact, donor_id))
    conn.commit()
    print(Fore.GREEN + "✅ Donor updated successfully!")

def main():
    while True:
        print_header()
        print(Fore.MAGENTA + """
1️⃣ Add Donor
2️⃣ Delete Donor
3️⃣ View All Donors
4️⃣ Search by Blood Group
5️⃣ Update Donor Info
6️⃣ Exit
""")
        choice = input(Fore.BLUE + "Enter your choice (1-6): ")

        if choice == "1":
            add_donor()
        elif choice == "2":
            delete_donor()
        elif choice == "3":
            view_donors()
        elif choice == "4":
            search_by_blood_group()
        elif choice == "5":
            update_donor()
        elif choice == "6":
            print(Fore.GREEN + "\n👋 Thank you for using Blood Donation Camp!")
            break
        else:
            print(Fore.RED + "❌ Invalid choice. Try again.")

    conn.close()

if __name__ == "__main__":
    main()