# Welcome to group 6 library - presented by amit kaplan, or salem and nadav ilany

# Setup

# Importing
from typing import Union, Any

from flask import Flask, request, render_template, session, redirect
from datetime import datetime
from datetime import timedelta

# import datetime
from flask_session import Session
from flaskext.mysql import MySQL
import oop
import pymysql as mdb
from pymysql.cursors import Cursor

mdb.install_as_MySQLdb()
app = Flask(__name__)
mysql = MySQL()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'project'
mysql.init_app(app)
connection=mysql.connect()
cursor: Union[Cursor, Any]=connection.cursor()
Session(app)
print("imported")

#Helper Functions

def ValidateLogin(mail,password): #validating login
    #validating username and identidying type of user
    type_of_user=""
    valid=0
    is_user = cursor.execute("SELECT UserMail FROM users WHERE UserMail=%s ", mail)
    is_librarian = cursor.execute("SELECT Librarian_Email FROM librarian WHERE Librarian_Email=%s ", mail)
    if is_user==1: #checking if user is registered as a user
        type_of_user = "user"
        valid= cursor.execute("SELECT UserMail FROM users WHERE UserMail=%s and User_Password=%s ", [mail,password])
    elif is_librarian==1: #checking if user is registered as a librarian
        type_of_user ="librarian"
        valid = cursor.execute("SELECT Librarian_Email FROM librarian WHERE Librarian_Email=%s and Librarian_Password=%s ", [mail, password])
    if type_of_user=="": #user is not found
        return "User dosent exist"
    #validating password
    if (valid==0):
        return "Wrong password"
    else: #passed validation
        return type_of_user


def is_book_exist(bookid): #checks if the BookId already in our database
    type_of_book = ""
    is_exist= cursor.execute("SELECT BookID FROM Books WHERE BookID=%s ", bookid)
    if is_exist == 0:
        type_of_book = "new"
    else:
        type_of_book= "old"
    return type_of_book


def ValidateBorrowRequest(mail,BorrowDate,BookID): #After a borrow is submitted, this function validates the request and returns the copy id to borrow
    is_user = cursor.execute("SELECT UserMail FROM users WHERE UserMail=%s ", mail) #user validation
    if is_user==0:
        return "Invalid user mail"
    if BorrowDate=="": #date validation
        return "Invalid date"
    BorrowDate=datetime.date(BorrowDate)
    is_book = cursor.execute("SELECT BookID FROM books WHERE BookID=%s ", BookID)  # checks if the book exists
    if is_book == 0:
        return "Unknown book"
    #checking for primary key singularity, cant allow a user to borrow same book at the same day
    is_valid= cursor.execute('''SELECT * 
                                FROM Borrows JOIN Copies ON Borrows.CopyID=Copies.CopyID
                                WHERE UserMail=%s AND BorrowDate=%s AND BookID=%s''',(mail,BorrowDate,BookID))
    if is_valid!=0:
        return "Cant borrow same book for same user in the same day"

    #check if the book is available
    is_available=cursor.execute('''SELECT CopyID FROM Copies
                                    WHERE Branch_Address=%s AND BookID=%s 
                                    AND (Copy_Status='Available' OR Copy_Status='Ordered')''',(session["librarian"][1],BookID))
    if is_available==0:
        return "Book is not available"
    CopyID=cursor.fetchone()[0] #chose a copy id

    #check if the user has more than 3 borrows
    MoreThen3=cursor.execute('''SELECT COUNT(*) AS num FROM borrows 
                                WHERE Real_Return_Date is %s AND UserMail=%s
                                GROUP BY UserMail HAVING num>3''',(None,mail))
    if MoreThen3==1:
        return "You have more than 3 borrows"

    #check if copy is ordered by a different user
    is_ordered=cursor.execute('''SELECT UserMail 
                                FROM Copies NATURAL JOIN Orders 
                                WHERE CopyID=%s AND Orders_Status='active' ''', CopyID)
    if is_ordered!=0 and cursor.fetchone()[0]!=mail:
        return "This book is ordered for another user"
    #if the order is by the requesting user,allow him to borrow it
    is_oredered_by_our_user = cursor.execute('''SELECT CopyID FROM Copies  NATURAL JOIN Orders 
                                                WHERE Branch_Address=%s AND BookID=%s AND UserMail=%s''',(session["librarian"][1], BookID, mail))
    if is_oredered_by_our_user == 1:
        CopyID = cursor.fetchone()[0]
        cursor.execute("UPDATE Orders SET Orders_Status = 'taken by user' WHERE UserMail=%s",mail)
        connection.commit()
    #got to the end
    return "Valid",CopyID


