import mysql.connector
from datetime import datetime, timedelta

# ---------- DATABASE CONNECTION ----------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",                # your MySQL username
        password="Aurojyoti@10",   # your MySQL password
        database="blood_donation_camp"    # your MySQL database name
    )

# ---------- TABLE FORMATTER ----------
def print_table(headers, rows):
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))
    print("\n" + "-" * (sum(col_widths) + len(col_widths) * 3 + 1))
    print("| " + " | ".join(f"{headers[i].ljust(col_widths[i])}" for i in range(len(headers))) + " |")
    print("-" * (sum(col_widths) + len(col_widths) * 3 + 1))
    for row in rows:
        print("| " + " | ".join(f"{str(row[i]).ljust(col_widths[i])}" for i in range(len(row))) + " |")
    print("-" * (sum(col_widths) + len(col_widths) * 3 + 1) + "\n")

# ---------- ELIGIBILITY CHECK ----------
def check_eligibility(age, last_donation_date):
    if age < 18:
        print("\n🚫 Underage! Donor must be at least 18 years old to donate.\n")
        return False

    if last_donation_date:
        last_date = datetime.strptime(str(last_donation_date), "%Y-%m-%d")
        next_eligible_date = last_date + timedelta(days=90)
        today = datetime.today()

        if today < next_eligible_date:
            remaining = next_eligible_date - today
            months_left = remaining.days // 30
            days_left = remaining.days % 30
            print(f"\n🩸 Donor cannot donate yet. Wait for {months_left} month(s) and {days_left} day(s).")
            print(f"Next eligible donation date: {next_eligible_date.date()}\n")
            return False
    return True

# ---------- ADD OR UPDATE DONOR ----------
def add_or_update_donor():
    name = input("Enter donor name: ").strip()
    contact = input("Enter contact number: ").strip()
    age = int(input("Enter age: "))
    blood_group = input("Enter blood group: ").strip().upper()
    donation_date = input("Enter donation date (YYYY-MM-DD): ").strip()

    db = connect_db()
    cursor = db.cursor()

    # Check if donor exists
    cursor.execute("""
        SELECT UID, Donation_Date FROM donors 
        WHERE Name=%s AND Contact_No=%s AND Age=%s
    """, (name, contact, age))
    result = cursor.fetchone()
#Result is being displayed
    
    if result:
        uid, last_donation_date = result
        print(f"\n🧾 Donor already registered with UID: {uid}")
        if check_eligibility(age, last_donation_date):
            cursor.execute("UPDATE donors SET Donation_Date=%s WHERE UID=%s", (donation_date, uid))
            db.commit()
            print(f"\n✅ Donation date updated successfully for {name}!\n")
        else:
            print("❌ Donation not updated due to ineligibility.\n")
#Chrcks the eligiblity
    else:
        if check_eligibility(age, None):
            cursor.execute("""
                INSERT INTO donors (Name, Contact_No, Age, Blood_Group, Donation_Date)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, contact, age, blood_group, donation_date))
            db.commit()
            print(f"\n✅ New donor {name} added successfully!\n")
        else:
            print("❌ Donor not added due to age restriction.\n")

    db.close()

# ---------- VIEW ALL DONORS ----------
def view_donors():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM donors")
    rows = cursor.fetchall()
    if rows:
        headers = ["UID", "Name", "Contact No", "Age", "Blood Group", "Donation Date"]
        print_table(headers, rows)
    else:
        print("\n❌ No donor records found.\n")
    db.close()

# ---------- UPDATE DONOR INFO ----------
def update_donor_info():
    name = input("Enter donor name: ").strip()
    contact = input("Enter current contact number: ").strip()

    db = connect_db()
    cursor = db.cursor()

    # Check if donor exists
    cursor.execute("SELECT UID, Name, Contact_No, Age, Blood_Group, Donation_Date FROM donors WHERE Name=%s AND Contact_No=%s", (name, contact))
    result = cursor.fetchone()

    if not result:
        print("\n❌ Donor not found.\n")
        db.close()
        return

    uid = result[0]
    print("\n--- Update Menu ---")
    print("1. Update Contact Number")
    print("2. Update Age")
    print("3. Update Blood Group")
    choice = input("Enter your choice: ")

    if choice == '1':
        new_contact = input("Enter new contact number: ")
        cursor.execute("UPDATE donors SET Contact_No=%s WHERE UID=%s", (new_contact, uid))
    elif choice == '2':
        new_age = int(input("Enter new age: "))
        cursor.execute("UPDATE donors SET Age=%s WHERE UID=%s", (new_age, uid))
    elif choice == '3':
        new_bg = input("Enter new blood group: ").strip().upper()
        cursor.execute("UPDATE donors SET Blood_Group=%s WHERE UID=%s", (new_bg, uid))
    else:
        print("❌ Invalid choice.")
        db.close()
        return

    db.commit()
    print("\n✅ Donor information updated successfully!\n")
    db.close()

# ---------- DELETE DONOR ----------
def delete_donor():
    name = input("Enter donor name to delete: ").strip()
    contact = input("Enter contact number: ").strip()

    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SELECT UID FROM donors WHERE Name=%s AND Contact_No=%s", (name, contact))
    result = cursor.fetchone()

    if not result:
        print("\n❌ Donor not found.\n")
    else:
        cursor.execute("DELETE FROM donors WHERE UID=%s", (result[0],))
        db.commit()
        print(f"\n🗑️ Donor {name} deleted successfully!\n")

    db.close()

# ---------- MAIN MENU ----------
def main():
    while True:
        print("\n=== 🩸 BLOOD DONATION MANAGEMENT SYSTEM ===")
        print("1. Add / Update Donor (Donation Date)")
        print("2. View All Donors")
        print("3. Update Donor Info (Contact/Age/Blood Group)")
        print("4. Delete Donor")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_or_update_donor()
        elif choice == '2':
            view_donors()
        elif choice == '3':
            update_donor_info()
        elif choice == '4':
            delete_donor()
        elif choice == '5':
            print("\n👋 Exiting program... Goodbye!\n")
            break
        else:
            print("\n❌ Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()
