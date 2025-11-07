import mysql.connector
from datetime import datetime, timedelta

# Connecting to DATABASE
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Aurojyoti@10",
        database="blood_donation_camp",

    )

# Checking eligibility of donor(only age and last donation date)
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

#Adding or updating a donor information(updating last donation date)
def add_or_update_donor():
    name = input("Enter donor name: ").strip()
    contact = input("Enter contact number: ").strip()
    age = int(input("Enter age: ").strip())
    blood_group = input("Enter blood group: ").strip().upper()
    donation_date = datetime.now().strftime("%Y-%m-%d")

    db = connect_db()
    cursor = db.cursor()

    # checking if donor with given information already exists or he is new
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

# Viewing the already registered donors
def view_donors():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT UID, Name, Contact_No, Age, Blood_Group, Donation_Date FROM donors")
    rows = cursor.fetchall()

    print("\n--- Donor List ---")
    print("{:<5} {:<20} {:<15} {:<5} {:<10} {:<15}".format("UID", "Name", "Contact", "Age", "BloodGrp", "DonationDate"))
    print("-" * 75)

    for row in rows:
        uid, name, contact, age, bg, date_val = row

        # Fix: Convert various possible types to string safely
        if isinstance(date_val, datetime):
            date_str = date_val.date().strftime("%Y-%m-%d")
        elif hasattr(date_val, "strftime"):
            date_str = date_val.strftime("%Y-%m-%d")
        else:
            date_str = str(date_val) if date_val else "N/A"

        print("{:<5} {:<20} {:<15} {:<5} {:<10} {:<15}".format(uid, name, contact, age, bg, date_str))

    db.close()


# Updating already existing donors contact number, age and blood group
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

#Deleting a donor from the dataset
def delete_donor():
    uid = input("Enter donor UID to delete: ").strip()
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM donors WHERE UID=%s", (uid,))
    db.commit()
    db.close()
    print("🗑️ Donor deleted successfully.")

# Running the program
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
