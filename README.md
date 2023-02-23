This is a library website - for a library named "Book King"
It was developed as a project for acedemic puprose.
We used FLASK enviroment with python, managed a database via MySQL, while desiging the pages with HTML and CSS.
Also, the database was built after using an ERD which is added to the main branch 

In order to user the website, you need to follow these few steps:
  - Download the project file from the main branch
  - Open Sql file and run it
  - Open main file and run it, than click the link.
  
What can you do in the website?
  - Search for a book in the database
  - Register as a user or a librarian
  - Log in as a user or a librarian
  - Users can:
    - Order a book
    - Watch their past and present borrows
    - Ask for a borrow extansion
    - Watch their past and present orders
   - Librarians can:
    - Add books to their branch
    - Loan books to users
    - Return books from customers
    


Our library was constructed allowing flexability about orders and borrow return. We took some assumptions in order to allow us to build our project as mentioned in this page and in our homepage:

  - Only a logged in librarian can register a new librarian account, this is because we want to make sure our clients information is safe
  - We used copy based approch for our library, according to our knowladge of how libraries work in real life
  - When a librarian submit a loan (borrow), he can see the book and it's book ID and fills the form according to it, this is for our comfort and common sense of a library
  - A client is not allowed to borrow the same book from the same branch in one day, this is to allow normalized databases with a key of (date,bookid,user mail), and according to common sense of a library
  - There are no 2 books(not copies) that have the same name and author in the same branch, this is because we want to allow clients to search and filter without being exposed to the book ID

Clarifications about orders

  - When a client orders a book, it is borrowed in the same time of the order
  - If there are more then one copies of the ordered book in the branch, the library will save the copy that has the closest estimated return date
  - If a copy that is not saved returns prior to its estimated return date, this copy will be now saved for the ordering client (automated)
  - From the day that an ordered book is available, it is saved for the user for 3 days (including), this is shown to the client as 'Active' order
  - If 3 days passed from the date of availability, the order is now shown to the client as 'expired' in his order history
  - If the ordering user borrows his ordered book, the order will be shown to the client as 'taken by user', and he can now monitor it in his borrows
  - If there is an ordered copy of a certin book, and a librarian adds new copies of this book for the branch, the order will remain in the same status and wont change to the available copy
