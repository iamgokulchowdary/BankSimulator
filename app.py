# import modules
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import time
import datetime
import os
from PIL import Image, ImageDraw, ImageFont, ImageTk
import io

# main variable's
color1 = 'dodger blue'
color2 = 'white'
tcolor = 'gold'

database1 = 'database/admin.db'
database2 = 'database/employee.db'
database3 = 'database/customer.db'
database4 = 'database/other.db'
database5 = 'database/passbook.db'

path_icon = 'appimages/icon.png'
path_adduser = 'appimages/adduser.png'
path_deleteuser = 'appimages/deleteuser.png'
path_updateuser = 'appimages/updateuser.png'
path_searchuser = 'appimages/searchuser.png'
path_transfer = 'appimages/transfer.png'
path_deposit = 'appimages/saving.png'
path_withdraw = 'appimages/withdraw.png'
path_exchange = 'appimages/exchange.png'
path_jobpost = 'appimages/jobpost.png'
path_city = 'appimages/city.png'
path_book = 'appimages/book.png'

employee_template = r'D:\gokul\python\bank\template\emptemp.png'
customer_template = r'D:\gokul\python\bank\template\usertemp.png'
card_template = r'D:\gokul\python\bank\template\cardtemp.png'

employeeid_folder = r'D:\gokul\python\bank\employee'
customerid_folder = r'D:\gokul\python\bank\customer'
card_folder = r'D:\gokul\python\bank\card'

appname = 'GC BANK'

font = ('baloo', 15)

genderlist = ['Male', 'Female', 'Other']
statuslist = ['Single', 'Married']
accounttypelist = ['Major', 'Minor']
statelist = ["Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jharkand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Naidu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Chandigarh","Delhi","Jammu and Kashmir","Ladakh","Puducherry"]
countrylist = ['India']

