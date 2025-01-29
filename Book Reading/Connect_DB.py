# Import required libraries
import pandas as pd
import sqlite3


class DB_Connect():
  
  # Setting up the database connection
  def __init__(self):
    self.conn = sqlite3.connect("book_users.db")
    self.cursor = self.conn.cursor()

    self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_data (
                          fullname TEXT NOT NULL,
                          email TEXT NOT NULL,
                          username TEXT NOT NULL,
                          password TEXT NOT NULL
                          )''')

# Database Operations
  
  def create_user(self, fname, mail, uname, passwd):
    self.cursor.execute("INSERT INTO user_data (fullname, email, username, password) VALUES (?,?,?,?) ",(fname,mail,uname,passwd))
    print("DB : User created")

## Book recored table for user
    table_name = fname.strip().replace(" ","").lower()
    query = "CREATE TABLE IF NOT EXISTS " + table_name + " (book_name TEXT NOT NULL, book_author TEXT NOT NULL, genre TEXT NOT NULL, reading_time TEXT, book_pages INTEGER NOT NULL, book_review TEXT, rating REAL, book_status TEXT, start_date TEXT, end_date TEXT)"
    
    self.cursor.execute(query)

    print("DB : Table created ", table_name)

    self.conn.commit()

## Display Particular user book data
  def show_book_data(self, tablename):
    query = "SELECT * FROM " + tablename
    self.cursor.execute(query)
    result = self.cursor.fetchall()
    return result
  
## Display all Users in the Database
  def show_users_data(self):
    self.cursor.execute("SELECT * FROM user_data")
    result = self.cursor.fetchall()
    return result

## Find User
  def findUser(self,user,passwd):
        
        self.cursor.execute("SELECT * FROM user_data WHERE username=? AND password=?", (user, passwd))
        result = self.cursor.fetchone()
        print("DB : ",result)
        return result
  
## Find User Book Data
  def findUserBook(self,tablename):
        query = "SELECT book_name FROM " + tablename
        try:
           self.cursor.execute(query)
           result = self.cursor.fetchall()
           print("DB : ",result)
           return result
        
        except Exception as e:
           print(e)


## Adding New Book to the Particular Users Table
  def save_new_book(self, tablename, bookname, bookauthor,genre,bpages,readtime,s_date, status):
    
    query = "INSERT INTO " + tablename + "(book_name, book_author, genre, book_pages,reading_time,start_date,book_status) values (?,?,?,?,?,?,?)"

    try:
      self.cursor.execute(query, (bookname, bookauthor, genre, bpages,readtime,s_date,status))
      print("DB : new book added")

      query = "SELECT * FROM " + tablename
      self.cursor.execute(query)
      self.conn.commit()
      res = self.cursor.fetchall()
      print(res)

    except Exception as e:
      print(e)


## Update Book Time
  def update_book_time(self,tablename, bookname, newtime, status):
    query = "UPDATE " + tablename + " SET reading_time = ?, book_status = ? WHERE book_name = ?"
    try : 
      self.cursor.execute(query, (newtime, status, bookname ))
      self.conn.commit()
      print("DB : time updated")

      query = "SELECT * FROM " + tablename
      self.cursor.execute(query)
      res = self.cursor.fetchall()
      print(res)
    
    except Exception as e:
      print(e)

## Update Book Time Rating Review
  def update_book_trr(self,tablename, bookname, newtime, rating, review, status,edate):
    query = "UPDATE " + tablename + " SET reading_time = ?, book_review = ?, rating = ?, book_status = ? , end_date = ? WHERE book_name = ?"
    try : 
      self.cursor.execute(query, (newtime,review, rating, status,edate,bookname ))
      self.conn.commit()
      print("DB : time updated")

      query = "SELECT * FROM " + tablename
      self.cursor.execute(query)
      res = self.cursor.fetchall()
      print(res)
    
    except Exception as e:
      print(e)

## Add Completed Old Book Data
  def add_com_old_book(self, tablename, bookname, author, genre, pages, newtime, stime, etime, rating, review, status):
    # book_name book_author genre reading_time book_pages book_review rating book_status start_date end_date     
    
    
    query = "INSERT INTO " + tablename + " (book_name, book_author, genre, reading_time, book_pages, book_review, rating, book_status, start_date, end_date) VALUES (?,?,?,?,?,?,?,?,?,?)"
    try : 
      self.cursor.execute(query,(bookname, author,genre,newtime,pages,review,rating,status,stime,etime))
      self.conn.commit()
      print("DB : time updated")

      query = "SELECT * FROM " + tablename
      self.cursor.execute(query)
      res = self.cursor.fetchall()
      print(res)
    
    except Exception as e:
      print(e)

## Add Incomplete Old Book Data
  def add_incom_old_book(self, tablename, bookname, author, genre, pages, newtime, stime,status):
           
    query = "INSERT INTO " + tablename + " (book_name, book_author, genre, reading_time, book_pages, book_status, start_date) VALUES (?,?,?,?,?,?,?)"
    try : 
      self.cursor.execute(query,(bookname, author,genre,newtime,pages,status,stime))
      self.conn.commit()
      print("DB : time updated")

      query = "SELECT * FROM " + tablename
      self.cursor.execute(query)
      res = self.cursor.fetchall()
      print(res)
    
    except Exception as e:
      print(e)

## Show All Book Data
  def show_all_data(self,tablename):

    try :
      query = "SELECT * FROM " + tablename
      return pd.read_sql(query, self.conn)
      
    except Exception as e:
      print(e)


## Delete Book From Table
  def del_book(self,tablename,bname):
    query = f"DELETE FROM {tablename} WHERE book_name = '{bname}'" 
    try:
      self.cursor.execute(query)
      self.conn.commit()
      print(f"DB : {bname} book deleted successfully")
      
    except Exception as e:
      print(e)

## Delete Table From Database
  def delete_table(self, tablename):
    query = "DROP TABLE IF EXISTS " + tablename.strip().replace(" ","").lower()
    try:
      self.cursor.execute(query)
      print(f"DB : {tablename} table deleted successfully")
      
    except Exception as e:
      print(e)
  



    
