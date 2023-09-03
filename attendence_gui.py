import pyodbc
from tkinter import *
from tkinter import simpledialog
root=Tk()
root.title("ATTENDENCE INTERFACE")
conn=pyodbc.connect(
    "Driver={SQL Server Native ClienT 11.0};"
    "Server=SIVARAMAKRISHNA\PROJECT_SIVA;"
    "Database=attendence;"
    'Trusted_connection=yes;'
    "uid=siva;"
    "pwd=1234;"
)
class Attendence:
    def __init__(self,username,conn):
        self.username=username
        self.conn=conn
    def creating_table(self):
        print("you are registered for atttendence now you can add subjects")
        cursor=self.conn.cursor()
        cursor.execute("create table {} (sub_name varchar(50) primary key,faculty_name varchar(50),total_classes integer default 0,attend_classes integer default 0, sub_attend_perc float(10) default 0,class_needed integer default 0 )".format(self.username))
        self.conn.commit()
    def add_sub(self):
        user_name=self.username
        sub_name = simpledialog.askstring("sub_name","Enter subject name:",parent=root)
        faculty_name = simpledialog.askstring("faculty_name","Enter faculty name:",parent=root)
        print("{} added".format(sub_name))
        cursor = self.conn.cursor()
        cursor.execute("insert into {} (sub_name,faculty_name) values(?,?)".format(user_name),(sub_name,faculty_name))
        self.conn.commit()
    def update_attend(self):
        user_name=self.username
        cursor = conn.cursor()
        cursor.execute("select sub_name from {}".format(user_name))
        l = []
        for i in list(cursor):
            l.append(*i)
        def pre_obs(sub_name):
            # CORRECT THE BELOW CODE FOR POSITIVE AND NEGATIVE VALUE OF UPDATE
            update = simpledialog.askinteger("ATTTENDENCE_UPDATE", "Enter the no of classes needed to update your attendence:", parent=root)
            temp_update=update
            if update<0:
                temp_update=0
            cursor.execute("update {} set attend_classes=attend_classes+?,total_classes=total_classes+? where sub_name=?".format(user_name), (temp_update,abs(update),sub_name))
            cursor.execute("update {} set sub_attend_perc=round((attend_classes*100)/(total_classes),2) where sub_name=? and total_classes>0".format(user_name),(sub_name))
            cursor.execute("update {} set class_needed=3*(total_classes)-4*(attend_classes) where sub_name=? and sub_attend_perc<75".format(user_name),(sub_name))
            self.conn.commit()
        r,c=3,4
        for j in l:
            temp_but = Button(frame1, text=j, font=("Arial Black", 10), fg="green", bg="white",command=lambda j=j :pre_obs(j))
            temp_but.grid(column=c, row=r)
            r+=1
    def show_data(self):
        user_name=self.username
        cursor=conn.cursor()
        cursor.execute("select sub_name,total_classes,attend_classes,sub_attend_perc,class_needed from {}".format(user_name))
        root2=Tk()
        root2.title("ATTENDENCE_DETAILS")
        l=[]
        for k in cursor:
            l.append(k)
        l1 = ["S.NO", "SUBJECT", "TOTAL_CLASSES", "ATTENDED_CLASSES", "ATTENDENCE", "CLASSES_NEEDED"]
        total_rows = len(l)
        total_columns = len(l1)
        for k in range(total_columns):
            if k == 0:
                e = Entry(root2, width=5, fg="red", bg="lightblue", font=('Arial', 16, 'bold'))
                e.grid(row=0, column=k)
                e.insert(END, l1[k])
            else:
                e = Entry(root2, width=23, fg="red", bg="lightblue", font=('Arial', 16, 'bold'))
                e.grid(row=0, column=k)
                e.insert(END, l1[k])
        for i in range(1, total_rows + 1):
            e = Entry(root2, width=5, fg="green", bg="lightblue", font=('Arial', 16, 'bold'))
            e.grid(row=i, column=0)
            e.insert(END, str(i) + ".")
            for j in range(1, total_columns):
                e = Entry(root2, width=23, fg="green", bg="lightblue", font=('Arial', 16, 'bold'))
                e.grid(row=i, column=j)
                if j == 4:
                    e.insert(END, str(l[i - 1][j - 1]) + " %")
                else:
                    e.insert(END, l[i - 1][j - 1])
        e = Entry(root2, width=5, fg="green", bg="gold", font=('Arial', 16, 'bold'))
        e.grid(row=total_rows+1, column=0)
        cursor.execute("select sum(total_classes) from {}".format(user_name))
        sum_tot_clas=0
        for i in cursor:
            sum_tot_clas=str(i[0])
        cursor.execute("select sum(attend_classes) from {}".format(user_name))
        sum_attend_clas=0
        for i in cursor:
            sum_attend_clas=str(i[0])
        cursor.execute("select round(sum(attend_classes)*100/sum(total_classes),2) as overal_perc from {} where total_classes>0".format(user_name))
        tot_perc=0
        for i in cursor:
            tot_perc=str(i[0])+" %"
        cursor.execute("select 3*sum(total_classes)-4*sum(attend_classes) as total_classes_needed from {} where 75>(select sum(attend_classes)/sum(total_classes*0.01) as overal_perc from {} where total_classes>0)".format(user_name,user_name))
        tot_clas_ned=0
        for i in cursor:
            tot_clas_ned=str(i[0])
        t=["TOTAL",sum_tot_clas,sum_attend_clas,tot_perc,tot_clas_ned]

        for i in range(1,6):
            e = Entry(root2, width=23, fg="blue", bg="gold", font=('Arial', 16, 'bold'))
            e.grid(row=total_rows+1, column=i)
            e.insert(END, t[i-1])
        self.conn.commit()
        root2.mainloop()

