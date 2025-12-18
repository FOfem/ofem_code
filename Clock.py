from tkinter import Label, Tk 

import time
import datetime

            #############################
            #   FORRACORP. LTD          #
            #   UBI, Fredrick           #
            #   Digital Clock           #   
            #############################

app_window = Tk() 
app_window.title("Digital Clock") 
app_window.geometry("1450x620") 
app_window.resizable(1,1)

text_font= ("Boulder", 312, 'bold')
text_font2= ("Boulder", 100, 'bold', 'italic')
#background = "white"
foreground= "#363529"
border_width = 25
border_hight = 1000

label = Label(app_window, font=text_font, fg=foreground, bd=border_width) 
#label = Label(app_window, font=text_font, bg=background, fg=foreground, bd=border_width) 
label.grid(row=5, column=1)

label2 = Label(app_window, font=text_font2, fg=foreground, bd=border_width) 
label2.grid(row=4, column=1)


def digital_clock(): 
   time_live = time.strftime("%H:%M:%S")
   label.config(text=time_live) 
   label.after(200, digital_clock)

def digital_date():
    date_live = datetime.datetime.now()
    date = date_live.strftime("%A %B %d, %Y")
    label2.config(text=date) 
    label2.after(1, digital_date)


digital_clock()
digital_date()

app_window.mainloop()

