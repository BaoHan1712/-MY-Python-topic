import tkinter as tk
from tkinter import *
import mysql.connector
from datetime import datetime
from tkinter import messagebox, scrolledtext

root = Tk()
root.title("Insert and Query Data")
root.configure(bg='lightblue')

# Kết nối database
try:
    connection = mysql.connector.connect(host='localhost', user='root', password='', port='3306', database='test')
    cursor = connection.cursor()
except mysql.connector.Error as err:
    messagebox.showerror("Error", f"Failed to connect to MySQL: {err}")
    exit()

frame = tk.Frame(root, bg='lightblue')

# Bảng 1
label_MSNC = tk.Label(frame, text="Enter MSNC", font=('verdana', 12), bg='lightblue')
entry_MSNC = tk.Entry(frame, font=('verdana', 12))

label_lastname = tk.Label(frame, text="Last Name: ", font=('verdana', 12), bg='lightblue')
entry_lastname = tk.Entry(frame, font=('verdana', 12))

label_sex = tk.Label(frame, text="Sex: ", font=('verdana', 12), bg='lightblue')
entry_sex = tk.Entry(frame, font=('verdana', 12))

label_age = tk.Label(frame, text="Age: ", font=('verdana', 12), bg='lightblue')
entry_age = tk.Entry(frame, font=('verdana', 12))

# Lấy thời gian bắt đầu
date_start = datetime.now().strftime('%Y-%m-%d')
time_start = datetime.now().strftime('%H:%M:%S')

# Bảng 3
label_city = tk.Label(frame, text="City ", font=('verdana', 12), bg='lightblue')
entry_city = tk.Entry(frame, font=('verdana', 12))

label_country = tk.Label(frame, text="Country ", font=('verdana', 12), bg='lightblue')
entry_country = tk.Entry(frame, font=('verdana', 12))

# chỗ để thực hiện insert
def insertData():
    try:
        MSNC = entry_MSNC.get()
        lastname = entry_lastname.get()
        sex = entry_sex.get()
        age = entry_age.get()
        city = entry_city.get()
        country = entry_country.get()

        # chèn vào bảng 1
        insert_query_1 = "INSERT INTO `thongtin`(`MSNC`, `lastname`, `sex`, `age`) VALUES (%s,%s,%s,%s)"
        vals_1 = (MSNC, lastname, sex, age)
        cursor.execute(insert_query_1, vals_1)

        # chèn vào bảng 2
        insert_query_2 = "INSERT INTO `thoigian`(`MSNC`,`date_start`,`time_start`) VALUES (%s,%s,%s)"
        vals_user_2 = (MSNC, date_start, time_start)
        cursor.execute(insert_query_2, vals_user_2)

        # Chèn bảng 3
        insert_query_3 = "INSERT INTO `diachi`(`MSNC`, `city`, `country`) VALUES (%s,%s,%s)"
        vals_3 = (MSNC, city, country)
        cursor.execute(insert_query_3, vals_3)

        connection.commit()
        messagebox.showinfo("Update", "Information has been updated")
    except Exception as e:
        messagebox.showerror("Error", f"Re-enter information: {e}")

####################################################################################################################################
# Chức năng show data
def open_sql():
    sql_window1 = tk.Toplevel(root)
    sql_window1.title("Execute MYSQL")

    chat_box = scrolledtext.ScrolledText(sql_window1, width=60, height=20)
    chat_box.grid(row=0, column=0, pady=10, padx=10)
    
    tables = ['thongtin', 'diachi', 'thoigian', 'muctieu_datra']
    for table_name in tables:
        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            column_names = [description[0] for description in cursor.description]
            chat_box.insert(tk.END, f"Table: {table_name}\n")
            chat_box.insert(tk.END, f"{', '.join(column_names)}\n")
            result = cursor.fetchall()
            for row in result:
                chat_box.insert(tk.END, f"{row}\n")
            chat_box.insert(tk.END, "\n")
            connection.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Error executing SQL command: {e}")