"""
ADMIN-PAGE SUB-FUNCTION'S START HERE
"""
def admin_adduser(appbody, loginpage_frame, adminpage_mainframe):

    # sub-function's
    def fn_adduser_backframe():
        def fn_back():
            # sub-function of fn_adduser back button
            adduser_mainframe.destroy()
            adminpage(appbody, loginpage_frame)

        back_btn = Button(adduser_backframe, text='Back', bg=color1, fg=color2, font=font, relief=FLAT, command=fn_back)
        back_btn.pack(side=LEFT)

    def fn_adduser_frame():
        # sub-function's
        def username_password(data, photopath):
            # sub-function
            def fn_create():
                # getting data from username frame
                username = username_entry.get()
                password = password_entry.get()
                conform_password = conform_password_entry.get()

                if (password.replace(' ', '') or conform_password.replace(' ', '') or username.replace(' ', '')) == '':
                    usernamepage_status_label.config(text='Invalid Input')
                else:
                    if password == conform_password :
                        conn = sqlite3.connect(database2)
                        c = conn.cursor()

                        c.execute('SELECT username FROM employee WHERE username = ?', (username,))

                        result = c.fetchall()
                        conn.commit()
                        conn.close()

                        # getting employee id
                        def fn_emp_lastid():
                            conn = sqlite3.connect(database4)
                            c = conn.cursor()
                            c.execute('SELECT * FROM employeeid')
                            data = c.fetchall()
                            lastid = data[0][0]
                            newid = lastid + 1
                            c.execute('''
                            UPDATE employeeid SET employeeid = ? WHERE employeeid = ? 
                            ''', (newid, lastid))
                            conn.commit()
                            conn.close()

                            return lastid

                        if result:
                            usernamepage_status_label.config(text='Username Exists')
                        else:
                            empid = fn_emp_lastid()
                            data.append(username)
                            data.append(password)
                            data.append(empid)
                            conn = sqlite3.connect(database2)
                            c = conn.cursor()

                            c.execute('''
                            INSERT INTO employee VALUES
                            (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                            ''', data)

                            conn.commit()
                            conn.close()

                            font = ImageFont.truetype('baloo.ttf', size=20)
                            temp = Image.open(employee_template)
                            photo = Image.open(photopath)
                            photo = photo.resize((110, 135))
                            temp.paste(photo, (480, 100, 590, 235))
                            draw = ImageDraw.Draw(temp)
                            draw.text((160, 105), text=f'{data[23]}', font=font, fill='black')
                            draw.text((160, 175), text=f'{data[0]} {data[1]}', font=font, fill='black')
                            draw.text((160, 255), text=f'{data[3]}', font=font, fill='black')
                            draw.text((160, 325), text=f'{data[2]}', font=font, fill='black')
                            draw.text((160, 395), text=f'{data[7]}', font=font, fill='black')
                            draw.text((160, 470), text=f'{data[19]}', font=font, fill='black')
                            draw.text((160, 540), text=f'{data[18]}', font=font, fill='black')
                            draw.text((160, 620), text=f'{data[8]}, {data[9]}, {data[10]},', font=font, fill='black')
                            draw.text((160, 690), text=f'{data[11]}, {data[12]}, {data[13]}.', font=font, fill='black')

                            temp.save(r'{}\{}.png'.format(employeeid_folder, data[23]))
                    

                            usernamepage_status_label.config(text='Employee Added')
                            create_btn.config(state=DISABLED)

                    else:
                        usernamepage_status_label.config(text='Invalid Conform Password')

            # delete adduser_frame
            adduser_frame.destroy()

            # create username and password frame
            username_frame = Frame(adduser_mainframe, bg=color1, relief=FLAT, padx=100, pady=100)
            username_frame.pack(fill=BOTH, expand=1)

            # username frame stuff
            username_label = Label(username_frame, text='Username', bg=color1, fg=color2, font=('baloo', 15))
            username_label.grid(row=0, column=0, padx=5, pady=5)
            username_entry = Entry(username_frame, bg=color2, fg=color1, font=('baloo', 15), relief=FLAT, justify=CENTER)
            username_entry.grid(row=0, column=1, padx=5, pady=5)

            password_label = Label(username_frame, text='Password', bg=color1, fg=color2, font=('baloo', 15))
            password_label.grid(row=1, column=0, padx=5, pady=5)
            password_entry = Entry(username_frame, bg=color2, fg=color1, font=('baloo', 15), justify=CENTER, relief=FLAT)
            password_entry.grid(row=1, column=1, padx=5, pady=5)

            conform_password_label = Label(username_frame, text='Conform Password', bg=color1, fg=color2, font=('baloo', 15))
            conform_password_label.grid(row=2, column=0, padx=5, pady=5)
            conform_password_entry = Entry(username_frame, bg=color2, fg=color1, font=('baloo', 15), justify=CENTER, relief=FLAT)
            conform_password_entry.grid(row=2, column=1, padx=5, pady=5)

            usernamepage_status_label = Label(username_frame, bg=color1, fg=color2, font=('baloo', 15))
            usernamepage_status_label.grid(row=3, column=0, padx=5, pady=5, columnspan=2)

            create_btn = Button(username_frame, text='Create', bg=color1, fg=color2, font=('baloo', 15), relief=FLAT, command=fn_create)
            create_btn.grid(row=4, column=1, padx=5, pady=5)

        def fn_nextpage():
            # getting data from form
            try:
                firstname = firstname_entry.get()
                lastname = lastname_entry.get()
                gender = gender_entry.get()
                dob = dob_entry.get()
                phoneno = int(phoneno_entry.get())
                gmail = gmail_entry.get()
                mothername = mothername_entry.get()
                fathername = fathername_entry.get()
                status = status_entry.get()
                doorno = int(doorno_entry.get())
                street = street_entry.get()
                city = city_entry.get()
                state = state_entry.get()
                country = country_entry.get()
                zipcode = int(zipcode_entry.get())
                aadharno = int(aadharno_entry.get())
                pancard = pancard_entry.get()
                branch_ifsccode_entry = branch_entry.get()
                jobpost = jobpost_entry.get()
                photo = bytes()

                photo_text_path = photo_entry.get()
                try:
                    img = Image.open(photo_text_path)
                    with open(photo_text_path, 'rb') as r:
                        photo = r.read()
                    branch, ifsccode = branch_ifsccode_entry.split('--')
                    data = [firstname, lastname, gender, dob, fathername, mothername, gmail, phoneno, doorno, street, city, state, country, zipcode, aadharno, pancard, status, ifsccode, branch, jobpost, photo]

                    # photo_text_path is photopath of username_password function
                    username_password(data, photo_text_path)

                except :
                    page_status_label.config(text='Invalid Input')
            except :
                page_status_label.config(text='Invalid Input')

        # add user form start here...
        firstname_lbn = Label(adduser_frame, text='First name', bg=color1, fg=color2, font=font)
        firstname_lbn.grid(row=0, column=0, pady=5)
        firstname_entry = Entry(adduser_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        firstname_entry.grid(row=0, column=1, pady=5)

        lastname_lbn = Label(adduser_frame, text='Last name', bg=color1, fg=color2, font=font)
        lastname_lbn.grid(row=0, column=2, pady=5)
        lastname_entry = Entry(adduser_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        lastname_entry.grid(row=0, column=3, pady=5)

        gender_entry = StringVar()
        gender_lbn = Label(adduser_frame, text='Gender', bg=color1, fg=color2, font=font)
        gender_lbn.grid(row=0, column=4, pady=5)
        gender_combobox = ttk.Combobox(adduser_frame, textvariable=gender_entry, values=genderlist, state='readonly', background=color2, foreground=color1, font=font, width=18)
        gender_combobox.grid(row=0, column=5, pady=5)
        gender_entry.set(genderlist[0])

        dob_lbn = Label(adduser_frame, text='Date of Birth', bg=color1, fg=color2, font=font)
        dob_lbn.grid(row=1, column=0, pady=5)
        dob_entry = Entry(adduser_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        dob_entry.grid(row=1, column=1, pady=5)

        phoneno_lbn = Label(adduser_frame, text='Phone no', bg=color1, fg=color2, font=font)
        phoneno_lbn.grid(row=1, column=2, pady=5)
        phoneno_entry = Entry(adduser_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        phoneno_entry.grid(row=1, column=3, pady=5)

        gmail_lbn = Label(adduser_frame, text='Gmail', bg=color1, fg=color2, font=font)
        gmail_lbn.grid(row=1, column=4, pady=5)
        gmail_entry = Entry(adduser_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        gmail_entry.grid(row=1, column=5, pady=5)

        fathername_label = Label(adduser_frame, text='Father Name', bg=color1, fg=color2, font=font)
        fathername_label.grid(row=2, column=0, pady=5)
        fathername_entry = Entry(adduser_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        fathername_entry.grid(row=2, column=1, pady=5)

        mothername_label = Label(adduser_frame, text='Mother Name', bg=color1, fg=color2, font=font)
        mothername_label.grid(row=2, column=2, pady=5)
        mothername_entry = Entry(adduser_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        mothername_entry.grid(row=2, column=3, pady=5)

        status_label = Label(adduser_frame, text='Status', bg=color1, fg=color2, font=font)
        status_label.grid(row=2, column=4, pady=5)
        status_entry = StringVar()
        status_combobox = ttk.Combobox(adduser_frame, textvariable=status_entry, values=statuslist, state='readonly', background=color2, foreground=color1, font=font, width=18)
        status_combobox.grid(row=2, column=5, pady=5)
        status_entry.set(statuslist[0])

        doorno_label = Label(adduser_frame, text='Door no', bg=color1, fg=color2, font=font)
        doorno_label.grid(row=3, column=0, pady=5)
        doorno_entry = Entry(adduser_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        doorno_entry.grid(row=3, column=1, pady=5)

        street_label = Label(adduser_frame, text='Street', bg=color1, fg=color2, font=font)
        street_label.grid(row=3, column=2, pady=5)
        street_entry = Entry(adduser_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        street_entry.grid(row=3, column=3, pady=5)

        city_label = Label(adduser_frame, text='City', bg=color1, fg=color2, font=font)
        city_label.grid(row=3, column=4, pady=5)
        city_entry = Entry(adduser_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        city_entry.grid(row=3, column=5, pady=5)

        state_label = Label(adduser_frame, text='State', bg=color1, fg=color2, font=font)
        state_label.grid(row=4, column=0, pady=5)
        state_entry = StringVar()
        state_combobox = ttk.Combobox(adduser_frame, textvariable=state_entry, values=statelist, state='readonly', background=color2, foreground=color1, font=font, width=18)
        state_combobox.grid(row=4, column=1, pady=5)
        state_entry.set(statelist[0])

        country_label = Label(adduser_frame, text='Country', bg=color1, fg=color2, font=font)
        country_label.grid(row=4, column=2, pady=5)
        country_entry = StringVar()
        country_combobox = ttk.Combobox(adduser_frame, textvariable=country_entry, values=countrylist, state='readonly', background=color2, foreground=color1, font=font, width=18)
        country_combobox.grid(row=4, column=3, pady=5)
        country_entry.set(countrylist[0])

        zipcode_label = Label(adduser_frame, text='Zipcode', bg=color1, fg=color2, font=font)
        zipcode_label.grid(row=4, column=4, pady=5)
        zipcode_entry = Entry(adduser_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        zipcode_entry.grid(row=4, column=5, pady=5)

        aadharno_label = Label(adduser_frame, text='Aadhar Id', bg=color1, fg=color2, font=font)
        aadharno_label.grid(row=5, column=0, pady=5)
        aadharno_entry = Entry(adduser_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        aadharno_entry.grid(row=5, column=1, pady=5)

        pancard_label = Label(adduser_frame, text='Pancard Id', bg=color1, fg=color2, font=font)
        pancard_label.grid(row=5, column=2, pady=5)
        pancard_entry = Entry(adduser_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        pancard_entry.grid(row=5, column=3, pady=5)

        # getting data for branch and jobpost combobox
        conn = sqlite3.connect(database1)
        c = conn.cursor()
        c.execute('SELECT * FROM branch')
        branch_database_list = c.fetchall()
        c.execute('SELECT * FROM jobpost')
        jobpost_database_list = c.fetchall()

        branchlist = []
        jobpostlist = []
        for i in range(len(branch_database_list)):
            branch_ifsccode = f'{branch_database_list[i][0]}--{branch_database_list[i][1]}'
            branchlist.append(branch_ifsccode)

        for i in range(len(jobpost_database_list)):
            jobpost_list_gen = f'{jobpost_database_list[i][0]}'
            jobpostlist.append(jobpost_list_gen)

        conn.commit()
        conn.close()

        # back to add user form

        branch_label = Label(adduser_frame, text='Branch', bg=color1, fg=color2, font=font)
        branch_label.grid(row=6, column=0, pady=5)
        branch_entry = StringVar()
        branch_combobox = ttk.Combobox(adduser_frame, textvariable=branch_entry, values=branchlist, state='readonly', background=color2, foreground=color1, font=font, width=18)
        branch_combobox.grid(row=6, column=1, pady=5)
        branch_entry.set(branchlist[0])

        jobpost_label = Label(adduser_frame, text='Jobpost', bg=color1, fg=color2, font=font)
        jobpost_label.grid(row=6, column=2, pady=5)
        jobpost_entry = StringVar()
        jobpost_combobox = ttk.Combobox(adduser_frame, textvariable=jobpost_entry, values=jobpostlist, state='readonly', background=color2, foreground=color1, font=font, width=18)
        jobpost_combobox.grid(row=6, column=3, pady=5)
        jobpost_entry.set(jobpostlist[0])

        # photo selection and update section
        def select_photo():
            photopath = filedialog.askopenfilename()
            phototext_label.config(text=photopath)
            photo_entry.delete(0, END)
            photo_entry.insert(0, photopath)
        
        photo_label = Label(adduser_frame, text='Photo', bg=color1, fg=color2, font=font)
        photo_label.grid(row=7, column=0, pady=5)
        phototext_label = Label(adduser_frame, bg=color2, fg=color1, font=font, width=20)
        phototext_label.grid(row=7, column=1, pady=5)
        photo_entry = Entry(adduser_frame)
        photoupload_btn = Button(adduser_frame, text='Upload Photo', font=font, bg=color1, fg=color2, relief=FLAT, command=select_photo)
        photoupload_btn.grid(row=7, column=2, pady=5)

        # status label
        page_status_label = Label(adduser_frame, bg=color1, fg=tcolor, font=font)
        page_status_label.grid(row=8, column=0, pady=5, columnspan=5)

        # fn_nextpage function is a sub-function of fn_adduser_frame
        next_btn = Button(adduser_frame, text='Next', font=font, bg=color1, fg=tcolor, relief=FLAT, command=fn_nextpage)
        next_btn.grid(row=8, column=0, pady=10)
        

    # first thing's first
    adminpage_mainframe.destroy()

    # create requied frames
    adduser_mainframe = Frame(appbody, bg=color1, relief=FLAT)
    adduser_mainframe.pack(fill=BOTH, expand=1)
    adduser_backframe = Frame(adduser_mainframe, bg=color1, relief=FLAT)
    adduser_backframe.pack(fill=X)
    adduser_frame = Frame(adduser_mainframe, bg=color1, relief=FLAT)
    adduser_frame.pack(fill=BOTH, expand=1)

    # calling requied function's
    fn_adduser_backframe()
    fn_adduser_frame()

def admin_updateuser(appbody, loginpage_frame, adminpage_mainframe):

    # sub-functions of update user page
    def fn_updateuser_backframe():
        updateuser_mainframe.destroy()
        adminpage(appbody, loginpage_frame)
        
    def fn_updateuser_frame():

        # sub-function
        def fn_update_inputframe(olddata):
            # update data
            def fn_update_new_data():
                try:
                    # getting data from form...
                    firstname = firstname_entry.get()
                    lastname = lastname_entry.get()
                    gender = gender_entry.get()
                    dob = dob_entry.get()
                    fathername = fathername_entry.get()
                    mothername = mothername_entry.get()
                    gmail = gmail_entry.get()
                    phoneno = int(phoneno_entry.get())
                    doorno = int(doorno_entry.get())
                    street = street_entry.get()
                    city = city_entry.get()
                    state = state_entry.get()
                    country = country_entry.get()
                    zipcode = int(zipcode_entry.get())
                    aadharno = int(aadharno_entry.get())
                    pancard = pancard_entry.get()
                    status = status_entry.get()
                    photo = bytes()

                    photopath_entry = photo_entry.get()
                    if photopath_entry:
                        with open(photopath_entry, 'rb') as r:
                            photo = r.read()
                    else:
                        photo = olddata[0][20]
                    
                    # add employee id to newdata at the end for database query
                    employeeid = olddata[0][23]
                    newdata = [firstname, lastname, gender, dob, fathername, mothername, gmail, phoneno, doorno, street, city, state, country, zipcode, aadharno, pancard, status, photo, employeeid]

                    # updating data to database...
                    conn = sqlite3.connect(database2)
                    c = conn.cursor()
                    c.execute("""
                    UPDATE employee SET
                    firstname = ?,
                    lastname = ?,
                    gender = ?,
                    dob = ?,
                    fathername = ?,
                    mothername = ?,
                    gmail = ?,
                    phoneno = ?,
                    doorno = ?,
                    street = ?,
                    city = ?,
                    state = ?,
                    country = ?,
                    zipcode = ?,
                    aadharno = ?,
                    pancardno = ?,
                    status = ?,
                    photo = ?
                    WHERE employeeid = ?
                    """, newdata)
                    conn.commit()
                    conn.close()
                
                    # update employeeid card
                    font = ImageFont.truetype('baloo.ttf', size=20)
                    temp = Image.open(employee_template)
                    photo_for_temp = Image.open(io.BytesIO(photo))
                    photo_for_temp = photo_for_temp.resize((110, 135))
                    temp.paste(photo_for_temp, (480, 100, 590, 235))
                    draw = ImageDraw.Draw(temp)
                    draw.text((160, 105), text=f'{employeeid}', font=font, fill='black')
                    draw.text((160, 175), text=f'{firstname} {lastname}', font=font, fill='black')
                    draw.text((160, 255), text=f'{dob}', font=font, fill='black')
                    draw.text((160, 325), text=f'{gender}', font=font, fill='black')
                    draw.text((160, 395), text=f'{phoneno}', font=font, fill='black')
                    draw.text((160, 470), text=f'{olddata[0][19]}', font=font, fill='black')
                    draw.text((160, 540), text=f'{olddata[0][18]}', font=font, fill='black')
                    draw.text((160, 620), text=f'{doorno}, {street}, {city},', font=font, fill='black')
                    draw.text((160, 690), text=f'{state}, {country}, {zipcode}.', font=font, fill='black')

                    os.remove(r'{}\{}.png'.format(employeeid_folder, employeeid))
                    temp.save(r'{}\{}.png'.format(employeeid_folder, employeeid))

                    page_status_label.config(text='Update Sucess')
                      
                except :
                    page_status_label.config(text='Invalid Input')
                
            # update form start here...
            firstname_lbn = Label(update_inputframe, text='First name', bg=color1, fg=color2, font=font)
            firstname_lbn.grid(row=0, column=0, pady=5)
            firstname_entry = Entry(update_inputframe, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            firstname_entry.grid(row=0, column=1, pady=5)

            lastname_lbn = Label(update_inputframe, text='Last name', bg=color1, fg=color2, font=font)
            lastname_lbn.grid(row=0, column=2, pady=5)
            lastname_entry = Entry(update_inputframe, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            lastname_entry.grid(row=0, column=3, pady=5)

            gender_entry = StringVar()
            gender_lbn = Label(update_inputframe, text='Gender', bg=color1, fg=color2, font=font)
            gender_lbn.grid(row=0, column=4, pady=5)
            gender_combobox = ttk.Combobox(update_inputframe, textvariable=gender_entry, values=genderlist, state='readonly', background=color2, foreground=color1, font=font, width=18)
            gender_combobox.grid(row=0, column=5, pady=5)

            dob_lbn = Label(update_inputframe, text='Date of Birth', bg=color1, fg=color2, font=font)
            dob_lbn.grid(row=1, column=0, pady=5)
            dob_entry = Entry(update_inputframe, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            dob_entry.grid(row=1, column=1, pady=5)

            phoneno_lbn = Label(update_inputframe, text='Phone no', bg=color1, fg=color2, font=font)
            phoneno_lbn.grid(row=1, column=2, pady=5)
            phoneno_entry = Entry(update_inputframe, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            phoneno_entry.grid(row=1, column=3, pady=5)

            gmail_lbn = Label(update_inputframe, text='Gmail', bg=color1, fg=color2, font=font)
            gmail_lbn.grid(row=1, column=4, pady=5)
            gmail_entry = Entry(update_inputframe, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            gmail_entry.grid(row=1, column=5, pady=5)

            fathername_label = Label(update_inputframe, text='Father Name', bg=color1, fg=color2, font=font)
            fathername_label.grid(row=2, column=0, pady=5)
            fathername_entry = Entry(update_inputframe, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            fathername_entry.grid(row=2, column=1, pady=5)

            mothername_label = Label(update_inputframe, text='Mother Name', bg=color1, fg=color2, font=font)
            mothername_label.grid(row=2, column=2, pady=5)
            mothername_entry = Entry(update_inputframe, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            mothername_entry.grid(row=2, column=3, pady=5)

            status_label = Label(update_inputframe, text='Status', bg=color1, fg=color2, font=font)
            status_label.grid(row=2, column=4, pady=5)
            status_entry = StringVar()
            status_combobox = ttk.Combobox(update_inputframe, textvariable=status_entry, values=statuslist, state='readonly', background=color2, foreground=color1, font=font, width=18)
            status_combobox.grid(row=2, column=5, pady=5)

            doorno_label = Label(update_inputframe, text='Door no', bg=color1, fg=color2, font=font)
            doorno_label.grid(row=3, column=0, pady=5)
            doorno_entry = Entry(update_inputframe, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            doorno_entry.grid(row=3, column=1, pady=5)

            street_label = Label(update_inputframe, text='Street', bg=color1, fg=color2, font=font)
            street_label.grid(row=3, column=2, pady=5)
            street_entry = Entry(update_inputframe, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            street_entry.grid(row=3, column=3, pady=5)

            city_label = Label(update_inputframe, text='City', bg=color1, fg=color2, font=font)
            city_label.grid(row=3, column=4, pady=5)
            city_entry = Entry(update_inputframe, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            city_entry.grid(row=3, column=5, pady=5)

            state_label = Label(update_inputframe, text='State', bg=color1, fg=color2, font=font)
            state_label.grid(row=4, column=0, pady=5)
            state_entry = StringVar()
            state_combobox = ttk.Combobox(update_inputframe, textvariable=state_entry, values=statelist, state='readonly', background=color2, foreground=color1, font=font, width=18)
            state_combobox.grid(row=4, column=1, pady=5)

            country_label = Label(update_inputframe, text='Country', bg=color1, fg=color2, font=font)
            country_label.grid(row=4, column=2, pady=5)
            country_entry = StringVar()
            country_combobox = ttk.Combobox(update_inputframe, textvariable=country_entry, values=countrylist, state='readonly', background=color2, foreground=color1, font=font, width=18)
            country_combobox.grid(row=4, column=3, pady=5)

            zipcode_label = Label(update_inputframe, text='Zipcode', bg=color1, fg=color2, font=font)
            zipcode_label.grid(row=4, column=4, pady=5)
            zipcode_entry = Entry(update_inputframe, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            zipcode_entry.grid(row=4, column=5, pady=5)

            aadharno_label = Label(update_inputframe, text='Aadhar Id', bg=color1, fg=color2, font=font)
            aadharno_label.grid(row=5, column=0, pady=5)
            aadharno_entry = Entry(update_inputframe, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            aadharno_entry.grid(row=5, column=1, pady=5)

            pancard_label = Label(update_inputframe, text='Pancard Id', bg=color1, fg=color2, font=font)
            pancard_label.grid(row=5, column=2, pady=5)
            pancard_entry = Entry(update_inputframe, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            pancard_entry.grid(row=5, column=3, pady=5)

            # photo selection and update section
            def select_photo():
                photopath = filedialog.askopenfilename()
                phototext_label.config(text=photopath)
                photo_entry.delete(0, END)
                photo_entry.insert(0, photopath)
            
            photo_label = Label(update_inputframe, text='Photo', bg=color1, fg=color2, font=font)
            photo_label.grid(row=6, column=0, pady=5)
            phototext_label = Label(update_inputframe, bg=color2, fg=color1, font=font, width=20)
            phototext_label.grid(row=6, column=1, pady=5)
            photo_entry = Entry(update_inputframe)
            photoupload_btn = Button(update_inputframe, text='Upload Photo', font=font, bg=color1, fg=color2, relief=FLAT, command=select_photo)
            photoupload_btn.grid(row=6, column=2, pady=5)

            # insert data into field's
            def fn_update_fields_with_olddata():

                firstname_entry.insert(0, olddata[0][0])
                lastname_entry.insert(0, olddata[0][1])
                gender_entry.set(olddata[0][2])
                dob_entry.insert(0, olddata[0][3])
                phoneno_entry.insert(0, olddata[0][7])
                gmail_entry.insert(0, olddata[0][6])
                fathername_entry.insert(0, olddata[0][4])
                mothername_entry.insert(0, olddata[0][5])
                status_entry.set(olddata[0][16])
                doorno_entry.insert(0, olddata[0][8])
                street_entry.insert(0, olddata[0][9])
                city_entry.insert(0, olddata[0][10])
                state_entry.set(olddata[0][11])
                country_entry.set(olddata[0][12])
                zipcode_entry.insert(0, olddata[0][13])
                aadharno_entry.insert(0, olddata[0][14])
                pancard_entry.insert(0, olddata[0][15])

            fn_update_fields_with_olddata()
            
            # back to form...
            page_status_label = Label(update_inputframe, bg=color1, fg=color2, font=font)
            page_status_label.grid(row=7, column=0, columnspan=5)

            update_btn = Button(update_inputframe, text='Update', bg=color1, fg=tcolor, relief=FLAT, font=font, command=fn_update_new_data)
            update_btn.grid(row=8, column=0, pady=10)
            

        def fn_search_frame():
            # sub-function
            def fn_search_data():
                # getting employee id from entry field
                id = search_entry.get()
                try:
                    conn = sqlite3.connect(database2)
                    c = conn.cursor()
                    c.execute('SELECT * FROM employee WHERE employeeid = ?', (int(id), ))
                    data = c.fetchall()
                    if data:
                        # sending data as old data into function
                        search_status = Label(search_frame, text='', bg=color1, fg=color2, font=font)
                        search_status.grid(row=1, column=0, columnspan=3, padx=5)
                        fn_update_inputframe(data)
                    else:
                        search_status = Label(search_frame, text='Invalid Input', bg=color1, fg=color2, font=font)
                        search_status.grid(row=1, column=0, columnspan=3, padx=5)
                    conn.commit()
                    conn.close()
                    
                except :
                    search_status = Label(search_frame, text='Invalid Input', bg=color1, fg=color2, font=font)
                    search_status.grid(row=1, column=0, columnspan=3, padx=5)

            # frame start here...
            search_lbn = Label(search_frame, text='Search ID', bg=color1, fg=color2, font=font)
            search_lbn.grid(row=0, column=0, padx=5)
            search_entry = Entry(search_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            search_entry.grid(row=0, column=1, padx=5)
            search_btn = Button(search_frame, text='Get Data', bg=color1, fg=color2, font=font, relief=FLAT, command=fn_search_data)
            search_btn.grid(row=0, column=2, padx=5)

        # fn_updateuser_frame start here...
        # create requied frame's
        search_frame = Frame(updateuser_frame, bg=color1, relief=FLAT)
        search_frame.pack(fill=X)
        update_inputframe = Frame(updateuser_frame, bg=color1, relief=FLAT)
        update_inputframe.pack(fill=BOTH, expand=1)

        # calling requied function
        fn_search_frame()
        
        
    # first thing's first
    adminpage_mainframe.destroy()

    # create requied frame's
    updateuser_mainframe = Frame(appbody, bg=color1, relief=FLAT)
    updateuser_mainframe.pack(fill=BOTH, expand=1)
    updateuser_backframe = Frame(updateuser_mainframe, bg=color1, relief=FLAT)
    updateuser_backframe.pack(fill=X)
    updateuser_frame = Frame(updateuser_mainframe, bg=color1, relief=FLAT)
    updateuser_frame.pack(fill=BOTH, expand=1)

    # back button for update user page
    back_btn = Button(updateuser_backframe, text='Back', bg=color1, fg=color2, relief=FLAT, font=font, command=fn_updateuser_backframe)
    back_btn.pack(side=LEFT)

    # calling requied function
    fn_updateuser_frame()
    
def admin_deleteuser(appbody, loginpage_frame, adminpage_mainframe):
    # sub-function
    def fn_deleteuser_backframe():
        deleteuser_mainframe.destroy()
        adminpage(appbody, loginpage_frame)
        
    def fn_deleteuser_frame():
        # sub-function
        def fn_delete_data(employeeid, img):
            # create requied frame's
            image_frame = Frame(delete_frame, bg=color1, relief=FLAT)
            image_frame.pack(side=LEFT, fill=BOTH, expand=1)
            button_frame = Frame(delete_frame, bg=color1, relief=FLAT)
            button_frame.pack(side=RIGHT, fill=BOTH, expand=1)
            
            # image frame stuff...

            image_lbn = Label(image_frame, image=img, bg=color1, fg=color2)
            image_lbn.pack()

            # fn_conform_delete function will delete data from database and all records of employee
            def fn_conform_delete():
                
                # deleting employee record from database...
                conn = sqlite3.connect(database2)
                c = conn.cursor()
                c.execute("DELETE FROM employee WHERE employeeid = ?", (employeeid, ))
                conn.commit()
                conn.close()

                # deleting id card of employee
                os.remove(r'{}\{}.png'.format(employeeid_folder, employeeid))

                delete_status_lbn.config(text='Employee Deleted')

            # button frame stuff...
            conform_message_lbn = Label(button_frame, text='Conform Delete Employee', font=font, bg=color1, fg=color2)
            conform_message_lbn.grid(row=0, column=0, padx=10, pady=10)
            conform_delete_btn = Button(button_frame, text='Delete', bg=color1, fg=tcolor, font=font, relief=FLAT, command=fn_conform_delete)
            conform_delete_btn.grid(row=1, column=0, padx=10, pady=10)

            delete_status_lbn = Label(button_frame, bg=color1, fg=color2, font=font)
            delete_status_lbn.grid(row=2, column=0, padx=10, pady=10)

        def fn_search_data():
            try: 
                global img, img1
                employeeid = int(search_entry.get())
                img1 = Image.open(r'{}\{}.png'.format(employeeid_folder, employeeid))
                img1 = img1.resize((300,400))
                img = ImageTk.PhotoImage(img1)
                fn_delete_data(employeeid, img)
                search_status_lbn.config(text='')
            except :
                search_status_lbn.config(text='Invaild Input')

        # create requied frame's for deleteuser_frame
        search_frame = Frame(deleteuser_frame, bg=color1, relief=FLAT)
        search_frame.pack(fill=X)
        delete_frame = Frame(deleteuser_frame, bg=color1, relief=FLAT)
        delete_frame.pack(fill=BOTH, expand=1)

        # search frame stuff...
        search_lbn = Label(search_frame, text='Search ID', bg=color1, fg=color2, font=font)
        search_lbn.grid(row=0, column=0, padx=5)
        search_entry = Entry(search_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        search_entry.grid(row=0, column=1, padx=5)
        search_btn = Button(search_frame, text='Delete', bg=color1, fg=color2, font=font, relief=FLAT, command=fn_search_data)
        search_btn.grid(row=0, column=2, padx=5)
        search_status_lbn = Label(search_frame, bg=color1, fg=color2, font=font)
        search_status_lbn.grid(row=1, column=0, columnspan=2, pady=5)
        
    # first thing's first
    adminpage_mainframe.destroy()

    # create requied frame's
    deleteuser_mainframe = Frame(appbody, bg=color1, relief=FLAT)
    deleteuser_mainframe.pack(fill=BOTH, expand=1)
    deleteuser_backframe = Frame(deleteuser_mainframe, bg=color1, relief=FLAT)
    deleteuser_backframe.pack(fill=X)
    deleteuser_frame = Frame(deleteuser_mainframe, bg=color1, relief=FLAT)
    deleteuser_frame.pack(fill=BOTH, expand=1)

    # back button for delete page
    back_btn = Button(deleteuser_backframe, text='Back', bg=color1, fg=color2, font=font, relief=FLAT, command=fn_deleteuser_backframe)
    back_btn.pack(side=LEFT)

    # calling requied function
    fn_deleteuser_frame()

def admin_addbranch(appbody, loginpage_frame, adminpage_mainframe):
    # sub-function
    def fn_backframe():
        # back function
        def fn_back():
            addbranch_mainframe.destroy()
            adminpage(appbody, loginpage_frame)

        back_btn = Button(addbranch_backframe, text='Back', bg=color1, fg=color2, font=font, relief=FLAT, command=fn_back)
        back_btn.pack(side=LEFT)

    def fn_addbranchframe():
        # sub-function

        def fn_listbox():
            conn = sqlite3.connect(database1)
            c = conn.cursor()
            c.execute('SELECT * FROM branch')
            result = c.fetchall()
            branch_listbox.delete(0,END)
            for i in range(len(result)):
                opt = f'{result[i][0]}  --  {result[i][1]}'
                branch_listbox.insert(END, opt)

            conn.commit()
            conn.close()

        def fn_submit():
            # sub-function
            def fn_gen_ifsccode():
                conn = sqlite3.connect(database4)
                c = conn.cursor()
                c.execute('SELECT * FROM ifsccode')
                result = c.fetchall()
                lastid = result[0][0]
                newid = lastid + 1
                c.execute('UPDATE ifsccode SET ifsccode = ? WHERE ifsccode = ? ', (newid, lastid))
                conn.commit()
                conn.close()
                lastid = str(lastid)
                return lastid[1:]

            # submit button from add branch frame
            branch = add_branch_entry.get()
            branch = branch.capitalize()

            if branch.replace(' ', '') != '':
                conn = sqlite3.connect(database1)
                c = conn.cursor()
                c.execute('SELECT * FROM branch WHERE branch = ?', (branch,))
                result = c.fetchall()
                if result:
                    status_label.config(text='Branch Exists')
                else:
                    ifsccode_int = fn_gen_ifsccode()
                    ifsccode = f'GC{ifsccode_int}'
                    c.execute('INSERT INTO branch values (?,?)', (branch, ifsccode))
                    status_label.config(text='Branch Added')

                conn.commit()
                conn.close()
            else:
                status_label.config(text='Invalid Input')

        # create requied frame's
        show_frame = Frame(addbranch_frame, bg=color1, relief=FLAT, padx=50, pady=50)
        show_frame.pack(side=LEFT, fill=BOTH, expand=1)
        add_frame = Frame(addbranch_frame, bg=color1, relief=FLAT, padx=100, pady=100)
        add_frame.pack(side=RIGHT, fill=BOTH, expand=1)

        # show frame stuff
        branch_ifsccode_listbox_label = Label(show_frame, text='Branch And IFSC Code', bg=color1, fg=color2, font=font)
        branch_ifsccode_listbox_label.pack(padx=5, pady=5)

        # listbox frame
        listbox_frame = Frame(show_frame, bg=color1, relief=FLAT)
        listbox_frame.pack(padx=5, pady=5)
        
        # listbox_yscrollbar
        listbox_yscrollbar = Scrollbar(listbox_frame, orient=VERTICAL)
        listbox_yscrollbar.pack(side=RIGHT, fill=Y)

        # listbox
        branch_listbox = Listbox(listbox_frame, bg=color2, fg=color1, relief=FLAT, selectbackground=tcolor, yscrollcommand=listbox_yscrollbar.set, font=font, width=50)
        branch_listbox.pack()

        # configure
        listbox_yscrollbar.config(command=branch_listbox.yview)

        # refresh button for listbox
        refresh_btn = Button(show_frame, text='Refresh', bg=color1, fg=color2, relief=FLAT, font=font, command=fn_listbox)
        refresh_btn.pack(padx=5, pady=5)

        # calling fn_listbox to add data into listbox
        fn_listbox()

        # add frame stuff
        add_branch_label = Label(add_frame, text='Branch', bg=color1, fg=color2, font=font)
        add_branch_label.grid(row=0, column=0, padx=5, pady=5)
        add_branch_entry = Entry(add_frame, bg=color2, fg=color1, font=font, relief=FLAT)
        add_branch_entry.grid(row=0, column=1, padx=5, pady=5)
        
        add_ifsccode_label = Label(add_frame, text='IFSC Code', bg=color1, fg=color2, font=font)
        add_ifsccode_label.grid(row=1, column=0, padx=5, pady=5)
        add_ifsccode_entry = Entry(add_frame, bg=color2, fg=color1, font=font, relief=FLAT, state=DISABLED)
        add_ifsccode_entry.grid(row=1, column=1, padx=5, pady=5)

        status_label = Label(add_frame, font=font, bg=color1, fg=tcolor)
        status_label.grid(row=2, column=0, padx=5, pady=5, columnspan=2)

        submit_btn = Button(add_frame, text='Submit', font=font, bg=color1, fg=color2, relief=FLAT, command=fn_submit)
        submit_btn.grid(row=3, column=1, padx=5, pady=5)

    # first thing's first
    adminpage_mainframe.destroy()

    # create requied frame's
    addbranch_mainframe = Frame(appbody, bg=color1, relief=FLAT)
    addbranch_mainframe.pack(fill=BOTH, expand=1)
    addbranch_backframe = Frame(addbranch_mainframe, bg=color1, relief=FLAT)
    addbranch_backframe.pack(fill=X)
    addbranch_frame = Frame(addbranch_mainframe, bg=tcolor, relief=FLAT)
    addbranch_frame.pack(fill=BOTH, expand=1)

    # calling requied function's
    fn_backframe()
    fn_addbranchframe()

def admin_addjobpost(appbody, loginpage_frame, adminpage_mainframe):
    # sub-funtcion's
    def fn_back():
        addjobpost_mainframe.destroy()
        adminpage(appbody, loginpage_frame)
    
    def fn_jobpostsection():

        # sub-function
        def fn_listbox():
            conn = sqlite3.connect(database1)
            c = conn.cursor()
            c.execute('SELECT * FROM jobpost')
            result = c.fetchall()
            jobpost_listbox.delete(0,END)
            for i in range(len(result)):
                opt = f'{result[i][0]}'
                jobpost_listbox.insert(END, opt)

            conn.commit()
            conn.close()

        def fn_submit():
            # submit button from add jobpost frame
            jobpost = add_jobpost_entry.get()
            jobpost = jobpost.capitalize()

            if jobpost.replace(' ', '') != '':
                conn = sqlite3.connect(database1)
                c = conn.cursor()
                c.execute('SELECT * FROM jobpost WHERE jobpost = ?', (jobpost,))
                result = c.fetchall()
                if result:
                    status_label.config(text='Jobpost Exists')
                else:
                    c.execute('INSERT INTO jobpost values (?)', (jobpost,))
                    status_label.config(text='Jobpost Added')

                conn.commit()
                conn.close()
            else:
                status_label.config(text='Invalid Input')

        # create two different frames for list of jobpost and add jobpost
        show_frame = Frame(addjobpost_frame, bg=color1, relief=FLAT, pady=20)
        show_frame.pack(fill=BOTH, expand=1, side=LEFT)
        add_frame = Frame(addjobpost_frame, bg=color1, relief=FLAT, pady=20)
        add_frame.pack(fill=BOTH, expand=1, side=RIGHT)

        # show frame stuff
        jobpost_listbox_label = Label(show_frame, text='JOB POST', bg=color1, fg=color2, font=font)
        jobpost_listbox_label.pack(padx=5, pady=5)

        # listbox frame
        listbox_frame = Frame(show_frame, bg=color1, relief=FLAT)
        listbox_frame.pack(padx=5, pady=5)
        
        # listbox_yscrollbar
        listbox_yscrollbar = Scrollbar(listbox_frame, orient=VERTICAL)
        listbox_yscrollbar.pack(side=RIGHT, fill=Y)

        # listbox
        jobpost_listbox = Listbox(listbox_frame, bg=color2, fg=color1, relief=FLAT, selectbackground=tcolor, yscrollcommand=listbox_yscrollbar.set, font=font)
        jobpost_listbox.pack()

        # configure
        listbox_yscrollbar.config(command=jobpost_listbox.yview)

        # refresh button for listbox
        refresh_btn = Button(show_frame, text='Refresh', bg=color1, fg=color2, relief=FLAT, font=font, command=fn_listbox)
        refresh_btn.pack(padx=5, pady=5)

        # calling fn_listbox to add data into listbox
        fn_listbox()

        # add frame stuff
        add_jobpost_label = Label(add_frame, text='Job Post', bg=color1, fg=color2, font=font)
        add_jobpost_label.grid(row=0, column=0, padx=5, pady=5)
        add_jobpost_entry = Entry(add_frame, bg=color2, fg=color1, font=font, relief=FLAT)
        add_jobpost_entry.grid(row=0, column=1, padx=5, pady=5)

        status_label = Label(add_frame, font=font, bg=color1, fg=tcolor)
        status_label.grid(row=2, column=0, padx=5, pady=5, columnspan=2)

        submit_btn = Button(add_frame, text='Submit', font=font, bg=color1, fg=color2, relief=FLAT, command=fn_submit)
        submit_btn.grid(row=3, column=1, padx=5, pady=5)

    # first things first
    adminpage_mainframe.destroy()

    # create requied frames
    addjobpost_mainframe = Frame(appbody, bg=color1, relief=FLAT)
    addjobpost_mainframe.pack(fill=BOTH, expand=1)
    addjobpost_backframe = Frame(addjobpost_mainframe, bg=color1, relief=FLAT)
    addjobpost_backframe.pack(fill=X)
    addjobpost_frame = Frame(addjobpost_mainframe, bg=color1, relief=FLAT)
    addjobpost_frame.pack(fill=BOTH, expand=1)

    # create back button for add jobpost frame (page)
    back_btn = Button(addjobpost_backframe, text="Back", bg=color1, fg=color2, font=font, relief=FLAT, command=fn_back)
    back_btn.pack(side=LEFT)

    # calling requied function
    fn_jobpostsection()

"""
ADMIN-PAGE SUB-FUNCTION'S END HERE
"""
"""
EMPLOYEE-PAGE SUB-FUNCTION'S START HERE
"""
def employee_adduser(appbody, loginpage_frame, employeepage_mainframe, branch, ifsccode):
    # sub-function
    def fn_adduser_backframe():
        adduser_mainframe.destroy()
        employeepage(appbody, loginpage_frame, branch, ifsccode)
    
    def fn_adduser_frame():
        # sub-function
        def fn_createaccount():
            # sub-function
            def fn_gen_accountno():
                conn = sqlite3.connect(database4)
                c = conn.cursor()
                c.execute('SELECT * FROM accountno')
                result = c.fetchall()
                lastno = result[0][0]
                newno = lastno + 1
                data = (newno, lastno)
                c.execute('UPDATE accountno SET accountno = ? WHERE accountno = ? ', data)
                conn.commit()
                conn.close()

                return lastno
                
            def fn_gen_cardno():
                conn = sqlite3.connect(database4)
                c = conn.cursor()
                c.execute('SELECT * FROM cardno')
                result = c.fetchall()
                lastno = result[0][0]
                newno = lastno + 1
                data = (newno, lastno)
                c.execute('UPDATE cardno SET cardno = ? WHERE cardno = ? ', data)
                conn.commit()
                conn.close()

                return lastno

            def fn_create_accountrecord(data):
                conn = sqlite3.connect(database3)
                c = conn.cursor()
                c.execute('INSERT INTO customer VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', data)
                conn.commit()
                conn.close()
                
            def fn_create_passbookrecord(data):
                conn = sqlite3.connect(database5)
                c = conn.cursor()
                query1 = """
                CREATE TABLE IF NOT EXISTS {} (
                    date TEXT NOT NULL,
                    remark Text NOT NULL,
                    transfer_type TEXT NOT NULL,
                    transfer_amount REAL NOT NULL,
                    balance REAL NOT NULL
                )
                """.format(f'acno{data[17]}')

                c.execute(query1)
                conn.commit()
                conn.close()
                
            def fn_create_deatils_photo(data):
                # creating account info photo
                font = ImageFont.truetype('baloo.ttf', size=20)
                temp = Image.open(customer_template)
                photo_for_temp = Image.open(io.BytesIO(photo))
                photo_for_temp = photo_for_temp.resize((110, 135))
                temp.paste(photo_for_temp, (480, 100, 590, 235))
                draw = ImageDraw.Draw(temp)
                draw.text((175, 105), text=f'{data[0]} {data[1]}', font=font, fill='black')
                draw.text((175, 160), text=f'{data[3]}', font=font, fill='black')
                draw.text((175, 210), text=f'{data[2]}', font=font, fill='black')
                draw.text((175, 260), text=f'{data[7]}', font=font, fill='black')
                draw.text((175, 310), text=f'{data[4]}', font=font, fill='black')
                draw.text((175, 365), text=f'{data[5]}', font=font, fill='black')
                draw.text((175, 415), text=f'{data[8]}, {data[9]}, {data[10]},', font=font, fill='black')
                draw.text((175, 455), text=f'{data[11]}, {data[12]}, {data[13]}', font=font, fill='black')
                draw.text((175, 565), text=f'{data[17]}', font=font, fill='black')
                draw.text((175, 620), text=f'{data[18]}', font=font, fill='black')
                draw.text((175, 670), text=f'{data[20]}', font=font, fill='black')
                draw.text((175, 720), text=f'{data[19]}', font=font, fill='black')

                temp.save(r'{}\{}.png'.format(customerid_folder, data[17]))
                # creating card info photo
                font = ImageFont.truetype('baloo.ttf', size=30)
                temp = Image.open(card_template)
                draw = ImageDraw.Draw(temp)
                draw.text((145,160), text=f'{data[21]}', font=font, fill='white')
                draw.text((145,240), text=f'{data[0]} {data[1]}', font=font, fill='white')

                temp.save(r'{}\{}.png'.format(card_folder, data[17]))
                
            # getting data from form
            try:
                firstname = firstname_entry.get()
                lastname = lastname_entry.get()
                gender = gender_entry.get()
                dob = dob_entry.get()
                phoneno = int(phoneno_entry.get())
                gmail = gmail_entry.get()
                mothername = mothername_entry.get()
                fathername = fathername_entry.get()
                status = status_entry.get()
                doorno = int(doorno_entry.get())
                street = street_entry.get()
                city = city_entry.get()
                state = state_entry.get()
                country = country_entry.get()
                zipcode = int(zipcode_entry.get())
                aadharno = int(aadharno_entry.get())
                pancard = pancard_entry.get()
                accounttype = accounttype_entry.get()
                balance = 0

                photo = bytes()

                photo_text_path = photo_entry.get()
                try:
                    img = Image.open(photo_text_path)
                    with open(photo_text_path, 'rb') as r:
                        photo = r.read()
                    
                    accountno = fn_gen_accountno()
                    cardno = fn_gen_cardno()
                    
                    data = [firstname, lastname, gender, dob, fathername, mothername, gmail, phoneno, doorno, street, city, state, country, zipcode, aadharno, pancard, status, accountno, accounttype, ifsccode, branch, cardno, balance, photo]

                    # calling requied function to create record of customer and create passbook
                    
                    fn_create_accountrecord(data)
                    fn_create_passbookrecord(data)
                    fn_create_deatils_photo(data)

                    page_status_label.config(text='Account Added')

                except :
                    page_status_label.config(text='Invalid Input')  
            except :
                page_status_label.config(text='Invalid Input')
            
        # add user form start here...
        firstname_lbn = Label(adduser_frame, text='First name', bg=color1, fg=color2, font=font)
        firstname_lbn.grid(row=0, column=0, pady=5)
        firstname_entry = Entry(adduser_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        firstname_entry.grid(row=0, column=1, pady=5)

        lastname_lbn = Label(adduser_frame, text='Last name', bg=color1, fg=color2, font=font)
        lastname_lbn.grid(row=0, column=2, pady=5)
        lastname_entry = Entry(adduser_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        lastname_entry.grid(row=0, column=3, pady=5)

        gender_entry = StringVar()
        gender_lbn = Label(adduser_frame, text='Gender', bg=color1, fg=color2, font=font)
        gender_lbn.grid(row=0, column=4, pady=5)
        gender_combobox = ttk.Combobox(adduser_frame, textvariable=gender_entry, values=genderlist, state='readonly', background=color2, foreground=color1, font=font, width=18)
        gender_combobox.grid(row=0, column=5, pady=5)
        gender_entry.set(genderlist[0])

        dob_lbn = Label(adduser_frame, text='Date of Birth', bg=color1, fg=color2, font=font)
        dob_lbn.grid(row=1, column=0, pady=5)
        dob_entry = Entry(adduser_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        dob_entry.grid(row=1, column=1, pady=5)

        phoneno_lbn = Label(adduser_frame, text='Phone no', bg=color1, fg=color2, font=font)
        phoneno_lbn.grid(row=1, column=2, pady=5)
        phoneno_entry = Entry(adduser_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        phoneno_entry.grid(row=1, column=3, pady=5)

        gmail_lbn = Label(adduser_frame, text='Gmail', bg=color1, fg=color2, font=font)
        gmail_lbn.grid(row=1, column=4, pady=5)
        gmail_entry = Entry(adduser_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        gmail_entry.grid(row=1, column=5, pady=5)

        fathername_label = Label(adduser_frame, text='Father Name', bg=color1, fg=color2, font=font)
        fathername_label.grid(row=2, column=0, pady=5)
        fathername_entry = Entry(adduser_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        fathername_entry.grid(row=2, column=1, pady=5)

        mothername_label = Label(adduser_frame, text='Mother Name', bg=color1, fg=color2, font=font)
        mothername_label.grid(row=2, column=2, pady=5)
        mothername_entry = Entry(adduser_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        mothername_entry.grid(row=2, column=3, pady=5)

        status_label = Label(adduser_frame, text='Status', bg=color1, fg=color2, font=font)
        status_label.grid(row=2, column=4, pady=5)
        status_entry = StringVar()
        status_combobox = ttk.Combobox(adduser_frame, textvariable=status_entry, values=statuslist, state='readonly', background=color2, foreground=color1, font=font, width=18)
        status_combobox.grid(row=2, column=5, pady=5)
        status_entry.set(statuslist[0])

        doorno_label = Label(adduser_frame, text='Door no', bg=color1, fg=color2, font=font)
        doorno_label.grid(row=3, column=0, pady=5)
        doorno_entry = Entry(adduser_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        doorno_entry.grid(row=3, column=1, pady=5)

        street_label = Label(adduser_frame, text='Street', bg=color1, fg=color2, font=font)
        street_label.grid(row=3, column=2, pady=5)
        street_entry = Entry(adduser_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        street_entry.grid(row=3, column=3, pady=5)

        city_label = Label(adduser_frame, text='City', bg=color1, fg=color2, font=font)
        city_label.grid(row=3, column=4, pady=5)
        city_entry = Entry(adduser_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        city_entry.grid(row=3, column=5, pady=5)

        state_label = Label(adduser_frame, text='State', bg=color1, fg=color2, font=font)
        state_label.grid(row=4, column=0, pady=5)
        state_entry = StringVar()
        state_combobox = ttk.Combobox(adduser_frame, textvariable=state_entry, values=statelist, state='readonly', background=color2, foreground=color1, font=font, width=18)
        state_combobox.grid(row=4, column=1, pady=5)
        state_entry.set(statelist[0])

        country_label = Label(adduser_frame, text='Country', bg=color1, fg=color2, font=font)
        country_label.grid(row=4, column=2, pady=5)
        country_entry = StringVar()
        country_combobox = ttk.Combobox(adduser_frame, textvariable=country_entry, values=countrylist, state='readonly', background=color2, foreground=color1, font=font, width=18)
        country_combobox.grid(row=4, column=3, pady=5)
        country_entry.set(countrylist[0])

        zipcode_label = Label(adduser_frame, text='Zipcode', bg=color1, fg=color2, font=font)
        zipcode_label.grid(row=4, column=4, pady=5)
        zipcode_entry = Entry(adduser_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        zipcode_entry.grid(row=4, column=5, pady=5)

        aadharno_label = Label(adduser_frame, text='Aadhar Id', bg=color1, fg=color2, font=font)
        aadharno_label.grid(row=5, column=0, pady=5)
        aadharno_entry = Entry(adduser_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        aadharno_entry.grid(row=5, column=1, pady=5)

        pancard_label = Label(adduser_frame, text='Pancard Id', bg=color1, fg=color2, font=font)
        pancard_label.grid(row=5, column=2, pady=5)
        pancard_entry = Entry(adduser_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        pancard_entry.grid(row=5, column=3, pady=5)

        accounttype_label = Label(adduser_frame, text='Account Type', bg=color1, fg=color2, font=font)
        accounttype_label.grid(row=5, column=4, pady=5)
        accounttype_entry = StringVar()
        accounttype_combobox = ttk.Combobox(adduser_frame, textvariable=accounttype_entry, values=accounttypelist, state='readonly', background=color2, foreground=color1, font=font, width=18)
        accounttype_combobox.grid(row=5, column=5, pady=5)
        accounttype_entry.set(accounttypelist[0])

        # photo selection and update section
        def select_photo():
            photopath = filedialog.askopenfilename()
            phototext_label.config(text=photopath)
            photo_entry.delete(0, END)
            photo_entry.insert(0, photopath)
        
        photo_label = Label(adduser_frame, text='Photo', bg=color1, fg=color2, font=font)
        photo_label.grid(row=6, column=0, pady=5)
        phototext_label = Label(adduser_frame, bg=color2, fg=color1, font=font, width=20)
        phototext_label.grid(row=6, column=1, pady=5)
        photo_entry = Entry(adduser_frame)
        photoupload_btn = Button(adduser_frame, text='Upload Photo', font=font, bg=color1, fg=color2, relief=FLAT, command=select_photo)
        photoupload_btn.grid(row=6, column=2, pady=5)

        # status label
        page_status_label = Label(adduser_frame, bg=color1, fg=tcolor, font=font)
        page_status_label.grid(row=8, column=0, pady=5, columnspan=5)

        # create button for adduser page
        create_btn = Button(adduser_frame, text='Create', font=font, bg=color1, fg=tcolor, relief=FLAT, command=fn_createaccount)
        create_btn.grid(row=7, column=0, pady=10)
        
    # first thing's first
    employeepage_mainframe.destroy()

    # create requied frame's
    adduser_mainframe = Frame(appbody, bg=color1, relief=FLAT)
    adduser_mainframe.pack(fill=BOTH, expand=1)
    adduser_backframe = Frame(adduser_mainframe, bg=color1, relief=FLAT)
    adduser_backframe.pack(fill=X)
    adduser_frame = Frame(adduser_mainframe, bg=color1, relief=FLAT)
    adduser_frame.pack(fill=BOTH, expand=1)

    # back button for adduserpage of employeepage
    back_btn = Button(adduser_backframe, text='Back', bg=color1, fg=color2, font=font, relief=FLAT, command=fn_adduser_backframe)
    back_btn.pack(side=LEFT)

    # calling requied function
    fn_adduser_frame()
    
def employee_deleteuser(appbody, loginpage_frame, employeepage_mainframe, branch, ifsccode):
    # sub-function
    def fn_deleteuser_backframe():
        deleteuser_mainframe.destroy()
        employeepage(appbody, loginpage_frame, branch, ifsccode)

    def fn_deleteuser_frame():
        # sub-function
        def fn_delete_data(customerno, img):
            # create requied frame's
            image_frame = Frame(delete_frame, bg=color1, relief=FLAT)
            image_frame.pack(side=LEFT, fill=BOTH, expand=1)
            button_frame = Frame(delete_frame, bg=color1, relief=FLAT)
            button_frame.pack(side=RIGHT, fill=BOTH, expand=1)
            
            # image frame stuff...
            image_lbn = Label(image_frame, image=img, bg=color1, fg=color2)
            image_lbn.pack()

            # fn_conform_delete function will delete data from database and all records of customer
            def fn_conform_delete():
                
                # deleting customer record from database...
                conn = sqlite3.connect(database3)
                c = conn.cursor()
                c.execute("DELETE FROM customer WHERE accountno = ?", (customerno, ))
                conn.commit()
                conn.close()

                # deleting transaction record's from passbook database...
                conn = sqlite3.connect(database5)
                c = conn.cursor()
                c.execute("DROP TABLE {}".format(f'acno{customerno}'))
                conn.commit()
                conn.close()

                # deleting id card of employee
                os.remove(r'{}\{}.png'.format(customerid_folder, customerno))

                delete_status_lbn.config(text='Customer Deleted')

            # button frame stuff...
            conform_message_lbn = Label(button_frame, text='Conform Delete Customer', font=font, bg=color1, fg=color2)
            conform_message_lbn.grid(row=0, column=0, padx=10, pady=10)
            conform_delete_btn = Button(button_frame, text='Delete', bg=color1, fg=tcolor, font=font, relief=FLAT, command=fn_conform_delete)
            conform_delete_btn.grid(row=1, column=0, padx=10, pady=10)

            delete_status_lbn = Label(button_frame, bg=color1, fg=color2, font=font)
            delete_status_lbn.grid(row=2, column=0, padx=10, pady=10)


        def fn_search_data():
            try: 
                global img, img1
                customerno = int(search_entry.get())
                img1 = Image.open(r'{}\{}.png'.format(customerid_folder, customerno))
                img1 = img1.resize((300,400))
                img = ImageTk.PhotoImage(img1)
                fn_delete_data(customerno, img)
                search_status_lbn.config(text='')
            except :
                search_status_lbn.config(text='Invaild Input')

        # create requied frame's for deleteuser_frame
        search_frame = Frame(deleteuser_frame, bg=color1, relief=FLAT)
        search_frame.pack(fill=X)
        delete_frame = Frame(deleteuser_frame, bg=color1, relief=FLAT)
        delete_frame.pack(fill=BOTH, expand=1)

        # search frame stuff...
        search_lbn = Label(search_frame, text='Search ac.no', bg=color1, fg=color2, font=font)
        search_lbn.grid(row=0, column=0, padx=5)
        search_entry = Entry(search_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        search_entry.grid(row=0, column=1, padx=5)
        search_btn = Button(search_frame, text='Delete', bg=color1, fg=color2, font=font, relief=FLAT, command=fn_search_data)
        search_btn.grid(row=0, column=2, padx=5)
        search_status_lbn = Label(search_frame, bg=color1, fg=color2, font=font)
        search_status_lbn.grid(row=1, column=0, columnspan=2, pady=5)
        

    # first thing's first
    employeepage_mainframe.destroy()

    # create requied frames
    deleteuser_mainframe = Frame(appbody, bg=color1, relief=FLAT)
    deleteuser_mainframe.pack(fill=BOTH, expand=1)
    deleteuser_backframe = Frame(deleteuser_mainframe, bg=color1, relief=FLAT)
    deleteuser_backframe.pack(fill=X)
    deleteuser_frame = Frame(deleteuser_mainframe, bg=color1, relief=FLAT)
    deleteuser_frame.pack(fill=BOTH, expand=1)

    # back button for delete page
    back_btn = Button(deleteuser_backframe, text='Back', bg=color1, fg=color2, font=font, relief=FLAT, command=fn_deleteuser_backframe)
    back_btn.pack(side=LEFT)

    # calling requied function
    fn_deleteuser_frame()
    
def employee_updateuser(appbody, loginpage_frame, employeepage_mainframe, branch, ifsccode):
    # sub-function
    def fn_updateuser_backframe():
        updateuser_mainframe.destroy()
        employeepage(appbody, loginpage_frame, branch, ifsccode)

    def fn_updateuser_frame():
        # sub-function
        def fn_update_inputframe(olddata):
            # update data
            def fn_update_new_data():
                try:
                    # getting data from form...
                    firstname = firstname_entry.get()
                    lastname = lastname_entry.get()
                    gender = gender_entry.get()
                    dob = dob_entry.get()
                    fathername = fathername_entry.get()
                    mothername = mothername_entry.get()
                    gmail = gmail_entry.get()
                    phoneno = int(phoneno_entry.get())
                    doorno = int(doorno_entry.get())
                    street = street_entry.get()
                    city = city_entry.get()
                    state = state_entry.get()
                    country = country_entry.get()
                    zipcode = int(zipcode_entry.get())
                    aadharno = int(aadharno_entry.get())
                    pancard = pancard_entry.get()
                    status = status_entry.get()
                    accounttype = accounttype_entry.get()
                    photo = bytes()

                    photopath_entry = photo_entry.get()
                    if photopath_entry:
                        with open(photopath_entry, 'rb') as r:
                            photo = r.read()
                    else:
                        photo = olddata[0][23]
                    
                    # add account.no to newdata at the end for database query
                    accountno = olddata[0][17]
                    newdata = [firstname, lastname, gender, dob, fathername, mothername, gmail, phoneno, doorno, street, city, state, country, zipcode, aadharno, pancard, status, photo, accounttype, accountno]

                    # updating data to database...
                    conn = sqlite3.connect(database3)
                    c = conn.cursor()
                    c.execute("""
                    UPDATE customer SET
                    firstname = ?,
                    lastname = ?,
                    gender = ?,
                    dob = ?,
                    fathername = ?,
                    mothername = ?,
                    gmail = ?,
                    phoneno = ?,
                    doorno = ?,
                    street = ?,
                    city = ?,
                    state = ?,
                    country = ?,
                    zipcode = ?,
                    aadharno = ?,
                    pancardno = ?,
                    status = ?,
                    photo = ?,
                    accounttype = ?
                    WHERE accountno = ?
                    """, newdata)
                    conn.commit()
                    conn.close()

                    def update_customerid():
                        # update customer id card
                        font = ImageFont.truetype('baloo.ttf', size=20)
                        temp = Image.open(customer_template)
                        photo_for_temp = Image.open(io.BytesIO(photo))
                        photo_for_temp = photo_for_temp.resize((110, 135))
                        temp.paste(photo_for_temp, (480, 100, 590, 235))
                        draw = ImageDraw.Draw(temp)
                        draw.text((175, 105), text=f'{firstname} {lastname}', font=font, fill='black')
                        draw.text((175, 160), text=f'{dob}', font=font, fill='black')
                        draw.text((175, 210), text=f'{gender}', font=font, fill='black')
                        draw.text((175, 260), text=f'{phoneno}', font=font, fill='black')
                        draw.text((175, 310), text=f'{fathername}', font=font, fill='black')
                        draw.text((175, 365), text=f'{mothername}', font=font, fill='black')
                        draw.text((175, 415), text=f'{doorno}, {street}, {city},', font=font, fill='black')
                        draw.text((175, 455), text=f'{state}, {country}, {zipcode}', font=font, fill='black')
                        draw.text((175, 565), text=f'{accountno}', font=font, fill='black')
                        draw.text((175, 620), text=f'{accounttype}', font=font, fill='black')
                        draw.text((175, 670), text=f'{branch}', font=font, fill='black')
                        draw.text((175, 720), text=f'{ifsccode}', font=font, fill='black')

                        os.remove(r'{}\{}.png'.format(customerid_folder, accountno))
                        temp.save(r'{}\{}.png'.format(customerid_folder, accountno))

                    def upadte_customercard():
                        font = ImageFont.truetype('baloo.ttf', size=30)
                        temp = Image.open(card_template)
                        draw = ImageDraw.Draw(temp)
                        draw.text((145,160), text=f'{accountno}', font=font, fill='white')
                        draw.text((145,240), text=f'{firstname} {lastname}', font=font, fill='white')

                        temp.save(r'{}\{}.png'.format(card_folder, accountno))

                    update_customerid()
                    upadte_customercard()

                    page_status_label.config(text='Update Sucess')
                      
                except :
                    page_status_label.config(text='Invalid Input')
                
            # update form start here...
            firstname_lbn = Label(update_inputframe, text='First name', bg=color1, fg=color2, font=font)
            firstname_lbn.grid(row=0, column=0, pady=5)
            firstname_entry = Entry(update_inputframe, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT, text=olddata[0][0])
            firstname_entry.grid(row=0, column=1, pady=5)

            lastname_lbn = Label(update_inputframe, text='Last name', bg=color1, fg=color2, font=font)
            lastname_lbn.grid(row=0, column=2, pady=5)
            lastname_entry = Entry(update_inputframe, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            lastname_entry.grid(row=0, column=3, pady=5)

            gender_entry = StringVar()
            gender_lbn = Label(update_inputframe, text='Gender', bg=color1, fg=color2, font=font)
            gender_lbn.grid(row=0, column=4, pady=5)
            gender_combobox = ttk.Combobox(update_inputframe, textvariable=gender_entry, values=genderlist, state='readonly', background=color2, foreground=color1, font=font, width=18)
            gender_combobox.grid(row=0, column=5, pady=5)

            dob_lbn = Label(update_inputframe, text='Date of Birth', bg=color1, fg=color2, font=font)
            dob_lbn.grid(row=1, column=0, pady=5)
            dob_entry = Entry(update_inputframe, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            dob_entry.grid(row=1, column=1, pady=5)

            phoneno_lbn = Label(update_inputframe, text='Phone no', bg=color1, fg=color2, font=font)
            phoneno_lbn.grid(row=1, column=2, pady=5)
            phoneno_entry = Entry(update_inputframe, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            phoneno_entry.grid(row=1, column=3, pady=5)

            gmail_lbn = Label(update_inputframe, text='Gmail', bg=color1, fg=color2, font=font)
            gmail_lbn.grid(row=1, column=4, pady=5)
            gmail_entry = Entry(update_inputframe, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            gmail_entry.grid(row=1, column=5, pady=5)

            fathername_label = Label(update_inputframe, text='Father Name', bg=color1, fg=color2, font=font)
            fathername_label.grid(row=2, column=0, pady=5)
            fathername_entry = Entry(update_inputframe, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            fathername_entry.grid(row=2, column=1, pady=5)

            mothername_label = Label(update_inputframe, text='Mother Name', bg=color1, fg=color2, font=font)
            mothername_label.grid(row=2, column=2, pady=5)
            mothername_entry = Entry(update_inputframe, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            mothername_entry.grid(row=2, column=3, pady=5)

            status_label = Label(update_inputframe, text='Status', bg=color1, fg=color2, font=font)
            status_label.grid(row=2, column=4, pady=5)
            status_entry = StringVar()
            status_combobox = ttk.Combobox(update_inputframe, textvariable=status_entry, values=statuslist, state='readonly', background=color2, foreground=color1, font=font, width=18)
            status_combobox.grid(row=2, column=5, pady=5)

            doorno_label = Label(update_inputframe, text='Door no', bg=color1, fg=color2, font=font)
            doorno_label.grid(row=3, column=0, pady=5)
            doorno_entry = Entry(update_inputframe, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            doorno_entry.grid(row=3, column=1, pady=5)

            street_label = Label(update_inputframe, text='Street', bg=color1, fg=color2, font=font)
            street_label.grid(row=3, column=2, pady=5)
            street_entry = Entry(update_inputframe, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            street_entry.grid(row=3, column=3, pady=5)

            city_label = Label(update_inputframe, text='City', bg=color1, fg=color2, font=font)
            city_label.grid(row=3, column=4, pady=5)
            city_entry = Entry(update_inputframe, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            city_entry.grid(row=3, column=5, pady=5)

            state_label = Label(update_inputframe, text='State', bg=color1, fg=color2, font=font)
            state_label.grid(row=4, column=0, pady=5)
            state_entry = StringVar()
            state_combobox = ttk.Combobox(update_inputframe, textvariable=state_entry, values=statelist, state='readonly', background=color2, foreground=color1, font=font, width=18)
            state_combobox.grid(row=4, column=1, pady=5)

            country_label = Label(update_inputframe, text='Country', bg=color1, fg=color2, font=font)
            country_label.grid(row=4, column=2, pady=5)
            country_entry = StringVar()
            country_combobox = ttk.Combobox(update_inputframe, textvariable=country_entry, values=countrylist, state='readonly', background=color2, foreground=color1, font=font, width=18)
            country_combobox.grid(row=4, column=3, pady=5)

            zipcode_label = Label(update_inputframe, text='Zipcode', bg=color1, fg=color2, font=font)
            zipcode_label.grid(row=4, column=4, pady=5)
            zipcode_entry = Entry(update_inputframe, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            zipcode_entry.grid(row=4, column=5, pady=5)

            aadharno_label = Label(update_inputframe, text='Aadhar Id', bg=color1, fg=color2, font=font)
            aadharno_label.grid(row=5, column=0, pady=5)
            aadharno_entry = Entry(update_inputframe, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            aadharno_entry.grid(row=5, column=1, pady=5)

            pancard_label = Label(update_inputframe, text='Pancard Id', bg=color1, fg=color2, font=font)
            pancard_label.grid(row=5, column=2, pady=5)
            pancard_entry = Entry(update_inputframe, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            pancard_entry.grid(row=5, column=3, pady=5)

            accounttype_label = Label(update_inputframe, text='Account Type', bg=color1, fg=color2, font=font)
            accounttype_label.grid(row=5, column=4, pady=5)
            accounttype_entry = StringVar()
            accounttype_combobox = ttk.Combobox(update_inputframe, textvariable=accounttype_entry, values=accounttypelist, state='readonly', background=color2, foreground=color1, font=font, width=18)
            accounttype_combobox.grid(row=5, column=5, pady=5)

            # photo selection and update section
            def select_photo():
                photopath = filedialog.askopenfilename()
                phototext_label.config(text=photopath)
                photo_entry.delete(0, END)
                photo_entry.insert(0, photopath)
            
            photo_label = Label(update_inputframe, text='Photo', bg=color1, fg=color2, font=font)
            photo_label.grid(row=6, column=0, pady=5)
            phototext_label = Label(update_inputframe, bg=color2, fg=color1, font=font, width=20)
            phototext_label.grid(row=6, column=1, pady=5)
            photo_entry = Entry(update_inputframe)
            photoupload_btn = Button(update_inputframe, text='Upload Photo', font=font, bg=color1, fg=color2, relief=FLAT, command=select_photo)
            photoupload_btn.grid(row=6, column=2, pady=5)

            # insert data into field's
            def fn_update_fields_with_olddata():

                firstname_entry.insert(0, olddata[0][0])
                lastname_entry.insert(0, olddata[0][1])
                gender_entry.set(olddata[0][2])
                dob_entry.insert(0, olddata[0][3])
                phoneno_entry.insert(0, olddata[0][7])
                gmail_entry.insert(0, olddata[0][6])
                fathername_entry.insert(0, olddata[0][4])
                mothername_entry.insert(0, olddata[0][5])
                status_entry.set(olddata[0][16])
                doorno_entry.insert(0, olddata[0][8])
                street_entry.insert(0, olddata[0][9])
                city_entry.insert(0, olddata[0][10])
                state_entry.set(olddata[0][11])
                country_entry.set(olddata[0][12])
                zipcode_entry.insert(0, olddata[0][13])
                aadharno_entry.insert(0, olddata[0][14])
                pancard_entry.insert(0, olddata[0][15])
                accounttype_entry.set(olddata[0][18])

            fn_update_fields_with_olddata()
            
            # back to form...
            page_status_label = Label(update_inputframe, bg=color1, fg=color2, font=font)
            page_status_label.grid(row=7, column=0, columnspan=5)

            update_btn = Button(update_inputframe, text='Update', bg=color1, fg=tcolor, relief=FLAT, font=font, command=fn_update_new_data)
            update_btn.grid(row=8, column=0, pady=10)

        def fn_search_frame():
            # sub-function
            def fn_search_data():
                # getting employee id from entry field
                id = search_entry.get()
                try:
                    conn = sqlite3.connect(database3)
                    c = conn.cursor()
                    c.execute('SELECT * FROM customer WHERE accountno = ?', (int(id), ))
                    data = c.fetchall()
                    if data:
                        # sending data as old data into function
                        search_status = Label(search_frame, text='', bg=color1, fg=color2, font=font)
                        search_status.grid(row=1, column=0, columnspan=3, padx=5)

                        fn_update_inputframe(data)
                    else:
                        search_status = Label(search_frame, text='Invalid Input', bg=color1, fg=color2, font=font)
                        search_status.grid(row=1, column=0, columnspan=3, padx=5)
                    conn.commit()
                    conn.close()
                    
                except :
                    search_status = Label(search_frame, text='Invalid Input', bg=color1, fg=color2, font=font)
                    search_status.grid(row=1, column=0, columnspan=3, padx=5)

            # frame start here...
            search_lbn = Label(search_frame, text='Search ID', bg=color1, fg=color2, font=font)
            search_lbn.grid(row=0, column=0, padx=5)
            search_entry = Entry(search_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            search_entry.grid(row=0, column=1, padx=5)
            search_btn = Button(search_frame, text='Get Data', bg=color1, fg=color2, font=font, relief=FLAT, command=fn_search_data)
            search_btn.grid(row=0, column=2, padx=5)
            
        # fn_updateuser_frame start here...
        # create requied frame's
        search_frame = Frame(updateuser_frame, bg=color1, relief=FLAT)
        search_frame.pack(fill=X)
        update_inputframe = Frame(updateuser_frame, bg=color1, relief=FLAT)
        update_inputframe.pack(fill=BOTH, expand=1)

        # calling requied function
        fn_search_frame()
        
    # first thing's first
    employeepage_mainframe.destroy()

    # create requied frame's
    updateuser_mainframe = Frame(appbody, bg=color1, relief=FLAT)
    updateuser_mainframe.pack(fill=BOTH, expand=1)
    updateuser_backframe = Frame(updateuser_mainframe, bg=color1, relief=FLAT)
    updateuser_backframe.pack(fill=X)
    updateuser_frame = Frame(updateuser_mainframe, bg=color1, relief=FLAT)
    updateuser_frame.pack(fill=BOTH, expand=1)

    # back button for update user page
    back_btn = Button(updateuser_backframe, text='Back', bg=color1, fg=color2, relief=FLAT, font=font, command=fn_updateuser_backframe)
    back_btn.pack(side=LEFT)

    # calling requied function
    fn_updateuser_frame()
    
def employee_infouser(appbody, loginpage_frame, employeepage_mainframe, branch, ifsccode):
    # sub-function
    def fn_infouser_backframe():
        infouser_mainframe.destroy()
        employeepage(appbody, loginpage_frame, branch, ifsccode)
        
    def fn_infouser_frame():
        # sub-function
        def fn_result_frame(data):
            # sub-function      
            def fn_details_of_customer():
                # create details of customer frame
                details_frame = Frame(data_frame, bg=color1, relief=FLAT)
                details_frame.pack(fill=BOTH, expand=1)
                # title's of detail's
                name_lbn = Label(details_frame, text='Name :', bg=color1, fg=color2, font=font, anchor=E)
                name_lbn.grid(row=0, column=0, padx=2, pady=2, sticky=E)
                dob_lbn = Label(details_frame, text='Date of Birth :', bg=color1, fg=color2, font=font, anchor=E)
                dob_lbn.grid(row=1, column=0, padx=2, pady=2, sticky=E)
                gender_lbn = Label(details_frame, text='Gender :', bg=color1, fg=color2, font=font, anchor=E)
                gender_lbn.grid(row=2, column=0, padx=2, pady=2, sticky=E)
                fathername_lbn = Label(details_frame, text='Father Name :', bg=color1, fg=color2, font=font, anchor=E)
                fathername_lbn.grid(row=3, column=0, padx=2, pady=2, sticky=E)
                mothername_lbn = Label(details_frame, text='Mother Name :', bg=color1, fg=color2, font=font, anchor=E)
                mothername_lbn.grid(row=4, column=0, padx=2, pady=2, sticky=E)
                phoneno_lbn = Label(details_frame, text='Phone No :', bg=color1, fg=color2, font=font, anchor=E)
                phoneno_lbn.grid(row=5, column=0, padx=2, pady=2, sticky=E)
                gmail_lbn = Label(details_frame, text='Gmail :', bg=color1, fg=color2, font=font, anchor=E)
                gmail_lbn.grid(row=6, column=0, padx=2, pady=2, sticky=E)
                status_lbn = Label(details_frame, text='Status :', bg=color1, fg=color2, font=font, anchor=E)
                status_lbn.grid(row=7, column=0, padx=2, pady=2, sticky=E)
                address_lbn = Label(details_frame, text='Address :', bg=color1, fg=color2, font=font, anchor=E)
                address_lbn.grid(row=8, column=0, padx=2, pady=2, sticky=E)

                
                accountno_lbn = Label(details_frame, text='Account No :', bg=color1, fg=color2, font=font, anchor=E)
                accountno_lbn.grid(row=0, column=2, padx=2, pady=2, sticky=E)
                accounttype_lbn = Label(details_frame, text='Account Type :', bg=color1, fg=color2, font=font, anchor=E)
                accounttype_lbn.grid(row=1, column=2, padx=2, pady=2, sticky=E)
                branch_lbn = Label(details_frame, text='Branch :', bg=color1, fg=color2, font=font, anchor=E)
                branch_lbn.grid(row=2, column=2, padx=2, pady=2, sticky=E)
                ifsccode_lbn = Label(details_frame, text='IFSC Code :', bg=color1, fg=color2, font=font, anchor=E)
                ifsccode_lbn.grid(row=3, column=2, padx=2, pady=2, sticky=E)
                balance_lbn = Label(details_frame, text='Balance :', bg=color1, fg=color2, font=font, anchor=E)
                balance_lbn.grid(row=4, column=2, padx=2, pady=2, sticky=E)
                aadharno_lbn = Label(details_frame, text='Aadhar No :', bg=color1, fg=color2, font=font, anchor=E)
                aadharno_lbn.grid(row=5, column=2, padx=2, pady=2, sticky=E)
                pancardno_lbn = Label(details_frame, text='Pancard No :', bg=color1, fg=color2, font=font, anchor=E)
                pancardno_lbn.grid(row=6, column=2, padx=2, pady=2, sticky=E)
                cardno_lbn = Label(details_frame, text='Card No :', bg=color1, fg=color2, font=font, anchor=E)
                cardno_lbn.grid(row=7, column=2, padx=2, pady=2, sticky=E)
                
                # information of customer
                name_value = Label(details_frame, text=f'{data[0]} {data[1]}', bg=color1, fg=color2, font=font, anchor=W)
                name_value.grid(row=0, column=1, padx=(2,5), pady=2, sticky=W)
                dob_value = Label(details_frame, text=f'{data[3]}', bg=color1, fg=color2, font=font, anchor=W)
                dob_value.grid(row=1, column=1, padx=(2,5), pady=2, sticky=W)
                gender_value = Label(details_frame, text=f'{data[2]}', bg=color1, fg=color2, font=font, anchor=W)
                gender_value.grid(row=2, column=1, padx=(2,5), pady=2, sticky=W)
                fathername_value = Label(details_frame, text=f'{data[4]}', bg=color1, fg=color2, font=font, anchor=W)
                fathername_value.grid(row=3, column=1, padx=(2,5), pady=2, sticky=W)
                mothername_value = Label(details_frame, text=f'{data[5]}', bg=color1, fg=color2, font=font, anchor=W)
                mothername_value.grid(row=4, column=1, padx=(2,5), pady=2, sticky=W)
                phoneno_value = Label(details_frame, text=f'{data[7]}', bg=color1, fg=color2, font=font, anchor=W)
                phoneno_value.grid(row=5, column=1, padx=(2,5), pady=2, sticky=W)
                gmail_value = Label(details_frame, text=f'{data[6]}', bg=color1, fg=color2, font=font, anchor=W)
                gmail_value.grid(row=6, column=1, padx=(2,5), pady=2, sticky=W)
                status_value = Label(details_frame, text=f'{data[16]}', bg=color1, fg=color2, font=font, anchor=W)
                status_value.grid(row=7, column=1, padx=(2,5), pady=2, sticky=W)
                address1_value = Label(details_frame, text=f'{data[8]},{data[9]},{data[10]}', bg=color1, fg=color2, font=font, anchor=W)
                address1_value.grid(row=8, column=1, padx=(2,5), pady=2, sticky=W)
                address2_value = Label(details_frame, text=f'{data[11]},{data[12]},{data[13]}', bg=color1, fg=color2, font=font, anchor=W)
                address2_value.grid(row=9, column=1, padx=(2,5), pady=2, sticky=W)

                accountno_value = Label(details_frame, text=f'{data[17]}', bg=color1, fg=color2, font=font, anchor=W)
                accountno_value.grid(row=0, column=3, padx=(2,5), pady=2, sticky=W)
                accounttype_value = Label(details_frame, text=f'{data[18]}', bg=color1, fg=color2, font=font, anchor=W)
                accounttype_value.grid(row=1, column=3, padx=(2,5), pady=2, sticky=W)
                branch_value = Label(details_frame, text=f'{data[20]}', bg=color1, fg=color2, font=font, anchor=W)
                branch_value.grid(row=2, column=3, padx=(2,5), pady=2, sticky=W)
                ifsccode_value = Label(details_frame, text=f'{data[19]}', bg=color1, fg=color2, font=font, anchor=W)
                ifsccode_value.grid(row=3, column=3, padx=(2,5), pady=2, sticky=W)
                balance_value = Label(details_frame, text=f'{data[22]}', bg=color1, fg=color2, font=font, anchor=W)
                balance_value.grid(row=4, column=3, padx=(2,5), pady=2, sticky=W)
                aadharno_value = Label(details_frame, text=f'{data[14]}', bg=color1, fg=color2, font=font, anchor=W)
                aadharno_value.grid(row=5, column=3, padx=(2,5), pady=2, sticky=W)
                pancardno_value = Label(details_frame, text=f'{data[15]}', bg=color1, fg=color2, font=font, anchor=W)
                pancardno_value.grid(row=6, column=3, padx=(2,5), pady=2, sticky=W)
                cardno_value = Label(details_frame, text=f'{data[21]}', bg=color1, fg=color2, font=font, anchor=W)
                cardno_value.grid(row=7, column=3, padx=(2,5), pady=2, sticky=W)

            # create requied frame's
            photo_frame = Frame(result_frame, bg=color1, relief=FLAT, padx=5)
            photo_frame.pack(side=LEFT, fill=Y)
            data_frame = Frame(result_frame, bg=color1, relief=FLAT, padx=5)
            data_frame.pack(side=RIGHT, fill=BOTH, expand=1)
            # photo frame start her...
            global img
            img = Image.open(io.BytesIO(data[23]))
            img = img.resize((200,250))
            img = ImageTk.PhotoImage(img)
            photo_lbn = Label(photo_frame, image=img)
            photo_lbn.grid(row=0, column=0, pady=5)

            # calling requied function
            fn_details_of_customer()
            
        def fn_search_frame():
            # sub-function
            def fn_getdata():
                try:
                    id = int(search_entry.get())
                    conn = sqlite3.connect(database3)
                    c = conn.cursor()
                    c.execute("SELECT * FROM customer WHERE accountno = ?", (id, ))
                    result = c.fetchall()
                    data = result[0]
                    # calling result function to display information...
                    search_status_lbn.config(text='')
                    fn_result_frame(data)
                    conn.commit()
                    conn.close()
                except :
                    search_status_lbn.config(text='Invalid Input')
                
            # create requied label, entry, button
            

            search_lbn = Label(search_frame, text='Search ac.no', bg=color1, fg=color2, font=font)
            search_lbn.grid(row=0, column=0, padx=5)
            search_entry = Entry(search_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            search_entry.grid(row=0, column=1, padx=5)
            search_btn = Button(search_frame, text='Search', bg=color1, fg=color2, font=font, relief=FLAT, command=fn_getdata)
            search_btn.grid(row=0, column=2, padx=5)
            search_status_lbn = Label(search_frame, bg=color1, fg=color2, font=font)
            search_status_lbn.grid(row=1, column=0, columnspan=3)

        # create requied frame's
        search_frame = Frame(infouser_frame, bg=color1, relief=FLAT)
        search_frame.pack(fill=X)
        result_frame = Frame(infouser_frame, bg=color1, relief=FLAT, padx=5)
        result_frame.pack(fill=BOTH, expand=1)
        

        # calling requied function
        fn_search_frame()
        
    # first thing's first
    employeepage_mainframe.destroy()

    # create requied frame's
    infouser_mainframe = Frame(appbody, bg=color1, relief=FLAT)
    infouser_mainframe.pack(fill=BOTH, expand=1)
    infouser_backframe = Frame(infouser_mainframe, bg=color1, relief=FLAT)
    infouser_backframe.pack(fill=X)
    infouser_frame = Frame(infouser_mainframe, bg=color1, relief=FLAT)
    infouser_frame.pack(fill=BOTH, expand=1)

    # back button for searchuser page
    back_btn = Button(infouser_backframe, text='Back', bg=color1, fg=color2, font=font, relief=FLAT, command=fn_infouser_backframe)
    back_btn.pack(side=LEFT)

    # calling requied function
    fn_infouser_frame()
    
def employee_deposit(appbody, loginpage_frame, employeepage_mainframe, branch, ifsccode):
    # sub-function
    def fn_deposit_backframe():
        deposit_mainframe.destroy()
        employeepage(appbody, loginpage_frame, branch, ifsccode)
        
    def fn_deposit_frame():
        # sub-function
        def fn_deposit_inputframe(id):
            # sub-function
            def fn_depositamount():
                # sub-function
                def fn_add_deposit_to_passbook(amount):
                    conn = sqlite3.connect(database5)
                    c = conn.cursor()
                    c.execute("SELECT * FROM {}".format(f'acno{id}'))
                    result = c.fetchall()
                    if result:
                        date = time.strftime("%d/%m/%Y")
                        remark = 'Self deposit from bank'
                        ttype = 'Credit'
                        tamount = amount
                        balance = result[-1][4] + amount
                        data = [date, remark, ttype, tamount, balance]
                        c.execute('INSERT INTO {} VALUES (?,?,?,?,?)'.format(f'acno{id}'), data)
                        addamount_status_lbn.config(text='Deposit sucess')
                    else:
                        date = time.strftime("%d/%m/%Y")
                        remark = 'Self deposit from bank'
                        ttype = 'Credit'
                        tamount = amount
                        balance = amount
                        data = [date, remark, ttype, tamount, balance]
                        c.execute('INSERT INTO {} VALUES (?,?,?,?,?)'.format(f'acno{id}'), data)
                        addamount_status_lbn.config(text='Deposit sucess')
                    conn.commit()
                    conn.close()

                def fn_add_deposit_to_customer(amount):
                    conn = sqlite3.connect(database3)
                    c = conn.cursor()
                    c.execute("SELECT balance FROM customer WHERE accountno = ?", (id, ))
                    result = c.fetchall()
                    oldamount = result[-1][0]
                    newamount = oldamount + amount
                    c.execute('UPDATE customer SET balance = ? WHERE accountno = ?', (newamount, id))
                    conn.commit()
                    conn.close()

                try:
                    amount = float(addamount_entry.get())
                    addamount_status_lbn.config(text='')
                    fn_add_deposit_to_passbook(amount)
                    fn_add_deposit_to_customer(amount)
                except :
                    addamount_status_lbn.config(text='Invaild Input')
                
            note_lbn = Label(deposit_inputframe, text="* Amount should be a number", bg=color1, fg=color2, font=font)
            note_lbn.grid(row=0, column=0, columnspan=2)
            addamount_lbn = Label(deposit_inputframe, text='Amount', bg=color1, fg=color2, font=font)
            addamount_lbn.grid(row=1, column=0, padx=5, pady=5, sticky=E)
            addamount_entry = Entry(deposit_inputframe, bg=color2, fg=color1, font=font, justify=CENTER)
            addamount_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)
            addamount_btn = Button(deposit_inputframe, text='Deposit', bg=color1, fg=color2, font=font, relief=FLAT, command=fn_depositamount)
            addamount_btn.grid(row=2, column=1, padx=5, pady=5, sticky=W)
            addamount_status_lbn = Label(deposit_inputframe, bg=color1, fg=color2, font=font)
            addamount_status_lbn.grid(row=3, column=0, columnspan=2)
            
        def fn_search_frame():
            # sub-function
            def fn_getdata():
                try:
                    id = int(search_entry.get())
                    conn = sqlite3.connect(database3)
                    c = conn.cursor()
                    c.execute('SELECT accountno FROM customer WHERE accountno = ?', (id, ))
                    result = c.fetchall()
                    if result:
                        search_status_lbn.config(text='')
                        fn_deposit_inputframe(id)
                    conn.commit()
                    conn.close()
                except :
                    search_status_lbn.config(text='Invaild Input')

            # create requied label, entry, button
            search_lbn = Label(search_frame, text='Search ac.no', bg=color1, fg=color2, font=font)
            search_lbn.grid(row=0, column=0, padx=5)
            search_entry = Entry(search_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            search_entry.grid(row=0, column=1, padx=5)
            search_btn = Button(search_frame, text='Search', bg=color1, fg=color2, font=font, relief=FLAT, command=fn_getdata)
            search_btn.grid(row=0, column=2, padx=5)
            search_status_lbn = Label(search_frame, bg=color1, fg=color2, font=font)
            search_status_lbn.grid(row=1, column=0, columnspan=3)
            
        # fn_deposit_frame start here...
        # create requied frame's
        search_frame = Frame(deposit_frame, bg=color1, relief=FLAT)
        search_frame.pack(fill=X)
        deposit_inputframe = Frame(deposit_frame, bg=color1, relief=FLAT, padx=200)
        deposit_inputframe.pack(fill=BOTH, expand=1)

        # calling requied function
        fn_search_frame()

    # first thing's first
    employeepage_mainframe.destroy()

    # create requied frame's
    deposit_mainframe = Frame(appbody, bg=color1, relief=FLAT)
    deposit_mainframe.pack(fill=BOTH, expand=1)
    deposit_backframe = Frame(deposit_mainframe, bg=color1, relief=FLAT)
    deposit_backframe.pack(fill=X)
    deposit_frame = Frame(deposit_mainframe, bg=color1, relief=FLAT)
    deposit_frame.pack(fill=BOTH, expand=1)

    # back button for searchuser page
    back_btn = Button(deposit_backframe, text='Back', bg=color1, fg=color2, font=font, relief=FLAT, command=fn_deposit_backframe)
    back_btn.pack(side=LEFT)

    # calling requied function
    fn_deposit_frame()

def employee_withdraw(appbody, loginpage_frame, employeepage_mainframe, branch, ifsccode):
    # sub-function
    def fn_withdraw_backframe():
        withdraw_mainframe.destroy()
        employeepage(appbody, loginpage_frame, branch, ifsccode)
        
    def fn_withdraw_frame():
        # sub-function
        def fn_withdraw_inputframe(id, balance):
            # sub-function
            def fn_withdrawamount():
                # sub-function
                def fn_add_withdraw_to_passbook(amount):
                    conn = sqlite3.connect(database5)
                    c = conn.cursor()
                    c.execute("SELECT * FROM {}".format(f'acno{id}'))
                    result = c.fetchall()
                    if result:
                        date = time.strftime("%d/%m/%Y")
                        remark = 'Self withdraw from bank'
                        ttype = 'Debit'
                        tamount = amount
                        tbalance = result[-1][4] - amount
                        data = [date, remark, ttype, tamount, tbalance]
                        c.execute('INSERT INTO {} VALUES (?,?,?,?,?)'.format(f'acno{id}'), data)
                        withdrawamount_status_lbn.config(text='Withdraw sucess')
                    else:
                        date = time.strftime("%d/%m/%Y")
                        remark = 'Self withdraw from bank'
                        ttype = 'Debit'
                        tamount = amount
                        tbalance = amount
                        data = [date, remark, ttype, tamount, tbalance]
                        c.execute('INSERT INTO {} VALUES (?,?,?,?,?)'.format(f'acno{id}'), data)
                        withdrawamount_status_lbn.config(text='Withdraw sucess')
                    conn.commit()
                    conn.close()

                def fn_add_withdraw_to_customer(checkfund):
                    conn = sqlite3.connect(database3)
                    c = conn.cursor()
                    c.execute('UPDATE customer SET balance = ? WHERE accountno = ?', (checkfund, id))
                    conn.commit()
                    conn.close()

                try:
                    amount = float(withdrawamount_entry.get())
                    checkfund = balance - amount
                    if checkfund < 0 :
                        withdrawamount_status_lbn.config(text='Insufficient funds')
                    else:
                        withdrawamount_status_lbn.config(text='')
                        fn_add_withdraw_to_passbook(amount)
                        fn_add_withdraw_to_customer(checkfund)
                except :
                    withdrawamount_status_lbn.config(text='Invaild Input')
                
            note_lbn = Label(withdraw_inputframe, text="* Amount should be a number", bg=color1, fg=color2, font=font)
            note_lbn.grid(row=0, column=0, columnspan=2)
            withdrawamount_lbn = Label(withdraw_inputframe, text='Amount', bg=color1, fg=color2, font=font)
            withdrawamount_lbn.grid(row=1, column=0, padx=5, pady=5, sticky=E)
            withdrawamount_entry = Entry(withdraw_inputframe, bg=color2, fg=color1, font=font, justify=CENTER)
            withdrawamount_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)
            withdrawamount_btn = Button(withdraw_inputframe, text='Withdraw', bg=color1, fg=color2, font=font, relief=FLAT, command=fn_withdrawamount)
            withdrawamount_btn.grid(row=2, column=1, padx=5, pady=5, sticky=W)
            withdrawamount_status_lbn = Label(withdraw_inputframe, bg=color1, fg=color2, font=font)
            withdrawamount_status_lbn.grid(row=3, column=0, columnspan=2)
            
        def fn_search_frame():
            # sub-function
            def fn_getdata():
                try:
                    id = int(search_entry.get())
                    conn = sqlite3.connect(database3)
                    c = conn.cursor()
                    c.execute('SELECT balance FROM customer WHERE accountno = ?', (id, ))
                    result = c.fetchall()
                    if result:
                        balance = result[-1][0]
                        search_status_lbn.config(text='')
                        fn_withdraw_inputframe(id, balance)
                    conn.commit()
                    conn.close()
                except :
                    search_status_lbn.config(text='Invaild Input')

            # create requied label, entry, button
            search_lbn = Label(search_frame, text='Search ac.no', bg=color1, fg=color2, font=font)
            search_lbn.grid(row=0, column=0, padx=5)
            search_entry = Entry(search_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            search_entry.grid(row=0, column=1, padx=5)
            search_btn = Button(search_frame, text='Search', bg=color1, fg=color2, font=font, relief=FLAT, command=fn_getdata)
            search_btn.grid(row=0, column=2, padx=5)
            search_status_lbn = Label(search_frame, bg=color1, fg=color2, font=font)
            search_status_lbn.grid(row=1, column=0, columnspan=3)
            
        # fn_withdraw_frame start here...
        # create requied frame's
        search_frame = Frame(withdraw_frame, bg=color1, relief=FLAT)
        search_frame.pack(fill=X)
        withdraw_inputframe = Frame(withdraw_frame, bg=color1, relief=FLAT, padx=200)
        withdraw_inputframe.pack(fill=BOTH, expand=1)

        # calling requied function
        fn_search_frame()

    # first thing's first
    employeepage_mainframe.destroy()

    # create requied frame's
    withdraw_mainframe = Frame(appbody, bg=color1, relief=FLAT)
    withdraw_mainframe.pack(fill=BOTH, expand=1)
    withdraw_backframe = Frame(withdraw_mainframe, bg=color1, relief=FLAT)
    withdraw_backframe.pack(fill=X)
    withdraw_frame = Frame(withdraw_mainframe, bg=color1, relief=FLAT)
    withdraw_frame.pack(fill=BOTH, expand=1)

    # back button for searchuser page
    back_btn = Button(withdraw_backframe, text='Back', bg=color1, fg=color2, font=font, relief=FLAT, command=fn_withdraw_backframe)
    back_btn.pack(side=LEFT)

    # calling requied function
    fn_withdraw_frame()

def employee_transfer(appbody, loginpage_frame, employeepage_mainframe, branch, ifsccode):
    # sub-function
    def fn_transfer_backframe():
        transfer_mainframe.destroy()
        employeepage(appbody, loginpage_frame, branch, ifsccode)
        
    def fn_transfer_frame():
         # sub-function
        def fn_transfer_inputframe(id, cbalance):
            # sub-function
            def fn_process_payment(id, amounttotransfer, toaccountno):
                # payment start here...
                def fn_update_fromaccount():
                    # step-1 customer database
                    def fn_update_customer():
                        conn = sqlite3.connect(database3)
                        c = conn.cursor()
                        c.execute("SELECT balance FROM customer WHERE accountno = ?", (id, ))
                        result = c.fetchall()
                        lastbalance = result[0][0]
                        newbalance = lastbalance - amounttotransfer
                        c.execute("UPDATE customer SET balance = ? WHERE accountno = ? ", (newbalance, id))
                        conn.commit()
                        conn.close()
                    # step-2 passbook database
                    def fn_update_passbook():
                        conn = sqlite3.connect(database5)
                        c = conn.cursor()
                        c.execute("SELECT balance FROM {}".format(f'acno{id}'))
                        result = c.fetchall()
                        lastbalance = result[-1][0]
                        newbalance = lastbalance - amounttotransfer
                        # record data for database(passbook)
                        date = time.strftime("%d/%b/%Y")
                        remark = f"Transfer to ac.no{toaccountno}"
                        ttype = "Dedit"
                        tamount = amounttotransfer
                        tbalance = newbalance
                        data = [date, remark, ttype, tamount, tbalance]
                        c.execute("INSERT INTO acno{} VALUES (?,?,?,?,?) ".format(id), data)
                        conn.commit()
                        conn.close()
                        pass
                    # calling function's (cut amount from sender...)
                    fn_update_customer()
                    fn_update_passbook()
                    
                def fn_update_toaccount():
                    # step-1 customer database
                    def fn_update_customer():
                        conn = sqlite3.connect(database3)
                        c = conn.cursor()
                        c.execute("SELECT balance FROM customer WHERE accountno = ?", (toaccountno, ))
                        result = c.fetchall()
                        lastbalance = result[0][0]
                        newbalance = lastbalance + amounttotransfer
                        c.execute("UPDATE customer SET balance = ? WHERE accountno = ? ", (newbalance, toaccountno))
                        conn.commit()
                        conn.close()
                    # step-2 passbook database
                    def fn_update_passbook():
                        conn = sqlite3.connect(database5)
                        c = conn.cursor()
                        c.execute("SELECT balance FROM {}".format(f'acno{toaccountno}'))
                        result = c.fetchall()
                        if result:
                            lastbalance = result[-1][0]
                            newbalance = lastbalance + amounttotransfer
                            # record data for database(passbook)
                            date = time.strftime("%d/%b/%Y")
                            remark = f"Received from ac.no{id}"
                            ttype = "Credit"
                            tamount = amounttotransfer
                            tbalance = newbalance
                            data = [date, remark, ttype, tamount, tbalance]
                            c.execute("INSERT INTO acno{} VALUES (?,?,?,?,?) ".format(toaccountno), data)
                        else:
                            date = time.strftime("%d/%b/%Y")
                            remark = f"Transfered from ac.no{id}"
                            ttype = "Credit"
                            tamount = amounttotransfer
                            tbalance = amounttotransfer
                            data = [date, remark, ttype, tamount, tbalance]
                            c.execute("INSERT INTO acno{} VALUES (?,?,?,?,?) ".format(toaccountno), data)
                        conn.commit()
                        conn.close()
                        
                    # calling function's (recive amount from sender...)
                    fn_update_customer()
                    fn_update_passbook()
                    
                # calling requied function's to do payment
                fn_update_fromaccount()
                fn_update_toaccount()

                transferamount_status_lbn.config(text='Payment Done')

            def fn_transferamount():
                # getting data from form...
                # try:
                toaccountno = int(toaccountno_entry.get())
                amounttotransfer = float(transferamount_entry.get())

                if amounttotransfer > cbalance :
                    transferamount_status_lbn.config(text='Insufficient funds')
                elif amounttotransfer <= 0 :
                    transferamount_status_lbn.config(text="You can not transfer zero amount")
                else:
                    # checking for toaccountno in database
                    conn = sqlite3.connect(database3)
                    c = conn.cursor()
                    c.execute('SELECT accountno FROM customer WHERE accountno = ?', (toaccountno, ))
                    result = c.fetchall()
                    if result:
                        transferamount_status_lbn.config(text='Processing payment')
                        fn_process_payment(id, amounttotransfer, toaccountno)
                    else:
                        transferamount_status_lbn.config(text='Acoount not found')
                    conn.commit()
                    conn.close()
                # except :
                #     transferamount_status_lbn.config(text='Invalid Input')
                
            
            note_lbn = Label(transfer_inputframe, text="* Amount should be a number", bg=color1, fg=color2, font=font)
            note_lbn.grid(row=0, column=0, columnspan=2)
            toaccountno_lbn = Label(transfer_inputframe, text="To Account.No", bg=color1, fg=color2, font=font)
            toaccountno_lbn.grid(row=1, column=0, padx=5, pady=5, sticky=E)
            toaccountno_entry = Entry(transfer_inputframe, bg=color2, fg=color1, font=font, justify=CENTER)
            toaccountno_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)
            
            transferamount_lbn = Label(transfer_inputframe, text='Amount', bg=color1, fg=color2, font=font)
            transferamount_lbn.grid(row=2, column=0, padx=5, pady=5, sticky=E)
            transferamount_entry = Entry(transfer_inputframe, bg=color2, fg=color1, font=font, justify=CENTER)
            transferamount_entry.grid(row=2, column=1, padx=5, pady=5, sticky=W)
            transferamount_btn = Button(transfer_inputframe, text='Transfer', bg=color1, fg=color2, font=font, relief=FLAT, command=fn_transferamount)
            transferamount_btn.grid(row=3, column=1, padx=5, pady=5, sticky=W)
            transferamount_status_lbn = Label(transfer_inputframe, bg=color1, fg=color2, font=font)
            transferamount_status_lbn.grid(row=4, column=0, columnspan=2)
            
        def fn_search_frame():
            # sub-function
            def fn_getdata():
                try:
                    id = int(search_entry.get())
                    conn = sqlite3.connect(database3)
                    c = conn.cursor()
                    c.execute('SELECT balance FROM customer WHERE accountno = ?', (id, ))
                    result = c.fetchall()
                    if result:
                        cbalance = result[0][0]
                        search_status_lbn.config(text='')
                        fn_transfer_inputframe(id, cbalance)
                    conn.commit()
                    conn.close()
                except :
                    search_status_lbn.config(text='Invaild Input')

            # create requied label, entry, button
            search_lbn = Label(search_frame, text='Search ac.no', bg=color1, fg=color2, font=font)
            search_lbn.grid(row=0, column=0, padx=5)
            search_entry = Entry(search_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            search_entry.grid(row=0, column=1, padx=5)
            search_btn = Button(search_frame, text='Search', bg=color1, fg=color2, font=font, relief=FLAT, command=fn_getdata)
            search_btn.grid(row=0, column=2, padx=5)
            search_status_lbn = Label(search_frame, bg=color1, fg=color2, font=font)
            search_status_lbn.grid(row=1, column=0, columnspan=3)
            
        # fn_saving_frame start here...
        # create requied frame's
        search_frame = Frame(transfer_frame, bg=color1, relief=FLAT)
        search_frame.pack(fill=X)
        transfer_inputframe = Frame(transfer_frame, bg=color1, relief=FLAT, padx=200)
        transfer_inputframe.pack(fill=BOTH, expand=1)

        # calling requied function
        fn_search_frame()

    # first thing's first
    employeepage_mainframe.destroy()

    # create requied frame's
    transfer_mainframe = Frame(appbody, bg=color1, relief=FLAT)
    transfer_mainframe.pack(fill=BOTH, expand=1)
    transfer_backframe = Frame(transfer_mainframe, bg=color1, relief=FLAT)
    transfer_backframe.pack(fill=X)
    transfer_frame = Frame(transfer_mainframe, bg=color1, relief=FLAT)
    transfer_frame.pack(fill=BOTH, expand=1)

    # back button for searchuser page
    back_btn = Button(transfer_backframe, text='Back', bg=color1, fg=color2, font=font, relief=FLAT, command=fn_transfer_backframe)
    back_btn.pack(side=LEFT)

    # calling requied function
    fn_transfer_frame()

def employee_passbook(appbody, loginpage_frame, employeepage_mainframe, branch, ifsccode):
    # sub-function
    def fn_passbook_backframe():
        passbook_mainframe.destroy()
        employeepage(appbody, loginpage_frame, branch, ifsccode)
    
        
    def fn_passbook_frame():
        # sub-function
        def fn_passbook_resultframe(result):
            # create passbook frame to hold passbook tree and scrollbar
            passbook = Frame(passbook_resultframe, bg=color1, relief=FLAT)
            passbook.pack(padx=5, pady=5)
            
            # scrollbar for passbook tree
            passbook_yscrollbar = Scrollbar(passbook, orient=VERTICAL)
            passbook_yscrollbar.pack(side=RIGHT, fill=Y)

            passbook_tree = ttk.Treeview(passbook, columns=(1,2,3,4,5), show='headings', height=15, yscrollcommand=passbook_yscrollbar.set)
            passbook_tree.pack()
            passbook_tree.heading(1, text="Date")
            passbook_tree.heading(2, text="Remark")
            passbook_tree.heading(3, text="Transfer type")
            passbook_tree.heading(4, text="Transfer amount")
            passbook_tree.heading(5, text="Balance")

            for i in result:
                passbook_tree.insert("", END, values=i)
            # configure scrollbar to passbook_tree
            passbook_yscrollbar.config(command=passbook_tree.yview)
            
            
        def fn_search_frame():
            # sub-function
            def fn_getdata():
                try:
                    id = int(search_entry.get())
                    conn = sqlite3.connect(database5)
                    c = conn.cursor()
                    c.execute('SELECT * FROM acno{}'.format(id))
                    result = c.fetchall()
                    if result:
                        search_status_lbn.config(text='')
                        fn_passbook_resultframe(result)
                    conn.commit()
                    conn.close()
                except :
                    search_status_lbn.config(text='Invaild Input')

            # create requied label, entry, button
            search_lbn = Label(search_frame, text='Search ac.no', bg=color1, fg=color2, font=font)
            search_lbn.grid(row=0, column=0, padx=5)
            search_entry = Entry(search_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
            search_entry.grid(row=0, column=1, padx=5)
            search_btn = Button(search_frame, text='Search', bg=color1, fg=color2, font=font, relief=FLAT, command=fn_getdata)
            search_btn.grid(row=0, column=2, padx=5)
            search_status_lbn = Label(search_frame, bg=color1, fg=color2, font=font)
            search_status_lbn.grid(row=1, column=0, columnspan=3)

        # fn_passbook_frame start here...
        # create requied frame's
        search_frame = Frame(passbook_frame, bg=color1, relief=FLAT)
        search_frame.pack(fill=X)
        passbook_resultframe = Frame(passbook_frame, bg=color1, relief=FLAT, padx=200)
        passbook_resultframe.pack(fill=BOTH, expand=1)

        # calling requied function
        fn_search_frame()

    # first thing's first
    employeepage_mainframe.destroy()

    # create requied frame's
    passbook_mainframe = Frame(appbody, bg=color1, relief=FLAT)
    passbook_mainframe.pack(fill=BOTH, expand=1)
    passbook_backframe = Frame(passbook_mainframe, bg=color1, relief=FLAT)
    passbook_backframe.pack(fill=X)
    passbook_frame = Frame(passbook_mainframe, bg=color1, relief=FLAT)
    passbook_frame.pack(fill=BOTH, expand=1)

    # back button for searchuser page
    back_btn = Button(passbook_backframe, text='Back', bg=color1, fg=color2, font=font, relief=FLAT, command=fn_passbook_backframe)
    back_btn.pack(side=LEFT)

    # calling requied function
    fn_passbook_frame()
"""
EMPLOYEE-PAGE SUB-FUNCTION'S END HERE
"""

# admin function's
def adminpage(appbody, loginpage_frame):
    # sub-function
    def fn_back():
        adminpage_mainframe.destroy()
        loginpage(appbody)
    
    def fn_adminsection():
        global img_adduser, img_updateuser, img_deleteuser, img_addbranch, img_addjobpost
        img_adduser = PhotoImage(file=path_adduser)
        img_updateuser = PhotoImage(file=path_updateuser)
        img_deleteuser = PhotoImage(file=path_deleteuser)
        img_addbranch = PhotoImage(file=path_city)
        img_addjobpost = PhotoImage(file=path_jobpost)

        adduser_btn = Button(adminpage_frame, image=img_adduser, text='Add\nUser', bg=color1, fg=color2, compound=TOP, font=font, relief=FLAT, command=lambda : admin_adduser(appbody, loginpage_frame, adminpage_mainframe))
        adduser_btn.grid(row=0, column=0)
        
        updateuser_btn = Button(adminpage_frame, image=img_updateuser, text='Update\nUser', bg=color1, fg=color2, compound=TOP, font=font, relief=FLAT, command=lambda : admin_updateuser(appbody, loginpage_frame, adminpage_mainframe))
        updateuser_btn.grid(row=0, column=1)
        
        deleteuser_btn = Button(adminpage_frame, image=img_deleteuser, text='Delete\nUser', bg=color1, fg=color2, compound=TOP, font=font, relief=FLAT, command=lambda : admin_deleteuser(appbody, loginpage_frame, adminpage_mainframe))
        deleteuser_btn.grid(row=0, column=2)
        
        addjobpost_btn = Button(adminpage_frame, image=img_addjobpost, text='Add\nJobpost', bg=color1, fg=color2, compound=TOP, font=font, relief=FLAT, command=lambda : admin_addjobpost(appbody, loginpage_frame, adminpage_mainframe))
        addjobpost_btn.grid(row=0, column=3)
        
        addbranch_btn = Button(adminpage_frame, image=img_addbranch, text='Add\nBranch', bg=color1, fg=color2, compound=TOP, font=font, relief=FLAT, command=lambda : admin_addbranch(appbody, loginpage_frame, adminpage_mainframe))
        addbranch_btn.grid(row=0, column=4)

    # first things first
    loginpage_frame.destroy()

    # create requied frames
    adminpage_mainframe = Frame(appbody, bg=color1, relief=FLAT)
    adminpage_mainframe.pack(fill=BOTH, expand=1)
    adminpage_backframe = Frame(adminpage_mainframe, bg=color1, relief=FLAT)
    adminpage_backframe.pack(fill=X)
    adminpage_frame = Frame(adminpage_mainframe, bg=color1, relief=FLAT, padx=100, pady=100)
    adminpage_frame.pack(fill=BOTH, expand=1)

    # back button of adminpage
    back_btn = Button(adminpage_backframe, text='Back', bg=color1, fg=color2, font=font, relief=FLAT, command=fn_back)
    back_btn.pack(side=LEFT)

    # calling requied function's
    fn_adminsection()
    
# employee function's
def employeepage(appbody, loginpage_frame, branch, ifsccode):
    # sub-function
    def fn_employeepage_back():
        employeepage_mainframe.destroy()
        loginpage(appbody)
    
    def fn_employeepage_frame():
        # employeepage start here...
        global img_adduser, img_updateuser, img_deleteuser, img_infouser, img_deposit, img_withdraw, img_transfer, img_passbook

        img_adduser = PhotoImage(file=path_adduser)
        img_updateuser = PhotoImage(file=path_updateuser)
        img_deleteuser = PhotoImage(file=path_deleteuser)
        img_infouser = PhotoImage(file=path_searchuser)
        img_deposit = PhotoImage(file=path_deposit)
        img_withdraw = PhotoImage(file=path_withdraw)
        img_transfer = PhotoImage(file=path_transfer)
        img_passbook = PhotoImage(file=path_book)

        adduser_btn = Button(employeepage_frame, text="Add\nUser", image=img_adduser, compound=TOP, bg=color1, fg=color2, font=font, relief=FLAT, command=lambda : employee_adduser(appbody, loginpage_frame, employeepage_mainframe, branch, ifsccode))
        adduser_btn.grid(row=0, column=0)

        updateuser_btn = Button(employeepage_frame, text="Update\nUser", image=img_updateuser, compound=TOP, bg=color1, fg=color2, font=font, relief=FLAT, command=lambda : employee_updateuser(appbody, loginpage_frame, employeepage_mainframe, branch, ifsccode))
        updateuser_btn.grid(row=0, column=1)

        deleteuser_btn = Button(employeepage_frame, text="Delete\nUser", image=img_deleteuser, compound=TOP, bg=color1, fg=color2, font=font, relief=FLAT, command=lambda : employee_deleteuser(appbody, loginpage_frame, employeepage_mainframe, branch, ifsccode))
        deleteuser_btn.grid(row=0, column=2)

        infouser_btn = Button(employeepage_frame, text="Info\nUser", image=img_infouser, compound=TOP, bg=color1, fg=color2, font=font, relief=FLAT, command=lambda : employee_infouser(appbody, loginpage_frame, employeepage_mainframe, branch, ifsccode))
        infouser_btn.grid(row=0, column=3)

        deposit_btn = Button(employeepage_frame, text="Deposit\n", image=img_deposit, compound=TOP, bg=color1, fg=color2, font=font, relief=FLAT, command=lambda : employee_deposit(appbody, loginpage_frame, employeepage_mainframe, branch, ifsccode))
        deposit_btn.grid(row=0, column=4)

        withdraw_btn = Button(employeepage_frame, text="Withdraw\n", image=img_withdraw, compound=TOP, bg=color1, fg=color2, font=font, relief=FLAT, command=lambda : employee_withdraw(appbody, loginpage_frame, employeepage_mainframe, branch, ifsccode))
        withdraw_btn.grid(row=0, column=5)

        transfer_btn = Button(employeepage_frame, text="Transfer\n", image=img_transfer, compound=TOP, bg=color1, fg=color2, font=font, relief=FLAT, command=lambda : employee_transfer(appbody, loginpage_frame, employeepage_mainframe, branch, ifsccode))
        transfer_btn.grid(row=0, column=6)

        transaction_history_btn = Button(employeepage_frame, text="Passbook\n", image=img_passbook, compound=TOP, bg=color1, fg=color2, font=font, relief=FLAT, command=lambda : employee_passbook(appbody, loginpage_frame, employeepage_mainframe, branch, ifsccode))
        transaction_history_btn.grid(row=0, column=7)

    # first thing's first
    loginpage_frame.destroy()

    # create requied frame's
    employeepage_mainframe = Frame(appbody, bg=color1, relief=FLAT)
    employeepage_mainframe.pack(fill=BOTH, expand=1)
    employeepage_backframe = Frame(employeepage_mainframe, bg=color1, relief=FLAT)
    employeepage_backframe.pack(fill=X)
    employeepage_frame = Frame(employeepage_mainframe, bg=color1, relief=FLAT, padx=100, pady=100)
    employeepage_frame.pack(fill=BOTH, expand=1)

    # back button for employee page
    back_btn = Button(employeepage_backframe, text='Back', bg=color1, fg=color2, font=font, relie=FLAT, command=fn_employeepage_back)
    back_btn.pack(side=LEFT)
    
    # calling requied function
    fn_employeepage_frame()

# login function
def loginpage(appbody):
    # sub-function's
    def fn_clockframe():
        # help function of clock frame
        def fn_update_clock():
            mon = time.strftime('%B %d')
            ctim = time.strftime('%I : %M : %S %p')
            wek = time.strftime('%A')

            month.config(text=mon)
            timenow.config(text=ctim)
            week.config(text=wek)

            timenow.after(500, fn_update_clock)
        # clock frame start here...
        month = Label(clock_frame, bg=color1, fg=color2, width=15, font=('baloo', 25))
        month.pack()
        timenow = Label(clock_frame, bg=color1, fg=color2, width=15, font=('baloo', 25))
        timenow.pack()
        week = Label(clock_frame, bg=color1, fg=color2, width=15, font=('baloo', 25))
        week.pack()

        # calling update_clock function to update clock
        fn_update_clock()

    def fn_loginform_frame():
        # sub-function of loginform frame
        def fn_validate():
            logintype = loginas.get()
            username = username_entry.get()
            password = password_entry.get()

            data = (username, password)
            
            if logintype == 'admin':
                conn = sqlite3.connect(database1)
                c = conn.cursor()
                c.execute('SELECT username FROM admin WHERE username = ? AND password = ? ', data)
                result = c.fetchall()
                if result:
                    # calling admin page
                    adminpage(appbody, loginpage_frame)
                else:
                    login_status_lbn.config(text='Invalid Input')
                conn.commit()
                conn.close()
            else:
                conn = sqlite3.connect(database2)
                c = conn.cursor()
                c.execute('SELECT branch, ifsccode FROM employee WHERE username = ? AND password = ? ', data)
                result = c.fetchall()
                if result:
                    branch = result[0][0]
                    ifsccode = result[0][1]
                    # calling employee page
                    employeepage(appbody, loginpage_frame, branch, ifsccode)
                else:
                    login_status_lbn.config(text='Invalid Input')
                conn.commit()
                conn.close()

        # loginform function start here...
        global loginas
        loginas = StringVar()
        loginas.set('employee')

        Radiobutton(loginform_frame, text='Admin', value='admin', variable=loginas, font=font, bg=color1).grid(row=0 , column=0, pady=5)
        Radiobutton(loginform_frame, text='Employee', value='employee', variable=loginas, font=font, bg=color1).grid(row=0 , column=1, pady=5)

        username_lbn = Label(loginform_frame, text='Username', bg=color1, fg=color2, font=font)
        username_lbn.grid(row=1, column=0, pady=5)
        username_entry = Entry(loginform_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT)
        username_entry.grid(row=1, column=1, pady=5)

        password_lbn = Label(loginform_frame, text='Password', bg=color1, fg=color2, font=font)
        password_lbn.grid(row=2, column=0, pady=5)
        password_entry = Entry(loginform_frame, bg=color2, fg=color1, font=font, justify=CENTER, relief=FLAT, show='*')
        password_entry.grid(row=2, column=1, pady=5)

        login_status_lbn = Label(loginform_frame, bg=color1, fg=tcolor, font=font)
        login_status_lbn.grid(row=3, column=0, columnspan=2)

        login_btn = Button(loginform_frame, text='Login', bg=color1, fg=color2, font=font, relief=FLAT, command=fn_validate)
        login_btn.grid(row=4, column=1, pady=5)

    # create requied frames
    loginpage_frame = Frame(appbody, bg=color1, relief=FLAT, padx=100, pady=100)
    loginpage_frame.pack(fill=BOTH, expand=1)
    clock_frame = Frame(loginpage_frame, bg=color1, relief=FLAT)
    clock_frame.pack(side=LEFT, fill=BOTH, expand=1)
    loginform_frame = Frame(loginpage_frame, bg=color1, relief=FLAT)
    loginform_frame.pack(side=RIGHT, fill=BOTH, expand=1)
    # calling requied function's
    fn_clockframe()
    fn_loginform_frame()

# main function
def main():
    app = Tk()
    # sub-function's
    def fn_apphead():
        headicon = Label(apphead, image=img_icon, bg=color1)
        headicon.pack(side=LEFT, padx=10)
        headtext = Label(apphead, text=appname, bg=color1, fg=color2, font=('baloo', 45))
        headtext.pack(side=LEFT)
    def fn_appbody():
        # calling loginpage
        loginpage(appbody)
    # app image variable
    img_icon = PhotoImage(file=path_icon)
    # app start here...
    apphead = Frame(app, bg=color1, relief=FLAT, height=100)
    apphead.pack(fill=X)
    appbody = Frame(app, bg=color1, relief=FLAT)
    appbody.pack(fill=BOTH, expand=1)
    # calling requied sub-function's
    fn_apphead()
    fn_appbody()
    # app config
    app.title(appname)
    app.geometry('500x500')
    app.iconphoto(True, PhotoImage(file=path_icon))
    # app mainloop
    app.mainloop()

# calling main function (running app)
main()