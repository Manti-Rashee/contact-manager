import sqlite3
import os
import csv

class ContactManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Create the contacts table if it doesn't already exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT
            )
        ''')
        self.conn.commit()

    def add_contact(self):
        """Add a new contact."""
        name = input("Enter contact name: ")
        phone = input("Enter contact phone number: ")
        email = input("Enter contact email (optional): ")

        self.cursor.execute('INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)', (name, phone, email))
        self.conn.commit()
        print("Contact added successfully.")

    def update_contact(self):
        """Update an existing contact."""
        contact_id = input("Enter the ID of the contact you want to update: ")
        name = input("Enter new contact name (leave blank to keep current): ")
        phone = input("Enter new contact phone number (leave blank to keep current): ")
        email = input("Enter new contact email (leave blank to keep current): ")

        # Construct the SQL update query dynamically based on user input
        updates = []
        if name:
            updates.append(f"name = '{name}'")
        if phone:
            updates.append(f"phone = '{phone}'")
        if email:
            updates.append(f"email = '{email}'")

        if updates:
            updates_query = ", ".join(updates)
            self.cursor.execute(f'UPDATE contacts SET {updates_query} WHERE id = ?', (contact_id,))
            self.conn.commit()
            print("Contact updated successfully.")
        else:
            print("No changes made.")

    def delete_contact(self):
        """Delete an existing contact."""
        contact_id = input("Enter the ID of the contact you want to delete: ")
        self.cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
        self.conn.commit()
        print("Contact deleted successfully.")

    def export_contacts_to_csv(self):
        """Export contacts to a CSV file."""
        filename = input("Enter the filename for the CSV (e.g., contacts.csv): ")
        self.cursor.execute('SELECT * FROM contacts')
        rows = self.cursor.fetchall()
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Phone", "Email"])  # header
            writer.writerows(rows)
        print(f"Contacts exported to {filename} successfully.")

    def view_contacts(self):
        """View all contacts."""
        self.cursor.execute('SELECT * FROM contacts')
        rows = self.cursor.fetchall()
        if rows:
            print("\nContacts List:")
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}, Email: {row[3]}")
        else:
            print("No contacts found.")

    def show_menu(self):
        """Show menu for managing contacts in the database."""
        while True:
            print("\nContact Manager Menu:")
            print("1. Add Contact")
            print("2. View Contacts")
            print("3. Update Contact")
            print("4. Delete Contact")
            print("5. Export Contacts to CSV")
            print("6. Exit to Main Menu")

            choice = input("Choose an option (1-6): ")
            if choice == '1':
                self.add_contact()
            elif choice == '2':
                self.view_contacts()
            elif choice == '3':
                self.update_contact()
            elif choice == '4':
                self.delete_contact()
            elif choice == '5':
                self.export_contacts_to_csv()
            elif choice == '6':
                print("Returning to the main menu...")
                break
            else:
                print("Invalid choice. Please try again.")

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()

    @staticmethod
    def create_new_database():
        """Function to create a new database for storing contacts."""
        db_name = input("Enter the name of your new contact database (e.g., new_contacts.db): ")
        
        if not os.path.exists(db_name):
            manager = ContactManager(db_name)
            print(f"New database '{db_name}' created successfully.")
            manager.show_menu()  # Shows the contact management menu after creation
            manager.close_connection()
        else:
            print(f"Database '{db_name}' already exists.")

    @staticmethod
    def view_existing_database():
        """Function to view an existing contact database."""
        db_name = input("Enter the name of your existing database (e.g., john_contacts.db): ")
        
        if os.path.exists(db_name):
            manager = ContactManager(db_name)
            print(f"Connected to database: {db_name}")
            manager.show_menu()  # Shows the contact management menu for the existing database
            manager.close_connection()
        else:
            print(f"Database '{db_name}' does not exist.")
