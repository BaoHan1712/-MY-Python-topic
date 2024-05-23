import tkinter as tk
from tkinter import *
import mysql.connector
from tkinter import messagebox
from datetime import datetime

root = Tk()
root.title("Insert Data")
root.configure(bg='lightblue')

# Kết nối database
connection = mysql.connector.connect(host='localhost', user='root', password='', port='3306', database='test')                            
c = connection.cursor()

frame = tk.Frame(root, bg='lightblue')

# bảng 1
label_MSNC = tk.Label(frame, text="Enter MSNC", font=('verdana',12),bg='lightblue')
entry_MSNC = tk.Entry(frame, font=('verdana',12))

label_lastname = tk.Label(frame, text="Last Name: ", font=('verdana',12), bg='lightblue')
entry_lastname = tk.Entry(frame, font=('verdana',12))

label_sex = tk.Label(frame, text="Sex: ", font=('verdana',12),bg='lightblue')
entry_sex = tk.Entry(frame, font=('verdana',12))

label_age = tk.Label(frame, text="Age: ", font=('verdana',12), bg='lightblue')
entry_age = tk.Entry(frame, font=('verdana',12))

# Bảng 2
# label_ngay = tk.Label(frame, text="dd_mm_yyyy ", font=('verdana',12),bg='lightblue')
# entry_ngay = tk.Entry(frame, font=('verdana',12))

# Lấy thời gian bắt đầu
date_start =datetime.now().strftime('%Y-%m-%d')
time_start = datetime.now().strftime('%H:%M:%S')


# Bảng 3
label_city = tk.Label(frame, text="City ", font=('verdana',12),bg='lightblue')
entry_city = tk.Entry(frame, font=('verdana',12))

label_country = tk.Label(frame, text="Country ", font=('verdana',12), bg='lightblue')
entry_country = tk.Entry(frame, font=('verdana',12))


# chỗ để thực hiện insert
def insertData():
    try:
        #Bảng 1
        MSNC = entry_MSNC.get()
        lastname = entry_lastname.get()
        sex = entry_sex.get()
        age = entry_age.get()
        
        # # bảng 2
        # ngay = entry_ngay.get()
        
        #Bảng 3
        city = entry_city.get()
        country = entry_country.get()

        # chèn vào bảng 1
        insert_query_1 = "INSERT INTO `thongtin`(`MSNC`, `lastname`, `sex`, `age`) VALUES (%s,%s,%s,%s)"
        vals_1 = (MSNC,lastname,sex,age)
        c.execute(insert_query_1,vals_1)
        
        # chèn vào bảng 2
        insert_query_2 =  "INSERT INTO `thoigian`(`MSNC`,`date_start`,`time_start`) VALUES (%s,%s,%s)"
        vals_user_2 = (MSNC,date_start,time_start)
        c.execute(insert_query_2,vals_user_2)
        
        # Chèn bảng 3
        insert_query_3 = "INSERT INTO `diachi`(`MSNC`, `city`, `country`) VALUES (%s,%s,%s)"
        vals_3 = (MSNC, city, country)
        c.execute(insert_query_3,vals_3) 
        connection.commit()
        messagebox.showinfo("Update", "Information has been updated")
    except:
        messagebox.showinfo("Error", "Re-enter information")

# Nút nhấn
button_insert = tk.Button(frame, text="Insert", font=('verdana',14), bg='orange', command = insertData)

# Setting vị trí các nút
label_MSNC.grid(row=0, column=0)
entry_MSNC.grid(row=0, column=1, pady=10, padx=10)

label_lastname.grid(row=1, column=0)
entry_lastname.grid(row=1, column=1, pady=10, padx=10)

label_sex.grid(row=2, column=0, sticky='e')
entry_sex.grid(row=2, column=1, pady=10, padx=10)

label_age.grid(row=3, column=0, sticky='e')
entry_age.grid(row=3, column=1, pady=10, padx=10)

# label_ngay.grid(row=4, column=0,sticky='e')
# entry_ngay.grid(row=4, column=1, pady=10, padx=10)

label_city.grid(row=4, column=0,sticky='e')
entry_city.grid(row=4, column=1, pady=10, padx=10)

label_country.grid(row=5, column=0, sticky='e')
entry_country.grid(row=5, column=1, pady=10, padx=10)

button_insert.grid(row=6,column=0, columnspan=2, pady=10, padx=10, sticky='nsew')

frame.grid(row=0, column=0)


root.mainloop()