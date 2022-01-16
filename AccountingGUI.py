import csv
from tkinter import * #use all function from tk
from tkinter import ttk, messagebox #สวยกว่า #popup
from datetime import datetime
from tkinter.ttk import Notebook, Style  #สำหรับทำ Tab

GUI = Tk() # Create gui
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย by Potae')
GUI.geometry('700x700+700+300') #ขนาดและความห่างจากซ้ายและบน

#-----------------MENU--------------------#
menubar = Menu(GUI)
GUI.config(menu=menubar)

# File menu
filemenu = Menu(menubar, tearoff=0) #เอาไปใส่ใน Menubar #tear off คือเปิด ----
menubar.add_cascade(label='file', menu=filemenu)
filemenu.add_command(label='Import CSV')
filemenu.add_command(label='Export CSV')

# Help menu
def About():
    messagebox.showinfo('About', 'สวัสดีครับ โปรแกรมบันทึกบัญชี')
helpmenu = Menu(menubar, tearoff=0) #เอาไปใส่ใน Menubar
menubar.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='About', command=About)

# Help menu
donatemenu = Menu(menubar, tearoff=0) #เอาไปใส่ใน Menubar
menubar.add_cascade(label='Donate', menu=donatemenu)

#-----------------FONT--------------------#
FONT1 = ('4711_AtNoon_Regular', 20) #font และ size
#B1 = Button(GUI, text='Calculate')
#B1.pack(ipadx=50, ipady=20) #แปะปุ่มลงบน GUI หลัก

s = ttk.Style()
s.configure('TNotebook.Tab', font=('4711_AtNoon_Regular','12') ) #font tab

Tab = ttk.Notebook(GUI) #สร้าง Tab
T1 = Frame(Tab) #สร้าง Frame ใน Tab
T2 = Frame(Tab) #width = ... ปรับขนาดได้
Tab.pack(fill=BOTH, expand=1) #fill คือขยายทั้งแกน x y

icon_t1 = PhotoImage(file='t1_expense.png') #โหลด icon เข้ามา #ใช้ .subsample(จำนวนเท่าที่จะย่อ) ย่อรูปได้
icon_t2 = PhotoImage(file='t2_list.png')

Tab.add(T1, text=f'{"ค่าใช้จ่าย":^{30}}', image=icon_t1, compound='top')  #จัดให้อยู่ตรงกลาง เว้นข้างละ 30 และรูปอยู่ด้าน...
Tab.add(T2, text=f'{"ค่าใช้จ่ายทั้งหมด":^{30}}', image=icon_t2, compound='top')


#-----------------สร้าง List ไว้แปลงวันภาษาอังกฤษเป็นไทย--------------------#
days = {'Mon':'จันทร์',
        'Tue':'อังคาร',
        'Wed':'พุธ',
        'Thu':'พฤหัสบดี',
        'Fri':'ศุกร์',
        'Sat':'เสาร์',
        'Sun':'อาทิตย์'}

#-----------------FUNCTION--------------------#
def Save(event=None): #รับค่าและบันทึกเป็น csv
    expense = v_expense.get() #.get คือดึงค่ามาจาก v_expense
    price = v_price.get() #.get คือดึงค่ามาจาก v_price
    qty = v_qty.get()

    if expense == '':
        print('No Data')
        messagebox.showwarning('ผิดพลาด', 'กรุณากรอกข้อมูล')
        return
    elif price == '':
        messagebox.showwarning('ผิดพลาด', 'กรุณากรอกราคา')
        return
    elif qty == '':
        qty = 1

    total = int(price) * int(qty)
    try:
        total = int(price) * int(qty)
        print('รายการ: {} ราคา: {}' .format(expense, price))
        print('จำนวน: {} รวมทั้งสิ้น: {}'.format(qty, total))
        text = 'รายการ: {} ราคา: {}\n' .format(expense, price)
        text = text + 'จำนวน: {} รวมทั้งสิ้น: {}'.format(qty, total)
        v_result.set(text)  #ลิ้งกับที่โชว์ผลลัพธ์ข้างล่าง
        v_expense.set('')
        v_price.set('') #หลังกรอกเสร็จ ให้ set ข้อความเป็น 'ค่าว่าง'
        v_qty.set('')

        today = datetime.now().strftime('%a')  #days['Mon'] = 'จันทร์'
        print(today)
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dt = days[today] + '-' + dt
        with open('savedata.csv', 'a', encoding='utf-8', newline='') as f: # Save in CSV File, With คือสั่งเปิดไฟล์แล้วปิด, a คือ บันทึกไฟล์ต่อท้ายเรื่อยๆ
            fw = csv.writer(f) #สร้าง function สำหรับเขียนข้อมูล
            data = [dt, expense, price, qty, total]
            fw.writerow(data)
        E1.focus()  #ทำให้กรอกเสร็จกลับไปช่องแรก (ช่อง E1)
        resulttable.delete(*resulttable.get_children())
        update_table()
        update_record()
    except:
        print("ERROR")  #ถ้ากรอกมั่วให้ป้องกัน
        messagebox.showinfo('ผิดพลาด', 'กรุณากรอกตัวเลขหรือตัวอักษรให้ถูกต้อง')

