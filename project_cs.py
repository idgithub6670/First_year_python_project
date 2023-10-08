import sqlite3
from tkinter import messagebox
from tkinter import *
from tkinter import ttk

def mainwindow() :
    #global menubar
    root = Tk()
    x = root.winfo_screenwidth()/2 - w/2
    y = root.winfo_screenheight()/2 - h/2
    root.geometry("%dx%d+%d+%d"%(w,h,x,y))
    root.config(bg='red')
    root.title("Dev Burger")
    root.option_add('*font',"'Calibri', 16")
    icon = PhotoImage(file='image/welcome.png')
    root.iconphoto(False,icon)
    root.rowconfigure((0,1,2,3),weight=1)
    root.columnconfigure((0,1,2,3),weight=1)
    root.resizable(False, False)
    return root


def createconnection() :
    global conn,cursor
    conn = sqlite3.connect('burger_ALLNEW.db')
    cursor = conn.cursor()

def loginlayout(root):

    global userentry , logo ,pwdentry ,loginframe
    
    root.title("Dev Burger")
    root.option_add('*font',"'Calibri', 16")
    loginframe = Frame(root,bg='white')
    loginframe.rowconfigure((0,1,2,3),weight=1)
    loginframe.columnconfigure((0,1),weight=1)
    emptyMenu = Menu(root) 
    root.config(bg='white',menu=emptyMenu)   
    
    logo = Label(loginframe,image=logowelcome,bg='white')
    logo.grid(row=0,column=0,columnspan=4)

    Label(loginframe,text="Login/Register Dev Burger",font="Calibri 26 bold",bg='white',fg='#000000').grid(row=1,columnspan=2)
    
    Label(loginframe,text="Username : ",bg='white',fg='#000000',padx=20).grid(row=2,column=0,sticky='e')
    userentry = Entry(loginframe,bg='yellow',width=20,textvariable=userinfo)
    userentry.grid(row=2,column=1,sticky='w',padx=20)
    Label(loginframe,text="Password  : ",bg='white',fg='#000000',padx=20).grid(row=3,column=0,sticky='e')
    pwdentry = Entry(loginframe,bg='gray',width=20,show='*',textvariable=pwdinfo)
    pwdentry.grid(row=3,column=1,sticky='w',padx=20)
    Button(loginframe,text="Login",width=10,command=loginclick,font=('Helvetica', 14)).grid(row=4,column=0,columnspan=2,padx=20,pady=20)
    #Button(loginframe,text="Exit",width=10,command=,font=('Helvetica', 14)).grid(row=4,column=0,columnspan=2,padx=20,pady=20)
    loginframe.grid(row=1,column=1,columnspan=2,rowspan=2,sticky='news')
    userentry.focus_force()


def loginclick():
    global usershow

    if userinfo.get() == "":
        messagebox.showwarning("ADMIN:","Please enter Username")
        userentry.focus_force()
    else:
        sql = "select * from employee where emp_username=?" 
        cursor.execute(sql,[userinfo.get()])
        result = cursor.fetchall()
        if result :
            if pwdinfo.get() ==  "":
                messagebox.showwarning("ADMIN","Please enter password")
                pwdentry.focus_force()
            else :
                sql = "select * from employee where emp_username=? AND emp_password=?"
                cursor.execute(sql,[userinfo.get(),pwdinfo.get()])
                result = cursor.fetchone()
                if result:
                    messagebox.showwarning("ADMIN","Login successfully")
                    if result[7] == 'admin':
                        userentry.delete(0, END)
                        pwdentry.delete(0, END)
                        showprofileadmin(result[1])
                        usershow = result[1]
                    else:
                        userentry.delete(0, END)
                        pwdentry.delete(0, END)
                        showprofile(result[1])
                        usershow = result[1]
                else:
                    messagebox.showwarning("ADMIN","Incorrect Password")
                    pwdentry.select_range(0,END)
                    pwdentry.focus_force()
        else :
            messagebox.showwarning("ADMIN","Username not found\nPlease register before login")


def showprofile(user) :
    global profile_frm,pro_fname,pro_lname,pro_id
    loginframe.destroy()
    
    profile_frm = Frame(root,bg='white',)
    profile_frm.option_add('*font',"'Calibri', 18")
    profile_frm.columnconfigure((0,1,2,3),weight=1)
    profile_frm.place(x=0,y=0,width=w,height=h)

    sql_user = 'SELECT emp_code,emp_fname,emp_lname From employee where emp_username=? '
    cursor.execute(sql_user,[user])
    result = cursor.fetchone()

    logo = Label(profile_frm,image=logowelcome,bg='white')
    logo.grid(row=0,column=0,columnspan=4)
    Label(profile_frm,text='EMP_Code : ',bg='white').grid(row=1,column=1)
    Label(profile_frm,text='First name : ',bg='white').grid(row=2,column=1)
    Label(profile_frm,text='Last name : ',bg='white').grid(row=3,column=1)
    #Label(profile_frm,text='Phone : ',bg='white').grid(row=3,column=1)
    #Label(profile_frm,text='Address : ',bg='white').grid(row=4,column=1)
    pro_id = Entry(profile_frm,textvariable=showproempid,bg='white',state=DISABLED)
    pro_id.grid(row=1,column=2,sticky='w')
    pro_fname = Entry(profile_frm,textvariable=showprofname,bg='white',state=DISABLED)
    pro_fname.grid(row=2,column=2,sticky='w')
    pro_lname = Entry(profile_frm,textvariable=showprolname,bg='white',state=DISABLED)
    pro_lname.grid(row=3,column=2,sticky='w')
    #pro_phone = Entry(profile_frm,textvariable=showprophone,bg='white',state=DISABLED)
    #pro_phone.grid(row=3,column=2,sticky='w')
    #pro_address = Entry(profile_frm,textvariable=showproaddress,bg='white',state=DISABLED)
    #pro_address.grid(row=4,column=2,sticky='w')

    Button(profile_frm,text='Change Password',command=changepassword).grid(row=5,column=0,sticky='se')
    Button(profile_frm,text='Edit Profile',command=editprofile).grid(row=5,column=1,sticky='s')
    Button(profile_frm,text="Let's dev burger",command=menu).grid(row=5,column=2,sticky='s')
    Button(profile_frm,text='Logout',command=logoutclick).grid(row=5,column=3,sticky='sw')

    showproempid.set(result[0])
    showprofname.set(result[1])
    showprolname.set(result[2])
    #showprophone.set(result[2])
    #showproaddress.set(result[3])

