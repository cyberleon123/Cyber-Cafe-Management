from fpdf import FPDF
import random
import math
import datetime
from datetime import datetime, time
from tkinter import*
from tkinter import messagebox

import mysql.connector as sqltor
user_st=str(input("Enter the username of the mysql database: \n"))
pass_st=str(input("Enter the password of mysql database: \n"))

##########################################################################################################
mycon=sqltor.connect(host="localhost",user=user_st,passwd=pass_st)

if mycon.is_connected():
    print("SUCCESSFULLY CONNECTED")                                     #Creating database ccmsdb
cursor=mycon.cursor(buffered=True)
#create database
cursor.execute("""CREATE DATABASE IF NOT EXISTS ccmsdb""")
mycon.commit()
#use database
cursor.execute("""USE ccmsdb""")
mycon.commit()

cursor.execute("CREATE TABLE IF NOT EXISTS tblusers(SrNo integer(20) AUTO_INCREMENT primary key,UserName varchar(120) DEFAULT NULL,UserAddress varchar(200) DEFAULT NULL,MobileNumber bigint(10) DEFAULT NULL,Email varchar(200) DEFAULT NULL,ComputerName varchar(120) DEFAULT NULL,IDProof varchar(120) DEFAULT NULL,InTime timestamp NULL DEFAULT current_timestamp() UNIQUE,OutTime timestamp NULL DEFAULT NULL ON UPDATE current_timestamp(),FEES varchar(120) DEFAULT NULL,RECEIPT_ID integer(30) DEFAULT NULL)")
mycon.commit()
###############################################################################################################


#####################################################################################################   
root=Tk()                               #Main window 
f=Frame(root)
frame1=Frame(root)
frame2=Frame(root)
frame3=Frame(root)

root.title("Cyber Cafe")
root.geometry("830x395")
root.configure(background="black")

scrollbar=Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
#########################################################################################################

#######################################################################################################
firstname=StringVar()                    #Declaration of all variables
lastname=StringVar()
mobile=IntVar()
email=StringVar()
dept=StringVar()
ID=StringVar()
time_in=StringVar()
time_out=StringVar()

searchfirstname=StringVar()
searchlastname=StringVar()
searchmobile=IntVar()


fees=0
######################################################################################################
def tmp_in(tmin):                                    # Intime Manipulation     
    import datetime
    now = datetime.datetime.now()

    tmout=now.strftime("%Y-%m-%d ")
    suut=tmout+tmin+":00"
    return suut

########################################################################################################

def add_entries():                       # Adding Entries to the database by clicking button
    f=firstname.get()
    f1=f.lower()
    l=lastname.get()
    l1=l
    m=mobile.get()
    ed=ID.get()
    em=email.get()
    d=dept.get()
    d1=d
    tmin=time_in.get()
    tmin1=tmp_in(tmin)
    tmout=time_out.get()
###########################################################################################################
    import datetime    
    now = datetime.datetime.now()                  #taking the currect date and time
    
    tmout=now.strftime("%Y-%m-%d %H:%M:%S")
##########################################################################################################
    tmout1=tmout
    fees=prc(tmin1,tmout)
    sam=gst1(fees)
    prom=("Amount to be paid=",sam)
    ################# INSERTING IT IN THE DATABASE
    
    st="INSERT INTO tblusers(Username,UserAddress,MobileNumber,Email,ComputerName,IDProof,InTime,OutTime,Fees) Values('{}','{}',{},'{}','{}','{}','{}','{}','{}')".format(f1,l1,m,em,d1,ed,tmin1,tmout1,sam)
    cursor.execute(st)
    mycon.commit()
    print("Successfully!! Added")
    messagebox.showinfo("Amount",prom)
    
    
    
    
