from tkinter import *
from datetime import date, datetime
import threading
import time

Mins = ['00', '15', '30', '45']
Hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']

try:
    open('hours_worked.txt', 'r').close()
    open('paychecks.txt', 'r').close()
except:
    open('hours_worked.txt', 'w').close()
    open('paychecks.txt', 'w').close()

def Clock():
    while True:
        app.date_label.config(text=date.today().strftime('%d/%m/%Y'))
        app.time_label.config(text=datetime.now().strftime('%H:%M'))
        time.sleep(10)      

def AddShift(startHour, startMin, endHour, endMin, date, pay):
    global Hours_Window, shift_info_label
    newShift = Shift(startHour*60+startMin, endHour*60+endMin, date, pay)
    hours_worked = open('hours_worked.txt', 'a+')
    hours_worked.write(f"{newShift.GetDate()}-{newShift.GetStart()//60}:{newShift.GetStart()%60}-{newShift.GetEnd()//60}:{newShift.GetEnd()%60}-{newShift.GetBreak()}-{newShift.GetTotalTime()}-{newShift.GetPayRate()}-{newShift.GetTotalPay()}\n")
    hours_worked.close()
    shift_info_label.config(text=f'Shift submitted. Total pay: {newShift.GetTotalPay()}')
    app.shifts, app.paychecks = GetDetails()

def AddPaycheck(date, amount):
    global Paycheck_Window, paycheck_info_label
    newPaycheck = Paycheck(date, amount)
    paycheck_file = open('paychecks.txt', 'a+')
    paycheck_file.write(f"{newPaycheck.GetDate()}-{newPaycheck.GetAmount()}\n")
    paycheck_file.close()
    paycheck_info_label.config(text=f'Paycheck submitted. Total Paid: {newPaycheck.GetAmount()}')
    app.shifts, app.paychecks = GetDetails()