def ExtensionCheck(CopyID,BorrowDate): #After an extension request is submited, checks if to addmit or reject
    is_ordered=cursor.execute("SELECT Copy_Status FROM Copies WHERE CopyID=%s AND Copy_Status='Ordered'",CopyID)
    is_extended=cursor.execute('''SELECT * FROM Borrows 
                                   WHERE CopyID=%s AND BorrowDate=%s AND UserMail=%s AND Extension_Request is not %s '''
                                    ,(CopyID,BorrowDate,session["user"],None))
    if is_ordered!=0: #copy is ordered, waiting for return
        return "Cant allow extension, book is ordered"
    if is_extended==1:#already extended once
        return "Cant allow extension, already extended once"
    return "Valid"


def UpdateReturnDate(UserMail, CopyID, BorrowDate): #Help funcation that update the return date based on the duration
    query = "SELECT Return_Date FROM borrows  WHERE UserMail=%s AND CopyID=%s AND BorrowDate=%s"
    cursor.execute(query, (UserMail, CopyID, BorrowDate))
    ReturnDate = cursor.fetchone()[0]
    ReturnDate=ReturnDate+ timedelta(days=7)
    return ReturnDate


def ValidateOrder(BookName, AuthorName, BranchAddress):
    # After an order request is submited, this function checks if we should reject or admit,
    # and return the copy of the soonest to return copy

    #Fetch the book id according to the data from the form
    global ReturnDate
    cursor.execute("SELECT BookID FROM Books NATURAL JOIN Copies NATURAL JOIN Branches WHERE BookName=%s AND AuthorName=%s AND Branch_Address=%s",(BookName,AuthorName,BranchAddress))
    BookID=cursor.fetchone()
    #Checks if the book exists in the requested branch
    in_branch=cursor.execute('''SELECT * 
                            FROM Books NATURAL JOIN Copies NATURAL JOIN Branches 
                            WHERE BookName=%s AND AuthorName=%s AND Branch_Address=%s''',(BookName,AuthorName,BranchAddress))
    if in_branch==0:
        return "Book dosent exist in branch"
    #Checks if the book is available - if it is, tell the client to come borrow it
    is_available=cursor.execute('''SELECT * 
                                FROM Books NATURAL JOIN Copies NATURAL JOIN Branches
                                WHERE BookName=%s AND AuthorName=%s AND Branch_Address=%s AND Copy_Status='Available' '''
                                ,(BookName,AuthorName,BranchAddress))
    if is_available!=0:
        return "Book is available in this branch, you may borrow it"
    #Now we check if the book is already ordered or borrowed, and returning an error message according to the book status
    is_borrwed=cursor.execute("SELECT * FROM Books NATURAL JOIN Copies NATURAL JOIN Branches WHERE BookName=%s AND AuthorName=%s AND Branch_Address=%s AND Copy_Status='Borrowed'",(BookName,AuthorName,BranchAddress))
    is_ordered=cursor.execute("SELECT * FROM Books NATURAL JOIN Copies NATURAL JOIN Branches WHERE BookName=%s AND AuthorName=%s AND Branch_Address=%s AND Copy_Status='Ordered'",(BookName,AuthorName,BranchAddress))
    if is_borrwed==0 and is_ordered!=0:
        return "cant order, high demand"
    is_ordered_by_user=cursor.execute("SELECT * FROM Copies NATURAL JOIN Orders WHERE BookID=%s AND Copy_Status='Ordered' AND Orders.UserMail=%s",(BookID,session["user"]))
    if is_ordered_by_user!=0:
        return "You already ordered this book"
    is_borrowed_by_you=cursor.execute("SELECT * FROM Copies NATURAL JOIN Borrows NATURAL JOIN  Orders WHERE BookID=%s AND Copy_Status='Borrowed' AND Orders.UserMail=%s",(BookID,session["user"]))
    if is_borrowed_by_you!=0:
        return "You currently have this book borrowed by you"

    #searching for a copy that will return closests
    cursor.execute("SELECT Return_Date FROM Copies NATURAL JOIN Borrows WHERE BookID=%s AND Copy_Status='Borrowed'",BookID)
    lst=cursor.fetchall()
    if len(lst)>1:
        ReturnDate=min(lst)
    elif len(lst)==1:
        ReturnDate=lst
    cursor.execute('''SELECT CopyID FROM Copies NATURAL JOIN Borrows
                      WHERE BookID=%s AND Return_Date=%s''',(BookID,ReturnDate))
    CopyID=cursor.fetchone()[0]
    return "Valid",CopyID

