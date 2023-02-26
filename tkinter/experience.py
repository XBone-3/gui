# generating wrd doc to create an experience form

from tkinter import *
from docx import Document
from docx import Inches
from matplotlib.ft2font import BOLD

window = Tk()
window.title('Generate exp document')
window.geometry('400x400')

eid     =       Label(window, text='Employee ID     : ' , font=BOLD).place(x=15, y=10)
ename   =       Label(window, text='Employee name   : ' , font=BOLD).place(x=15, y=40)
edesig  =       Label(window, text='Designation     : ' , font=BOLD).place(x=15, y=70)
ejd     =       Label(window, text='Joining Date    : ' , font=BOLD).place(x=15, y=100)
eld     =       Label(window, text='Last working    : ' , font=BOLD).place(x=15, y=130)
egender =       Label(window, text='Gender          : ' , font=BOLD).place(x=15, y=160)








window.mainloop()