GUI.bind('<Return>', Save) #ให้กด enter ได้ แต่ต้องไปเพิ่มใน Def ด้วย

#-----------------MAIN GUI--------------------#

F1 = Frame(T1) #F1 แปะลงบน GUI
#F1.place(x=150, y=70) #สร้างเฟรมก่อนแล้วเอา B2 มาแปะทับไป
F1.pack() #อยู่ตรงกลาง

#-----------------รายการค่าใช้จ่าย+กล่องกรอกข้อมูล--------------------#
L = ttk.Label(F1, text='รายการค่าใช้จ่าย', font = FONT1).pack() #pack ในบรรทัดเดียวกันได้เลย
v_expense = StringVar() #ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E1 = ttk.Entry(F1, textvariable = v_expense, font = FONT1)
E1.pack()

#-----------------ราคา+กล่องกรอกข้อมูล--------------------#
L = ttk.Label(F1, text='ราคา', font = FONT1).pack() #pack ในบรรทัดเดียวกันได้เลย
v_price = StringVar() #ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E2 = ttk.Entry(F1, textvariable = v_price, font = FONT1)
E2.pack()

#-----------------จำนวน--------------------#
L = ttk.Label(F1, text='จำนวน', font = FONT1).pack() #pack ในบรรทัดเดียวกันได้เลย
v_qty = StringVar() #ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E3 = ttk.Entry(F1, textvariable = v_qty, font = FONT1)
E3.pack()

#-----------------ปุ่มเซฟ--------------------#
icon_t3 = PhotoImage(file='t3_save.png')
B2 = ttk.Button(F1, text='Save', command=Save, image=icon_t3, compound='top') #แปะไปกับ Frame 1 และแปะฟังก์ชัน
B2.pack(ipadx=50, ipady=20, pady=20) #แปะแบบกำหนดตำแหน่งลงบน GUI

#-----------------โชว์ผลลัพธ์--------------------#
v_result = StringVar()
v_result.set('------ผลลัพธ์------')
result = ttk.Label(F1, textvariable=v_result, font=FONT1)  #foreground='pink' ปรับสี
result.pack(pady=20)

GUI.bind('<Tab>',lambda x: E2.focus())



#-------------TAB2----------------#
def read_csv():
	with open('savedata.csv', newline='', encoding='utf-8') as f:
		fr = csv.reader(f)
		data = list(fr)
	return data

def update_record():
	getdata = read_csv()
	v_allrecord.set('')
	text = ''
	for d in getdata:
		txt = '{}---{}---{}---{}---{}\n'.format(d[0],d[1],d[2],d[3],d[4])
		text = text + txt

	v_allrecord.set(text)

v_allrecord = StringVar()
v_allrecord.set('-------All Record-------')
#Allrecord = ttk.Label(T2,textvariable=v_allrecord,font=('4711_AtNoon_Regular','20'),foreground='green')
#Allrecord.pack()

style = ttk.Style()
style.configure("Treeview.Heading", font = ('4711_AtNoon_Regular', 15))
L = ttk.Label(T2, text='ตารางแสดงผลลัพธ์', font = ('4711_AtNoon_Regular', 25)).pack(pady=20)
header = ['วัน-เวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม']
resulttable = ttk.Treeview(T2,columns=header, show='headings',height=10) #ตารางโชว์ค่า
resulttable.pack()

for h in header:
	resulttable.heading(h,text=h)

headerwidth = [150,170,80,80,80] #ความกว้างแต่ละคอลัมน์
for h,W in zip(header,headerwidth):
	resulttable.column(h,width=W)

def update_table():
	getdata = read_csv()
	for dt in getdata:
		resulttable.insert('','end',value=dt)


update_table()

update_record()

GUI.mainloop()