def UpdateOrderStatus() -> object:
    #A function that updates order status - runs before borrow book, order book and order history
    #Also, this function switches to a copy that returns before the waiting copy
    #If an order is active, checks when 3 days passed to than make it expired
    global Real_Return_Date, Copy_Status
    #A query to accsess all the relevant orders
    num_of_orders=cursor.execute('''SELECT Copy_Status,Orders_Status,Real_Return_Date,Order_Date,Copies.CopyID,BookID,Branch_Address 
                                    FROM Copies NATURAL JOIN Orders JOIN Borrows ON Orders.CopyID=Borrows.CopyID 
                                    WHERE Orders_Status<>'expired' ''')
    if num_of_orders==0: #No relevant orders
        return
    orders=cursor.fetchall()
    for i in orders: #Iterating for every order
        Copy_Status=i[0]
        Orders_Status = i[1]
        Real_Return_Date = i[2]
        Order_Date=i[3]
        CopyID=i[4]
        BookID=i[5]
        BranchAddress=i[6]
        if Orders_Status=='expired' or Orders_Status=='taken by user': #Make sure not to activate past orders
            pass
        elif Real_Return_Date is None: #Book is still borrowed
            num_of_available=cursor.execute('''SELECT CopyID 
                                                FROM Copies NATURAL JOIN Borrows 
                                                WHERE BookID=%s AND Branch_Address=%s AND Copy_Status='Available' ''',(BookID,BranchAddress))
            if num_of_available==0: #No other book is available
                cursor.execute("UPDATE Orders SET Orders_Status='Waiting' WHERE CopyID=%s",CopyID)
                connection.commit()
            else:
                NewCopyID = cursor.fetchone()[0] #Need to find the soonest
                cursor.execute("UPDATE Copies SET Copy_Status='Borrowed' WHERE CopyID=%s",CopyID) #Freeing the old copy
                connection.commit()
                cursor.execute("UPDATE Orders SET CopyID=%s WHERE CopyID=%s", (NewCopyID,CopyID)) #Changing the order to the new copy
                connection.commit()
                cursor.execute("UPDATE Orders SET Orders_Status='Active' WHERE CopyID=%s", NewCopyID) #Activating the new order
                connection.commit()
                cursor.execute("UPDATE Copies SET Copy_Status='Ordered' WHERE CopyID=%s",NewCopyID) #Changing the copy status to order for the new copy
                connection.commit()
            #Check if maybe another copy is available now to order
        else:
            #Book is held for more than 3 days
            if (Real_Return_Date+timedelta(days=3)<datetime.date(datetime.today())) : #3 days have past
                cursor.execute("UPDATE Orders SET Orders_Status='expired' WHERE CopyID=%s",CopyID)
                connection.commit()
                cursor.execute("UPDATE Copies SET Copy_Status='Available' WHERE CopyID=%s",CopyID) #canceling the order in copies
            else: #Order is active
                cursor.execute("UPDATE Orders SET Orders_Status='active' WHERE CopyID=%s",CopyID)
                connection.commit()