def showprofileadmin(usershow) :
    global adminframe
    global p_id, p_name, p_price,mytree,search_box,p_tid
    loginframe.destroy()

    sql = "select * from employee where emp_username=?" 
    cursor.execute(sql,[usershow])
    result = cursor.fetchone()
    
    root.title("Maneger Burger : "+ result[2]+" "+result[3])
    adminframe = Frame(root, bg='skyblue')
    adminframe.columnconfigure((0,1,2,3,4,5),weight=1)
    adminframe.rowconfigure((0,1,2,3,4),weight=1)
    
    Label(adminframe,text='Maneger Burger : '+result[3]+" "+result[4],bg='skyblue', fg='white',font='calibri 18 bold',padx=20).grid(row=0,column=0,columnspan=2,sticky='w')
    
    search_box = Entry(adminframe, width=50)
    search_box.grid(row=1,column=1,columnspan=3,ipady=8,padx=10)
    Button(adminframe, text='Search',command=fetch_search).grid(row=1,column=3,padx=20,sticky='e')
    Button(adminframe, text='Show all',command=fetch_tree).grid(row=1,column=4,padx=20,sticky='w')

    mytree = ttk.Treeview(adminframe, columns=('type','ingredient','price','xxxtest'),height=2)
    
    mytree.heading('#0',text='')
    mytree.heading('type',text='ID',anchor=CENTER)
    mytree.heading('ingredient',text='Ingredient',anchor=CENTER)
    mytree.heading('price',text='Price',anchor=CENTER)
    mytree.heading('xxxtest',text='Type',anchor=CENTER)
    
    mytree.column('#0',width=0,minwidth=0)
    mytree.column('type',anchor=CENTER,width=200)
    mytree.column('ingredient',anchor=CENTER,width=200)
    mytree.column('price',anchor=CENTER,width=200)
    mytree.column('xxxtest',anchor=CENTER,width=200)

    mytree.grid(row=2,column=0,columnspan=6,sticky='ns')
    mytree.bind('<Double-1>',treeviewclick)
    fetch_tree()
    
    tree_scrollbar = ttk.Scrollbar(adminframe,orient="vertical", command=mytree.yview)
    tree_scrollbar.grid(row=2,column=4,sticky='ns')
    mytree.configure(yscrollcommand=tree_scrollbar.set)
    
    Label(adminframe,text='ID',bg='skyblue',fg='white').grid(row=3,column=1,sticky='wes')
    p_id = Entry(adminframe,width=15,bg='#d3e0ea',justify='center',font="Calibri 12", textvariable=ingid)
    p_id.grid(row=4,column=1,ipady=10,sticky='new')
    
    Label(adminframe,text='Ingredient',bg='skyblue',fg='white').grid(row=3,column=2,sticky='wes')
    p_name = Entry(adminframe,width=15,bg='#d3e0ea',justify='center',font="Calibri 12", textvariable=ingname)
    p_name.grid(row=4,column=2,ipady=10,sticky='nwe')

    Label(adminframe,text='Price',bg='skyblue',fg='white').grid(row=3,column=3,sticky='wes')
    p_price = Entry(adminframe,width=15,bg='#d3e0ea',justify='center',font="Calibri 12", textvariable=ingprice)
    p_price.grid(row=4,column=3,ipady=10,sticky='nwe')

    Label(adminframe,text='T_id',bg='skyblue',fg='white').grid(row=3,column=4,sticky='wes')
    p_tid = Entry(adminframe,width=15,bg='#d3e0ea',justify='center',font="Calibri 12", textvariable=tid)
    p_tid.grid(row=4,column=4,ipady=10,sticky='nwe')
    
    Button(adminframe,text="Add record", font=('Helvetica', 14),command=add_record).grid(row=5,column=1,padx=10,pady=10)
    Button(adminframe,text="Update record",  font=('Helvetica', 14),command=update_record).grid(row=5,column=2,padx=10,pady=10,sticky='w')
    Button(adminframe,text="Remove Selected",  font=('Helvetica', 14),command=remove_one).grid(row=5,column=3,padx=10,pady=10,sticky='w')
    Button(adminframe,text="Clear",  font=('Helvetica', 14),command=clear_data).grid(row=5,column=4,padx=10,pady=10,sticky='w')

    Button(adminframe,text="Add Employee",font='calibri 16 bold',command=register_employee,width=15).grid(row=6,column=2,padx=10,pady=10)
    Button(adminframe,text="History",font='calibri 16 bold',command=history,width=10).grid(row=6,column=3,padx=10,pady=10)
    Button(adminframe,text="Log out",font='calibri 16 bold',command=logoutadmin,width=10).grid(row=6,column=5,padx=10,pady=10,sticky='e')
    
    adminframe.grid(row=0,column=0,columnspan=4,rowspan=5,sticky='news')

