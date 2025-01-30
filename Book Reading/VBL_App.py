# Import all required libraries
import customtkinter as ct
import tkinter as tk
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry
from CTkDatePicker.CTkDatePicker import ctk_date_picker
import pandas as pd
from pandastable import Table
import cv2
from PIL import Image,ImageTk
from datetime import datetime
import Connect_DB as db
import time
import pygame
import textwrap
import os
## Setting the Database Connection

ab = db.DB_Connect()
pygame.mixer.init()

# Setting the app appearance and theme
ct.set_appearance_mode("dark")
ct.set_default_color_theme("blue")



class App(ct.CTk):
    def __init__(self):
        super().__init__() 
       
        self.title("VBL")
        self.geometry("1400x850")

        # Main frame for the app
        self.main_frame = ct.CTkScrollableFrame(self)
        self.main_frame.pack(fill='both', expand=True)

        # Title Frame
        self.titlelabelframe = ct.CTkFrame(self.main_frame, width=600, height=100, fg_color="transparent")
        self.titlelabelframe.grid(row=0, column=0, columnspan=10,pady=20, padx=20)  

        self.apptitlelabel = ct.CTkLabel(self.titlelabelframe, text="Virtual Book Library", fg_color="transparent",
                                      text_color="white", font=("arial black", 38))
        self.apptitlelabel.pack()  

        ########
        self.current_user_name = None
        self.current_table = None
        self.current_book_name = None
        self.current_book_time = None
        self.is_newBook = False
        self.is_existingBook = False
        self.is_completed = False
        ########
        
        # Front image frame (on the left side)
        self.frontimgframe = ct.CTkFrame(self.main_frame, width=1200 // 2, height=700, fg_color="transparent")
        self.frontimgframe.grid(row=2, column=0, pady=20, padx=20, sticky="nsew")  

        # Front login frame (on the right side)
        self.frontlogframe = ct.CTkFrame(self.main_frame, width=1200 // 2, height=700, fg_color="transparent")
        self.frontlogframe.grid(row=2, column=1, pady=20, padx=20, sticky="nsew")

        # Front register frame (on the right side)
        self.frontregframe = ct.CTkFrame(self.main_frame, width=1200 // 2, height=700, fg_color="transparent")
        # self.frontregframe.grid(row=1, column=2, pady=20, padx=20, sticky="nsew")

        
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)


        # Image configuration on left side
        self.frontimglabel = ct.CTkLabel(self.frontimgframe,text="")
        self.frontimglabel.pack(padx=20, pady=10)

        image = Image.open("img/book1.jpg")

        ctk_image = ct.CTkImage(light_image=image, size=(575,575))
        
        self.frontimglabel.configure(image=ctk_image)
        self.frontimglabel.image = ctk_image

        
        # Login field configuration on right side
        self.titlelabel = ct.CTkLabel(self.frontlogframe, text="Login User", fg_color="transparent",
                                      text_color="white", font=("arial black", 32))
        self.titlelabel.grid(row=0,column=3,padx=20, pady=20)
               
        self.fronttextlabel1 = ct.CTkLabel(self.frontlogframe,text="User ID    : ", fg_color="transparent",
                                      text_color="white", font=("Palatino Linotype", 20))
        self.fronttextlabel1.grid(row=1,column=2,padx=20, pady=20, sticky="w")

        self.frontentrylabel1 = ct.CTkEntry(self.frontlogframe,placeholder_text="Enter Your User ID",justify="center",width=350,height=50,bg_color="transparent",fg_color="transparent",font=("arial", 16))
        self.frontentrylabel1.grid(row=1,column=3,padx=20, pady=20)

        
        self.fronttextlabel2 = ct.CTkLabel(self.frontlogframe,text="Password    : ", fg_color="transparent",
                                      text_color="white", font=("Palatino Linotype", 20))
        self.fronttextlabel2.grid(row=2,column=2,padx=20, pady=20, sticky="w")

        self.frontentrylabel2 = ct.CTkEntry(self.frontlogframe,placeholder_text="Enter Your Password",justify="center",show="*",width=350,height=50,bg_color="transparent",fg_color="transparent",font=("arial", 16))
        self.frontentrylabel2.grid(row=2,column=3,padx=20, pady=20)
        
        
        img = Image.open("img/open_eye.png")
        self.eye_open = ct.CTkImage(light_image=img, size=(35,30))

        img = Image.open("img/closed_eye.png")
        self.eye_closed = ct.CTkImage(light_image=img, size=(35,30))

        self.eyeButton = ct.CTkButton(self.frontlogframe,image=self.eye_open,corner_radius=20, compound="left",text="",width=40,height=40, command=self.show_password)
        self.eyeButton.grid(row=2,column=4,padx=20, pady=20)
        self.password_visible = False

        img = Image.open("img/login.png")
        self.logbtnimg = ct.CTkImage(light_image=img, dark_image=img, size=(180, 40))  
        
        img = Image.open("img/register.png")
        self.regbtnimg = ct.CTkImage(light_image=img, dark_image=img, size=(180, 40))  
        

        self.login_button = ct.CTkButton(self.frontlogframe,text="", hover_color="#3d3d3d",image=self.logbtnimg,corner_radius=1000,bg_color="transparent",fg_color="transparent", width=180, height=40 ,compound="left", command=self.login)
        self.login_button.grid(row=4,column=3,padx=20, pady=20)

        self.register_button = ct.CTkButton(self.frontlogframe,text="",image=self.regbtnimg,width=180,height=40,corner_radius=1000,text_color="white",bg_color="transparent",fg_color="transparent",hover_color="#3d3d3d",font=("arial", 16), command=self.register)
        self.register_button.grid(row=5,column=3,padx=20, pady=20)


        
        # Register field configuration

        self.titlelabel = ct.CTkLabel(self.frontregframe, text="Register User", fg_color="transparent",
                                      text_color="white", font=("arial black", 32))
        self.titlelabel.grid(row=0,column=3,padx=20, pady=20)

        self.regnametextlabel = ct.CTkLabel(self.frontregframe,text="Full Name   : ", fg_color="transparent",
                                      text_color="white", font=("Palatino Linotype", 20))
        self.regnametextlabel.grid(row=1,column=2,padx=20, pady=20, sticky="w")

        self.regnameentrylabel = ct.CTkEntry(self.frontregframe,placeholder_text="Enter Your Name",justify="center",width=350,height=50,bg_color="transparent",fg_color="transparent",font=("arial", 16))
        self.regnameentrylabel.grid(row=1,column=3,padx=20, pady=20)

        self.regmailtextlabel = ct.CTkLabel(self.frontregframe,text="Email Id   : ", fg_color="transparent",
                                      text_color="white", font=("Palatino Linotype", 20))
        self.regmailtextlabel.grid(row=2,column=2,padx=20, pady=20, sticky="w")

        self.regmailentrylabel = ct.CTkEntry(self.frontregframe,placeholder_text="Enter Your Email ID",justify="center",width=350,height=50,bg_color="transparent",fg_color="transparent",font=("arial", 16))
        self.regmailentrylabel.grid(row=2,column=3,padx=20, pady=20)

        self.regusertextlabel = ct.CTkLabel(self.frontregframe,text="User Id   : ", fg_color="transparent",
                                      text_color="white", font=("Palatino Linotype", 20))
        self.regusertextlabel.grid(row=3,column=2,padx=20, pady=20, sticky="w")

        self.reguserentrylabel = ct.CTkEntry(self.frontregframe,placeholder_text="Enter Your User ID",justify="center",width=350,height=50,bg_color="transparent",fg_color="transparent",font=("arial", 16))
        self.reguserentrylabel.grid(row=3,column=3,padx=20, pady=20)
        
        self.regpasstextlabel = ct.CTkLabel(self.frontregframe,text="Password    : ", fg_color="transparent",
                                      text_color="white", font=("Palatino Linotype", 20))
        self.regpasstextlabel.grid(row=4,column=2,padx=20, pady=20, sticky="w")

        self.regpassentrylabel = ct.CTkEntry(self.frontregframe,placeholder_text="Enter Your Password",justify="center",show="*",width=350,height=50,bg_color="transparent",fg_color="transparent",font=("arial", 16))
        self.regpassentrylabel.grid(row=4,column=3,padx=20, pady=20)
        
        self.regeyeButton = ct.CTkButton(self.frontregframe,image=self.eye_open,corner_radius=20, compound="left",text="",width=40,height=40, command=self.show_password)
        self.regeyeButton.grid(row=4,column=4,padx=20, pady=20)
        

        img = Image.open("img/submit.png")
        self.subbtnimg = ct.CTkImage(light_image=img, dark_image=img, size=(180, 40))  
        
        self.regSub_button = ct.CTkButton(self.frontregframe,text="", hover_color="#3d3d3d",image=self.subbtnimg,corner_radius=1000,bg_color="transparent",fg_color="transparent", width=180, height=40 ,compound="left", command=self.newRegister)
        self.regSub_button.grid(row=6,column=3,padx=20, pady=20)
        
        

        self.reglog_button = ct.CTkButton(self.frontregframe,text="", hover_color="#3d3d3d",image=self.logbtnimg,corner_radius=1000,bg_color="transparent",fg_color="transparent", width=180, height=40 ,compound="left", command=self.backto_login)
        self.reglog_button.grid(row=7,column=3,padx=20, pady=20)


#######################################################################

    def show_password(self):
        if self.password_visible:

            self.frontentrylabel2.configure(show="*")
            self.regpassentrylabel.configure(show="*")
            self.password_visible=False
            self.eyeButton.configure(image=self.eye_open)
            self.regeyeButton.configure(image=self.eye_open)
        
        else:
            self.frontentrylabel2.configure(show="")
            self.regpassentrylabel.configure(show="")
            self.password_visible=True
            self.eyeButton.configure(image=self.eye_closed)
            self.regeyeButton.configure(image=self.eye_closed)



#######################################################################


    def login(self):
        # self.current_user_name = "jay"
        # self.current_table = "jay"
        # self.changeScreen()
        if self.frontentrylabel1.get()== '' or self.frontentrylabel2.get() == '':
            messagebox.showwarning("Input Error","Enter UserID and Password")
        
        else:

            
            try:
                result = ab.findUser(self.frontentrylabel1.get(),self.frontentrylabel2.get())

                if result is not None:

                    self.current_user_name = result[0]
                    self.current_table = self.current_user_name.strip().replace(" ","").lower()
                    messagebox.showinfo("Login Successful",f"Welcome  {result[0]}")

                    self.changeScreen()


                else:
                    messagebox.showerror("Login Error","Invalid UserId or Password")

            except Exception as e:
                print(e)



#######################################################################

    def register(self):
                
        self.frontlogframe.grid_forget()
        self.frontregframe.grid_configure(row=2, column=1, pady=20, padx=20, sticky="nsew")


    def newRegister(self):
        if self.regnameentrylabel.get()== '' or self.regmailentrylabel.get() == '' or self.reguserentrylabel.get()== '' or self.regpassentrylabel.get()== '' :
            messagebox.showwarning("Input Error","All fields are required.")
        
        else:

            try:
                ab.create_user(self.regnameentrylabel.get(),self.regmailentrylabel.get(),self.reguserentrylabel.get() ,self.regpassentrylabel.get())

                messagebox.showinfo("Successfull", f"You have successfully registered as {self.regnameentrylabel.get()}")
               
                self.regnameentrylabel.delete(0, ct.END)
                self.regmailentrylabel.delete(0, ct.END)
                self.reguserentrylabel.delete(0, ct.END)
                self.regpassentrylabel.delete(0, ct.END)

                self.backto_login()
                    

            except Exception as e:
                print(e)



#######################################################################

    def backto_login(self):
        
        self.frontregframe.grid_forget()
        self.frontimgframe.grid_configure(row=2, column=0, pady=20, padx=20, sticky="nsew")
        self.frontlogframe.grid_configure(row=2, column=1, pady=20, padx=20, sticky="nsew")


#######################################################################

    def changeScreen(self):
        self.apptitlelabel.configure(text="Dashboard")

        self.frontimgframe.grid_forget()
        self.frontlogframe.grid_forget()
        self.frontentrylabel1.delete(0, ct.END)
        self.frontentrylabel2.delete(0, ct.END)
        self.is_newBook = False
        self.is_existingBook = False
        

        messagebox.showinfo("Welcome",f"Hello, {self.current_user_name}! Welcome to the Virtual Book Library. \n\nWe hope you have a wonderful time exploring and reading. \nHappy Reading!")
        
        self.dashboardframe = ct.CTkFrame(self.main_frame, width=1200, height=700, fg_color="transparent")
        self.dashboardframe.grid(row=2, column=0, pady=20, padx=20, sticky="nsew")
        
        self.emptyframe1 = ct.CTkFrame(self.dashboardframe, width=1250, height=50, fg_color="transparent")
        self.emptyframe1.grid(row=0, column=0, columnspan=9, pady=20, padx=20, sticky="nsew")

        img = Image.open("img/logout.png")
        self.loutbtnimg = ctk_image = ct.CTkImage(light_image=img, dark_image=img, size=(120, 30))  

        self.logout_button = ct.CTkButton(self.dashboardframe,text="", hover_color="#3d3d3d",image=self.loutbtnimg,corner_radius=1000,bg_color="transparent",fg_color="transparent", width=120, height=30 ,compound="left", command=self.logout)
        self.logout_button.grid(row=0, column=10, padx=20, pady=20, sticky="ne")
        
        self.dashUser = ct.CTkLabel(self.dashboardframe,text=f"Hello {self.current_user_name}!",width=250,height=60,text_color="white",bg_color="transparent",font=("Verdana", 20,"bold"))
        self.dashUser.grid(row=0,column=0,padx=20, pady=20)
        
        self.newbook = ct.CTkButton(self.dashboardframe,text="Read New Book",width=250,height=60,corner_radius=10,text_color="white",bg_color="transparent",font=("arial", 20,"bold"), command=self.readbook)
        self.newbook.grid(row=4,column=3,padx=20, pady=20)

        self.existingbook = ct.CTkButton(self.dashboardframe,text="Read Existing Book",width=250,height=60,corner_radius=10,text_color="white",bg_color="transparent",font=("arial", 20,"bold"), command=self.read_existingBook)
        self.existingbook.grid(row=4,column=4,padx=20, pady=20)

        self.emptyframe2 = ct.CTkFrame(self.dashboardframe, width=1250, height=50, fg_color="transparent")
        self.emptyframe2.grid(row=5, column=0, columnspan=9, pady=20, padx=20, sticky="nsew")

        self.booklist = ct.CTkButton(self.dashboardframe,text="My Book Details",width=250,height=60,corner_radius=10,text_color="white",bg_color="transparent",font=("arial", 20,"bold"), command=self.show_book_list)
        self.booklist.grid(row=6,column=3,padx=20, pady=20)

        self.showanalysis = ct.CTkButton(self.dashboardframe,text="Show Analysis",width=250,height=60,corner_radius=10,text_color="white",bg_color="transparent",font=("arial", 20,"bold"), command=self.show_book_analysis)
        self.showanalysis.grid(row=6,column=4,padx=20, pady=20)
        
        self.emptyframe3 = ct.CTkFrame(self.dashboardframe, width=1250, height=50, fg_color="transparent")
        self.emptyframe3.grid(row=7, column=0, columnspan=9, pady=20, padx=20, sticky="nsew")

        self.oldbook = ct.CTkButton(self.dashboardframe,text="Add Old Book",width=250,height=60,corner_radius=10,text_color="white",bg_color="transparent",font=("arial", 20,"bold"), command=self.addoldbook)
        self.oldbook.grid(row=8,column=3, padx=20, pady=20)

        self.mybook_lib = ct.CTkButton(self.dashboardframe,text="My Book Lib",width=250,height=60,corner_radius=10,text_color="white",bg_color="transparent",font=("arial", 20,"bold"), command=self.my_library)
        self.mybook_lib.grid(row=8,column=4, padx=20, pady=20)

#######################################################################

    def logout(self):

        logout = messagebox.askyesno("Logout","Are you sure to logout?")

        if logout:
            self.apptitlelabel.configure(text="Virtual Book Library")
            self.dashboardframe.grid_forget()

            messagebox.showinfo("",f"Thank you, {self.current_user_name}, for visiting the Virtual Library! \n\nWe hope you had a great experience. Looking forward to seeing you again soon!")

            self.frontimgframe.grid_configure(row=2, column=0, pady=20, padx=20, sticky="nsew")
            self.frontlogframe.grid_configure(row=2, column=1, pady=20, padx=20, sticky="nsew")

            self.current_book_name=None
            self.current_user_name=None
            self.current_table=None
            self.is_newBook = False
            self.is_existingBook = False

            
        else:
            pass
#######################################################################

    def readbook(self):
        self.apptitlelabel.configure(text="Read New Book")

        self.dashboardframe.grid_forget()

        # Image and GIF Frame (on the left side)
        self.gifimgframe = ct.CTkFrame(self.main_frame, width=1200 // 2, height=700, fg_color="transparent")
        self.gifimgframe.grid(row=2, column=0, pady=20, padx=20, sticky="nsew")  

        # Book Details Frame (on the right side)
        self.bookdetailsframe = ct.CTkFrame(self.main_frame, width=1200 // 2, height=700, fg_color="transparent")
        self.bookdetailsframe.grid(row=2, column=1, pady=20, padx=20, sticky="nsew")

        # Book Reading Frame (on the right side)
        self.bookreadframe = ct.CTkFrame(self.main_frame, width=1200 // 2, height=700, fg_color="transparent")
        
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)


        # GIF Image configuration on left side

        image = Image.open("img/home.png")

        ctk_image = ct.CTkImage(light_image=image, size=(120,35))

        self.backtodash = ct.CTkButton(self.gifimgframe,text="", hover_color="#3d3d3d",image=ctk_image,corner_radius=1000,bg_color="transparent",fg_color="transparent", width=150, height=40 ,compound="left", command=self.backtodashboard1)
        self.backtodash.pack(padx=20, pady=10, anchor="nw")
        

        self.gifimglabel = ct.CTkLabel(self.gifimgframe,text="")
        self.gifimglabel.pack(padx=20, pady=90)

        image = Image.open("img/read0.png")

        ctk_image = ct.CTkImage(light_image=image, size=(600,400))
        
        self.gifimglabel.configure(image=ctk_image)
        self.gifimglabel.image = ctk_image

        
        # Book Details configuration on right side
        self.bdetailslabel = ct.CTkLabel(self.bookdetailsframe, text="Book Details", fg_color="transparent",
                                      text_color="white", font=("arial black", 32))
        self.bdetailslabel.grid(row=0,column=3,padx=20, pady=20)

        self.booktitletextlabel = ct.CTkLabel(self.bookdetailsframe,text="Book Title   : ", fg_color="transparent",
                                      text_color="white", font=("Palatino Linotype", 20))
        self.booktitletextlabel.grid(row=1,column=2,padx=20, pady=20, sticky="w")

        self.booktitleentrylabel = ct.CTkEntry(self.bookdetailsframe,placeholder_text="Enter Your Book Title",justify="center",width=350,height=50,bg_color="transparent",fg_color="transparent",font=("arial", 16))
        self.booktitleentrylabel.grid(row=1,column=3,padx=20, pady=20)

        self.bauthortextlabel = ct.CTkLabel(self.bookdetailsframe,text="Author Name   : ", fg_color="transparent",
                                      text_color="white", font=("Palatino Linotype", 20))
        self.bauthortextlabel.grid(row=2,column=2,padx=20, pady=20, sticky="w")

        self.bauthorentrylabel = ct.CTkEntry(self.bookdetailsframe,placeholder_text="Enter Book Author Name",justify="center",width=350,height=50,bg_color="transparent",fg_color="transparent",font=("arial", 16))
        self.bauthorentrylabel.grid(row=2,column=3,padx=20, pady=20)

        self.bookgentextlabel = ct.CTkLabel(self.bookdetailsframe,text="Book Genre   : ", fg_color="transparent",
                                      text_color="white", font=("Palatino Linotype", 20))
        self.bookgentextlabel.grid(row=3,column=2,padx=20, pady=20, sticky="w")

        book_genres = [
                    'Action Fiction', 'Adventure Fiction', 'Alternate History', 'Autobiography', 'Biography', 
                    'Contemporary Literature', 'Contemporary Romance', 'Crime Fiction', 'Detective Fiction', 'Essay',
                    'Fairy Tale', 'Fantasy', 'Fantasy Fiction', 'Fiction', 'Genre Fiction', 'Graphic Novel', 
                    'Historical Fantasy', 'Historical Fiction', 'Historical Romance', 'History',
                    'Horror Fiction', 'Humor', 'Literary Fiction', 'Magical Realism', 'Memoir', 'Mystery', 'Narrative', 
                    'New Adult Fiction', 'Non-fiction', 'Novel', 'Paranormal Romance', 'Philosophy', 'Poetry', 'Quotation', 
                    'Romance', 'Romance Novel', 'Satire', 'Science', 'Science Fantasy', 'Science Fiction',
                    'Self-help Book', 'Short Story', 'Social Science', 'Speculative Fiction', 'Spirituality', 'Thriller', 
                    'Travel Literature', 'True Crime', 'Western Fiction', "Women's Fiction", 'Young Adult Literature'
                    ]

        self.bookgenentrylabel = ct.CTkOptionMenu(self.bookdetailsframe,values=book_genres,width=350,height=50,bg_color="transparent", fg_color="#ebb434",font=("arial", 16),text_color="white")
        self.bookgenentrylabel.grid(row=3,column=3,padx=20, pady=20)

        # self.bookgenentrylabel = ct.CTkEntry(self.bookdetailsframe,placeholder_text="Enter Book Genre",justify="center",width=350,height=50,bg_color="transparent",fg_color="transparent",font=("arial", 16))
        # self.bookgenentrylabel.grid(row=3,column=3,padx=20, pady=20)

        
        self.bookpgtextlabel = ct.CTkLabel(self.bookdetailsframe,text="Number of Book Pages    : ", fg_color="transparent",
                                      text_color="white", font=("Palatino Linotype", 20))
        self.bookpgtextlabel.grid(row=4,column=2,padx=20, pady=20, sticky="w")

        self.bookpgentrylabel = ct.CTkEntry(self.bookdetailsframe,placeholder_text="eg. 465 (Note: Numbers only)",justify="center",width=350,height=50,bg_color="transparent",fg_color="transparent",font=("arial", 16))
        self.bookpgentrylabel.grid(row=4,column=3,padx=20, pady=20)

        self.bookSub_button = ct.CTkButton(self.bookdetailsframe,text="", hover_color="#3d3d3d",image=self.subbtnimg,corner_radius=1000,bg_color="transparent",fg_color="transparent", width=180, height=40 ,compound="left", command=self.valBookData)
        self.bookSub_button.grid(row=6,column=3,padx=20, pady=40)
        

        # Book Reading configuration on right side
        self.is_running = False
        self.is_existingBook = False
        self.is_newBook = True

        self.music_var = tk.BooleanVar()

        self.music_check_btn = ct.CTkCheckBox(self.bookreadframe, text="Background Music", variable=self.music_var,font=("Palatino Linotype", 20), command=self.play_music)
        self.music_check_btn.grid(row=0, column=4,padx=20, pady=10, sticky="ne")

        self.booktitleframe = ct.CTkFrame(self.bookreadframe, width=600, height=100, fg_color="transparent")
        self.booktitleframe.grid(row=1, column=0, columnspan=6, pady=20, padx=20, sticky="nsew")

        self.booktitle = ct.CTkLabel(self.booktitleframe, text="", fg_color="transparent",justify="center",
                                      text_color="white", font=("arial black", 32))
        self.booktitle.grid(row=1,column=3,padx=20, pady=20,sticky="nsew") 

        self.booktimerlabel = ct.CTkLabel(self.bookreadframe, text="00:00:00", fg_color="transparent",
                                      text_color="white", font=("Verdana ", 32,"bold"))
        self.booktimerlabel.grid(row=3,column=3,padx=20, pady=20) 

        image = Image.open("img/sandclock.gif")

        self.sandclockimg = ct.CTkImage(light_image=image, size=(100,100))
        

        self.clockimglabel = ct.CTkLabel(self.bookreadframe, text="", image=self.sandclockimg , fg_color="transparent")
        self.clockimglabel.grid(row=4,column=3,padx=20, pady=20)

        self.bookstartbtn = ct.CTkButton(self.bookreadframe,text="Start Timer",width=180,height=50,corner_radius=10,text_color="white",bg_color="transparent",font=("arial", 20,"bold"), command=self.start)
        self.bookstartbtn.grid(row=5,column=2,padx=20, pady=20)

        self.bookpausebtn = ct.CTkButton(self.bookreadframe,text="Pause",width=180,height=50,corner_radius=10,text_color="white",bg_color="transparent",font=("arial", 20,"bold"),state="disabled", command=self.pausetimer)
        self.bookpausebtn.grid(row=5,column=3,padx=20, pady=20)

        self.bookstopbtn = ct.CTkButton(self.bookreadframe,text="Stop",width=180,height=50,corner_radius=10,text_color="white",bg_color="transparent",font=("arial", 20,"bold"),state="disabled", command=self.stoptimer)
        self.bookstopbtn.grid(row=5,column=4,padx=20, pady=20)

        
        
#######################################################################
    def valBookData(self):
        if self.booktitleentrylabel.get()== '' or self.bauthorentrylabel.get() == '' or self.bookgenentrylabel.get()== '' or self.bookpgentrylabel.get()== '' :
            messagebox.showwarning("Input Error","All fields are required.")
        
        else:

            try:
                start_date = datetime.now().strftime("%d/%m/%Y")
                print("new book: "+self.current_table ,self.booktitleentrylabel.get(),self.bauthorentrylabel.get(),self.bookgenentrylabel.get() ,self.bookpgentrylabel.get(),"00:00:00",type(start_date),"New Added")
                
                ab.save_new_book(self.current_table ,self.booktitleentrylabel.get(),self.bauthorentrylabel.get(),self.bookgenentrylabel.get() ,self.bookpgentrylabel.get(),"00:00:00",start_date,"New Added")
                
                self.current_book_name = self.booktitleentrylabel.get().title()
                title = "Reading : " + self.current_book_name
                messagebox.showinfo("Successfull","Book Saved Successfully!")

                self.booktitleentrylabel.delete(0, ct.END)
                self.bauthorentrylabel.delete(0, ct.END)
                # self.bookgenentrylabel.delete(0, ct.END)
                self.bookpgentrylabel.delete(0, ct.END)

                
                self.newBook(title)
                    

            except Exception as e:
                print(e)


    def newBook(self,title):
        self.bookdetailsframe.grid_forget()
        self.bookreadframe.grid(row=2, column=1, pady=20, padx=20, sticky="nsew")
        self.booktitle.configure(text=title)
        
        print("Book Saved")

    def startread(self):

        self.gif_path_1 = "img/sandclock.gif" 
        self.gif_1 = Image.open(self.gif_path_1)
        self.current_frame_1 = 0
        self.frames_1 = self.load_gif_1(self.gif_1)

        self.gif_paths = ["img/read1.gif", "img/read2.gif"]

        self.frames_2 = []
        self.current_gif_index = 0  
        self.load_all_gifs()  
        self.current_frame_2 = 0
        self.is_paused = False
        self.elapsed_time = 0

    def play_music(self):
        if self.music_var.get():
            pygame.mixer.music.load(r"C:\Users\jaymo\Downloads\music.mp3")  
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.unload()

    def start(self):
        

        if self.is_newBook:

            self.startread()
            self.bookstartbtn.configure(state="disabled")
            self.bookpausebtn.configure(state="normal")
            self.bookstopbtn.configure(state="normal")
            self.is_running=True
            self.update_time()
            self.animate_gif_1()   
            self.animate_gif_2()   

        elif self.is_existingBook:
            self.startread()
            self.bookstartbtn1.configure(state="disabled")
            self.bookpausebtn1.configure(state="normal")
            self.bookstopbtn1.configure(state="normal")
            self.is_running=True
            self.update_time()
            self.animate_gif_1()   
            self.animate_gif_2()   
        
        else:
            pass

    def load_gif_1(self, gif):
        frames = []
        try:
            while True:
                frame = gif.copy()
                frame = frame.resize((150, 150), Image.LANCZOS)
                frames.append(ImageTk.PhotoImage(frame))
                gif.seek(len(frames))  
        except EOFError:
            pass  
        return frames 

    def load_gif_2(self, gif):
        frames = []
        try:
            while True:
                frame = gif.copy()
                frame = frame.resize((800, 550), Image.LANCZOS)
                frames.append(ImageTk.PhotoImage(frame))
                gif.seek(len(frames))  
        except EOFError:
            pass  
        return frames

    def load_all_gifs(self):
        for path in self.gif_paths:
            gif = Image.open(path)
            frames = self.load_gif_2(gif)
            self.frames_2.append(frames)
    
    def animate_gif_1(self):
        if self.is_newBook:
            if self.frames_1 and self.is_running and not self.is_paused:
                self.clockimglabel.configure(image=self.frames_1[self.current_frame_1])
                self.current_frame_1 = (self.current_frame_1 + 1) % len(self.frames_1)
                self.after(100, self.animate_gif_1)  # Set delay to 1000 milliseconds (1 second)

        elif self.is_existingBook:
            if self.frames_1 and self.is_running and not self.is_paused:
                self.clockimglabel1.configure(image=self.frames_1[self.current_frame_1])
                self.current_frame_1 = (self.current_frame_1 + 1) % len(self.frames_1)
                self.after(100, self.animate_gif_1)  # Set delay to 1000 milliseconds (1 second)

        else:
            pass


    def animate_gif_2(self):
        if self.is_newBook:

            if self.frames_2 and self.is_running and not self.is_paused:
                current_frames = self.frames_2[self.current_gif_index]
                self.gifimglabel.configure(image=current_frames[self.current_frame_2])
                self.current_frame_2 = (self.current_frame_2 + 1) % len(current_frames)

                
                if self.current_frame_2 == 0:  
                    self.current_gif_index = (self.current_gif_index + 1) % len(self.frames_2)  

                self.after(30, self.animate_gif_2) 

        elif self.is_existingBook:
            if self.frames_2 and self.is_running and not self.is_paused:
                current_frames = self.frames_2[self.current_gif_index]
                self.gifimglabel1.configure(image=current_frames[self.current_frame_2])
                self.current_frame_2 = (self.current_frame_2 + 1) % len(current_frames)

                
                if self.current_frame_2 == 0:  
                    self.current_gif_index = (self.current_gif_index + 1) % len(self.frames_2)  

                self.after(30, self.animate_gif_2) 

        else:
            pass        


    def update_time(self):
        if self.is_newBook:

            if self.is_running and not self.is_paused:
                self.elapsed_time += 1
                current_time = time.strftime("%H:%M:%S", time.gmtime(self.elapsed_time))
                self.booktimerlabel.configure(text=current_time)
                self.after(1000, self.update_time)

        elif self.is_existingBook:
            # self.elapsed_time = self.existingTime
            if self.is_running and not self.is_paused:
                self.existingTime += 1        # self.elapsed_time += 1
                current_time = time.strftime("%H:%M:%S", time.gmtime(self.existingTime))
                self.booktimerlabel1.configure(text=current_time)
                self.after(1000, self.update_time)
        
        else:
            pass

    def pausetimer(self):
        if self.is_newBook:
            if self.is_running:            
                self.is_paused = not self.is_paused  # Toggle pause state
                if self.is_paused:
                    pygame.mixer.music.pause()
                    self.bookpausebtn.configure(text="Continue")  # Change button text to Continue
                else:
                    pygame.mixer.music.unpause()
                    self.bookpausebtn.configure(text="Pause")  # Change button text to Pause
                    self.update_time()
                    self.animate_gif_1()
                    self.animate_gif_2()

        elif self.is_existingBook:
            
            if self.is_running:            
                self.is_paused = not self.is_paused  # Toggle pause state
                if self.is_paused:
                    pygame.mixer.music.pause()
                    self.bookpausebtn1.configure(text="Continue")  # Change button text to Continue
                else:
                    pygame.mixer.music.unpause()
                    self.bookpausebtn1.configure(text="Pause")  # Change button text to Pause
                    self.update_time()
                    self.animate_gif_1()
                    self.animate_gif_2()
        
        else:
            pass

    def stoptimer(self):
        pygame.mixer.music.stop()
        self.pausetimer()

        result = messagebox.askyesno("Stop Timer", "Are you sure you want to stop the timer?")
        
        if self.is_newBook:
            bookstatus = messagebox.askyesno("Book Status",f"Is {self.current_book_name} book completed ? ")

            if result and bookstatus:  
                self.bookstartbtn.configure(state="disabled")
                self.bookpausebtn.configure(state="disabled")
                self.bookstopbtn.configure(state="disabled")
                self.is_running = False 
                self.is_completed = True 

                self.ratingLabel = ct.CTkLabel(self.bookreadframe,text=f"Rate {self.current_book_name} :", fg_color="transparent",
                                      text_color="white", font=("Palatino Linotype", 20))
                self.ratingLabel.grid(row=5,column=2,padx=20, pady=20)

                self.ratingEntry = ct.CTkEntry(self.bookreadframe, placeholder_text="eg. 3.5, 4.0, 5  ",justify="center",width=180,height=50,bg_color="transparent",fg_color="transparent",font=("arial", 16))
                self.ratingEntry.grid(row=5,column=3,padx=20, pady=20)

                self.reviewLabel = ct.CTkLabel(self.bookreadframe,text=f"Write book review :", fg_color="transparent",
                                      text_color="white", font=("Palatino Linotype", 20))
                self.reviewLabel.grid(row=6,column=2,padx=20, pady=20)

                self.reviewEntry = ct.CTkTextbox(self.bookreadframe, width=600,height=400,bg_color="#3d3d3d",fg_color="transparent",font=("Palatino Linotype", 16))
                self.reviewEntry.grid(row=7,column=2, columnspan=3,padx=20, pady=20)
                
                self.timesavebtn = ct.CTkButton(self.bookreadframe,text="Save Time",width=180,height=50,corner_radius=10,text_color="white",bg_color="transparent",font=("arial", 20,"bold"), command=self.update_dbtime)
                self.timesavebtn.grid(row=8,column=3,padx=20, pady=20)

            elif result:  
                self.bookstartbtn.configure(state="disabled")
                self.bookpausebtn.configure(state="disabled")
                self.bookstopbtn.configure(state="disabled")
                self.is_running = False

                self.timesavebtn = ct.CTkButton(self.bookreadframe,text="Save Time",width=180,height=50,corner_radius=10,text_color="white",bg_color="transparent",font=("arial", 20,"bold"), command=self.update_dbtime)
                self.timesavebtn.grid(row=5,column=3,padx=20, pady=20) 

        elif self.is_existingBook:
            bookstatus = messagebox.askyesno("Book Status",f"Is {self.current_book_name} book completed ? ")
            if result and bookstatus:
                self.bookstartbtn1.configure(state="disabled")
                self.bookpausebtn1.configure(state="disabled")
                self.bookstopbtn1.configure(state="disabled")
                self.is_running = False  
                self.is_completed = True 

                self.ratingLabel1 = ct.CTkLabel(self.existingbookframe_2,text=f"Rate {self.current_book_name} :", fg_color="transparent",
                                      text_color="white", font=("Palatino Linotype", 20))
                self.ratingLabel1.grid(row=5,column=2,padx=20, pady=20)

                self.ratingEntry1 = ct.CTkEntry(self.existingbookframe_2, placeholder_text="eg. 3.5, 4.0, 5  ",justify="center",width=180,height=50,bg_color="transparent",fg_color="transparent",font=("arial", 16))
                self.ratingEntry1.grid(row=5,column=3,padx=20, pady=20)

                self.reviewLabel1 = ct.CTkLabel(self.existingbookframe_2,text=f"Write book review :", fg_color="transparent",
                                      text_color="white", font=("Palatino Linotype", 20))
                self.reviewLabel1.grid(row=6,column=2,padx=20, pady=20)

                self.reviewEntry1 = ct.CTkTextbox(self.existingbookframe_2, width=600,height=400,bg_color="#3d3d3d",fg_color="transparent",font=("Palatino Linotype", 16))
                self.reviewEntry1.grid(row=7,column=2, columnspan=3,padx=20, pady=20)

                self.timesavebtn1 = ct.CTkButton(self.existingbookframe_2,text="Save Time",width=180,height=50,corner_radius=10,text_color="white",bg_color="transparent",font=("arial", 20,"bold"), command=self.update_dbtime)
                self.timesavebtn1.grid(row=8,column=3,padx=20, pady=20)

            elif result:  
                self.bookstartbtn1.configure(state="disabled")
                self.bookpausebtn1.configure(state="disabled")
                self.bookstopbtn1.configure(state="disabled")
                self.is_running = False  
                
                self.timesavebtn1 = ct.CTkButton(self.existingbookframe_2,text="Save Time",width=180,height=50,corner_radius=10,text_color="white",bg_color="transparent",font=("arial", 20,"bold"), command=self.update_dbtime)
                self.timesavebtn1.grid(row=5,column=3,padx=20, pady=20)

            else:  
                pass

        else:
            pass

    def update_dbtime(self):
        if self.is_newBook:
                           
            print("Time updated in db ", self.booktimerlabel.cget("text"))
            btime = self.booktimerlabel.cget("text")

            if self.is_completed:
                end_date = datetime.now().strftime("%d/%m/%Y")
                print(self.current_table, self.current_book_name, btime,self.ratingEntry.get(),self.reviewEntry.get("0.0", "end-1c"),end_date)

                ab.update_book_trr(self.current_table, self.current_book_name, btime,float(self.ratingEntry.get()),self.reviewEntry.get("0.0", "end-1c"), "Completed",end_date)

                messagebox.showinfo("Successfull", "Your reading data is saved!")

            else:
                ab.update_book_time(self.current_table, self.current_book_name, btime, "In Progress")

                messagebox.showinfo("Successfull", "Your reading time is saved!")
            
            self.gifimgframe.grid_forget()
            self.bookdetailsframe.grid_forget()
            self.bookreadframe.grid_forget()
            self.apptitlelabel.configure(text="Dashboard")            
            self.dashboardframe.grid_configure(row=2, column=0, pady=20, padx=20, sticky="nsew")
            self.is_completed=False

        elif self.is_existingBook:
             
            print("Time updated in existing db ", self.booktimerlabel1.cget("text"))
            btime = self.booktimerlabel1.cget("text")
             
            if self.is_completed:
                print("before print")
                end_date = datetime.now().strftime("%d/%m/%Y")
                print(self.current_table, self.current_book_name, btime, float(self.ratingEntry1.get()),self.reviewEntry1.get("0.0", "end-1c"),end_date)
                print("afore print")
                ab.update_book_trr(self.current_table, self.current_book_name, btime, float(self.ratingEntry1.get()),self.reviewEntry1.get("0.0", "end-1c"), "Completed",end_date)
                print("after update")
                messagebox.showinfo("Successfull", "Your reading data is saved!")

            else:
                ab.update_book_time(self.current_table, self.current_book_name, btime, "In Progress")
                messagebox.showinfo("Successfull", "Your reading time is saved!")
            
            self.gifimgframe.grid_forget()
            self.existingbookframe_1.grid_forget()
            self.dropdown_frame.grid_forget()
            self.existingbookframe_2.grid_forget()
            self.booktitleframe.grid_forget()
            self.apptitlelabel.configure(text="Dashboard")
            self.dashboardframe.grid_configure(row=2, column=0, pady=20, padx=20, sticky="nsew")
            self.is_completed=False

        else:
            pass


    def read_existingBook(self):
        self.apptitlelabel.configure(text="Read Existing Book")

        self.dashboardframe.grid_forget()
        print(self.current_table, self.current_user_name)
        res = ab.findUserBook(self.current_table)

        books=[]
        for book in res:
            books.append(book[0])
        print(books)    
        self.items= books
        self.bsearchVar = ct.StringVar()

        # Image and GIF Frame (on the left side)
        self.gifimgframe = ct.CTkFrame(self.main_frame, width=1200 // 2, height=700, fg_color="transparent")
        self.gifimgframe.grid(row=2, column=0, pady=20, padx=20, sticky="nsew")  

        
        image = Image.open("img/home.png")
        ctk_image = ct.CTkImage(light_image=image, size=(120,35))
        self.backtodash = ct.CTkButton(self.gifimgframe,text="", hover_color="#3d3d3d",image=ctk_image,corner_radius=1000,bg_color="transparent",fg_color="transparent", width=150, height=40 ,compound="left", command=self.backtodashboard3)
        self.backtodash.pack(padx=20, pady=10, anchor="nw")

        
        self.gifimglabel1 = ct.CTkLabel(self.gifimgframe,text="")
        self.gifimglabel1.pack(padx=20, pady=90)

        image = Image.open("img/read0.png")

        ctk_image = ct.CTkImage(light_image=image, size=(600,400))
        
        self.gifimglabel1.configure(image=ctk_image)
        self.gifimglabel1.image = ctk_image

        # Read Existing Book Frame (on the right side)
        self.existingbookframe_1 = ct.CTkFrame(self.main_frame, width=1200 // 2, height=700, fg_color="transparent")
        self.existingbookframe_1.grid(row=2, column=1, pady=20, padx=20, sticky="nsew")
        
        self.bsearchBox = ct.CTkEntry(self.existingbookframe_1, textvariable=self.bsearchVar,justify="center" , width=400, height=40, fg_color="transparent",
                                      text_color="white", font=("Palatino Linotype", 20))
        self.bsearchBox.grid(row=0,column=0, columnspan=4,padx=20, pady=20)
        self.bsearchBox.bind("<KeyRelease>", self.update_dropdown)


        self.bsearchBtn = ct.CTkButton(self.existingbookframe_1,text="Search",width=60, height=40,corner_radius=10,text_color="white",bg_color="transparent", font=("Palatino Linotype", 20), command=self.srchBook)
        self.bsearchBtn.grid(row=0,column=5,padx=20, pady=20)
        
        self.dropdown_frame = ct.CTkFrame(self.existingbookframe_1, fg_color="transparent")
        self.dropdown_frame.grid(row=1, column=0, columnspan=4)


        #############################################
        self.existingbookframe_2 = ct.CTkFrame(self.main_frame, width=1200 // 2, height=700, fg_color="transparent")
        # self.existingbookframe_2.grid(row=2, column=1, pady=20, padx=20, sticky="nsew")

        self.is_running = False
        self.is_existingBook = True
        self.is_newBook = False

        self.music_var = tk.BooleanVar()

        self.music_check_btn = ct.CTkCheckBox(self.existingbookframe_2, text="Background Music", variable=self.music_var, font=("Palatino Linotype", 20), command=self.play_music)
        self.music_check_btn.grid(row=0, column=4, sticky="nsew")

        self.booktitleframe = ct.CTkFrame(self.existingbookframe_2, width=600, height=100, fg_color="transparent")
        self.booktitleframe.grid(row=1, column=0, columnspan=6, pady=20, padx=20, sticky="nsew")

        self.booktitle = ct.CTkLabel(self.booktitleframe, text="", fg_color="transparent",justify="center",
                                      text_color="white", font=("arial black", 32))
        self.booktitle.grid(row=1,column=3,padx=20, pady=20,sticky="nsew") 

        self.booktimerlabel1 = ct.CTkLabel(self.existingbookframe_2, text="00:00:00", fg_color="transparent",
                                      text_color="white", font=("Verdana ", 32,"bold"))
        self.booktimerlabel1.grid(row=3,column=3,padx=20, pady=20) 

        image = Image.open("img/sandclock.gif")

        self.sandclockimg1 = ct.CTkImage(light_image=image, size=(100,100))
        

        self.clockimglabel1 = ct.CTkLabel(self.existingbookframe_2, text="", image=self.sandclockimg1 , fg_color="transparent")
        self.clockimglabel1.grid(row=4,column=3,padx=20, pady=20)

        self.bookstartbtn1 = ct.CTkButton(self.existingbookframe_2,text="Start Timer",width=180,height=50,corner_radius=10,text_color="white",bg_color="transparent",font=("arial", 20,"bold"), command=self.start)
        self.bookstartbtn1.grid(row=5,column=2,padx=20, pady=20)

        self.bookpausebtn1 = ct.CTkButton(self.existingbookframe_2,text="Pause",width=180,height=50,corner_radius=10,text_color="white",bg_color="transparent",font=("arial", 20,"bold"),state="disabled", command=self.pausetimer)
        self.bookpausebtn1.grid(row=5,column=3,padx=20, pady=20)

        self.bookstopbtn1 = ct.CTkButton(self.existingbookframe_2,text="Stop",width=180,height=50,corner_radius=10,text_color="white",bg_color="transparent",font=("arial", 20,"bold"),state="disabled", command=self.stoptimer)
        self.bookstopbtn1.grid(row=5,column=4,padx=20, pady=20)
        #############################################


    def update_dropdown(self, event=None):
        # Clear the previous dropdown
        for widget in self.dropdown_frame.winfo_children():
            widget.destroy()

        # Get the search query
        query = self.bsearchVar.get().lower()

        if query:  # Display dropdown only if query is not empty
            matches = [item for item in self.items if query in item.lower()]  
            for match in matches:
                
                suggestion_button = ct.CTkButton(
                    self.dropdown_frame,
                    text=match,
                    corner_radius=0,
                    fg_color="#a3a3a3",
                    hover_color="#3d3d3d",
                    text_color="white",
                    font=("Palatino Linotype", 20),
                    width=400,
                    command=lambda m=match: self.select_item(m)  
                )
                suggestion_button.pack(fill="x", pady=2)

    def select_item(self, item):
        
        self.bsearchVar.set(item)
        for widget in self.dropdown_frame.winfo_children():
            widget.destroy()


    def srchBook(self):
        if self.bsearchBox.get() != '' and self.bsearchBox.get() in self.items:
            
            messagebox.showinfo("Book Found",f"{self.bsearchBox.get()} is present in the database!")

            self.existingbookframe_1.grid_forget()
            self.existingbookframe_2.grid(row=2, column=1, pady=20, padx=20, sticky="nsew")
            self.current_book_name=self.bsearchBox.get()
            print("Searched book : ",self.bsearchBox.get())
            print("Current book : ",self.current_book_name)

            res = ab.show_book_data(self.current_table)

            print(res)
            nameTime = dict()
            for i in res:
                nameTime[i[0]] = i[3]

            print(nameTime)
            self.booktitle.configure(text=f"Reading : {self.bsearchBox.get()}")
            self.booktimerlabel1.configure(text= nameTime[self.bsearchBox.get()])
            
            
            time_obj = datetime.strptime(nameTime[self.bsearchBox.get()], "%H:%M:%S")
            self.existingTime = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second
            
            print(nameTime)


        elif self.bsearchBox.get() == '':
            messagebox.showerror("Warning","Enter Book Name")

        else:
            messagebox.showerror("Error",f"{self.bsearchBox.get()} is not present!")

#######################################################################

    def show_book_list(self):
        self.apptitlelabel.configure(text="Book Details")

        self.dashboardframe.grid_forget()


        self.booklistframe = ct.CTkFrame(self.main_frame, width=1200, height=700, fg_color="transparent")
        self.booklistframe.grid(row=2, column=0, pady=20, padx=20, sticky="nsew")

        image = Image.open("img/home.png")
        ctk_image = ct.CTkImage(light_image=image, size=(120,35))
        self.backtodash = ct.CTkButton(self.booklistframe,text="", hover_color="#3d3d3d",image=ctk_image,corner_radius=1000,bg_color="transparent",fg_color="transparent", width=150, height=40 ,compound="left", command=self.backtodashboard2)
        self.backtodash.grid(row=0,column=0,padx=20, pady=10, sticky="nw")

        

        self.dispbookdata = ct.CTkLabel(self.booklistframe,text="", fg_color="transparent",
                                      text_color="white", font=("Palatino Linotype", 20))
        self.dispbookdata.grid(row=2,column=1, columnspan=6,padx=20, pady=20, sticky="w")
        
        self.cleardispbookdata = ct.CTkButton(self.booklistframe,text="Clear data", hover_color="#3d3d3d",corner_radius=1000,bg_color="transparent", width=120, height=40 ,compound="left",text_color="white", font=("arial", 18), command=self.cleardispdata)
        # self.cleardispbookdata.grid(row=2,column=0,padx=20, pady=10, sticky="nw")

        res = ab.findUserBook(self.current_table)

        bookData = ab.show_book_data(self.current_table)

        books=[]
        for book in res:
            books.append(book[0])

        self.bookcount = ct.CTkLabel(self.booklistframe,text=f"Books Count : {len(books)}" ,width=250,height=60,text_color="white",bg_color="transparent",font=("Verdana", 16,"bold"))
        self.bookcount.grid(row=0,column=5,padx=20, pady=20)

        rowNo = 4
        colNo = 2
        blen = 0
        bd= 0
        for item in books:
            button = ct.CTkButton(
                self.booklistframe,
                text=item,
                width=250,
                height=60,
                corner_radius=10,
                text_color="white",
                bg_color="transparent",
                font=("arial", 20, "bold"),
                command=self.aboutbookData(bookData[bd])  # Pass item as argument
            )
            button.grid(padx=10, pady=10, row=rowNo, column=colNo, sticky="nsew")  
            colNo +=1
            blen += 1
            bd+=1

            if blen > 3:
                colNo = 2
                rowNo += 1
                blen = 0

    def cleardispdata(self):
        self.dispbookdata.configure(text="")
        self.cleardispbookdata.grid_forget()

    def aboutbookData(self, book):
        
        def on_click():
            self.cleardispbookdata.grid(row=2,column=0,padx=20, pady=10, sticky="nw")
            if book[3] is not None:
                read_time = book[3]
                hr, min, sec = map(int, read_time.split(":"))
                formatted_time = f"{hr} hrs, {min} min and {sec} sec"
            else:
                formatted_time = f"0 hrs, 0 min and 0 sec"
            review = book[5] if book[5] else 'N/A'
            
            if len(review) > 90:
                wrapped_review = "\n".join(textwrap.wrap(review, width=90))
            else:
                wrapped_review = review

            details = f"""
            Book Title:- {book[0]} \t Author Name:- {book[1]} \t Genre:- {book[2]} \t Status:- {book[7]} \n 
            Start Date: {book[8] if book[8] else 'N/A'} \t Reading Time:- {formatted_time} \t Pages:- {book[4]} \t Rating:- {book[6] if book[6] else 'N/A'} \n
            End Date: {book[9] if book[9] else 'N/A'}\n
            Review:- {wrapped_review}
            """
            self.dispbookdata.configure(text=details)

        return on_click



#######################################################################

    def addoldbook(self):
        self.apptitlelabel.configure(text="Add Old Book")

        self.dashboardframe.grid_forget()
        
        self.oldbookframe = ct.CTkFrame(self.main_frame, width=1200, height=50, fg_color="transparent")
        self.oldbookframe.grid(row=2, column=0, pady=20, padx=20, sticky="nsew")

        self.oldbooklabel = ct.CTkLabel(self.main_frame, text="Enter Details Here", fg_color="transparent",
                                      text_color="white", font=("arial black", 26))
        self.oldbooklabel.grid(row=2,column=1,padx=20, pady=20)

        image = Image.open("img/home.png")
        ctk_image = ct.CTkImage(light_image=image, size=(120,35))

        self.backtodash = ct.CTkButton(self.oldbookframe,text="", hover_color="#3d3d3d",image=ctk_image,corner_radius=1000,bg_color="transparent",fg_color="transparent", width=150, height=40 ,compound="left", command=self.backtodashboard5)
        self.backtodash.grid(row=0,column=0,padx=20, pady=10, sticky="nw")

        
        # Right image frame (on the left side)
        self.rightimgframe = ct.CTkFrame(self.main_frame, width=1200 // 2, height=700, fg_color="transparent")
        self.rightimgframe.grid(row=3, column=0, pady=20, padx=20, sticky="nsew")  

        # Left Book Details frame (on the right side)
        self.obdetailsframe = ct.CTkFrame(self.main_frame, width=1200 // 2, height=700)
        self.obdetailsframe.grid(row=3, column=1, pady=20, padx=20, sticky="nsew")

                
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)


        # Image configuration on left side
        self.rightimglabel = ct.CTkLabel(self.rightimgframe,text="")
        self.rightimglabel.pack(padx=20, pady=10)

        image = Image.open("img/book3.jpg")

        ctk_image = ct.CTkImage(light_image=image, size=(575,1123))
        
        self.rightimglabel.configure(image=ctk_image)
        self.rightimglabel.image = ctk_image

        self.is_book_que = messagebox.askyesno("Important","Are you adding fully completed book ?")
                     
        self.obname_label = ct.CTkLabel(self.obdetailsframe,text="Book Title   :", fg_color="transparent",
                                      text_color="white", font=("Palatino Linotype", 20))
        self.obname_label.grid(row=1,column=2,padx=20, pady=20, sticky="w")

        self.obname_entry = ct.CTkEntry(self.obdetailsframe,placeholder_text="Enter Book Name ",justify="center",width=350,height=50,bg_color="transparent",fg_color="transparent",font=("arial", 16))
        self.obname_entry.grid(row=1,column=3,padx=20, pady=20)

        self.obauthor_label = ct.CTkLabel(self.obdetailsframe,text="Book Author   :", fg_color="transparent",
                                      text_color="white", font=("Palatino Linotype", 20))
        self.obauthor_label.grid(row=2,column=2,padx=20, pady=20, sticky="w")

        self.obauthor_entry = ct.CTkEntry(self.obdetailsframe,placeholder_text="Enter Book Author Name ",justify="center",width=350,height=50,bg_color="transparent",fg_color="transparent",font=("arial", 16))
        self.obauthor_entry.grid(row=2,column=3,padx=20, pady=20)

        book_genres = [
                    'Action Fiction', 'Adventure Fiction', 'Alternate History', 'Autobiography', 'Biography', 
                    'Contemporary Literature', 'Contemporary Romance', 'Crime Fiction', 'Detective Fiction', 'Essay',
                    'Fairy Tale', 'Fantasy', 'Fantasy Fiction', 'Fiction', 'Genre Fiction', 'Graphic Novel', 
                    'Historical Fantasy', 'Historical Fiction', 'Historical Romance', 'History',
                    'Horror Fiction', 'Humor', 'Literary Fiction', 'Magical Realism', 'Memoir', 'Mystery', 'Narrative', 
                    'New Adult Fiction', 'Non-fiction', 'Novel', 'Paranormal Romance', 'Philosophy', 'Poetry', 'Quotation', 
                    'Romance', 'Romance Novel', 'Satire', 'Science', 'Science Fantasy', 'Science Fiction',
                    'Self-help Book', 'Short Story', 'Social Science', 'Speculative Fiction', 'Spirituality', 'Thriller', 
                    'Travel Literature', 'True Crime', 'Western Fiction', "Women's Fiction", 'Young Adult Literature'
                    ]

        self.obgenre_label = ct.CTkLabel(self.obdetailsframe,text="Book Genre   :", fg_color="transparent",
                                      text_color="white", font=("Palatino Linotype", 20))
        self.obgenre_label.grid(row=3,column=2,padx=20, pady=20, sticky="w")

        self.obgenre_entry = ct.CTkOptionMenu(self.obdetailsframe,values=book_genres,width=350,height=50,bg_color="transparent", fg_color="#ebb434",font=("arial", 16),text_color="white")
        self.obgenre_entry.grid(row=3,column=3,padx=20, pady=20)

        self.obreadtime_label = ct.CTkLabel(self.obdetailsframe,text="Book Reading Time   :", fg_color="transparent",
                                      text_color="white", font=("Palatino Linotype", 20))
        self.obreadtime_label.grid(row=4,column=2,padx=20, pady=20, sticky="w")

        self.obreadtime_entry = ct.CTkEntry(self.obdetailsframe,placeholder_text="eg (04:56:23) like (hh:mm:ss) ",justify="center",width=350,height=50,bg_color="transparent",fg_color="transparent",font=("arial", 16))
        self.obreadtime_entry.grid(row=4,column=3,padx=20, pady=20)

        self.obpage_label = ct.CTkLabel(self.obdetailsframe,text="Number of Book Pages   :", fg_color="transparent",
                                      text_color="white", font=("Palatino Linotype", 20))
        self.obpage_label.grid(row=5,column=2,padx=20, pady=20, sticky="w")

        self.obpage_entry = ct.CTkEntry(self.obdetailsframe,placeholder_text="eg. 465 (Note: Numbers only)",justify="center",width=350,height=50,bg_color="transparent",fg_color="transparent",font=("arial", 16))
        self.obpage_entry.grid(row=5,column=3,padx=20, pady=20)

        self.obstartdt_label = ct.CTkLabel(self.obdetailsframe,text="Book Started Date   :", fg_color="transparent",
                                      text_color="white", font=("Palatino Linotype", 20))
        self.obstartdt_label.grid(row=6,column=2,padx=20, pady=20, sticky="w")

        self.obstartdt_entry = ctk_date_picker.CTkDatePicker(self.obdetailsframe,width=280,height=50,bg_color="transparent",fg_color="transparent")
        self.obstartdt_entry.grid(row=6,column=3,padx=20, pady=20)

        if self.is_book_que:
            self.obenddt_label = ct.CTkLabel(self.obdetailsframe,text="Book End Date   :", fg_color="transparent",
                                        text_color="white", font=("Palatino Linotype", 20))
            self.obenddt_label.grid(row=7,column=2,padx=20, pady=20, sticky="w")

            self.obenddt_entry = ctk_date_picker.CTkDatePicker(self.obdetailsframe,width=280,height=50,bg_color="transparent",fg_color="transparent")
            self.obenddt_entry.grid(row=7,column=3,padx=20, pady=20)

            self.obrate_label = ct.CTkLabel(self.obdetailsframe,text="Book Rating   :", fg_color="transparent",
                                        text_color="white", font=("Palatino Linotype", 20))
            self.obrate_label.grid(row=8,column=2,padx=20, pady=20, sticky="w")

            self.obrate_entry = ct.CTkEntry(self.obdetailsframe,placeholder_text="eg. 4.8 (Note: Float Numbers only)",justify="center",width=350,height=50,bg_color="transparent",fg_color="transparent",font=("arial", 16))
            self.obrate_entry.grid(row=8,column=3,padx=20, pady=20)

            self.obreview_label = ct.CTkLabel(self.obdetailsframe,text="Book Review   :", fg_color="transparent",
                                        text_color="white", font=("Palatino Linotype", 20))
            self.obreview_label.grid(row=9,column=2,padx=20, pady=20, sticky="nw")


            self.obreview_entry = ct.CTkTextbox(self.obdetailsframe, width=350,height=400,bg_color="#3d3d3d",fg_color="transparent",font=("Palatino Linotype", 16))
            self.obreview_entry.grid(row=9,column=3,padx=20, pady=20)
        
        
       
        self.oldbookSub_button = ct.CTkButton(self.obdetailsframe,text="",image=self.subbtnimg, hover_color="#3d3d3d",corner_radius=1000,bg_color="transparent",fg_color="transparent", width=180, height=40 ,compound="left", command=self.submit_oldbook_data)
        self.oldbookSub_button.grid(row=10,column=3,padx=20, pady=40)
        
        
        

        

#######################################################################

    def submit_oldbook_data(self):
        
        try:
            if self.is_book_que:
                if self.obname_entry.get().strip().replace(" ","") == "" or self.obauthor_entry.get().strip().replace(" ","") == "" or self.obgenre_entry.get().strip().replace(" ","") == "" or self.obreadtime_entry.get().strip().replace(" ","") == "" or self.obpage_entry.get().strip().replace(" ","") == "" or self.obstartdt_entry.get_date().strip().replace(" ","") == "" or self.obenddt_entry.get_date().strip().replace(" ","") == "" or self.obrate_entry.get().strip().replace(" ","") == "" or self.obreview_entry.get("0.0", "end-1c") == "":
                    messagebox.showwarning("Warning", "All fields are required!")
            
                elif isinstance(int(self.obpage_entry.get().strip().replace(" ","")), int)==False or isinstance(float(self.obrate_entry.get().strip().replace(" ","")), float)==False:
                    messagebox.showwarning("Warning","Enter Field value as mentioned!")
                    
                else:
                    print(f''' 
                            Table Name : {self.current_table}\n
                            Book Name : {self.obname_entry.get().strip().replace(" ","")}\n
                            Author : {self.obauthor_entry.get().strip().replace(" ","")}\n
                            Genre : {self.obgenre_entry.get()}\n
                            Time : {self.obreadtime_entry.get().strip().replace(" ","")}\n
                            Pages : {int(self.obpage_entry.get().strip().replace(" ",""))}\n
                            Start : {self.obstartdt_entry.get_date().strip().replace(" ","")}\n
                            End : {self.obenddt_entry.get_date().strip().replace(" ","")}\n
                            Rating : {float(self.obrate_entry.get().strip().replace(" ",""))}\n
                            Review : {self.obreview_entry.get("0.0", "end-1c")}

                        ''')
                    
                    ab.add_com_old_book(self.current_table,self.obname_entry.get(),self.obauthor_entry.get(),self.obgenre_entry.get(),int(self.obpage_entry.get().strip().replace(" ","")),self.obreadtime_entry.get().strip().replace(" ",""),self.obstartdt_entry.get_date().strip().replace(" ",""),self.obenddt_entry.get_date().strip().replace(" ",""),float(self.obrate_entry.get().strip().replace(" ","")),self.obreview_entry.get("0.0", "end-1c"),"Completed")

                    messagebox.showinfo("Success","Your Book Data Saved Successfully!")
            
            else:
                if self.obname_entry.get().strip().replace(" ","") == "" or self.obauthor_entry.get().strip().replace(" ","") == "" or self.obgenre_entry.get().strip().replace(" ","") == "" or self.obreadtime_entry.get().strip().replace(" ","") == "" or self.obpage_entry.get().strip().replace(" ","") == "" or self.obstartdt_entry.get_date().strip().replace(" ","") == "" :
                    messagebox.showwarning("Warning", "All fields are required!")
            
                elif isinstance(int(self.obpage_entry.get().strip().replace(" ","")), int)==False :
                    messagebox.showwarning("Warning","Enter Field value as mentioned!")
                
                else:
                    print(f''' 
                            Table Name : {self.current_table}\n
                            Book Name : {self.obname_entry.get().strip().replace(" ","")}\n
                            Author : {self.obauthor_entry.get().strip().replace(" ","")}\n
                            Genre : {self.obgenre_entry.get()}\n
                            Time : {self.obreadtime_entry.get().strip().replace(" ","")}\n
                            Pages : {int(self.obpage_entry.get().strip().replace(" ",""))}\n
                            Start : {self.obstartdt_entry.get_date().strip().replace(" ","")}
                            ''')
                    
                    ab.add_incom_old_book(self.current_table,self.obname_entry.get(),self.obauthor_entry.get(),self.obgenre_entry.get(),int(self.obpage_entry.get().strip().replace(" ","")),self.obreadtime_entry.get().strip().replace(" ",""),self.obstartdt_entry.get_date().strip().replace(" ",""),"In Progress")

                    messagebox.showinfo("Success","Your Book Data Saved Successfully!")
            
            self.backtodashboard5()

        except Exception as e:
            messagebox.showwarning("Warning","Enter Field value as mentioned!")

#######################################################################


    def show_book_analysis(self):
        self.apptitlelabel.configure(text="Book Analysis")

        self.dashboardframe.grid_forget()
        self.titlelabelframe.grid_forget()

        self.analysistitlelabel = ct.CTkLabel(self.main_frame, text="Book Analysis", fg_color="transparent",
                                      text_color="white", font=("arial black", 38))
        self.analysistitlelabel.pack()


        self.bookanalysisframe = ct.CTkFrame(self.main_frame, width=1200, height=40, fg_color="transparent")
        self.bookanalysisframe.pack(pady=20, padx=20)

        image = Image.open("img/home.png")
        ctk_image = ct.CTkImage(light_image=image, size=(120,35))
        self.backtodash = ct.CTkButton(self.bookanalysisframe,text="", hover_color="#3d3d3d",image=ctk_image,corner_radius=1000,bg_color="transparent",fg_color="transparent", width=150, height=40 ,compound="left", command=self.backtodashboard4)
        self.backtodash.grid(row=0, column=0, padx=20, pady=10,sticky="w")
        
        self.tempframe = ct.CTkFrame(self.bookanalysisframe, width=800, height=40, fg_color="transparent")
        self.tempframe.grid(row=0, column=1, padx=20, pady=10)

        self.downBookData = ct.CTkButton(self.bookanalysisframe,text="Download Data", hover_color="#3d3d3d",corner_radius=1000,bg_color="transparent", width=150, height=40 , font=("Palatino Linotype", 20),compound="left", command=self.download_mydata)
        self.downBookData.grid(row=0, column=8, padx=20, pady=10,sticky="e")


        self.tableframe = ct.CTkFrame(self.main_frame, fg_color="transparent", width=700)
        self.tableframe.pack(fill='both', expand=True, padx=20, pady=20)

        df = ab.show_all_data(self.current_table)

        table = Table(self.tableframe, dataframe=df, showtoolbar=True, showstatusbar=True)
        table.show()


    def download_mydata(self):
        df = ab.show_all_data(self.current_table)
        df.to_csv(r".\book_data.csv")     
        current_time = datetime.now().strftime("%Y-%m-%d")
        desktop_path = os.path.join(os.path.expanduser("~"), "Downloads")
    
        filename = f"{self.current_user_name} book data {current_time}.csv"
        file_path = os.path.join(desktop_path, filename)
        
        df.to_csv(file_path, index=False)
        
        messagebox.showinfo("Successfull",f"Your book data has been successfully downloaded to \n {file_path}")
        

    


#######################################################################

    
    def my_library(self):
        self.apptitlelabel.configure(text="Library")
        self.lib_gif_flag = True
        self.dashboardframe.grid_forget()
        self.titlelabelframe.grid_forget()

        self.librarytitlelabel = ct.CTkLabel(self.main_frame, text="Book Library", fg_color="transparent",
                                      text_color="white", font=("arial black", 38))
        self.librarytitlelabel.pack()

        self.booklibrarytopframe = ct.CTkFrame(self.main_frame, width=1200, height=40, fg_color="transparent")
        self.booklibrarytopframe.pack(pady=20, padx=20)

        image = Image.open("img/home.png")
        ctk_image = ct.CTkImage(light_image=image, size=(120,35))
        self.libbacktodash = ct.CTkButton(self.booklibrarytopframe,text="", hover_color="#3d3d3d",image=ctk_image,corner_radius=1000,bg_color="transparent",fg_color="transparent", width=150, height=40 ,compound="left", command=self.backtodashboard6)
        self.libbacktodash.grid(row=0, column=0, padx=20, pady=10,sticky="w")

        self.tempframe = ct.CTkFrame(self.booklibrarytopframe, width=800, height=40, fg_color="transparent")
        self.tempframe.grid(row=0, column=1, padx=20, pady=10)
        
        self.templabel = ct.CTkLabel(self.booklibrarytopframe,text="             ", bg_color="transparent", width=150, height=40 , font=("Palatino Linotype", 20))
        self.templabel.grid(row=0, column=8, padx=20, pady=10,sticky="e")



        self.booklibrarybtnframe = ct.CTkFrame(self.main_frame, width=1200, height=40, fg_color="transparent")
        self.booklibrarybtnframe.pack(pady=20, padx=20)

        self.mylib_button = ct.CTkButton(self.booklibrarybtnframe,text="Library",width=250,height=60,corner_radius=10,text_color="white",bg_color="transparent",font=("arial", 20,"bold"), command=self.lib_button_toggle1)
        self.mylib_button.grid(row=0, column=1, padx=20, pady=10)

        self.lib_edit_button = ct.CTkButton(self.booklibrarybtnframe,text="Edit Book Data",width=250,height=60,corner_radius=10,text_color="white",bg_color="transparent",font=("arial", 20,"bold"),command=self.lib_button_toggle2)
        self.lib_edit_button.grid(row=0, column=2, padx=20, pady=10)

        self.lib_del_button = ct.CTkButton(self.booklibrarybtnframe,text="Delete Book",width=250,height=60,corner_radius=10,text_color="white",bg_color="transparent",font=("arial", 20,"bold"),command=self.lib_button_toggle3)
        self.lib_del_button.grid(row=0, column=3, padx=20, pady=10)

        self.temp_hr_frame = ct.CTkFrame(self.booklibrarybtnframe,width=1200,height=6,fg_color="#3d3d3d")    
        self.temp_hr_frame.grid(row=1, column=0, padx=20, pady=10,columnspan=6,sticky='nsew')

        self.booklibrarygifframe = ct.CTkFrame(self.main_frame, width=1200, height=600, fg_color="transparent")
        self.booklibrarygifframe.pack(pady=20, padx=20)

        self.booklibrarymainframe = ct.CTkFrame(self.main_frame, width=1200, height=600, fg_color="transparent")
        #self.booklibrarymainframe.pack(pady=20, padx=20)

        self.booklibraryeditframe = ct.CTkFrame(self.main_frame, width=1200, height=600, fg_color="transparent")
        #self.booklibraryeditframe.pack(pady=20, padx=20)
        self.bookeditchkframe = ct.CTkFrame(self.main_frame, width=1200, height=600, fg_color="transparent")
        self.bookeditlablframe = ct.CTkFrame(self.main_frame, width=1200, height=600, fg_color="transparent")

        self.booklibrarydelframe = ct.CTkFrame(self.main_frame, width=1200, height=600, fg_color="transparent")
        #self.booklibrarydelframe.pack(pady=20, padx=20)


        self.lib_gifimg = ct.CTkLabel(self.booklibrarygifframe, text = "")
        self.lib_gifimg.pack()

        self.lib_gif_path = "img/lib_bg.gif"  
        self.gif = Image.open(self.lib_gif_path)

        self.resize_width = 1044  
        self.resize_height = 735  

        self.lib_frames = []
        try:
            while self.lib_gif_flag:
                frame = self.gif.copy()
                frame = frame.resize((self.resize_width, self.resize_height), Image.LANCZOS)  
                self.lib_frames.append(ImageTk.PhotoImage(frame))
                self.gif.seek(len(self.lib_frames)) 
        except EOFError:
            pass
        
        self.lib_current_frame = 0
        self.lib_animation_id = None
        self.lib_animate_gif()

    def lib_animate_gif(self):
        if self.lib_gif_flag:

            if self.lib_animation_id:
                self.after_cancel(self.lib_animation_id)

            if self.lib_frames:
                self.lib_gifimg.configure(image=self.lib_frames[self.lib_current_frame])
                self.lib_current_frame = (self.lib_current_frame + 1) % len(self.lib_frames)

            self.lib_animation_id = self.after(1500, self.lib_animate_gif)  
    

    def stop_lib_animation(self):    
        self.lib_gif_flag = False
        if self.lib_animation_id:
            self.after_cancel(self.lib_animation_id)

    def lib_button_toggle1(self):
        try:
            self.lib_gif_flag = False
            self.booklibrarygifframe.pack_forget()
            self.booklibraryeditframe.pack_forget()
            self.booklibrarydelframe.pack_forget()
            self.bookeditlablframe.pack_forget()
            self.bookeditchkframe.pack_forget()

        except Exception as e:
            print(e)

        self.booklibrarymainframe.pack(pady=20, padx=20)
        self.current_lib_button = "Library"
        self.lib_book_details()

    def lib_button_toggle2(self):
        try:
            self.lib_gif_flag = False
            self.booklibrarygifframe.pack_forget()
            self.booklibrarymainframe.pack_forget()
            self.booklibrarydelframe.pack_forget()

        except Exception as e:
            print(e)

        self.booklibraryeditframe.pack(pady=20, padx=20)
        self.current_lib_button = "Edit"
        self.lib_book_details()

    def lib_button_toggle3(self):
        try:
            self.lib_gif_flag = False
            self.booklibrarygifframe.pack_forget()
            self.booklibraryeditframe.pack_forget()
            self.booklibrarymainframe.pack_forget()
            self.bookeditlablframe.pack_forget()
            self.bookeditchkframe.pack_forget()

        except Exception as e:
            print(e)

        self.booklibrarydelframe.pack(pady=20, padx=20)
        self.current_lib_button = "Delete"
        self.lib_book_details()

    def lib_book_details(self):
        

        if self.current_lib_button =="Library":

            self.lib_detlabel = ct.CTkLabel(self.booklibrarymainframe, text = "Book Shelf : ", fg_color="transparent",
                                        text_color="white", font=("Britannic Bold", 26,"bold"))
            
            self.lib_detlabel.grid(padx=10, pady=10, row=0, column=0)

            temp_hr_frame0 = ct.CTkFrame(self.booklibrarymainframe,width=1000,height=6,fg_color="#3d3d3d")    
            temp_hr_frame0.grid(padx=10, pady=10, row=1, column=0, columnspan=5 ,sticky="nsew")

            lib_df = ab.show_all_data(self.current_table)

            genre = sorted(list(lib_df['genre'].unique()))

            btn_rowNo = 2
            btn_colNo = 0
            
            for item in genre:
                gen_button = ct.CTkButton(
                    self.booklibrarymainframe,
                    text=item,
                    width=250,
                    height=60,
                    hover_color="#3d3d3d",
                    corner_radius=10,
                    text_color="white",
                    bg_color="transparent",
                    fg_color="#4b7552",
                    font=("elephant", 20, "bold")
                )

                gen_button.grid(padx=10, pady=10, row=btn_rowNo, column=btn_colNo, sticky="nsew")  
                
                lib_book = lib_df[lib_df['genre']==item]['book_name'].tolist()

                count_button = ct.CTkButton(self.booklibrarymainframe,text=f"Books Count : {len(lib_book)}",width=250,height=60,hover_color="#3d3d3d",
                                        corner_radius=10,text_color="white", bg_color="transparent",fg_color="transparent",font=("arial", 20, "bold"))
                count_button.grid(padx=10, pady=10, row=btn_rowNo, column=4, sticky="nsew") 


                btn_rowNo +=1
                book_colNO = 0
                blen = 0

                for book_name in lib_book:
                    book_button = ct.CTkButton(
                        self.booklibrarymainframe,
                        text=book_name,
                        width=200,
                        height=50,
                        hover_color=None,
                        text_color="white",
                        fg_color="transparent",
                        font=("Berlin Sans FB Demi", 20, "bold")
                    )
                    book_button.grid(padx=10, pady=10, row=btn_rowNo, column=book_colNO, sticky="nsew")  

                    book_colNO +=1
                    blen += 1

                    if blen > 4:
                        book_colNO = 0
                        btn_rowNo += 1
                        blen = 0

                btn_rowNo +=1
                temp_hr_frame = ct.CTkFrame(self.booklibrarymainframe,width=1000,height=5,fg_color="#668385")    
                temp_hr_frame.grid(padx=10, pady=10, row=btn_rowNo, column=0, columnspan=5 ,sticky="nsew")     
                btn_rowNo +=1

        elif self.current_lib_button =="Edit":
            self.booklibraryeditframe.pack(pady=20, padx=20)

            self.lib_edt_label = ct.CTkLabel(self.booklibraryeditframe, text="Which book data you want to edit!!", width=250,height=60, text_color="white",bg_color="transparent",font=("Georgia", 26, "bold"))
            self.lib_edt_label.grid(row=1, column=0,padx=20, pady=20)  
            
            res = ab.findUserBook(self.current_table)

            books=[]
            for book in res:
                books.append(book[0])
           
            self.items= books
            self.bsearchVar = ct.StringVar()

            self.edit_searchBox = ct.CTkEntry(self.booklibraryeditframe, textvariable=self.bsearchVar,justify="center" , width=400, height=40, fg_color="transparent",
                                      text_color="white", font=("Palatino Linotype", 20))
            self.edit_searchBox.grid(row=2,column=0, columnspan=4,padx=20, pady=20)
            self.edit_searchBox.bind("<KeyRelease>", self.update_dropdown)


            self.edit_searchBtn = ct.CTkButton(self.booklibraryeditframe,text="Search",width=60, height=40,corner_radius=10,text_color="white",bg_color="transparent", font=("Palatino Linotype", 22), command=self.libedit_srchBook)
            self.edit_searchBtn.grid(row=2,column=5,padx=20, pady=20)

            self.dropdown_frame = ct.CTkFrame(self.booklibraryeditframe, fg_color="transparent")
            self.dropdown_frame.grid(row=3, column=0, columnspan=4)

            self.check_fields = ['book_name', 'book_author', 'genre', 'reading_time', 'book_pages',
                       'book_review', 'rating', 'book_status', 'start_date', 'end_date']

            self.checkboxes = {}  
            self.entry_fields = {} 
            self.row_counter = 0 



        elif self.current_lib_button =="Delete":
                        
            self.booklibrarydelframe.pack(pady=20, padx=20)

            self.lib_del_label = ct.CTkLabel(self.booklibrarydelframe, text="Search the book you want to delete !!", width=250,height=60, text_color="white",bg_color="transparent",font=("Georgia", 26, "bold"))

            self.lib_del_label.grid(row=1, column=0,padx=20, pady=20) 

            res = ab.findUserBook(self.current_table)

            books=[]
            for book in res:
                books.append(book[0])
           
            self.items= books
            self.bsearchVar = ct.StringVar()

            self.lib_searchBox = ct.CTkEntry(self.booklibrarydelframe, textvariable=self.bsearchVar,justify="center" , width=400, height=40, fg_color="transparent",
                                      text_color="white", font=("Palatino Linotype", 20))
            self.lib_searchBox.grid(row=2,column=0, columnspan=4,padx=20, pady=20)
            self.lib_searchBox.bind("<KeyRelease>", self.update_dropdown)


            self.lib_searchBtn = ct.CTkButton(self.booklibrarydelframe,text="Search",width=60, height=40,corner_radius=10,text_color="white",bg_color="transparent", font=("Palatino Linotype", 22), command=self.lib_srchBook)
            self.lib_searchBtn.grid(row=2,column=5,padx=20, pady=20)

            self.dropdown_frame = ct.CTkFrame(self.booklibrarydelframe, fg_color="transparent")
            self.dropdown_frame.grid(row=3, column=0, columnspan=4)

            self.lib_delTemp_lbl = ct.CTkLabel(self.booklibrarydelframe,text="", width=250,height=60, text_color="white",bg_color="transparent",font=("Georgia", 26, "bold"))
            self.lib_delTemp_lbl.grid(row=4, column=0, columnspan=4)

            self.lib_bookdel_btn = ct.CTkButton(self.booklibrarydelframe,text="Delete",width=140, height=50,corner_radius=10,text_color="white",bg_color="transparent", font=("Verdana", 22), command=self.delete_lib_book)
            

    def lib_srchBook(self):
        if self.lib_searchBox.get() != '' and self.lib_searchBox.get() in self.items:
            messagebox.showinfo("Book Found",f"{self.lib_searchBox.get()} is present in the database!")
            self.lib_delTemp_lbl.configure(text=f"Selected book for deletion : {self.lib_searchBox.get()}")
            self.lib_bookdel_btn.grid(row=5,column=0,padx=20, pady=20)

        elif self.lib_searchBox.get() == '':
            messagebox.showerror("Warning","Enter Book Name")

        else:
            messagebox.showerror("Error",f"{self.lib_searchBox.get()} is not present!")

    def delete_lib_book(self):
        del_ans = messagebox.askyesno("Attention",f"After deletion of book the data will not be able to recover!! \n Are you sure want to delete book '{self.lib_searchBox.get()}' ")
        print(self.lib_searchBox.get())

        if del_ans:
            messagebox.showinfo("Successfull","Book deleted successfully!")
            ab.del_book(self.current_table,self.lib_searchBox.get())
            self.lib_delTemp_lbl.configure(text="")
            self.lib_bookdel_btn.grid_forget()
            self.lib_book_details()

    def libedit_srchBook(self):
        if self.edit_searchBox.get() != '' and self.edit_searchBox.get() in self.items:
            messagebox.showinfo("Book Found",f"{self.edit_searchBox.get()} is present in the database!")
            self.selected_book = self.edit_searchBox.get()
            book_data = ab.show_book_data(self.current_table,self.selected_book)

            self.book_data_dict = {self.check_fields[i]: book_data[i] for i in range(len(self.check_fields))}

            


            self.bookeditchkframe.pack(padx=20, pady=20)
            row = 0
            col = 0

            for index, field in enumerate(self.check_fields):
                var = ct.BooleanVar()  # Track checkbox state
                checkbox = ct.CTkCheckBox(
                    self.bookeditchkframe, text=field.replace("_", " ").title(),
                    variable=var, command=lambda f=field, v=var: self.toggle_field(f, v),text_color="white", font=("arial black", 18)
                )
                checkbox.grid(row=row, column=col, padx=10, pady=5, sticky="w")
                self.checkboxes[field] = var  # Store reference

                col += 1
                if (index + 1) % 5 == 0:  # Move to the next row after every 5 checkboxes
                    row += 1
                    col = 0

            self.bookeditlablframe.pack(padx=20, pady=20)
            self.edit_save_btn = ct.CTkButton(self.bookeditlablframe,text="Save Changes",width=180,height=50,corner_radius=10,state="disabled",text_color="white",bg_color="transparent",font=("arial", 20,"bold"),command=self.save_edited_bdata)
            self.edit_save_btn.grid(row=6, column=3, padx=10, pady=30, sticky="w")
            


            # Clear checkboxes and entry fields
            for field in self.check_fields:
                self.checkboxes[field].set(False)  # Uncheck all initially
                if field in self.entry_fields:
                    self.entry_fields[field]['entry'].delete(0, "end")  # Clear existing entry fields
            

        elif self.edit_searchBox.get() == '':
            messagebox.showerror("Warning","Enter Book Name")

        else:
            messagebox.showerror("Error",f"{self.edit_searchBox.get()} is not present!")

    
    def toggle_field(self, field, var):
        
        self.edit_save_btn.configure(state="normal")
        if var.get():  # If checked, add input field
            
            self.entry_fields[field] = {}

            # Determine row and column for label-entry pair (2 per row)
            row = len(self.entry_fields) // 2  # Every 2 fields, move to the next row
            col = (len(self.entry_fields) % 2) * 2  # Column 0 for first, Column 2 for second

            # Create label and entry field
            self.entry_fields[field]['label'] = ct.CTkLabel(self.bookeditlablframe, text=field.replace("_", " ").title(),fg_color="transparent",text_color="white", font=("Palatino Linotype", 20))
            self.entry_fields[field]['label'].grid(row=row, column=col, padx=10, pady=5, sticky="w")

            self.entry_fields[field]['entry'] = ct.CTkEntry(self.bookeditlablframe, justify="center",width=350,height=50,bg_color="transparent",fg_color="transparent",font=("arial", 16))
            self.entry_fields[field]['entry'].grid(row=row, column=col + 1, padx=10, pady=5, sticky="w")

            if self.selected_book and field in self.book_data_dict:
                self.entry_fields[field]['entry'].insert(0, str(self.book_data_dict[field]))

        else:  # If unchecked, remove input field
            if field in self.entry_fields:
                
                self.entry_fields[field]['label'].destroy()
                self.entry_fields[field]['entry'].destroy()
                del self.entry_fields[field]

                # Reset the grid layout dynamically
        self.rearrange_entries()

    def rearrange_entries(self):
        
        row_counter = 0
        col_counter = 0

        for field, widgets in self.entry_fields.items():
            widgets['label'].grid(row=row_counter, column=col_counter, padx=10, pady=5, sticky="w")
            widgets['entry'].grid(row=row_counter, column=col_counter + 1, padx=10, pady=5, sticky="w")

            col_counter += 2  # Move to next column
            if col_counter >= 4:  # Only 2 pairs per row
                row_counter += 1
                col_counter = 0 
    
    def save_edited_bdata(self):
        

        if not self.selected_book:
            print("No book selected.")
            return

        update_data = {}
        for field, widgets in self.entry_fields.items():
            value = widgets['entry'].get()
            update_data[field] = value if value else None  # Store None if empty

        if not update_data:
            print("No fields selected for update.")
            return

        # Build dynamic UPDATE query
        query_parts = [f"{field} = ?" for field in update_data.keys()]
        query = f"UPDATE {self.current_table} SET {', '.join(query_parts)} WHERE book_name = ?"
        values = list(update_data.values()) + [self.selected_book]

        try:
            
            ab.edit_book_in_data(query,values)
            messagebox.showinfo("Successfull","Your Book Data Is Edited!!")
        except Exception as e:
            messagebox.showerror("Failed",f"Error updating database{e}")
        
        self.bookeditchkframe.pack_forget()
        self.bookeditlablframe.pack_forget()
        self.lib_book_details()
        

#######################################################################

    def backtodashboard1(self):
        self.apptitlelabel.configure(text="Dashboard")
        self.current_book_name=None
        self.gifimgframe.grid_forget()
        self.bookdetailsframe.grid_forget()
        self.bookreadframe.grid_forget()
        self.dashboardframe.grid_configure(row=2, column=0, pady=20, padx=20, sticky="nsew")

    def backtodashboard2(self):
        try:
            self.backtodashboard1()
            self.booklistframe.grid_forget()

        except:
            self.booklistframe.grid_forget()
            self.dashboardframe.grid_configure(row=2, column=0, pady=20, padx=20, sticky="nsew")

    def backtodashboard3(self):
        try:
            self.backtodashboard1()
            self.booktitleframe.grid_forget()
            self.dropdown_frame.grid_forget()
            self.existingbookframe_1.grid_forget()
            self.existingbookframe_2.grid_forget()

        except:
            self.dropdown_frame.grid_forget()
            self.booktitleframe.grid_forget()
            self.existingbookframe_1.grid_forget()
            self.existingbookframe_2.grid_forget()
            self.dashboardframe.grid_configure(row=2, column=0, pady=20, padx=20, sticky="nsew")

    def backtodashboard4(self):
        try:
            self.backtodashboard1()
            self.bookanalysisframe.pack_forget()
            self.tableframe.pack_forget()
            self.analysistitlelabel.pack_forget()

        except:
            self.bookanalysisframe.pack_forget()
            self.tableframe.pack_forget()
            self.analysistitlelabel.pack_forget()
            self.dashboardframe.grid_configure(row=2, column=0, pady=20, padx=20, sticky="nsew")
            self.titlelabelframe.grid_configure(row=0, column=0, columnspan=10,pady=20, padx=20) 

    def backtodashboard5(self):
        try:
            self.backtodashboard1()
            self.oldbookframe.grid_forget()
            self.rightimgframe.grid_forget()     
            self.obdetailsframe.grid_forget()
            self.oldbooklabel.grid_forget()
        except:
            self.oldbookframe.grid_forget()
            self.rightimgframe.grid_forget()     
            self.obdetailsframe.grid_forget()
            self.oldbooklabel.grid_forget()
            self.dashboardframe.grid_configure(row=2, column=0, pady=20, padx=20, sticky="nsew")
            

    def backtodashboard6(self):
        try:
            self.backtodashboard1()
            self.librarytitlelabel.pack_forget()
            self.booklibrarytopframe.pack_forget()
            self.booklibrarybtnframe.pack_forget()
            self.booklibrarygifframe.pack_forget()
            self.booklibrarymainframe.pack_forget()
            self.booklibrarydelframe.pack_forget()
            self.booklibraryeditframe.pack_forget()
            self.bookeditchkframe.pack_forget()
            self.bookeditlablframe.pack_forget()

        except:
            self.librarytitlelabel.pack_forget()
            self.booklibrarytopframe.pack_forget()
            self.booklibrarybtnframe.pack_forget()
            self.booklibrarygifframe.pack_forget()
            self.booklibrarymainframe.pack_forget()
            self.booklibrarydelframe.pack_forget()
            self.booklibraryeditframe.pack_forget()
            self.bookeditchkframe.pack_forget()
            self.bookeditlablframe.pack_forget()
            self.dashboardframe.grid_configure(row=2, column=0, pady=20, padx=20, sticky="nsew")
            self.titlelabelframe.grid_configure(row=0, column=0, columnspan=10,pady=20, padx=20) 

## Main function to run the app
if __name__ == "__main__":
    app = App()
    app.mainloop()