@app.route('/', methods=['POST', 'GET'])
# Defining the view function to homepage route:
def view_func():
    if request.method == 'POST': #Runs if the librarian return a book
        CopyID=request.form["Submit"]
        cursor.execute("SELECT Copy_Status FROM Copies WHERE CopyID=%s",CopyID)
        Copy_Status=cursor.fetchone()[0]
        #Adding back to stock if not ordered
        if Copy_Status=='Borrowed':
            cursor.execute("UPDATE Copies SET Copy_Status='Available' WHERE CopyID=%s", CopyID)
            connection.commit()
        #Updating the date of the return
        cursor.execute("UPDATE Borrows SET Real_Return_Date=%s WHERE CopyID=%s", (datetime.today(),CopyID))
        connection.commit()
        UpdateOrderStatus() #Update the order status
        return redirect("/")
    else:
        try:
            if session["librarian"] is not None: #Librarian homepage
                j = cursor.execute('''SELECT BookID,BookName,AuthorName,Year_of_publication,Publsher,COUNT(*) AS Amount_In_Stock
                                      FROM Copies NATURAL JOIN books 
                                      WHERE Copy_Status='Available' AND Branch_Address=%s 
                                      GROUP BY BookID ORDER BY BookID ASC ''',session["librarian"][1])
                stock_in_branch = cursor.fetchall()
                k = cursor.execute('''SELECT * FROM Borrows JOIN Copies ON Borrows.CopyID=Copies.CopyID NATURAL JOIN Books
                                      WHERE Branch_Address=%s AND Copy_Status='Borrowed' OR Copy_Status='Ordered' AND Borrows.Real_Return_Date is %s
                                      ORDER BY Return_Date ASC''',(session["librarian"][1], None))
                borrows_in_branch = cursor.fetchall()
                cursor.execute("SELECT * FROM Books")  # Showing the user our collection
                books = cursor.fetchall()
                if j == 0 and k!=0: #No books in stock
                    return render_template('homepage.html', finished="No books in stock",borrows_in_branch=borrows_in_branch,books=books)
                elif k == 0 and j!=0:#No active borrows
                    return render_template('homepage.html', noborrows="No books being borrowed",my_collection=stock_in_branch,books=books)
                return render_template('homepage.html', my_collection=stock_in_branch,borrows_in_branch=borrows_in_branch,books=books)

            if session["user"] is not None: #User homepage
                cursor.execute("SELECT * FROM Branches") #Showing our branches
                branches = cursor.fetchall()
                cursor.execute("SELECT * FROM Books")  # Showing the user our collection
                books = cursor.fetchall()
                is_late=cursor.execute("SELECT * FROM Borrows WHERE UserMail=%s AND Return_Date<%s AND Real_Return_Date is %s",(session["user"],datetime.today(),None))
                if is_late!=0:
                    return render_template('homepage.html',late="you are late to return a borrow! please check your borrows",branches=branches,books=books)
                return render_template('homepage.html',branches=branches,books=books)
            else: #User that is not logged in
                cursor.execute("SELECT * FROM Branches")
                branches = cursor.fetchall()
                cursor.execute("SELECT * FROM Books")  # Showing the user our collection
                books = cursor.fetchall()
                return render_template('homepage.html', branches=branches,books=books)

        except KeyError: #User that is not logged in
            cursor.execute("SELECT * FROM Branches")
            branches=cursor.fetchall()
            cursor.execute("SELECT * FROM Books")  # Showing the user our collection
            books = cursor.fetchall()
            return render_template('homepage.html',branches=branches,books=books)


@app.route('/LoginPage', methods=['POST', 'GET'])
def LoginPage(): #Login page
    if request.method == 'POST':
        # Retrieving the information from the form:
        mail = str(request.form["mail"])
        password = str(request.form["password"])
        #Validating inputs
        type_of_user=ValidateLogin(mail,password)
        if type_of_user=="User dosent exist" or type_of_user=="Wrong password":
            return render_template('LoginPage.html',type_of_user=type_of_user)
        #Sessions
        if type_of_user=="user":
            session["user"]=mail
        elif type_of_user=="librarian":
            cursor.execute("SELECT Branch_Address FROM librarian WHERE Librarian_Email=%s", mail)
            LibrarianBranch = cursor.fetchone()[0]
            session["librarian"] = (mail,LibrarianBranch)
        UpdateOrderStatus() #Updating all orders status
        return redirect("/")
    else: #Before submission
        return render_template('LoginPage.html')


@app.route('/logout') #Logout
def logout():
    session["user"]=None
    session["librarian"] = None
    return redirect("/")