def fetch_tree():
    mytree.delete(*mytree.get_children())
    sql = 'select ing_id, ing_name, ing_price, t_name from ingredients JOIN type ON ingredients.t_id = type.t_id'
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        for i,data in enumerate(result):
            mytree.insert('','end',values=(data[0],data[1],data[2],data[3]))


def fetch_search():
    mytree.delete(*mytree.get_children())
    sql = 'select * from ingredients WHERE ing_name=?'
    cursor.execute(sql,[search_box.get()])
    result = cursor.fetchall()
    if result:
        for i,data in enumerate(result):
            mytree.insert('','end',values=(data[0],data[1],data[2],data[3]))

def treeviewclick(event):
    food = mytree.item(mytree.focus(),'values')
    ingid.set(food[0])
    ingname.set(food[1])
    ingprice.set(food[2])
    tid.set(food[3])


def add_record() :
    if ingid.get() == '':
        messagebox.showwarning('Admin','Enter ID first')
    else:
        sql = 'INSERT INTO ingredients ("ing_id","ing_name","ing_price","t_id")VALUES(?,?,?,?) '
        cursor.execute(sql,[ingid.get(),ingname.get(),ingprice.get(),tid.get()])
        conn.commit()
        messagebox.showinfo('Admin','Add menu successfully')
        clear_data()
        fetch_tree()
    
def update_record() :
    if ingid.get() == '':
        messagebox.showwarning('Admin','Enter ID first')
    else:
        food = mytree.item(mytree.focus(),'values')
        old_food_name = food[1]
        sql = '''
            UPDATE ingredients
            SET ing_id=?,ing_name=?,ing_price=?,t_id=?
            WHERE t_id=? and ing_name=?
        '''
        cursor.execute(sql,[ingid.get(),ingname.get(),ingprice.get(),tid.get(),old_food_name,ingname.get()])
        conn.commit()
        messagebox.showinfo('Admin','Update menu successfully')
        clear_data()
        fetch_tree()

def remove_one() :
    msg = messagebox.askquestion('Delete','Are you sure you want to delete this product',icon='warning')
    if msg == 'no':
        clear_data()
    else:
        food = mytree.item(mytree.focus(),'values')
        sql ='DELETE FROM ingredients WHERE t_id=? and ing_name=?'
        cursor.execute(sql,[food[3],food[1]])
        conn.commit()
        clear_data()
        fetch_tree()

def history() :
    global adminframeh
    global p_id,p_name,price,mytree1,search_box1
    loginframe.destroy()

    sql = "select * from employee where emp_username=?" 
    cursor.execute(sql,[usershow])
    result = cursor.fetchone()
    
    root.title("Welcome : "+ result[3]+" "+result[4])
    adminframeh = Frame(root, bg='skyblue')
    adminframeh.columnconfigure((0,1,2,3,4),weight=1)
    adminframeh.rowconfigure((0,1,2,3,4),weight=1)
    
    Label(adminframeh,text='Welcome : '+result[3]+" "+result[4],bg='skyblue', fg='white',font='calibri 18 bold',padx=20).grid(row=0,column=0,columnspan=2,sticky='w')
    
    search_box1 = Entry(adminframeh, width=35)
    search_box1.grid(row=1,column=0,columnspan=3,sticky='e',ipady=8,padx=10)
    Button(adminframeh, text='Search',command=fetch_search1).grid(row=1,column=3,padx=20,sticky='w')
    Button(adminframeh, text='Show all',command=fetch_tree1).grid(row=1,column=3,padx=20)

    mytree1 = ttk.Treeview(adminframeh, columns=('username','egg','cucumber','onion','tomato','lettuce','mushroom','bread','cheese','bacon','meat','frenchfries','cola','price'),height=2)
    
    mytree1.heading('#0',text='')
    mytree1.heading('username',text='username',anchor=CENTER)
    mytree1.heading('egg',text='egg',anchor=CENTER)
    mytree1.heading('cucumber',text='cucumber',anchor=CENTER)
    mytree1.heading('onion',text='onion',anchor=CENTER)
    mytree1.heading('tomato',text='tomato',anchor=CENTER)
    mytree1.heading('lettuce',text='lettuce',anchor=CENTER)
    mytree1.heading('mushroom',text='mushroom',anchor=CENTER)
    mytree1.heading('bread',text='bread',anchor=CENTER)
    mytree1.heading('cheese',text='cheese',anchor=CENTER)
    mytree1.heading('bacon',text='bacon',anchor=CENTER)
    mytree1.heading('meat',text='meat',anchor=CENTER)
    mytree1.heading('frenchfries',text='frenchfries',anchor=CENTER)
    mytree1.heading('cola',text='cola',anchor=CENTER)
    mytree1.heading('price',text='price',anchor=CENTER)
    
    mytree1.column('#0',width=0,minwidth=0)
    mytree1.column('username',anchor=CENTER,width=90)
    mytree1.column('egg',anchor=CENTER,width=90)
    mytree1.column('cucumber',anchor=CENTER,width=90)
    mytree1.column('onion',anchor=CENTER,width=90)
    mytree1.column('tomato',anchor=CENTER,width=90)
    mytree1.column('lettuce',anchor=CENTER,width=90)
    mytree1.column('mushroom',anchor=CENTER,width=90)
    mytree1.column('bread',anchor=CENTER,width=90)
    mytree1.column('cheese',anchor=CENTER,width=90)
    mytree1.column('bacon',anchor=CENTER,width=90)
    mytree1.column('meat',anchor=CENTER,width=90)
    mytree1.column('frenchfries',anchor=CENTER,width=90)
    mytree1.column('cola',anchor=CENTER,width=90)
    mytree1.column('price',anchor=CENTER,width=90)

    mytree1.grid(row=2,column=0,columnspan=5,sticky='ns')
    fetch_tree1()
    
    tree_scrollbar_h = ttk.Scrollbar(adminframeh,orient="vertical", command=mytree1.yview)
    tree_scrollbar_h.grid(row=2,column=4,sticky='ns')
    mytree1.configure(yscrollcommand=tree_scrollbar_h.set)

    Button(adminframeh,text="Back to update",  font=('Helvetica', 14),command=backtoupdate).grid(row=5,column=2,padx=10,pady=10,sticky='w')
    Button(adminframeh,text="Logout",  font=('Helvetica', 14),command=logoutadminh).grid(row=5,column=2,padx=10,pady=10,sticky='e')
    
    adminframeh.grid(row=0,column=0,columnspan=4,rowspan=5,sticky='news')

