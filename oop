
from flask import Flask
from datetime import datetime

#class for users
class User:
    def __init__(self,password,mail,firstname,surname,birth_date,phone,city,street,apartment):
        self.mail=mail
        self.password=password
        self.firstname=firstname
        self.surname=surname
        self.birth_date=birth_date
        self.phone=phone
        self.city=city
        self.street=street
        self.apartment=apartment

    def ValidateUserSignUp(self): #validation for user signup
        mailcheck = "@" in self.mail #mail stractcure check
        if mailcheck is False:
            return "Invalid mail"
        if self.birth_date == "":  # default birth_date
            self.birth_date = 1 / 1 / 2022
        if len(self.password) < 8: #validating password
            return "Password needs to be longer then 8 characters"
        try:  # checking phone number
            if len(self.phone) != 10:
                return "Invalid phone number"
            self.phone = int(self.phone)
        except ValueError:
            return "Invalid phone number"
        else:
            return "Valid"


#class for librarians
class Librarian:
    def __init__(self, mail,password,firstname,surname, phone,city,street,apartment,work_start_date,branch):
        self.mail = mail
        self.password=password
        self.firstname = firstname
        self.surname = surname
        self.phone = phone
        self.city = city
        self.street = street
        self.apartment = apartment
        self.work_start_date=work_start_date
        self.branch=branch

    def ValidateLibrarianSignUp(self):  # validate librarian sign up
        mailcheck = "@" in self.mail
        if mailcheck == False:
            return "Invalid mail"
        if self.work_start_date == "":  # default birth_date
            self.work_start_date = 1 / 1 / 2022
        if len(self.password) < 8:
            return "Password needs to be longer then 8 characters"
        try:  # checking phone number
            if len(self.phone) != 10:
                return "Invalid phone number"
            self.phone = int(self.phone)
        except ValueError:
            return "Invalid phone number"

        else:
            return "Valid"



#class for books
class Book:
    def __init__(self,book_id,book_name,writer_name,publish_year,publisher):
        self.book_id=book_id
        self.book_name=book_name
        self.writer_name=writer_name
        self.publish_year=publish_year
        self.publisher=publisher


    def ValidateNewBook(self):
        try:
            self.publish_year = int(self.publish_year)
        except ValueError:
            return " Invalid publish year"
        if self.publish_year > datetime.today().year:
            return "Invalid publish year"
        if self.book_name == "":
            return "Invalid book name"
        if self.writer_name == "":
            return "Invalid writer name"
        if self.publisher == "":
            return "Invalid publisher"
        return "Valid"


if __name__ == "__main__":
    try:
        print("fuck")
    except ValueError:
        print("shit")