#######################################################################################################
def add_info():                                           #for taking user input to add the enteries
    frame2.pack_forget()
    frame3.pack_forget()
    emp_first_name=Label(frame1,text="Username: ",font=('Italic',28),bg="sky blue",fg="white")
    emp_first_name.grid(row=1,column=1,padx=10)
    e1=Entry(frame1,textvariable=firstname)
    e1.grid(row=1,column=2,padx=10)
    e1.focus()
    emp_last_name=Label(frame1,text="User Address: ",font=('Italic',28),bg="sky blue",fg="white")
    emp_last_name.grid(row=2,column=1,padx=10)
    e2=Entry(frame1,textvariable=lastname)
    e2.grid(row=2,column=2,padx=10)
    emp_mobile_number=Label(frame1,text="Mobile Number: ",font=('Italic',28),bg="sky blue",fg="white")
    emp_mobile_number.grid(row=3,column=1,padx=10)
    e3=Entry(frame1,textvariable=mobile)
    e3.grid(row=3,column=2,padx=10)
    emp_email=Label(frame1,text="Email : ",font=('Italic',28),bg="sky blue",fg="white")
    emp_email.grid(row=4,column=1,padx=10)
    e4=Entry(frame1,textvariable=email)
    e4.grid(row=4,column=2,padx=10)
    emp_dept=Label(frame1,text="Computer: ",font=('Italic',28),bg="sky blue",fg="white")
    emp_dept.grid(row=5,column=1,padx=10)
    dept.set("Select Option")
    e5=OptionMenu(frame1,dept,"Select Option","1. Asus 121","2. Acer 361","3. Dell 450","4. MSI Gaming","5. Asus Gaming")
    e5.grid(row=5,column=2,padx=10)
    emp_ID_proof=Label(frame1,text="ID Proof: ",font=('Italic',28),bg="sky blue",fg="white")
    emp_ID_proof.grid(row=6,column=1,padx=10)
    e6=Entry(frame1,textvariable=ID)
    e6.grid(row=6,column=2,padx=10)
    emp_time_in=Label(frame1,text="Time in(hh:mm): ",font=('Italic',28),bg="sky blue",fg="white")
    emp_time_in.grid(row=7,column=1,padx=10)
    e6=Entry(frame1,textvariable=time_in)
    e6.grid(row=7,column=2,padx=10)
    
    button4=Button(frame1,text="Print Reciept",font=('Italic',32),command=pdf1)
    button4.grid(row=8,column=1,pady=10)
    button4=Button(frame1,text="READY TO PAY",font=('Italic',32),command=add_entries)
    button4.grid(row=8,column=2,pady=10)
    frame1.configure(background="sky blue")
    frame1.pack(pady=10)
    
####################################################################################################

def clear_all():             #for clearing the entry widgets
    frame1.pack_forget()
    frame2.pack_forget()
    frame3.pack_forget()
#########################################################################################################

def tmo(tmin,tmout):                                          #Converting the time in seconds and then in minutes
    datetimeFormat = '%Y-%m-%d %H:%M:%S'
    date1 = tmin
    date2 = tmout
    def date_diff_in_Seconds(dt2, dt1):
        timedelta = dt2 - dt1
        return timedelta.days * 24 * 3600 + timedelta.seconds
#Specified date
    date1 = datetime.strptime(date1, datetimeFormat)
#Current date
    date2 = datetime.strptime(date2, datetimeFormat)
    ak="\n%d " %(date_diff_in_Seconds(date2, date1))
    bk=int(ak)
    ok=math.fabs(bk)
    print("Seconds",ok)
    return ok
def prc(tmin,tmout):                                           #Calculating the amount by the used minutes
    d=dept.get()
    if d in ["4. MSI Gaming","5. Asus Gaming"]:
        tm=tmo(tmin,tmout)
        minum=tm//60
        pric=minum*0.30
        return pric 
    else:
        tm=tmo(tmin,tmout)
        minum=tm//60
        pric=minum*0.50
        return pric
        
##############################################################################################################

##########################################################################################################

def gst1(fees):                         # GST INCLUDED AMOUNT
    abbr=int(fees)
    bbbr=abbr*0.046
    cbbr=abbr+bbbr
    return cbbr
askey=random.randint(1,9999999)
ask_for=askey
askey=str(askey)
askey=askey+".pdf"

##############################################################################################################

def pdf1():                                          #Creating the pdf of the bill
    f=firstname.get()
    f1=f.lower()
    l=lastname.get()
    
    m=mobile.get()
    
    
    
    tmin=time_in.get()
    tmin1=tmp_in(tmin)
    tmout=time_out.get()
###########################################################################################################
    import datetime    
    now = datetime.datetime.now()                  #taking the currect date and time
    
    tmout=now.strftime("%Y-%m-%d %H:%M:%S")