def fetch_tree1():
    mytree1.delete(*mytree1.get_children())
    sql = 'select * from receipt'
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        for i,data in enumerate(result):
            mytree1.insert('','end',values=(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13]))


def fetch_search1():
    mytree1.delete(*mytree1.get_children())
    sql = 'select * from history WHERE username=?'
    cursor.execute(sql,[search_box1.get()])
    result = cursor.fetchall()
    if result:
        for i,data in enumerate(result):
            mytree1.insert('','end',values=(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13]))
    
def clear_data():
    p_id.delete(0, END)
    p_name.delete(0, END)
    p_price.delete(0, END)
    p_tid.delete(0, END)
    

def logoutadmin() :
    adminframe.destroy()
    loginlayout(root) 
    resetlogin()

def logoutadminh() :
    adminframeh.destroy()
    adminframe.destroy()
    loginlayout(root) 
    resetlogin()

def backtoupdate():
    adminframeh.destroy()

def resetlogin():
    userentry.delete(0, END)
    pwdentry.delete(0,END)
    userentry.focus_force()


def register_employee() :
    global firstname,lastname,newuser,newpwd,cfpwd,regisframe,address,phone
    adminframe.destroy()
    
    root.title("Welcome to Employee Registration : ")
    root.config(bg='white')
    regisframe = Frame(root,bg='white')
    regisframe.rowconfigure((0,1,2,3,4,5,6),weight=1)
    regisframe.columnconfigure((0,1),weight=1)
    Label(regisframe,text="Employee information",font="Garamond 26 bold",fg='#000000',image=logowelcome,compound=TOP,bg='white').grid(row=0,column=0,columnspan=2,sticky='news',pady=10)
    Label(regisframe,text='Frist name : ',bg='white',fg='#000000').grid(row=1,column=0,sticky='e',padx=10)
    firstname = Entry(regisframe,width=20,bg='white',textvariable=fname)
    firstname.grid(row=1,column=1,sticky='w',padx=10)
    Label(regisframe,text='Last name : ',bg='white',fg='#000000').grid(row=2,column=0,sticky='e',padx=10)
    lastname = Entry(regisframe,width=20,bg='white',textvariable=lname)
    lastname.grid(row=2,column=1,sticky='w',padx=10)
    Label(regisframe,text="Phone number : ",bg='white',fg='#000000').grid(row=3,column=0,sticky='e',padx=10)
    phone = Entry(regisframe,width=20,bg='white',textvariable=phoneinfo)
    phone.grid(row=3,column=1,sticky='w',padx=10)
    Label(regisframe,text="Address : ",bg='white',fg='#000000').grid(row=4,column=0,sticky='e',padx=10)
    address = Entry(regisframe,width=20,bg='white',textvariable=addressinfo)
    address.grid(row=4,column=1,sticky='w',padx=10)
    Label(regisframe,text="Username : ",bg='white',fg='#000000').grid(row=5,column=0,sticky='e',padx=10)
    newuser = Entry(regisframe,width=20,bg='white',textvariable=newuserinfo)
    newuser.grid(row=5,column=1,sticky='w',padx=10)
    Label(regisframe,text="Password : ",bg='white',fg='#000000').grid(row=6,column=0,sticky='e',padx=10)
    newpwd = Entry(regisframe,width=20,bg='#a1cae2',textvariable=newpwdinfo,show='*')
    newpwd.grid(row=6,column=1,sticky='w',padx=10)
    Label(regisframe,text="Confirm Password : ",bg='white',fg='#000000').grid(row=7,column=0,sticky='e',padx=10)
    cfpwd = Entry(regisframe,width=20,bg='#a1cae2',textvariable=cfinfo,show='*')
    cfpwd.grid(row=7,column=1,sticky='w',padx=10)
    regisaction = Button(regisframe,text="Register Submit",command=registration)
    regisaction.grid(row=8,column=0,columnspan=2,ipady=5,ipadx=5,pady=5)
    cancel_regis = Button(regisframe,text="Cancel",command=cancelregistration)
    cancel_regis.grid(row=8,column=1,columnspan=2,ipady=5,ipadx=5,pady=5)
    firstname.focus_force()
    regisframe.grid(row=1,column=1,columnspan=2,rowspan=2,sticky='news')

