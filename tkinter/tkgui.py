import tkinter

window = tkinter.Tk()
window.geometry('400x400')
window.title('what ever that describes this later on')
T =tkinter.Text(window, height=350, width=390)
T.place(x=0, y=0)
message = '...............test...............'
i = 0
while i < 40:
    T.insert(tkinter.END, message)
    i+=1
# bt1 = tkinter.Button(window, text='button1', command=changemessage(message, T)).place(x=350, y=370)
# bt1.grid(column=1, row=1)
# for i in range(5):
#     window.columnconfigure(index=i,weight=1,minsize=50)
#     window.rowconfigure(index=i,weight=1,minsize=50)
#     for j in range(5):
#         frame = tkinter.Frame(
#             master=window,
#             relief=tkinter.RAISED,
#             borderwidth=1,
#         )
#         frame.grid(row=i, column=j, padx=1, pady=1)
#         bt = tkinter.Button(master=frame, text=f'button{j}' )
#         bt.pack()


window.mainloop()


# import tkinter as tk


# root = tk.Tk()

# # specify size of window.
# root.geometry("250x170")

# # Create text widget and specify size.
# T = tk.Text(root, height = 5, width = 52)

# # Create label
# l = tk.Label(root, text = "Fact of the Day")
# l.config(font =("Courier", 14))

# Fact = """A man can be arrested in
# Italy for wearing a skirt in public."""

# # Create button for next text.
# b1 = tk.Button(root, text = "Next", )

# # Create an Exit button.
# b2 = tk.Button(root, text = "Exit",
# 			command = root.destroy)

# l.pack()
# T.pack()
# b1.pack()
# b2.pack()

# # Insert The Fact.
# T.insert(tk.END, Fact)

# tk.mainloop()
