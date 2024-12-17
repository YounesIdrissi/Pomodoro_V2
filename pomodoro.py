import tkinter as tk
import threading
from functools import partial
import time

#the MAIN THREAD is the default/initial thread of execution in any given program
#OBJECTS & CLASSES - this is the avoidance of global declaration, with no need for mutable containers (lists, dicts, etc.)

class Pomodoro:
    def __init__(self, work, rest, state, wr_state, total):#work/rest state, work=true, rest=false
        self.work = work
        self.rest = rest
        self.state = state
        self.wr_state = wr_state#brute forced this, created a new object which determines work/rest state
        self.total = total#total elasped time, includes work and rest times; total session time
        self.remain = work #time remaining for work/rest cycle
        self.saved = {}#dictionary pairs: ("text_entry": "elapsed_time"), we can use enumerate to extract index

    def clock(self):
        seconds = self.remain % 60
        minutes = int(self.remain / 60) % 60
        hours = int((self.remain / 60) / 60)
        text = tk.Label(timer, text=f"{hours:02}:{minutes:02}:{seconds:02}", font=("Ariel", 60))
        text.grid(row=0, column=0)
        pomodoro.display_wr_state()
        while True:#infinite loop is required here, prevents thread from ending once inner loop is False
            while self.state and self.remain >= 1:#self.remain >= 1 and not 0, because it decrements an extra 1
                self.total += 1#increment total session time
                self.remain -= 1
                seconds = self.remain % 60
                minutes = int(self.remain / 60) % 60
                hours = int((self.remain / 60) / 60)
                text = tk.Label(timer, text=f"{hours:02}:{minutes:02}:{seconds:02}", font=("Ariel", 60))
                text.grid(row=0, column=0)
                pomodoro.auto_switch()
                time.sleep(1)#place time.sleep() at the end to immidiately display initial time before 1 second wait
                #time.sleep slows down & gets in the way of immediate and precise actions, how can we fix this?

    def start_stop(self):
        if self.state:
            self.state = False
        else:
            self.state = True

    def reset(self):#should simply reset clock to original set starting time
        if self.wr_state:
            self.remain = self.work
        else:
            self.remain = self.rest
        #The below block of code is necessary to display restarted timer when clock is paused
        seconds = self.remain % 60
        minutes = int(self.remain / 60) % 60
        hours = int((self.remain / 60) / 60)
        text = tk.Label(timer, text=f"{hours:02}:{minutes:02}:{seconds:02}", font=("Ariel", 60))
        text.grid(row=0, column=0)

    def display_wr_state(self):#we could use this method more often to reduce redundancy
        #using a while loop here would create infinite loop
        for widget in wr_display.winfo_children():
            widget.destroy()
        if self.wr_state:
            #display 'WORK' text on the top
            text = tk.Label(wr_display, text="WORK", font=("Ariel", 20))
            text.grid(row=0, column=0)
        else:
            #display 'REST' text on the top
            text = tk.Label(wr_display, text="REST", font=("Ariel", 20))
            text.grid(row=0, column=0)
        #immediately display time so GUI looks better
        seconds = self.remain % 60
        minutes = int(self.remain / 60) % 60
        hours = int((self.remain / 60) / 60)
        text = tk.Label(timer, text=f"{hours:02}:{minutes:02}:{seconds:02}", font=("Ariel", 60))
        text.grid(row=0, column=0)

    def auto_switch(self):#switches from work timer to rest timer
        if self.remain >= 1:#barrier
            return
        #alarm/notification
        for widget in wr_display.winfo_children():
            widget.destroy()
        if self.wr_state:
            self.remain = self.rest#setting remaining time equal to rest time
            #display 'REST' text on the top
            text = tk.Label(wr_display, text="REST", font=("Ariel", 20))
            text.grid(row=0, column=0)
            self.wr_state = False
        else:
            self.remain = self.work#setting remaining time equal to work time
            #display 'WORK' text on the top
            text = tk.Label(wr_display, text="WORK", font=("Ariel", 20))
            text.grid(row=0, column=0)
            self.wr_state = True
        #immediately display time so GUI looks better
        seconds = self.remain % 60
        minutes = int(self.remain / 60) % 60
        hours = int((self.remain / 60) / 60)
        text = tk.Label(timer, text=f"{hours:02}:{minutes:02}:{seconds:02}", font=("Ariel", 60))
        text.grid(row=0, column=0)

    def instant_switch(self):#spaghetti code...
        #maybe alarm or notification, depends on user testing
        for widget in wr_display.winfo_children():
            widget.destroy()
        if self.wr_state:
            self.remain = self.rest#setting remaining time equal to rest time
            #display 'REST' text on the top
            text = tk.Label(wr_display, text="REST", font=("Ariel", 20))
            text.grid(row=0, column=0)
            self.wr_state = False
        else:
            self.remain = self.work#setting remaining time equal to work time
            #display 'WORK' text on the top
            text = tk.Label(wr_display, text="WORK", font=("Ariel", 20))
            text.grid(row=0, column=0)
            self.wr_state = True
        #immediately display time so GUI looks better
        seconds = self.remain % 60
        minutes = int(self.remain / 60) % 60
        hours = int((self.remain / 60) / 60)
        text = tk.Label(timer, text=f"{hours:02}:{minutes:02}:{seconds:02}", font=("Ariel", 60))
        text.grid(row=0, column=0)


    def save(self):#initial save button; pauses timer and opens save prompt
        if self.state:
            self.state = False
        pomodoro.save_prompt()

    def save_prompt(self):
        top = tk.Toplevel(root)
        top.geometry("430x50")
        top.title("Save Prompt")

        save_menu = tk.Frame(top)
        save_menu.columnconfigure(0, weight=1)
        save_menu.columnconfigure(1, weight=1)
        save_menu.columnconfigure(2, weight=1)

        text = tk.Label(save_menu, text="Session Name:", font=("Ariel", 15))
        text.grid(row=0, column=0)
        entry = tk.Entry(save_menu, text="", font=("Ariel", 15))
        entry.grid(row=0, column=1)
        save = tk.Button(save_menu, text="Save", font=("Ariel", 10))
        save.config(command=partial(pomodoro.appender, entry, top))
        save.grid(row=0, column=2)

        save_menu.pack()
        

    def appender(self, entry, top):
        seconds = self.total % 60
        minutes = int(self.total / 60) % 60
        hours = int((self.total / 60) / 60)
        self.saved[entry.get()] = f"{hours:02}:{minutes:02}:{seconds:02}"#can't have identical entry names
        top.destroy()#pass the top window as an argument, and destroy it
        self.total = 0#resets total elapsed time when a new save entry is made
        pomodoro.save_iter()

    def save_iter(self):
        if not self.saved:#ensures iteration of a blank space when there are no more dict elements
            space = tk.Label(session)
            space.grid(row=0)
        for index, (key, value) in enumerate(self.saved.items()):
            sesh = tk.Label(session, text=f"{key} -- Elapsed time: {value}", font=("Ariel", 15))
            sesh.grid(row=index, column=0)
            dlt = tk.Button(session, text="Delete", font=("Ariel", 10))
            dlt.config(command=partial(pomodoro.delete, key))
            dlt.grid(row=index, column=1)
    
    def delete(self, key):
        self.saved.pop(key)#poping a key pops the entire dict element; index, (key, value) pair is removed
        for widget in session.winfo_children():
            widget.destroy()
        pomodoro.save_iter()

    def settings_gate(self):#pop up window for all other options
        top = tk.Toplevel(root)
        top.geometry("400x300")
        top.title("Settings")

        menu = tk.Frame(top)
        menu.columnconfigure(0, weight=1)#grid menu of settings options

        #first button; change time button
        change_time = tk.Button(menu, text="Change Time", font=("Ariel", 20))
        change_time.config(command=pomodoro.change_times)
        change_time.grid(row=0, column=0)

        menu.pack()

    def change_times(self):#under settings, user enters custom work/rest time
        top = tk.Toplevel(root)#create a child window; pop up window
        top.geometry("500x100")
        top.title("Work and Rest Times")
        custom_times = tk.Frame(top)
        custom_times.columnconfigure(0, weight=1)#text column
        custom_times.columnconfigure(1, weight=1)#entry column
        custom_times.columnconfigure(2, weight=1)#submit button column

        wtext = tk.Label(custom_times, text="Enter custom work time: ", font=("Ariel", 15))
        wtext.grid(row=0, column=0)
        wentry = tk.Entry(custom_times, text="", font=("Ariel", 15))
        wentry.grid(row=0, column=1)
        wbtn = tk.Button(custom_times, text="Submit", font=("Ariel", 10))
        wbtn.config(command=partial(pomodoro.change_work, wentry))
        wbtn.grid(row=0, column=2)

        rtext = tk.Label(custom_times, text="Enter custom rest time: ", font=("Ariel", 15))
        rtext.grid(row=1, column=0)
        rentry = tk.Entry(custom_times, text="", font=("Ariel", 15))
        rentry.grid(row=1, column=1)
        rbtn = tk.Button(custom_times, text="Submit", font=("Ariel", 10))
        rbtn.config(command=partial(pomodoro.change_rest, rentry))
        rbtn.grid(row=1, column=2)

        custom_times.pack()

    def change_work(self, w):#updates work time
        #we include error handling for wrong user input
        try:
            self.work = int(w.get())
        except ValueError:
            pomodoro.value_error()

    def change_rest(self, r):#updates rest time
        #we include error handling for wrong user input
        try:
            self.rest = int(r.get())
        except ValueError:
            pomodoro.value_error()

    def value_error(self):#create a pop up error message
        top = tk.Toplevel(root)
        top.geometry("350x70")
        top.title("Value Error")

        error = tk.Label(top, text="Invalid input, please enter an integer.", font=("Ariel", 15))
        error.pack()



