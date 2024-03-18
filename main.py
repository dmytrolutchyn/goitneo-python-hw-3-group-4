from datetime import datetime, timedelta
from classes import Field, Name, Phone, Record, AddressBook


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"ValueError: {str(e)}"
        except KeyError:
            return "User not found."
        except IndexError:
            return "Invalid command. Use format: command [arguments]."
        except Exception as e:
            return f"An error occurred: {str(e)}"

    return inner

def input_error_birthday(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError) as e:
            print(e)
            return "Give correct date please."
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, addressbook):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    addressbook.add_record(record)
    return "Contact added."

@input_error
def change_phone(args, addressbook):
    name, phone = args
    record = addressbook.find(name)
    if record:
        record.edit_phone(record.phones[0], phone)
        return "Phone updated."
    else:
        return "Contact not found."
    
@input_error
def show_phone(args, addressbook):
    name, = args
    record = addressbook.find(name)
    return record.phones[0] if record else "Contact not found."

@input_error
def show_all(addressbook):
    if addressbook:
        for name, record in addressbook.data.items():
            print(f"{record.name}: {record.phones}")
    else:
        print("No contacts found.")

@input_error_birthday
def add_birthday(args, addressbook):
    name, birthday = args
    record = addressbook.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        return "Contact not found."

@input_error
def show_birthday(args, addressbook):
    name = args[0]
    record = addressbook.find(name)
    if record:
        return record.birthday.value
    return "Birthday not set."

@input_error
def show_birthdays(_, addressbook):
    birthdays = addressbook.get_birthdays_per_week()
    if birthdays:
        return birthdays
    else:
        return "No birthdays next week."

def main():
    addressbook = AddressBook()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == 'add':
            print(add_contact(args, addressbook))
        elif command == 'change':
            print(change_phone(args, addressbook))
        elif command == 'phone':
            print(show_phone(args, addressbook))
        elif command == 'all':
            for record in addressbook.data.values():
                print(record)
        elif command == 'add-birthday':
            print(add_birthday(args, addressbook))
        elif command == 'show-birthday':
            print(show_birthday(args, addressbook))
        elif command == 'birthdays':
            print(show_birthdays(args, addressbook))

        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()