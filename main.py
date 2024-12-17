import threading
from pomodoro import Pomodoro
from gui import Gui

#this file handles multithreading and main execution of the classes

pomo = Pomodoro(1500, 300, False, True, 0)

clock_thread = threading.Thread(target=pomo.clock)#this is a CHILD/WORKER THREAD, which can execute its target function 
                                                  #simultaneously while we do our other processes
clock_thread.start()

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

    ssbtn = tk.Button(timer, text="Start/Stop", font=("Ariel", 20))
    ssbtn.config(command=pomo.start_stop)
    ssbtn.grid(row=1, column=0)

    #below text and buttons are part of the side panel
    options = tk.Label(side_panel, text="Options", font=("Ariel", 30))
    options.grid(row=0, column=0)

    rbtn = tk.Button(side_panel, text="Reset", font=("Ariel", 20))
    rbtn.config(command=pomo.reset)
    rbtn.grid(row=1, column=0)

    sbtn = tk.Button(side_panel, text="Save", font=("Ariel", 20))
    sbtn.config(command=pomo.save)
    sbtn.grid(row=2, column=0)

    switchbtn = tk.Button(side_panel, text="Switch", font=("Ariel", 20))
    switchbtn.config(command=pomo.instant_switch)
    switchbtn.grid(row=3, column=0)

    settingsbtn = tk.Button(side_panel, text="Settings", font=("Ariel", 20))
    settingsbtn.config(command=pomo.settings_gate)
    settingsbtn.grid(row=4, column=0)

    wr_display.pack()

    side_panel.grid(row=0, column=0)#left side

    timer.grid(row=0, column=1)#right side

    two_sides.pack()

    session.pack()#outstanding element; placed last to be out of the way

    root.mainloop()