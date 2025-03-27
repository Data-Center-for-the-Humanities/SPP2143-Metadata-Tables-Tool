#create a tk inter window with two columns and two rows
# with a button in the first row and a label in the second row

import tkinter as tk

root = tk.Tk()

# create a button
button = tk.Button(root, text="Click Me!")
button.grid(row=0, column=0)

# create a label
label = tk.Label(root, text="Hello, World!")
label.grid(row=1, column=0)

#column 1 should have a blue frame
frame = tk.Frame(root, width=100, height=100, bg="blue")
frame.grid(row=0, column=0, rowspan=2)

#column 2 should have a red frame
frame = tk.Frame(root, width=100, height=100, bg="red")
frame.grid(row=0, column=1, rowspan=2)




root.mainloop()