def registration() :
    
    if fname.get() == "" :
        messagebox.showwarning("Admin: ","Please enter First name")
        firstname.focus_force()
    elif lname.get() == "" :
        messagebox.showwarning("Admin: ","Pleasse enter Last name")
        lastname.focus_force()
    elif phone.get() =="":
        messagebox.showwarning("Admin: ","Pleasse enter Phone number")
        phone.focus_force()
    elif address.get() == "":
        messagebox.showwarning("Admin: ","Pleasse enter Your address")
        address.focus_force()
    elif newuserinfo.get() == "" :
        messagebox.showwarning("Admin: ","Please enter a new Username")
        newuser.focus_force()
    elif newpwdinfo.get() == "" :
        messagebox.showwarning("Admin: ","Please enter a Password")
        newpwd.focus_force()
    elif cfinfo.get() == "" :
        messagebox.showwarning("Admin: ","Please enter a Confirm password")
        cfpwd.focus_force()
    else :
        sql = "select * from employee where emp_username=?"
        cursor.execute(sql,[newuserinfo.get()])
        result = cursor.fetchall()
        if result :
            messagebox.showerror("Admin:","The username is already exists")
            newuser.select_range(0,END)
            newuser.focus_force()
        else :
            if newpwdinfo.get() == cfinfo.get() :
                sql = "select emp_code from employee ORDER BY emp_code DESC LIMIT 1"
                cursor.execute(sql)
                new_emp_id = cursor.fetchall()
                new_emp_id = (new_emp_id[-1][-1]) + 1
                sql = "insert into employee values (?,?,?,?,?,?,?,?)"

                cursor.execute(sql,[new_emp_id, newuserinfo.get(),newpwdinfo.get(),fname.get(),lname.get(),phoneinfo.get(),addressinfo.get(),'Employee'])
                conn.commit()
                messagebox.showinfo("Admin:","Registration Successfully")
                newuser.delete(0,END)
                newpwd.delete(0,END)
                cfpwd.delete(0,END)
                phone.delete(0,END)
                firstname.delete(0,END)
                lastname.delete(0,END)
                address.delete(0,END)

                

            else :
                messagebox.showwarning("Admin: ","Incorrect a confirm password\n Try again")
                cfpwd.selection_range(0,END)
                cfpwd.focus_force()

def cancelregistration():
    regisframe.destroy()
    loginlayout(root)

def changepassword():
    global old_pass,new_pass,connew_pass,changef
    profile_frm.destroy()

    root.title('Change Password') 
    changef = Frame(root, bg='white')
    changef.columnconfigure((0,1,2),weight=1)
    changef.rowconfigure((0,1,2,3,4),weight=1)
    changef.grid(row=0,column=0,columnspan=4,rowspan=4)


    logo = Label(changef,image=logowelcome,bg='white')
    logo.grid(row=0,column=0,columnspan=3,sticky='ew')

    Label(changef,text='Old Password:',bg='white').grid(row=1,column=0,sticky='e',padx=10)
    old_pass = Entry(changef,width=20 ,bg='white',textvariable=oldpass_info)
    old_pass.grid(row=1,column=1,sticky='w',padx=10)

    Label(changef,text='New Password:',bg='white').grid(row=2,column=0,sticky='e',padx=10)
    new_pass = Entry(changef,width=20 ,bg='white',textvariable=newpass_info)
    new_pass.grid(row=2,column=1,sticky='w',padx=10)

    Label(changef,text='Confirm New Password:',bg='white').grid(row=3,column=0,sticky='e',padx=10)
    connew_pass = Entry(changef,width=20 ,bg='white',textvariable=confirmpass_info)
    connew_pass.grid(row=3,column=1,sticky='w',padx=10)

    Button(changef,text="Confirm",command=confrim_click).grid(row=4,column=0,pady=20)
    Button(changef,text="Cancel",command=cancel_click).grid(row=4,column=1,pady=20)

def confrim_click():
    if oldpass_info.get() =='':
        messagebox.showwarning('Admin','Please Enter Old Password')
        old_pass.focus_force()
    else:
        sql = "SELECT * from employee where emp_username=? AND emp_password=?"
        cursor.execute(sql,[usershow,oldpass_info.get()])
        result = cursor.fetchone()
        if result:
            if newpass_info.get() =='':
                messagebox.showwarning('Admin','Please enter new password')
                new_pass.focus_force()
            elif confirmpass_info.get()=='':
                messagebox.showwarning('Admin','Please enter confirm password')
                connew_pass.focus_force()
            else:
                if new_pass.get() == connew_pass.get():
                    sql = 'update employee set emp_password=? where emp_username=?'
                    cursor.execute(sql,[newpass_info.get(),usershow])
                    conn.commit()
                    messagebox.showinfo('Admin','Change password successfully')
                    old_pass.delete(0,END)
                    new_pass.delete(0,END)
                    connew_pass.delete(0,END)
                else:
                    messagebox.showwarning("Admin","Confirm password does'n match")
                    connew_pass.focus_force()
        else:
            messagebox.showwarning("Admin","Incorrect Old password")
            old_pass.focus_force()

def cancel_click():
    changef.destroy()
    loginlayout(root)

def logoutclick():
    profile_frm.destroy()
    loginlayout(root)
    resetlogin()

def editprofile():
    pro_fname.config(state=NORMAL)
    pro_lname.config(state=NORMAL)
    #pro_phone.config(state=NORMAL)
    #pro_address.config(state=NORMAL)
    Button(profile_frm,text='Update',command=update_data,height=1).grid(row=5,column=2,sticky='w')