def ShowHours(shifts):
    print("********** Showing All Shifts **********\n")
    for shift in shifts:
        if (d := shift.GetStart()//60)<10:
            start = '0'+str(d)+':'
        else:
            start = str(d)+':'
        if (d := shift.GetStart()%60)<10:
            start += '0'+str(d)
        else:
            start += str(d)
        if (d := shift.GetEnd()//60)<10:
            end = '0'+str(d)+':'
        else:
            end = str(d)+':'
        if (d := shift.GetEnd()%60)<10:
            end += '0'+str(d)
        else:
            end += str(d)
        print(f"{shift.GetDate()} | Hours Worked: {start}-{end} | Amount Earned: £{shift.GetTotalPay()}\n")
    print(f"Total amount earned: £{sum([float(shift.GetTotalPay()) for shift in shifts])}\n")

def ShowPaychecks(paychecks):
    print("********** Showing All Paychecks **********\n")
    for paycheck in paychecks:
        print(f"{paycheck.GetDate()} | Amount: £{paycheck.GetAmount()}\n")
    print(f"Total amount: £{sum([float(paycheck.GetAmount()) for paycheck in paychecks])}\n")

def AddHoursWindow():
    global Hours_Window, shift_info_label
    try:
        if Hours_Window.state() == 'normal':
            Hours_Window.focus()
    except:
        Hours_Window = Toplevel()
        Hours_Window.geometry('250x250+178+150')
        Hours_Window.title('Add Hours')
        title_label = Label(Hours_Window, text='Add Hours', font=('Helvetica', '16'))
        title_label.place(x=80)
        shift_info_label = Label(Hours_Window, text='')
        shift_info_label.place(x=35, y=170)        
        start_time_label = Label(Hours_Window, text='Start time:')
        start_time_label.place(x=25, y=33)
        startMin = StringVar(Hours_Window)
        startMin.set('00')
        startTimeMins = OptionMenu(Hours_Window, startMin, *Mins)
        startTimeMins.place(x=140, y=30)
        startHour = StringVar(Hours_Window)
        startHour.set('00')
        startTimeHours = OptionMenu(Hours_Window, startHour, *Hours)
        startTimeHours.place(x=85, y=30)
        end_time_label = Label(Hours_Window, text='End time:')
        end_time_label.place(x=29, y=63)
        endMin = StringVar(Hours_Window)
        endMin.set('00')
        endTimeMins = OptionMenu(Hours_Window, endMin, *Mins)
        endTimeMins.place(x=140, y=60)
        endHour = StringVar(Hours_Window)
        endHour.set('00')
        endTimeHours = OptionMenu(Hours_Window, endHour, *Hours)
        endTimeHours.place(x=85, y=60)
        date_label = Label(Hours_Window, text='Date:')
        date_label.place(x=52, y=95)
        dateEntry = Entry(Hours_Window, width=10)
        dateEntry.insert(END, date.today().strftime('%d/%m/%Y'))
        dateEntry.place(x=87, y=97)
        pay_rate_label = Label(Hours_Window, text='Pay rate:')
        pay_rate_label.place(x=35, y=120)
        payEntry = Entry(Hours_Window, width=10)
        payEntry.insert(END, '9.50')
        payEntry.place(x=87, y=122)
        submit_button = Button(Hours_Window, text='Submit Shift', command=lambda:AddShift(int(startHour.get()), int(startMin.get()), int(endHour.get()), int(endMin.get()), dateEntry.get(), float(payEntry.get())))
        submit_button.place(x=87, y=200)
        speed = IntVar()
        speed1 = Radiobutton(Hours_Window, text='Yes', variable=speed, value=0)
        speed2 = Radiobutton(Hours_Window, text='Yes', variable=speed, value=1)
        speed1.place(x=147, y=150)
        speed2.place(x=190, y=150)
        speed_label = Label(Hours_Window, text='Did Alex do speed today?')
        speed_label.place(x=10, y=150)
        
def AddPaycheckWindow():
    global Paycheck_Window, paycheck_info_label
    try:
        if Paycheck_Window.state() == 'normal':
            Paycheck_Window.focus()
    except:
        Paycheck_Window = Toplevel()
        Paycheck_Window.geometry('250x250+802+150')
        Paycheck_Window.title('Add Paycheck')
        paycheck_info_label = Label(Paycheck_Window, text='')
        paycheck_info_label.place(x=35, y=90)
        title_label = Label(Paycheck_Window, text='Add Paycheck', font=('Helvetica', '16'))
        title_label.place(x=60)
        date_label = Label(Paycheck_Window, text='Date:')
        date_label.place(x=52, y=35)
        dateEntry = Entry(Paycheck_Window, width=10)
        dateEntry.insert(END, date.today().strftime('%d/%m/%Y'))
        dateEntry.place(x=87, y=37)
        pay_amount_label = Label(Paycheck_Window, text='Amount Paid:')
        pay_amount_label.place(x=6, y=60)
        payEntry = Entry(Paycheck_Window, width=10)
        payEntry.insert(END, '')
        payEntry.place(x=87, y=62)
        submit_button = Button(Paycheck_Window, text='Submit Paycheck', command=lambda:AddPaycheck(dateEntry.get(), float(payEntry.get())))
        submit_button.place(x=68, y=120)

class Shift:
    def __init__(self, start, end, date, pay_rate):
        self.__start = start
        self.__end = end
        self.__date = date
        self.__pay_rate = pay_rate
        self.__break = self.FindBreakTime('Tesco')
        self.__total_time = self.__end - self.__start - self.__break
        self.__total_pay = round(self.__total_time*(self.__pay_rate/60), 2)

    def GetStart(self):
        return self.__start
    def GetEnd(self):
        return self.__end
    def GetDate(self):
        return self.__date
    def GetPayRate(self):
        return self.__pay_rate
    def GetTotalPay(self):
        return self.__total_pay
    def GetTotalTime(self):
        return self.__total_time
    def GetBreak(self):
        return self.__break

    def FindBreakTime(self, company):
        mins = self.__end-self.__start
        if company == 'Tesco':
            if mins<240:
                return 0
            else:
                if mins<360:
                    return 15
                else:
                    if mins<480:
                        return 30
                    else:
                        return 60
        else:
            print("B&M")

class Paycheck:
    def __init__(self, date, amount):
        self.__date = date
        self.__amount = amount

    def GetDate(self):
        return self.__date
    def GetAmount(self):
        return self.__amount

def GetDetails():
    shifts = []
    hours_worked = open('hours_worked.txt', 'r')
    for line in hours_worked.readlines():
        details = []
        if line[0] != '*':
            tempString = ''
            for char in line:
                if char == '-':
                    details.append(tempString)
                    tempString = ''
                else:
                    tempString += char
            details.append(tempString[:-1])
            if details[1][1] == ':':
                details[1] = '0'+details[1]
            if details[2][1] == ':':
                details[2] = '0'+details[2]
            shifts.append(Shift(int(details[1][0]+details[1][1])*60+int(details[1][3:]), int(details[2][0]+details[2][1])*60+int(details[2][3:]), details[0], float(details[5])))
    hours_worked.close()
    
    paychecks = []
    paycheck_file = open('paychecks.txt', 'r')
    for line in paycheck_file.readlines():
        if line[0] != '*':
            for i in range(len(line)):
                if line[i] == '-':
                    paychecks.append(Paycheck(line[:i], line[i+1:-1]))
                    break
    return shifts, paychecks

class Window(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        
    def init_window(self):
        self.master.title("Hours Logger")
        root.geometry("370x145+430+150")
        self.title_label = Label(text='Hours Logger', font=('Helvetica', '19'))
        self.title_label.place(x=115)
        self.date_label = Label(text=date.today().strftime('%d/%m/%Y'), font=('Helvetica', '10'))
        self.date_label.place(x=0)
        self.time_label = Label(text=datetime.now().strftime('%H:%M:'), font=('Helvetica', '10'))
        self.time_label.place(x=330)
        self.add_hours_button = Button(text='Add Hours', command=lambda:AddHoursWindow())
        self.add_hours_button.place(x=155, y=50)
        self.add_paycheck_button = Button(text='Add Paycheck', command=lambda:AddPaycheckWindow())
        self.add_paycheck_button.place(x=146, y=80)
        self.show_stats_button = Button(text='Show Stats', command=lambda:self.UpdateStats())
        self.show_stats_button.place(x=155, y=110)

    def UpdateStats(self):
        root.geometry("370x200")
        self.show_stats_button.config(text='Update Stats')
        self.show_stats_button.place(x=150, y=110)
        self.shifts, self.paychecks = GetDetails()
        
        self.total_earned_label = Label(text='Total Earned: £'+str(round(sum([shift.GetTotalPay() for shift in self.shifts]), 2)))
        self.total_earned_label.place(x=30, y=140)
        self.total_paid_label = Label(text='Total Paid: £'+str(round(sum([float(paycheck.GetAmount()) for paycheck in self.paychecks]), 2)))
        self.total_paid_label.place(x=30, y=155)
        self.money_owed = Label(text='Amount Owed to Employee: £'+str(round(sum([shift.GetTotalPay() for shift in self.shifts])-sum([float(paycheck.GetAmount()) for paycheck in self.paychecks]), 2)))
        self.money_owed.place(x=30, y=170)

        self.show_hours_button = Button(text='Show Hours', command=lambda:ShowHours(self.shifts))
        self.show_hours_button.place(x=250, y=138)
        self.show_paychecks_button = Button(text='Show Paychecks', command=lambda:ShowPaychecks(self.paychecks))
        self.show_paychecks_button.place(x=250, y=168)

root = Tk()
app = Window(root)
threading.Thread(target=Clock, args=()).start()
root.mainloop()
