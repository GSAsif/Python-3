class Person:
   
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display_info(self):
        print(f"Name : {self.name}")
        print(f"Age  : {self.age}")


class Member(Person):
   

    def __init__(self, member_id, name, age):
        super().__init__(name, age)
        self.member_id = member_id
        self.borrowed_books = []  

    def borrow_book(self, book):
        
        self.borrowed_books.append(book)

    def return_book(self, book):
        
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)

    def has_borrowed(self, isbn):
        
        return any(book.isbn == isbn for book in self.borrowed_books)

    def display_info(self):
        
        print(f"Member ID      : {self.member_id}")
        print(f"Name           : {self.name}")
        print(f"Age            : {self.age}")
        print(f"Borrowed Books : {len(self.borrowed_books)}")


class Book:
    

    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.__available = True  

    @property
    def available(self):
        
        return self.__available

    @available.setter
    def available(self, value):
        
        if not isinstance(value, bool):
            raise ValueError("Availability must be True or False.")
        self.__available = value

    @property
    def status(self):
        
        return "Available" if self.__available else "Borrowed"

    def display_book(self):
        print(f"ISBN   : {self.isbn}")
        print(f"Title  : {self.title}")
        print(f"Author : {self.author}")
        print(f"Status : {self.status}")


class Library:
    

    def __init__(self):
        self.books = []      
        self.members = []    
    
    @staticmethod
    def is_valid_text(value):
        
        return isinstance(value, str) and value.strip() != ""

    
    def find_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def add_book(self, title, author, isbn):
        if not self.is_valid_text(title):
            raise ValueError("Book title cannot be empty.")
        if not self.is_valid_text(author):
            raise ValueError("Author name cannot be empty.")
        if self.find_book(isbn) is not None:
            raise ValueError("ISBN already exists.")

        new_book = Book(title, author, isbn)
        self.books.append(new_book)
        return new_book

    def show_books(self):
        if len(self.books) == 0:
            print("No books available in the library.")
            return

        print("------------- BOOK LIST -------------")
        for book in self.books:
            book.display_book()
            print("-------------------------------------")

    def search_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    
    def find_member(self, member_id):
        for member in self.members:
            if member.member_id == member_id:
                return member
        return None

    def register_member(self, member_id, name, age):
        if not self.is_valid_text(name):
            raise ValueError("Member name cannot be empty.")
        if age <= 0:
            raise ValueError("Age must be greater than 0.")
        if self.find_member(member_id) is not None:
            raise ValueError("Member ID already exists.")

        new_member = Member(member_id, name, age)
        self.members.append(new_member)
        return new_member

    def show_members(self):
        if len(self.members) == 0:
            print("No members registered yet.")
            return

        print("----------- MEMBER LIST ------------")
        for member in self.members:
            member.display_info()
            print("------------------------------------")

    
    def borrow_book(self, member_id, isbn):
        member = self.find_member(member_id)
        if member is None:
            raise LookupError("Member not found.")

        book = self.find_book(isbn)
        if book is None:
            raise LookupError("Book not found.")

        if not book.available:
            raise ValueError("Sorry! This book is currently unavailable.")

        if member.has_borrowed(isbn):
            raise ValueError("This member has already borrowed this book.")

        book.available = False
        member.borrow_book(book)

    def return_book(self, member_id, isbn):
        member = self.find_member(member_id)
        if member is None:
            raise LookupError("Member not found.")

        book = self.find_book(isbn)
        if book is None:
            raise LookupError("Book not found.")

        if not member.has_borrowed(isbn):
            raise ValueError("This member did not borrow this book.")

        book.available = True
        member.return_book(book)


# ---------------------------------------------------------------------------
# Console interface
# ---------------------------------------------------------------------------

def print_header():
    print("=========================================")
    print("LIBRARY MANAGEMENT SYSTEM")
    print("=========================================")


def print_menu():
    print("1. Add Book")
    print("2. Register Member")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Show All Books")
    print("6. Show All Members")
    print("7. Search Book")
    print("8. Exit")


def add_book_flow(library):
    print("----- Add New Book -----")
    title = input("Enter Book Title : ")
    author = input("Enter Author : ")
    isbn = input("Enter ISBN : ")

    try:
        library.add_book(title, author, isbn)
        print("Book added successfully!")
    except ValueError as e:
        print(f"Error: {e}")


def register_member_flow(library):
    print("----- Register Member -----")
    member_id = input("Enter Member ID : ")
    name = input("Enter Name : ")

    try:
        age = int(input("Enter Age : "))
    except ValueError:
        print("Error: Age must be a valid number.")
        return

    try:
        library.register_member(member_id, name, age)
        print("Member registered successfully!")
    except ValueError as e:
        print(f"Error: {e}")


def borrow_book_flow(library):
    print("------ Borrow Book ------")
    member_id = input("Enter Member ID : ")
    isbn = input("Enter Book ISBN : ")

    try:
        library.borrow_book(member_id, isbn)
        print("Book borrowed successfully.")
    except (LookupError, ValueError) as e:
        print(str(e))


def return_book_flow(library):
    print("------ Return Book ------")
    member_id = input("Enter Member ID : ")
    isbn = input("Enter Book ISBN : ")

    try:
        library.return_book(member_id, isbn)
        print("Book returned successfully.")
    except (LookupError, ValueError) as e:
        print(str(e))


def search_book_flow(library):
    print("------ Search Book ------")
    title = input("Enter Book Title : ")

    book = library.search_book(title)
    if book is None:
        print("Book not found.")
    else:
        print("Book Found!")
        book.display_book()


def main():
    library = Library()

    while True:
        print_header()
        print_menu()

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                add_book_flow(library)
            elif choice == "2":
                register_member_flow(library)
            elif choice == "3":
                borrow_book_flow(library)
            elif choice == "4":
                return_book_flow(library)
            elif choice == "5":
                library.show_books()
            elif choice == "6":
                library.show_members()
            elif choice == "7":
                search_book_flow(library)
            elif choice == "8":
                print("Thank you for using Library Management System.")
                print("Goodbye!")
                break
            else:
                print("Invalid choice! Please select a valid option.")
        except Exception as e:
            
            print(f"An unexpected error occurred: {e}")

        input("Press Enter to continue...")


if __name__ == "__main__":
    main()