####################################################################################################################################
def join_sql1():
    sql_window2 = tk.Toplevel(root)
    sql_window2.title("Execute MYSQL")

    chat_box = scrolledtext.ScrolledText(sql_window2, width=60, height=20)
    chat_box.grid(row=0, column=0, pady=10, padx=10)
    
    try:
        cursor.execute("SELECT thongtin.lastname, thongtin.age, muctieu_datra.REP, muctieu_datra.COUNT FROM thongtin JOIN muctieu_datra ON thongtin.MSNC = muctieu_datra.MSNC")
        column_names = [description[0] for description in cursor.description]
        chat_box.insert(tk.END, f"{', '.join(column_names)}\n")
        result = cursor.fetchall()
        for row in result:
            chat_box.insert(tk.END, f"{row}\n")
        chat_box.insert(tk.END, "\n")
        connection.commit()
    except Exception as e:
        messagebox.showerror("Error", f"Error executing SQL command: {e}")
####################################################################################################################################
def join_sql2():
    sql_window3 = tk.Toplevel(root)
    sql_window3.title("Execute MYSQL")

    chat_box = scrolledtext.ScrolledText(sql_window3, width=60, height=20)
    chat_box.grid(row=0, column=0, pady=10, padx=10)
    
    try:
        cursor.execute("SELECT thongtin.lastname, thongtin.age,diachi.city, diachi.country FROM thongtin JOIN diachi ON thongtin.MSNC = diachi.MSNC")
        column_names = [description[0] for description in cursor.description]
        chat_box.insert(tk.END, f"{', '.join(column_names)}\n")
        result = cursor.fetchall()
        for row in result:
            chat_box.insert(tk.END, f"{row}\n")
        chat_box.insert(tk.END, "\n")
        connection.commit()
    except Exception as e:
        messagebox.showerror("Error", f"Error executing SQL command: {e}")
####################################################################################################################################

# Chức năng custom
def open_sql_window():
    sql_window = tk.Toplevel(root)
    sql_window.title("Execute MYSQL")

    
    chat_box = scrolledtext.ScrolledText(sql_window, width=60, height=20)
    chat_box.grid(row=0, column=0, pady=10, padx=10)
    
    sql_entry = tk.Text(sql_window, width=60, height=3)
    sql_entry.grid(row=1, column=0, pady=5, padx=10)

    def execute_sql():
        sql_command = sql_entry.get("1.0", "end-1c")
        try:
            cursor.execute(sql_command)
            result = cursor.fetchall()
            for row in result:
                chat_box.insert(tk.END, f"{row}\n")
            chat_box.insert(tk.END, "\n")
            connection.commit()
            messagebox.showinfo("Success", "SQL command successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error executing SQL command: {e}")

    execute_button = tk.Button(sql_window, text="Execute", command=execute_sql)
    execute_button.grid(row=3, column=0, pady=5)

################################################################################################################################################
# Chức năng select *
def open_select_window():
    select_window = tk.Toplevel(root)
    select_window.title("Select Table")
    select_window.configure(bg='lightblue')

    label_select = tk.Label(select_window, text="Select ",bg='lightblue', font=('verdana', 12,'bold'))
    label_select.pack(pady=10)

    # Danh sách các bảng
    tables = ["thongtin", "diachi", "thoigian", "muctieu_datra"]
    table_name = StringVar(select_window)
    table_name.set(tables[0])  
    dropdown = OptionMenu(select_window, table_name, *tables)
    dropdown.pack(pady=10)
    
    b_value_label = tk.Label(select_window, text="From",bg='lightblue',font=('verdana', 12,'bold'))
    b_value_label.pack(pady=10)
    
    # Danh sách các cột
    columns = ["*","MSNC", "lastname", "sex", "age","city","country","REP","COUNT","date_start","time_start"]
    columns_na = StringVar(select_window)
    columns_na.set(columns[0])  
    dropdown_column = OptionMenu(select_window, columns_na, *columns)
    dropdown_column.pack(pady=10)
    
    # Cắt ngang -----
    c_value_label = tk.Label(select_window, text="-----------------------------",bg='lightblue',font=('verdana', 12,'bold'))
    c_value_label.pack(pady=10)
    
    # Ô để nhập điều kiện
    where_value_label = tk.Label(select_window, text="Where ",bg='lightblue',font=('verdana', 12,'bold'))
    where_value_label.pack(pady=10)
    
     #Danh sách Cột 2
    columns2 = ["MSNC", "lastname", "sex", "age","city","country","REP","COUNT","date_start","time_start"]
    columns_na2 = StringVar(select_window)
    columns_na2.set(columns2[0])
    dropdown_column2 = OptionMenu(select_window, columns_na2, *columns2)
    dropdown_column2.pack(pady=10)
    
    value_label_b = tk.Label(select_window, text=" = ",bg='lightblue',font=('verdana', 17,'bold'))
    value_label_b.pack(pady=10)
    
    where_value_entry = tk.Entry(select_window, font=('verdana', 12))
    where_value_entry.pack(pady=10)
    