def register():
    user_name=simpledialog.askstring("Input","create new username",parent=root)
    obj=Attendence(user_name,conn)
    obj.creating_table()
def login():
    user_name = simpledialog.askstring("Login","Enter your username",parent=root)
    if len(user_name)>0:
        global obj1
        obj1 = Attendence(user_name, conn)
        add_sub_button = Button(frame1, text="ADD_SUBJECT", font=("Arial Black", 15), fg="blue", bg="white", command=obj1.add_sub)
        add_sub_button.grid(column=2, row=1)
        space_l=Label(frame1,text="    ")
        space_l.grid(column=3,row=1)
        update_attendence_button = Button(frame1, text="UPDATE_ATTENDENCE", font=("Arial Black", 15), fg="blue", bg="white",command=obj1.update_attend)
        update_attendence_button.grid(column=4, row=1)
        space_l = Label(frame1, text="    ")
        space_l.grid(column=5, row=1)
        show_data_button = Button(frame1, text="SHOW_DATA", font=("Arial Black", 15), fg="green",bg="white", command=obj1.show_data)
        show_data_button.grid(column=6, row=1)
        entry_label.destroy()
def initial_widgets():
    menu1 = Menu(root)
    root.config(menu=menu1)
    sub_menu = Menu(menu1)
    menu1.add_cascade(label="menu", menu=sub_menu, font=("Arial Black", 15))
    sub_menu.add_command(label="Register", command=register)
    sub_menu.add_separator()
    sub_menu.add_command(label="login", command=login)
    sub_menu.add_separator()
    sub_menu.add_command(label="exit", command=exit)
    global frame1
    frame1 = Frame(root)
    frame1.grid(row=1, column=1, padx=50, pady=50)
    global entry_label
    entry_label = Label(frame1, text="WELCOME TO\n\n!__ATTENDENCE_REGISTER__!\n\nPLEASE LOGIN THROUGH MENU",font=('Arial', 65), fg="green", bg="skyblue")
    entry_label.grid(column=4, row=3)
    root.mainloop()


##CALLING PROGRAM
initial_widgets()