@app.route('/SignUp_User', methods=['POST', 'GET']) #Signup page for users
def SignUp_User():
    if request.method == 'POST':
        # Retrieving the information from the form:
        UserMail = str(request.form["UserMail"])
        UserPassword = str(request.form["UserPassword"])
        UserFirstName = str(request.form["UserFirstName"])
        UserSurname = str(request.form["UserSurname"])
        UserBirthDate = request.form["UserBirthDate"]
        UserPhone = request.form["UserPhone"]
        UserCity = str(request.form["UserCity"])
        UserStreet = str(request.form["UserStreet"])
        UserApartment = str(request.form["UserApartment"])
        user=oop.User(mail=UserMail,password=UserPassword,firstname=UserFirstName,surname=UserSurname,birth_date=UserBirthDate,phone=UserPhone,city=UserCity,street=UserStreet,apartment=UserApartment)
        # Validating
        validate=user.ValidateUserSignUp()
        is_registered = cursor.execute("SELECT UserMail FROM users WHERE UserMail=%s ", user.mail) #Making sure the mail is unregistered
        if is_registered == 1:
            return render_template('SignUp_User.html',validation="Mail already registered")
        if validate!="Valid":
            return render_template('SignUp_User.html',validation=validate)
        else:
        # Insert into DB
            cursor.execute("INSERT INTO users VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                           ,[user.mail,user.firstname,user.surname,user.city,user.street,user.apartment,user.phone,user.birth_date,user.password])
            connection.commit()
        # Redirecting to login
        return redirect('/LoginPage')
    else: #Before submission
        return render_template('SignUp_User.html')


@app.route('/SignUp_Librarian', methods=['POST', 'GET'])
def SignUp_Librarian():
    if request.method == 'POST':
        # Retrieving the information from the form:
        LibrarianMail = str(request.form["LibrarianMail"])
        LibrarianPassword = str(request.form["LibrarianPassword"])
        LibrarianFirstName = str(request.form["LibrarianFirstName"])
        LibrarianSurname = str(request.form["LibrarianSurname"])
        LibrarianPhone = request.form["LibrarianPhone"]
        LibrarianStartWorkDate = request.form["LibrarianStartWorkDate"]
        LibrarianCity = str(request.form["LibrarianCity"])
        LibrarianStreet = str(request.form["LibrarianStreet"])
        LibrarianApartment = str(request.form["LibrarianApartment"])
        LibrarianBranch = str(request.form["LibrarianBranch"]).replace('_',' ')
        librarian=oop.Librarian(mail=LibrarianMail,password=LibrarianPassword,firstname=LibrarianFirstName,surname=LibrarianSurname,phone=LibrarianPhone,city=LibrarianCity,street=LibrarianStreet,apartment=LibrarianApartment,work_start_date=LibrarianStartWorkDate,branch=LibrarianBranch)
        # Validating
        validate=librarian.ValidateLibrarianSignUp()
        is_registered = cursor.execute("SELECT Librarian_Email FROM librarian WHERE Librarian_Email=%s ",
                                       librarian.mail) #Making sure mail is unregistered
        if is_registered == 1:
            return "Mail already registered"
        # Insert into DB
        if validate!="Valid":
            return render_template('SignUp_Librarian.html',validation=validate)
        else:
            cursor.execute("INSERT INTO librarian VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                       [librarian.mail, librarian.password, librarian.branch,librarian.work_start_date,librarian.phone,librarian.city,librarian.street,librarian.apartment,librarian.firstname,librarian.surname])
            connection.commit()
        # Redirecting to login
        return redirect('/LoginPage')
    else: #Before submission
        cursor.execute("SELECT Branch_Address FROM Branches") #Fetching branches for selection in form
        branches=cursor.fetchall()
        branch_lst=[]
        for branch in branches: #For jinja2 syntax, needed to change spaces to chars
            branch=branch[0].replace(' ','_')
            branch_lst.append(branch)
        return render_template('SignUp_Librarian.html', my_collection=branch_lst)


@app.route('/BookId', methods=['POST', 'GET'])
def BookId():
    #When a librarian adds new book, this is the page he will see, with a form that contains book id only.
    #This page will redirect him for old or new book
    if request.method == 'POST':
        BookID = request.form["BookID"]
        if BookID=="":
            return render_template('BookId.html',validation="Please enter book id")
        session["BookID"]=BookID
        book_status = is_book_exist(BookID)  # Check if the book appear in books table
        if book_status == "old":
            return render_template('AddBook.html')
        else: #Before submittion
            return render_template('AddNewBook.html')

    else:#Before submission
        return render_template('BookId.html')


@app.route("/AddBook", methods=['POST', 'GET'])
def AddBook(): #If the book appears in our database we'll create new copies
    if request.method == 'POST':
        # Retrieving the information from the form:
        BookID =session["BookID"]
        book_status=is_book_exist(BookID) #Validate if the book appear in books table
        BookQuantity = request.form["BookQuantity"]
        # Making sure the input is valid for quantity
        if BookQuantity=="":
            return render_template("AddBook.html",validation="Please enter quantity")
        try:
            if int(BookQuantity)<0:
                return render_template("AddBook.html", validation="invalid quantity")
        except ValueError:
            return render_template("AddBook.html", validation="invalid quantity")
        BranchAddress = session["librarian"][1]
        if book_status== "old":
            #Add to Copies table the new amount of copies
            for i in range(0,int(BookQuantity)):
                cursor.execute("INSERT INTO Copies VALUES(%s,%s,%s,%s)" ,
                            ['Available',None,BranchAddress, BookID])
                connection.commit()
            return redirect('/')
        else: #In case the book wasn't in Books table we'll add it in another page
            return render_template('AddNewBook.html')
    else: #Before submission
        return render_template('AddBook.html')


@app.route('/AddNewBook', methods=['POST', 'GET'])
def AddNewBook(): #In case the book wasn't in our data base
    if request.method == 'POST':
        #Retrieving the information from the form
        BookID = session["BookID"]
        BookName=str(request.form["BookName"])
        BookAuthorName=str(request.form["BookAuthorName"])
        Year_of_Publication= request.form["BookPublishYear"]
        Publsher= str(request.form["BookPublisher"])
        BookImage=str(request.form["BookImage"])
        book=oop.Book(book_id=BookID,book_name=BookName,writer_name=BookAuthorName,publisher=Publsher,publish_year=Year_of_Publication)
        #Validating
        validate=book.ValidateNewBook()
        BookQuantity = request.form["BookQuantity"]
        #Validating book quantity
        if BookQuantity == "":
            return render_template("AddNewBook.html", validation="Please enter quantity")
        try:
            if int(BookQuantity)<0:
                return render_template("AddNewBook.html", validation="invalid quantity")
        except ValueError:
            return render_template("AddNewBook.html", validation="invalid quantity")
        if validate!="Valid":
            return render_template("AddNewBook.html",validation=validate)
        cursor.execute("INSERT INTO Books VALUES(%s,%s,%s,%s,%s,%s)",
                       [BookID,BookName, BookAuthorName,Year_of_Publication,Publsher,BookImage])
        connection.commit()
        #Add the new copies to Copies table
        BranchAddress = session["librarian"][1]
        for i in range(0, int(BookQuantity)):
            cursor.execute("INSERT INTO Copies VALUES(%s,%s,%s,%s)",
                            ['Available', None, BranchAddress, BookID])
            connection.commit()
        return redirect('/')

    else:#Befeore submission
        return render_template('AddNewBook.html')


@app.route('/BorrowBook', methods=['POST', 'GET'])
def BorrowBook(): #This is the page for the librarian to submit a borrow
    if request.method == 'POST':
        UpdateOrderStatus() #Update the order status
        # Retrieving the information from the form:
        UserMail = str(request.form["UserMail"])
        BookID = str(request.form["BookID"])
        BorrowDate = datetime.today()
        Duration = int(request.form["Duration"])
        ReturnDate=BorrowDate+timedelta(days=Duration)
        ReturnDate=str(ReturnDate)
        # Validating
        validate = ValidateBorrowRequest(UserMail,BorrowDate,BookID)
        if validate[0] != "Valid":
            return render_template('BorrowBook.html', validation=validate)
        else:
        #Using the copy id
            CopyID=validate[1]
        # Insert into DB
            is_ordered=cursor.execute("SELECT * FROM Copies WHERE CopyID=%s AND Copy_Status='Ordered'",CopyID)
            if is_ordered==1: #Borrowing an ordered book - the one the user ordered
                cursor.execute("UPDATE Orders SET Orders_Status='taken by user' WHERE CopyID=%s",CopyID)
                connection.commit()
            cursor.execute("INSERT INTO Borrows VALUES(%s,%s,%s,%s,%s,%s)",
                        [ReturnDate,None, BorrowDate,None,UserMail,CopyID])
            connection.commit()
        #Update stock
            cursor.execute("UPDATE Copies SET Copy_Status='Borrowed' WHERE CopyID=%s", CopyID)
            connection.commit()
        #Show book in stock
        j=cursor.execute(
            '''SELECT BookID,BookName,AuthorName,Year_of_publication,Publsher,COUNT(*) AS Amount_In_Stock 
               FROM Copies NATURAL JOIN books WHERE Copy_Status='Available' AND Branch_Address=%s 
               GROUP BY BookID ORDER BY BookID ASC ''',session["librarian"][1])
        if j==0: #No more books in stock
            return render_template('BorrowBook.html', validation="Borrow accepted, no more books in stock")
        return render_template('BorrowBook.html', my_collection=cursor.fetchall())

    else:#Before submission
        return render_template('BorrowBook.html')


@app.route('/UserBorrowHistory', methods=['POST', 'GET'])
def UserBorrowHistory():
    #This page is for the user to see his past and present borrows
    #Also, in this page the user can submit a request for extension request
    if request.method == 'POST': #After submitting request
        #Retriving data from form:
        CopyID=request.form["Submit"].split(':')[0]
        BorrowDate=request.form["Submit"].split(':')[1]
        validate=ExtensionCheck(CopyID,BorrowDate) #Validate the request
        if validate=="Valid":
            #Set extension request to todays date
            cursor.execute('''UPDATE borrows SET Extension_Request=%s 
                              WHERE UserMail=%s AND CopyID=%s AND BorrowDATE=%s'''
                              ,(datetime.today(),session["user"],CopyID,BorrowDate))
            connection.commit()
            #Update return date
            UpdatedDate=UpdateReturnDate(session["user"], CopyID, BorrowDate)
            cursor.execute('''UPDATE borrows SET Return_Date=%s 
                              WHERE UserMail=%s AND CopyID=%s AND BorrowDATE=%s'''
                              ,(UpdatedDate,session["user"],CopyID,BorrowDate))
            connection.commit()
        #Showing the user his/hers current borrow status
        cursor.execute('''SELECT * FROM borrows NATURAL JOIN Copies NATURAL JOIN Books NATURAL JOIN Branches 
                          WHERE UserMail=%s AND  Real_Return_Date is %s 
                          ORDER BY Return_Date ASC''',(session["user"],None))
        active = cursor.fetchall()
        cursor.execute('''SELECT * FROM borrows NATURAL JOIN Copies NATURAL JOIN books NATURAL JOIN Branches 
                          WHERE UserMail=%s AND  Real_Return_Date is not %s 
                          ORDER BY Real_Return_Date ASC''',(session["user"],None))
        #Showing the user his/hers past borrows
        history = cursor.fetchall()
        if validate!="Valid":
            return render_template('UserBorrowHistory.html', history=history, active=active, pop_up=validate)
        return render_template('UserBorrowHistory.html',history=history,active=active,pop_up="Request accepted")
    else: #Before submission of an extension request
        a=cursor.execute('''SELECT * FROM borrows NATURAL JOIN Copies NATURAL JOIN Books NATURAL JOIN Branches
                            WHERE UserMail=%s AND  Real_Return_Date is %s 
                            ORDER BY Return_Date ASC''',(session["user"],None))
        # Showing the user his/hers current borrow status
        active=cursor.fetchall()
        h=cursor.execute('''SELECT * FROM borrows NATURAL JOIN Copies NATURAL JOIN books NATURAL JOIN Branches
                            WHERE UserMail=%s AND  Real_Return_Date is not %s 
                            ORDER BY Real_Return_Date ASC''',(session["user"],None))
        # Showing the user his/hers past borrows
        history=cursor.fetchall()
        if a==0 and h!=0:#No active borrows
            return render_template('UserBorrowHistory.html', noborrows="No active borrows", history=history)
        if a!=0 and h==0:#No history borrows
            return render_template('UserBorrowHistory.html', nohistory="No past borrows", active=active)
        if a == 0 and h == 0: #No active borrows and no history of borrows
            return render_template('UserBorrowHistory.html', noborrows="No active borrows", nohistory="No past borrows")
        return render_template('UserBorrowHistory.html',active=active,history=history)


@app.route('/UserSearchBook', methods=['POST', 'GET'])
def UserSearchBook(): #This page is for the user to search for a book in our branches
    UpdateOrderStatus()  # Update the order status
    if request.method == 'POST':
        # Retrieving the information from the form:
        BookName=request.form["BookName"]
        AuthorName=request.form["AuthorName"]
        if AuthorName=="": #Search by book name only
            num_of_results = cursor.execute(
                '''SELECT *,COUNT(*) AS num_in_stock FROM Books NATURAL JOIN Copies NATURAL JOIN Branches 
                   WHERE BookName=%s AND Copy_Status<>'Ordered' 
                   GROUP BY BookID,Branch_Address ORDER BY Branch_Address,BookName ''',BookName)
        elif BookName=="": #Search by author name only
            num_of_results = cursor.execute(
                '''SELECT *,COUNT(*) AS num_in_stock FROM Books NATURAL JOIN Copies NATURAL JOIN Branches
                   WHERE AuthorName=%s AND Copy_Status<>'Ordered' 
                   GROUP BY BookID,Branch_Address ORDER BY Branch_Address,BookName''',AuthorName)
        else: #Search by both
            num_of_results=cursor.execute('''SELECT *,COUNT(*) AS num_in_stock 
                                             FROM Books  NATURAL JOIN Copies NATURAL JOIN Branches
                                             WHERE BookName=%s AND AuthorName=%s AND Copy_Status<>'Ordered' 
                                             GROUP BY BookID,Branch_Address 
                                             ORDER BY Branch_Address,BookName''',(BookName,AuthorName))
        if num_of_results==0: #No results
            return render_template('UserSearchBook.html', validation="didnt find this book")
        result=cursor.fetchall()
        return render_template('UserSearchBook.html',my_collection=result)

    else: #Before submission
        return render_template('UserSearchBook.html')


@app.route('/UserOrderBook', methods=['POST', 'GET'])
def UserOrderBook(): #This page is for the user to order a book
    UpdateOrderStatus()  # Update the order status
    if request.method == 'POST':
        # Retrieving the information from the form:
        BookName=request.form["BookName"]
        AuthorName=request.form["AuthorName"]
        BranchAddress=request.form["BranchAddress"].replace('_',' ')
        # Validating
        validation = ValidateOrder(BookName, AuthorName, BranchAddress)
        # Insert into DB
        if validation[0] == "Valid":
            cursor.execute("INSERT INTO Orders VALUES(%s,%s,%s,%s)",('Waiting',datetime.today(),session["user"],validation[1]))
            connection.commit()
            cursor.execute("UPDATE Copies SET Copy_Status='Ordered' WHERE CopyID=%s",validation[1])
            connection.commit()
            return render_template('UserOrderBook.html',validation="Order accepted, you can watch your orders status throught your homepage")
        else:
            return render_template('UserOrderBook.html', validation=validation)
    else: #Before submission
        cursor.execute("SELECT * FROM Books") #Showing the user our collection
        books=cursor.fetchall()
        cursor.execute("SELECT Branch_Address FROM Branches")  # Fetching branches for form
        branches = cursor.fetchall()
        branch_lst = []
        for branch in branches: #For jinja2 syntax, needed to change spaces to chars
            branch = branch[0].replace(' ', '_')
            branch_lst.append(branch)
        return render_template('UserOrderBook.html', my_collection=branch_lst,books=books)


@app.route('/UserOrderHistory', methods=['POST', 'GET'])
def UserOrderHistory(): #In this page the user can watch his past and current orders
    UpdateOrderStatus()
    if request.method == 'POST':
        redirect('/')
    else:
        UpdateOrderStatus() #Update orders status
        #Filtering active orders
        a=cursor.execute('''SELECT *,MAX(Return_Date),MAX(Real_Return_Date)
                            FROM Orders NATURAL JOIN Copies JOIN Borrows ON Orders.CopyID=Borrows.CopyID NATURAL JOIN Books
                            WHERE Orders.UserMail=%s AND (Orders_Status='Active' OR Orders_Status='waiting') 
                            GROUP BY (Copies.CopyID)ORDER BY Orders_Status ASC''',session["user"])
        active=cursor.fetchall()
        #Filtering past orders
        h=cursor.execute('''SELECT * 
                            FROM Orders NATURAL JOIN Copies JOIN Borrows ON Orders.CopyID=Borrows.CopyID NATURAL JOIN Books
                            WHERE Orders.UserMail=%s AND (Orders_Status='expired' OR Orders_Status='taken by user') AND Real_Return_Date is not %s 
                            ORDER BY Real_Return_Date ASC''',(session["user"],None))
        history = cursor.fetchall()
        if a == 0 and h != 0:  # No active borrows
            return render_template('UserOrderHistory.html', noorders="No active orders", history=history)
        if a != 0 and h == 0:  # No history borrows
            return render_template('UserOrderHistory.html', noordershistory="No past orders", active=active)
        if a == 0 and h == 0:  # No active borrows and no history of borrows
            return render_template('UserOrderHistory.html', noorders="No active orders", noordershistory="No past orderss")
        return render_template('UserOrderHistory.html',active=active,history=history)


@app.route('/assumptions', methods=['POST', 'GET']) #Assumptions page - for the tester
def assumptions():
    return render_template('assumptions.html')


# Running the script
if __name__ == "__main__":
    app.run()
    cursor.close()
    connection.close()