'''
work time, rest time, start/stop state, work/rest state (work is true; first by default),
total elapsed time (0 by default)
'''
pomodoro = Pomodoro(1500, 300, False, True, 0)

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("700x700")
    root.title("Pomodoro")

    two_sides = tk.Frame(root)#GUI split into two sides: options and timer
    two_sides.columnconfigure(0, weight=1)

    timer = tk.Frame(two_sides)#right side
    timer.columnconfigure(0, weight=1)

    side_panel = tk.Frame(two_sides)#left side
    side_panel.columnconfigure(0, weight=1)

    session = tk.Frame(root)
    session.columnconfigure(0, weight=1)#general info
    session.columnconfigure(1, weight=1)#delete session

    wr_display = tk.Frame(root)#part of root
    wr_display.columnconfigure(0, weight=1)
    
    clock_thread = threading.Thread(target=pomodoro.clock)#this is a CHILD/WORKER THREAD, which can execute its target function 
                                                #simultaneously while we do our other processes
    clock_thread.start()

    ssbtn = tk.Button(timer, text="Start/Stop", font=("Ariel", 20))
    ssbtn.config(command=pomodoro.start_stop)
    ssbtn.grid(row=1, column=0)

    #below text and buttons are part of the side panel
    options = tk.Label(side_panel, text="Options", font=("Ariel", 30))
    options.grid(row=0, column=0)

    rbtn = tk.Button(side_panel, text="Reset", font=("Ariel", 20))
    rbtn.config(command=pomodoro.reset)
    rbtn.grid(row=1, column=0)

    sbtn = tk.Button(side_panel, text="Save", font=("Ariel", 20))
    sbtn.config(command=pomodoro.save)
    sbtn.grid(row=2, column=0)

    switchbtn = tk.Button(side_panel, text="Switch", font=("Ariel", 20))
    switchbtn.config(command=pomodoro.instant_switch)
    switchbtn.grid(row=3, column=0)

    settingsbtn = tk.Button(side_panel, text="Settings", font=("Ariel", 20))
    settingsbtn.config(command=pomodoro.settings_gate)
    settingsbtn.grid(row=4, column=0)

    wr_display.pack()

    side_panel.grid(row=0, column=0)#left side

    timer.grid(row=0, column=1)#right side

    two_sides.pack()

    session.pack()#outstanding element; placed last to be out of the way

    root.mainloop()