def update_data():
    print('saved')
    sql = '''
            UPDATE employee
            SET emp_fname=?,emp_lname=?
            WHERE emp_username=?
    '''

    cursor.execute(sql,[pro_fname.get(),pro_lname.get(),usershow])
    conn.commit()
    messagebox.showinfo('Admin','Update Successfully')
    profile_frm.destroy()
    showprofile(usershow)


def menu():
    global price,totalprice,menuframe
    global spinegg,spincucumber,spinonion,spintomato,spinlettuce,spinmushroom
    global spinbread,spincheese,spinbacon,spinmeat,spinfrench,spincola
    global amount
    totalprice.set("%d Baht"%(20))
    menuframe = Frame(root,bg='white')
    menuframe.rowconfigure((0,1,2,3,4,5),weight=1)
    menuframe.columnconfigure((0,1,2),weight=1)
    menuframe.grid(row=0,column=0,columnspan=4,rowspan=4,sticky='news')
    image1 = [egg,tang,onien,tomato,puk,mushroom]
    text1 = ["Egg","Cucumber","Onion","Tomato","Lettuce","Mushroom"]
    image2 = [bread,cheese,bacon,meat,ff,cola]
    text2 = ["Bread","Cheese","Bacon","Meat","French fries","Cola"]

    for i,images in enumerate(image1):
        Label(menuframe,bg='white',image=images).grid(row=i,column=0,pady=5,sticky='w')
        for i,texts in enumerate(text1):
            Label(menuframe,bg='white',text=texts).grid(row=i,column=0,pady=5,sticky='n')

    for i,images in enumerate(image2):
        Label(menuframe,bg='white',image=images).grid(row=i,column=1,pady=5,sticky='w')
        for i,texts in enumerate(text2):
            Label(menuframe,bg='white',text=texts).grid(row=i,column=1,pady=5,sticky='n')

    sql = "SELECT ing_name FROM ingredients WHERE t_id='101'"
    cursor.execute(sql)
    result_egg = cursor.fetchall()
    spinegg = Spinbox(menuframe,values=result_egg,width=10,command=calculate,justify=CENTER)
    spinegg.grid(row=0,column=0,padx=40,pady=5)

    sql = "SELECT ing_name FROM ingredients WHERE t_id='102'"
    cursor.execute(sql)
    result_cucumber = cursor.fetchall()
    spincucumber = Spinbox(menuframe,values=result_cucumber,width=10,command=calculate,justify=CENTER)
    spincucumber.grid(row=1,column=0,pady=5)

    sql = "SELECT ing_name FROM ingredients WHERE t_id='103'"
    cursor.execute(sql)
    result_onion = cursor.fetchall()
    spinonion = Spinbox(menuframe,bg='white',values=result_onion,width=10,command=calculate,justify=CENTER)
    spinonion.grid(row=2,column=0,pady=5)

    sql = "SELECT ing_name FROM ingredients WHERE t_id='104'"
    cursor.execute(sql)
    result_tomato = cursor.fetchall()
    spintomato = Spinbox(menuframe,bg='white',values=result_tomato,width=10,command=calculate,justify=CENTER)
    spintomato.grid(row=3,column=0,pady=5)

    sql = "SELECT ing_name FROM ingredients WHERE t_id='105'"
    cursor.execute(sql)
    result_lecttuce = cursor.fetchall()
    spinlettuce = Spinbox(menuframe,bg='white',values=result_lecttuce,width=10,command=calculate,justify=CENTER)
    spinlettuce.grid(row=4,column=0,pady=5)

    sql = "SELECT ing_name FROM ingredients WHERE t_id='106'"
    cursor.execute(sql)
    result_mushroom = cursor.fetchall()
    spinmushroom = Spinbox(menuframe,bg='white',values=result_mushroom,width=10,command=calculate,justify=CENTER)
    spinmushroom.grid(row=5,column=0,pady=5)

    sql = "SELECT ing_name FROM ingredients WHERE t_id='107'"
    cursor.execute(sql)
    result_bread = cursor.fetchall()
    spinbread = Spinbox(menuframe,bg='white',values=result_bread,width=10,command=calculate,justify=CENTER)
    spinbread.grid(row=0,column=1,padx=40,pady=5)

    sql = "SELECT ing_name FROM ingredients WHERE t_id='108'"
    cursor.execute(sql)
    result_cheese = cursor.fetchall()
    spincheese = Spinbox(menuframe,bg='white',values=result_cheese,width=10,command=calculate,justify=CENTER)
    spincheese.grid(row=1,column=1,pady=5)

    sql = "SELECT ing_name FROM ingredients WHERE t_id='109'"
    cursor.execute(sql)
    result_bacon = cursor.fetchall()
    spinbacon = Spinbox(menuframe,bg='white',values=result_bacon,width=10,command=calculate,justify=CENTER)
    spinbacon.grid(row=2,column=1,pady=5)

    sql = "SELECT ing_name FROM ingredients WHERE t_id='110'"
    cursor.execute(sql)
    result_meat = cursor.fetchall()
    spinmeat = Spinbox(menuframe,bg='white',values=result_meat,width=10,command=calculate,justify=CENTER)
    spinmeat.grid(row=3,column=1,pady=5)

    sql = "SELECT ing_name FROM ingredients WHERE t_id='111'"
    cursor.execute(sql)
    result_french = cursor.fetchall()
    spinfrench = Spinbox(menuframe,bg='white',values=result_french,width=10,command=calculate,justify=CENTER)
    spinfrench.grid(row=4,column=1,pady=5)

    sql = "SELECT ing_name FROM ingredients WHERE t_id='112'"
    cursor.execute(sql)
    result_cola = cursor.fetchall()
    spincola = Spinbox(menuframe,bg='white',values=result_cola,width=10,command=calculate,justify=CENTER)
    spincola.grid(row=5,column=1,pady=5)

    amount = Spinbox(menuframe,width=10,from_=1,to=10,command=calculate)
    amount.grid(row=4,column=2,sticky='n')

    Label(menuframe,text="Choose burger ingredients",bg='white').grid(row=0,column=2)
    Label(menuframe,textvariable=totalprice,bg='white').grid(row=1,column=2)
    Button(menuframe,text="Check bill",command=checkbin).grid(row=2,column=2,sticky='n')
    Label(menuframe,bg='white',text="Amount").grid(row=3,column=2)
    Button(menuframe,text="Cancel",command=cancell2).grid(row=5,column=2)
    calculate()

