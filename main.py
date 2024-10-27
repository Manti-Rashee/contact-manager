from contacts import ContactManager

def main_menu():
    """Main menu to handle database creation and viewing."""
    while True:
        print("\nMain Menu:")
        print("1. Create New Contact Database")
        print("2. View Existing Contact Database")
        print("3. Exit")

        choice = input("Choose an option (1, 2, or 3): ")
        if choice == '1':
            ContactManager.create_new_database()
        elif choice == '2':
            ContactManager.view_existing_database()
        elif choice == '3':
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