##########################################################################################################
    fees=prc(tmin1,tmout)
    class PDF(FPDF):
        def header(self):
            
            self.image("E:\sed.jpg", 10,8,33)
            # Arial bold 15
            self.set_font('Arial', 'B', 15)
            # Move to the right
            self.cell(80)
            # Title
            self.cell(0, 6, 'Receipt', 0, 1, 'L')
            # Line break
            self.ln(20)

        # Page footer
        def footer(self):
            # Position at 1.5 cm from bottom
            self.set_y(-15)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            # Page number
            self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 1, 1, 'C')

    # Instantiation of inherited class
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    for i in range(1):
        far_in=f1.capitalize()
        ld_ad=l
        mobi_dn=str(m)
        free_fire=str(fees)
        cbbr=gst1(fees)
        as_cbbr=str(cbbr)
        pdf.cell(0, 10, 'Name                : ' + far_in, 0, 1)
        pdf.cell(0, 10, 'Address             : ' + ld_ad, 0, 1)
        pdf.cell(0, 10, 'Mobile Number       : ' + mobi_dn, 0, 1)
        pdf.cell(0, 10, 'Time In             : ' + tmin1, 0, 1)
        pdf.cell(0, 10, 'Time Out            : ' + tmout, 0, 1)
        pdf.cell(0, 10, 'Shop Address        : ' + 'Somewhere, somewhere', 0, 1)
        pdf.cell(0, 10, 'Price(Non Gaming)   : ' + 'Rs 0.5/min', 0, 1)
        pdf.cell(0, 10, 'Price(Gaming)       : ' + 'Rs 0.25/min', 0, 1)
        pdf.cell(0, 10, 'Original Amount     : ' + free_fire, 0, 1)
        pdf.cell(0, 10, 'GST                 : ' + '0.046%', 0, 1)
        pdf.cell(0, 10, 'Paid Amount         : ' + as_cbbr, 0, 1)
      
    
    genius="F:/Cyber_cafe (INVESTIG)/Software/Receipt/"+askey              # Have to specify the path
    pdf.output(genius, 'F')
    sql = "UPDATE tblusers SET RECEIPT_ID = %s WHERE Username = %s"
    val = (ask_for,f1)

    cursor.execute(sql, val)

    mycon.commit()
    
    print("Successfully! Printed")
    clear_all()

#######################################################################################################
    
def search_emp():     #can implement search by name 
    clear_all()
    emp_first_name=Label(frame3,text="Enter User",font=('Italic',32),bg="sky blue",fg="white")   #to take user input to seach
    emp_first_name.grid(row=1,column=1,padx=10)
    e11=Entry(frame3,textvariable=searchfirstname)
    e11.grid(row=1,column=2,padx=10)
    e11.focus()
    
    search_button=Button(frame3,text="Click To Search",font=('Italic',32),command=search_entry)
    search_button.grid(row=5,column=2,pady=10)
    
    frame3.configure(background="sky blue")
    frame3.pack(pady=10)
    
def search_entry():
    sf=searchfirstname.get()
    ssf1=sf.lower()
    print(ssf1)
    sam="SELECT * FROM tblusers where Username = %s"
    cursor.execute(sam,(ssf1,))
    
    rowdb=cursor.fetchall()
    data=cursor.rowcount

    
    if data==0:
        print("Not found")
        messagebox.showerror("Sorry","Record not in the database")
        
        clear_all()
        
    else:
        print("Found")
        messagebox.showinfo("Found","This Customer is in the database")
        clear_all()
        for row in rowdb:
            messagebox.showinfo("Info",row)
            
            
            
#########################################################################################################
def smQuit():                                   # Message Box to quit
    ku=messagebox.askyesno("Close Cyber Cafe","Really you want to exit    \n       Think it Again")
    if ku > 0:
        root.destroy()
        return  
###############################################################################################################
#Main window buttons and labels

label1=Label(root,text="Cyber Cafe")
label1.config(font=('Italic',100,'bold'), justify=CENTER, background="black",fg="Yellow", anchor="center")
label1.pack(fill=X)

label2=Label(f,text="MENU ",font=('bold',75), background="Black", fg="White")
label2.pack(side=LEFT,pady=10)
button1=Button(f,text="Add",font=('Italic',50), background="Brown", fg="White", command=add_info, width=8)
button1.pack(side=LEFT,ipadx=20,pady=20)
button2=Button(f,text="Search",font=('Italic',50), background="Brown", fg="white", command=search_emp, width=8)
button2.pack(side=LEFT,ipadx=20,pady=10)
button3=Button(f,text="Close",font=('Italic',50), background="Brown", fg="White", width=8, command=smQuit)
button3.pack(side=LEFT,ipadx=20,pady=10)
f.configure(background="Black")
f.pack()

root.mainloop()
mycon.close()
print("SUCCESSFULLY DISCONNECTED")





