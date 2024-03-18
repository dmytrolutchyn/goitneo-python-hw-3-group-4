from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain 10 digits.")
        super().__init__(value)
    
    def validate_phone(self, value):
        return len(str(value)) == 10 and str(value).isdigit()

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid birthday format. Use DD.MM.YYYY.")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if str(phone) == str(old_phone):
                self.phones[i] = Phone(new_phone)
                break

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"


class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        
    def get_birthdays_per_week(self): 
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        bd_weekdays = {day: [] for day in weekdays}
        
        today = datetime.now().date()

        for user in self.data.values():
            if user.birthday.value:
                name = user.name.value
                birthday = datetime.strptime(user.birthday.value, '%d.%m.%Y').date()

                birthday_this_year = birthday.replace(year=today.year)

                if birthday_this_year < today: # check if birthday already happened
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                delta_days = (birthday_this_year - today).days # how many days left to birthday

                birthday_weekday = birthday_this_year.strftime("%A")

                time_to_next_Saturday = timedelta((12 - today.weekday()) % 7).days # days left to this Saturday, so we can congratulate them on next Monday

                if time_to_next_Saturday <= delta_days < time_to_next_Saturday + 7: # is within next week (this Saturday - next Saturday)
                    day_of_week = birthday_this_year.weekday()
                    if day_of_week > 4: # check for weekends
                        bd_weekdays["Monday"].append(name)
                    else:
                        bd_weekdays[birthday_weekday].append(name)

        bds = ''
        for day, names in bd_weekdays.items():
            if names:
                bds += f"{day}: {', '.join(names)}\n"
        
        return bds

if __name__ == "__main__":
   # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")