def calculate():
    global eggprice,cucumberprice,onionprice,tomatoprice,lettuceprice,mushroomprice
    global breadprice,cheeseprice,baconprice,meatprice,frenchprice,colaprice
    global realtotalprice,multiprice,tmp

    sql = "SELECT ing_name,ing_price FROM ingredients WHERE t_id='109' and ing_name=?"
    cursor.execute(sql,[spinbacon.get()])
    resultbacon = cursor.fetchone()
    baconprice = int(resultbacon[1]) 
    
    sql = "SELECT ing_name,ing_price FROM ingredients WHERE t_id='110' and ing_name=?"
    cursor.execute(sql,[spinmeat.get()])
    resultmeat = cursor.fetchone()
    meatprice = int(resultmeat[1])

    sql = "SELECT ing_name,ing_price FROM ingredients WHERE t_id='107' and ing_name=?"
    cursor.execute(sql,[spinbread.get()])
    resultbread = cursor.fetchone()
    breadprice = int(resultbread[1])

    sql = "SELECT ing_name,ing_price FROM ingredients WHERE t_id='108' and ing_name=?"
    cursor.execute(sql,[spincheese.get()])
    resultcheese = cursor.fetchone()
    cheeseprice = int(resultcheese[1])

    sql = "SELECT ing_name,ing_price FROM ingredients WHERE t_id='102' and ing_name=?"
    cursor.execute(sql,[spincucumber.get()])
    resultcucumber = cursor.fetchone()
    cucumberprice = int(resultcucumber[1]) 

    sql = "SELECT ing_name,ing_price FROM ingredients WHERE t_id='101' and ing_name=?"
    cursor.execute(sql,[spinegg.get()])
    resultegg = cursor.fetchone()
    eggprice = int(resultegg[1])

    sql = "SELECT ing_name,ing_price FROM ingredients WHERE t_id='111' and ing_name=?"
    cursor.execute(sql,[spinfrench.get()])
    resultfrench = cursor.fetchone()
    frenchprice = int(resultfrench[1])

    sql = "SELECT ing_name,ing_price FROM ingredients WHERE t_id='105' and ing_name=?"
    cursor.execute(sql,[spinlettuce.get()])
    resultlecttuce = cursor.fetchone()
    lettuceprice = int(resultlecttuce[1]) 

    sql = "SELECT ing_name,ing_price FROM ingredients WHERE t_id='106' and ing_name=?"
    cursor.execute(sql,[spinmushroom.get()])
    resultmushroom = cursor.fetchone()
    mushroomprice = int(resultmushroom[1])

    sql = "SELECT ing_name,ing_price FROM ingredients WHERE t_id='103' and ing_name=?"
    cursor.execute(sql,[spinonion.get()])
    resultonion = cursor.fetchone()
    onionprice = int(resultonion[1])

    sql = "SELECT ing_name,ing_price FROM ingredients WHERE t_id='112' and ing_name=?"
    cursor.execute(sql,[spincola.get()])
    resultcola = cursor.fetchone()
    colaprice = int(resultcola[1])

    sql = "SELECT ing_name,ing_price FROM ingredients WHERE t_id='104' and ing_name=?"
    cursor.execute(sql,[spintomato.get()])
    resulttomato = cursor.fetchone()
    tomatoprice = int(resulttomato[1])

    multi=amount.get()
    multiprice = int(multi)

    realtotalprice = (mushroomprice+eggprice+cucumberprice+onionprice+tomatoprice+lettuceprice+breadprice+cheeseprice+baconprice+meatprice+frenchprice+colaprice)*multiprice
    totalprice.set("%d Baht"%(realtotalprice))
    tmp = realtotalprice

def setdefault():
    menu()
    realtotalprice = 20
    totalprice.set(str("20 Baht"))
    print(realtotalprice)
    

