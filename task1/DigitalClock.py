from tkinter import *
from tkinter import ttk
import tkinter as tk
from time import strftime, sleep
from pygame import mixer
from datetime import datetime
import pyglet
from threading import Thread

# custom font
pyglet.font.add_file('digital-7.ttf')

is_24_hour_format = False

def open_new_window():
    new_window = tk.Toplevel(root)
    new_window.title("Set Alarm")
    new_window.configure(bg='black')
    new_window.geometry("350x180")


    title_label = tk.Label(new_window, text="Set Alarm", font=('calibri', 30, 'bold'), background='black', foreground='cyan')
    title_label.grid(row=0, column=0, columnspan=4, pady=(5, 2))

    new_window.grid_columnconfigure(0, weight=1)
    new_window.grid_columnconfigure(1, weight=1)
    new_window.grid_columnconfigure(2, weight=1)
    new_window.grid_columnconfigure(3, weight=1)


    hour = tk.Label(new_window, text="Hour", font=('calibri', 12, 'bold'), background='black', foreground='cyan')
    hour.grid(row=1, column=0, padx=5, pady=(2, 0), sticky='ew')

    minute = tk.Label(new_window, text="Minute", font=('calibri', 12, 'bold'), background='black', foreground='cyan')
    minute.grid(row=1, column=1, padx=5, pady=(2, 0), sticky='ew')

    second = tk.Label(new_window, text="Second", font=('calibri', 12, 'bold'), background='black', foreground='cyan')
    second.grid(row=1, column=2, padx=5, pady=(2, 0), sticky='ew')
    
    period = tk.Label(new_window, text="Period", font=('calibri', 12, 'bold'), background='black', foreground='cyan')
    period.grid(row=1, column=3, padx=5, pady=(2, 0), sticky='ew')

    # Comboboxes for hour, minute, second, and period
    c_hour = ttk.Combobox(new_window, width=4, font=('arial', 12))
    c_hour['values'] = ("00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12")
    c_hour.current(0)
    c_hour.grid(row=2, column=0, padx=5, pady=(5, 0))

    c_min = ttk.Combobox(new_window, width=4, font=('arial', 12))
    c_min['values'] = tuple(f"{i:02d}" for i in range(60))
    c_min.current(0)
    c_min.grid(row=2, column=1, padx=5, pady=(5, 0))

    c_sec = ttk.Combobox(new_window, width=4, font=('arial', 12))
    c_sec['values'] = tuple(f"{i:02d}" for i in range(60))
    c_sec.current(0)
    c_sec.grid(row=2, column=2, padx=5, pady=(5, 0))

    c_period = ttk.Combobox(new_window, width=4, font=('arial', 12))
    c_period['values'] = ("AM", "PM")
    c_period.current(0)
    c_period.grid(row=2, column=3, padx=5, pady=(5, 0))

    def sound_alarm():
        mixer.music.load('oversimplified-alarm-clock-113180.mp3')
        mixer.music.play()

    def alarm():
        while selected.get() == 1:
            alarm_hour = c_hour.get()
            alarm_minute = c_min.get()
            alarm_sec = c_sec.get()
            alarm_period = c_period.get().upper()

            now = datetime.now()

            hour = now.strftime("%I")
            minute = now.strftime("%M")
            second = now.strftime("%S")
            period = now.strftime("%p")

            if alarm_period == period and alarm_hour == hour and alarm_minute == minute and alarm_sec == second:
                print("Time to take a break")
                sound_alarm()
                deactivate_button.grid(row=3, column=0, columnspan=4, pady=10)  # Show the deactivate button
                activate_button.grid_forget()  # Hide the activate button
                break
            sleep(1)

    def activate_alarm():
        selected.set(1)
        t = Thread(target=alarm)
        t.start()
        activate_button.grid_forget() 
        deactivate_button.grid(row=3, column=0, columnspan=4, pady=10)

    def deactivate_alarm():
        mixer.music.stop()
        selected.set(0)
        deactivate_button.grid_forget()  # Hide the deactivate button
        activate_button.grid(row=3, column=0, columnspan=4, pady=10)  # Show the activate button

    selected = IntVar()

    # Activate button
    activate_button = tk.Button(new_window, text="Activate", command=activate_alarm, font=('calibri', 14, 'bold'),
                                bg='#1a1b1c', fg='cyan', bd=2, relief="solid", highlightbackground='cyan', highlightthickness=2,
                                activebackground='#1c1b1b', activeforeground='cyan')
    activate_button.grid(row=3, column=0, columnspan=4, padx=25, pady=10)

    # Deactivate button hidden initially
    deactivate_button = tk.Button(new_window, text="Deactivate", command=deactivate_alarm, font=('calibri', 14, 'bold'),
                                  bg='#1a1b1c', fg='cyan', bd=2, relief="solid", highlightbackground='cyan', highlightthickness=2,
                                  activebackground='#1c1b1b', activeforeground='cyan')

mixer.init()

def toggle_format():
    global is_24_hour_format
    is_24_hour_format = not is_24_hour_format  # Toggle between 12-hour and 24-hour formats
    
    # Update the button text
    toggle_button.config(text="12-Hour Format" if is_24_hour_format else "24-Hour Format")

def showtime():
    time_format = "%H:%M:%S" if is_24_hour_format else "%I:%M:%S %p"
    string1 = strftime(time_format)
    label1.config(text=string1)
    
    string2 = strftime("%A, %d %B, %Y")
    label2.config(text=string2)
    
    label1.after(1000, showtime)

root = tk.Tk()
root.title("Digital Clock")
root.configure(bg='black')
root.geometry("350x180")


label1 = tk.Label(root, font=('digital-7', 50), background='black', foreground='cyan')
label1.pack(anchor='center')

label2 = tk.Label(root, font=('calibri', 20, 'bold'), background='black', foreground='cyan')
label2.pack(anchor='center')


button = tk.Button(root, text="Set Alarm", command=open_new_window, font=('calibri', 14, 'bold'),
                   bg='#1a1b1c', fg='cyan', bd=2, relief="solid", highlightbackground='cyan', highlightthickness=2,
                   activebackground='#1c1b1b', activeforeground='cyan')
button.pack(side='right', padx=10, pady=10, ipadx=15, ipady=20)  


toggle_button = tk.Button(root, text="24-Hour Format", command=toggle_format, font=('calibri', 14, 'bold'),
                          bg='#1a1b1c', fg='cyan', bd=2, relief="solid", highlightbackground='cyan', highlightthickness=2,
                          activebackground='#1c1b1b', activeforeground='cyan')
toggle_button.pack(side='left', padx=10, pady=10, ipadx=15, ipady=20) 


showtime()
root.mainloop()

