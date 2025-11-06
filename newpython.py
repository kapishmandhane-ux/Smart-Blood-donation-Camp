import mysql.connector
from datetime import datetime, timedelta

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
        print("🚫 Underage! Donor must be at least 18 years old.")
        return False

    if last_donation_date:
        last_date = datetime.strptime(str(last_donation_date), "%Y-%m-%d")
        next_eligible_date = last_date + timedelta(days=90)
        today = datetime.today()

        if today < next_eligible_date:
            remaining = next_eligible_date - today
            months_left = remaining.days // 30
            days_left = remaining.days % 30
            print(f"🩸 Not eligible yet. Wait {months_left} month(s) and {days_left} day(s).")
            print(f"Next eligible date: {next_eligible_date.date()}")
            return False
    return True

# ---------- ADD / UPDATE DONOR ----------
def add_or_update_donor():
    name = input("Enter donor name: ").strip()
    contact = input("Enter contact number: ").strip()
    age = int(input("Enter age: ").strip())
    blood_group = input("Enter blood group: ").strip().upper()
    donation_date = datetime.now().strftime("%Y-%m-%d")

    db = connect_db()
    cursor = db.cursor()

    # Check if donor already exists (by name and contact)
    cursor.execute("""
        SELECT UID, Donation_Date, Age FROM donors WHERE Name=%s AND Contact_No=%s
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
            print(f"✅ Updated donation record for {name} on {donation_date}")
    else:
        if check_eligibility(age, None):
            cursor.execute("""
                INSERT INTO donors (Name, Contact_No, Age, Blood_Group, Donation_Date)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, contact, age, blood_group, donation_date))
            db.commit()
            print(f"✅ Added donor {name} successfully on {donation_date}")

    db.close()

# ---------- VIEW ALL DONORS ----------
def view_donors():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM donors")
    rows = cursor.fetchall()

    print("\n--- All Donors ---")
    print("{:<5} {:<20} {:<15} {:<5} {:<10} {:<12}".format("UID", "Name", "Contact", "Age", "BloodGrp", "DonationDate"))
    print("-" * 70)
    for row in rows:
        print("{:<5} {:<20} {:<15} {:<5} {:<10} {:<12}".format(*row))
    db.close()

# ---------- UPDATE CONTACT / AGE / BLOOD GROUP ----------
def update_donor_info():
    uid = input("Enter donor UID to update: ").strip()
    new_contact = input("Enter new contact (leave blank to skip): ").strip()
    new_age = input("Enter new age (leave blank to skip): ").strip()
    new_bg = input("Enter new blood group (leave blank to skip): ").strip().upper()

    db = connect_db()
    cursor = db.cursor()

    if new_contact:
        cursor.execute("UPDATE donors SET Contact_No=%s WHERE UID=%s", (new_contact, uid))
    if new_age:
        cursor.execute("UPDATE donors SET Age=%s WHERE UID=%s", (new_age, uid))
    if new_bg:
        cursor.execute("UPDATE donors SET Blood_Group=%s WHERE UID=%s", (new_bg, uid))

    db.commit()
    db.close()
    print("✅ Donor information updated successfully.")

# ---------- DELETE DONOR ----------
def delete_donor():
    uid = input("Enter donor UID to delete: ").strip()
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM donors WHERE UID=%s", (uid,))
    db.commit()
    db.close()
    print("🗑️ Donor deleted successfully.")

# ---------- MAIN MENU ----------
def main():
    while True:
        print("\n=== 🩸 Blood Donation Management System ===")
        print("1. Add / Update Donation")
        print("2. View All Donors")
        print("3. Update Donor Info")
        print("4. Delete Donor")
        print("5. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_or_update_donor()
        elif choice == "2":
            view_donors()
        elif choice == "3":
            update_donor_info()
        elif choice == "4":
            delete_donor()
        elif choice == "5":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