##########################################################################################################################################
   
    def execute_select():
        selected_table = table_name.get()
        select_column = columns_na.get()
        
        try:
            cursor.execute(f"SELECT {select_column} FROM {selected_table}")
            result = cursor.fetchall()
            column_names_1 = [desc[0] for desc in cursor.description]
            select_window.destroy()  
            show_result_window(result,column_names_1)
        except Exception as e:
            messagebox.showerror("Error", f"Error executing SQL command: {e}")
            
    def ifelse_select():
        selected_table = table_name.get()
        select_column = columns_na.get()
        select_column2 = columns_na2.get()
        where_value = where_value_entry.get()
        
        try:
            cursor.execute(f"SELECT {select_column} FROM {selected_table} WHERE {select_column2} = '{where_value}'")
            result_2 = cursor.fetchall()
            column_names_2 = [desc[0] for desc in cursor.description]
            select_window.destroy()  
            show_result_window(result_2,column_names_2)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error executing SQL command: {e}")

    def show_result_window(result,column_names):
        result_window = tk.Toplevel(root)
        result_window.title("Select Results")

        result_box = scrolledtext.ScrolledText(result_window, width=60, height=20)
        result_box.pack(pady=10, padx=10)
        result_box.insert(tk.END, f"{', '.join(column_names)}\n\n")
        for row in result:
            result_box.insert(tk.END, f"{row}\n")
        result_box.insert(tk.END, "\n")
    
    # Ktra xem where có được nhập hay không
    def check_where_value_and_execute():
        where_value = where_value_entry.get()
        if where_value: 
            ifelse_select()
        else:  
            execute_select()   
    # nút select thông thường
    button_export = tk.Button(select_window, text="Export ", font=('verdana', 12), bg='light yellow', command=check_where_value_and_execute)
    button_export.pack(pady=10)
    
    
# Nút nhấn
button_insert = tk.Button(frame, text="Insert Data", font=('verdana', 12), bg='orange', command=insertData)
button_custom = tk.Button(frame, text="Custom", font=('verdana', 12), bg='green', command=open_sql_window)
button_select = tk.Button(frame, text="Query Select ", font=('verdana', 12), bg='yellow', command=open_select_window)
button_show = tk.Button(frame, text="Show data", font=('verdana', 12), bg='green', command=open_sql)
button_join = tk.Button(frame, text="Show join 1", font=('verdana', 12), bg='light green', command=join_sql1)
button_join_2= tk.Button(frame, text="Show join 2", font=('verdana', 12), bg='light green', command=join_sql2)

# Setting vị trí các nút
label_MSNC.grid(row=0, column=0, pady=5, sticky='e')
entry_MSNC.grid(row=0, column=1, pady=5, padx=10)

label_lastname.grid(row=1, column=0, pady=5, sticky='e')
entry_lastname.grid(row=1, column=1, pady=5, padx=10)

label_sex.grid(row=2, column=0, pady=5, sticky='e')
entry_sex.grid(row=2, column=1, pady=5, padx=10)

label_age.grid(row=3, column=0, pady=5, sticky='e')
entry_age.grid(row=3, column=1, pady=5, padx=10)

label_city.grid(row=4, column=0, pady=5, sticky='e')
entry_city.grid(row=4, column=1, pady=5, padx=10)

label_country.grid(row=5, column=0, pady=5, sticky='e')
entry_country.grid(row=5, column=1, pady=5, padx=10)

button_insert.grid(row=6, column=1, pady=20, padx=10, sticky='n')
button_custom.grid(row=6, column=0, pady=20, padx=10, sticky='e')
button_select.grid(row=7, column=1, pady=20, padx=10, sticky='n')
button_show.grid(row=6, column=2, pady=20, padx=10, sticky='e')
button_join.grid(row=7, column=2, pady=20, padx=10, sticky='e')
button_join_2.grid(row=7, column=0, pady=20, padx=10, sticky='e')
frame.grid(row=0, column=0)

root.mainloop()