def checkbin():
    global checkframe,total,ree
    checkframe = Frame(root,bg='white')
    checkframe.rowconfigure((0,1,2,3,4,5,6),weight=1)
    checkframe.columnconfigure((0,1,2),weight=1)
    checkframe.grid(row=0,column=0,columnspan=4,rowspan=4,sticky='news')
    sql = "select * from employee where emp_username=?" 
    cursor.execute(sql,[usershow])
    checkbillname = cursor.fetchone()
    
    #logo = Label(checkframe,image=logowelcome,bg='white')
    #logo.grid(row=1,column=0)
    Label(checkframe,text='Customer name : '+checkbillname[3]+" "+checkbillname[4],bg='white').grid(row=3,column=0,columnspan=3)
    #Label(checkframe,text='Phone : '+" "+str(checkbillname[4]),bg='white').grid(row=4,column=0,columnspan=3)
    #Label(checkframe,text='Address : '+" "+str(checkbillname[5]),bg='white').grid(row=5,column=0,columnspan=3)
    #Label(checkframe,text='Receipt',bg='white').grid(row=2,column=0,pady=10,padx=10)
    ree = (spinegg.get(),spincucumber.get(),spinonion.get(),spintomato.get(),spinlettuce.get(),spinmushroom.get(),spinbread.get(),spincheese.get(),spinbacon.get(),spinmeat.get(),spinfrench.get(),spincola.get(),multiprice)
    total += tmp
    for i in ree:
        if i != "none":
            lst.append(i)
    total_lst.append(lst)
    receipt = Label(checkframe,text="%s \n"%lst,bg='white')
    receipt.grid(row=1,column=0,columnspan=3)

    Label(checkframe,text=total,bg='white').grid(row=2,column=2)
    Button(checkframe,text="Another One",command=edit).grid(row=3,column=2,pady=10,padx=10)
    Button(checkframe,text="Checkout",command=checkout).grid(row=4,column=2,pady=10,padx=10)
    Button(checkframe,text="Cancel",command=cancell2).grid(row=5,column=2,pady=10,padx=10)

def checkout():
    global pickframe,total
    pickframe = Frame(root,bg='white')
    pickframe.rowconfigure((0,1,2),weight=1)
    pickframe.columnconfigure(0,weight=1)
    pickframe.grid(row=0,column=0,columnspan=4,rowspan=4,sticky='news')
    #สําหรับตารางใหม่
    sql = "select rec_id from receipt ORDER BY rec_id DESC LIMIT 1"
    cursor.execute(sql)
    rec_id = cursor.fetchall()
    rec_id = (rec_id[-1][-1]) + 1

    sql = "select emp_code from employee where emp_username= ?"
    cursor.execute(sql,[usershow])
    emp_code = cursor.fetchall()
    emp_code = (emp_code[-1][-1])

    sql = 'insert into receipt values (?,?,?,?)'
    cursor.execute(sql,[rec_id,emp_code,str(lst)[1:-1],total])
    conn.commit()
    total = 0

    Label(pickframe,image=burgershop,bg='white').grid(row=0,column=0)
    Label(pickframe,text="Come and grab your burger \n Thanks for buying",bg='white').grid(row=1,column=0)
    Button(pickframe,text="Back to profile",command=cancell1).grid(row=2,column=0)

def cancell1():
    global total
    lst.clear()
    total = 0
    totalprice.set("%d Baht"%(20))
    menuframe.destroy()
    checkframe.destroy()
    pickframe.destroy()
    menuframe.destroy()

def cancell2():
    global total
    lst.clear()
    total = 0
    totalprice.set("%d Baht"%(20))
    menuframe.destroy()
    checkframe.destroy()
    pickframe.destroy()
    menuframe.destroy()

def edit():
    checkframe.destroy()

w = 1500
h = 750
total = 0
lst = []
total_lst = []

createconnection()
root = mainwindow()

logowelcome = PhotoImage(file='image/logo.png').subsample(1,1)
bread = PhotoImage(file='image/pangbon.png').subsample(3,3)
tang = PhotoImage(file='image/tang.png').subsample(3,3)
onien = PhotoImage(file='image/onien.png').subsample(3,3)
tomato = PhotoImage(file='image/tomato.png').subsample(3,3)
mushroom = PhotoImage(file='image/musroom.png').subsample(3,3)
oleave = PhotoImage(file='image/oleave.png').subsample(3,3)
puk = PhotoImage(file='image/puk.png').subsample(3,3)
bacon = PhotoImage(file='image/bacon.png').subsample(3,3)
ham = PhotoImage(file='image/ham.png').subsample(3,3)
cheese = PhotoImage(file='image/cheese.png').subsample(3,3)
cheese2 = PhotoImage(file='image/cheese2.png').subsample(3,3)
egg = PhotoImage(file='image/egg.png').subsample(3,3)
meat = PhotoImage(file='image/beef.png').subsample(3,3)
pork = PhotoImage(file='image/pork.png').subsample(3,3)
ff = PhotoImage(file='image/ff.png').subsample(3,3)
cola = PhotoImage(file='image/cola.png').subsample(3,3)
fish = PhotoImage(file='image/Fish.png').subsample(3,3)
soure = PhotoImage(file='image/soure.png').subsample(3,3)
burgershop = PhotoImage(file='image/burgershop.png').subsample(2,2)
delivery = PhotoImage(file='image/delivery.png').subsample(2,2)

totalprice = StringVar()
totalprice.set(str("20 Baht"))

userinfo = StringVar()
pwdinfo = StringVar()
fname = StringVar()
lname = StringVar()
newuserinfo = StringVar()
newpwdinfo = StringVar()
cfinfo = StringVar()
addressinfo = StringVar()
phoneinfo = StringVar()
oldpass_info = StringVar()
newpass_info = StringVar()
confirmpass_info = StringVar()
firstnameeditinfo = StringVar()
lastnameeditinfo = StringVar()
addresseditinfo = StringVar()
phoneeditinfo = StringVar()
testt = StringVar()
showproempid = StringVar()
showprofname = StringVar()
showprolname = StringVar()
showprophone = StringVar()
showproaddress = StringVar()
ingid = StringVar()
ingname = StringVar()
ingprice = StringVar()
tid = StringVar()
quantity_info = StringVar()

loginlayout(root)

root.mainloop()
cursor.close() 
conn.close()