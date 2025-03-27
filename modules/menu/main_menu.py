import tkinter as tk
from tkinter import ttk
import pandas as pd
from modules.menu import new_person_and_institution

def main_menu_design():
    # Create the main window
    root = tk.Tk()
    root.title("FAIR.rdm MTT v 0.2")
    root.geometry("800x750")

    label_title = tk.Label(root, text="FAIR.rdm Metadata Table Tool v 0.2", font=("Helvetica", 16, "bold"), anchor="w")
    label_title.pack(pady=10, padx=10, side=tk.TOP, anchor="w")

    label_subtitle = tk.Label(root, text="Metadata Converter from multiple different repositories to ARIADNE Portal", font=("Helvetica", 12, "bold"), anchor="w")
    label_subtitle.pack(pady=10, padx=10, anchor="w")

    button1 = tk.Button(root, text="New Person / Institution", command=button1_action, width=35, height=2)
    button1.pack(pady=10, padx=15, anchor="w")

    button2 = tk.Button(root, text="New Data Record", command=button2_action, width=35, height=2)
    button2.pack(pady=10, padx=15, anchor="w")

    button3 = tk.Button(root, text="Change Data Record", command=button3_action, width=35, height=2)
    button3.pack(pady=10, padx=15, anchor="w")

    button4 = tk.Button(root, text="Placeholder4", command=button2_action, width=35, height=2)
    button4.pack(pady=10, padx=15, anchor="w")

    button5 = tk.Button(root, text="Placeholder5", command=button3_action, width=35, height=2)
    button5.pack(pady=10, padx=15, anchor="w")

    #Data Selector

    scrollbar_frame = tk.Frame(root)
    scrollbar_frame.pack(fill=tk.Y, pady=10, padx=15, anchor="w")

    label_list = tk.Label(scrollbar_frame, text="Data Selector", font=("Helvetica", 8), anchor="w")
    label_list.pack(side=tk.TOP, anchor="w")

    scrollbar = tk.Scrollbar(scrollbar_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    value_list = tk.Listbox(scrollbar_frame, yscrollcommand=scrollbar.set, width=40, height=15)
    for i in range(100):
        value_list.insert(tk.END, str(i))

    value_list.pack(fill=tk.BOTH)
    scrollbar.config(command=value_list.yview)

    #Data Viewer
    #Muss noch an die richtige Stelle 

    viewer_frame = tk.Frame(root)
    viewer_frame.pack(fill=tk.BOTH, pady=10, padx=15)

    df_test = pd.DataFrame({
        'Column1': ['Value1', 'Value2', 'Value3'],
        'Column2': ['Value4', 'Value5', 'Value6']
    })

    tree = ttk.Treeview(viewer_frame, columns=('Column1', 'Column2'), show='headings')
    tree.heading('Column1', text='Metadata Property')
    tree.heading('Column2', text='Metadata Value')

    for index, row in df_test.iterrows():
        tree.insert('', tk.END, values=(row['Column1'], row['Column2']))

    tree.pack(pady=10, padx=15, fill=tk.BOTH, expand=True)



    # Create a frame to hold the bottom buttons
    bottom_frame = tk.Frame(root)
    bottom_frame.pack(side=tk.BOTTOM, pady=10, padx=10, fill=tk.X)

    # Exit button
    exit_button = tk.Button(bottom_frame, text="Exit", command=root.quit, width=25, height=1, bg="red", fg="white")
    exit_button.grid(row=0, column=0, padx=5)

    # Open documentation button
    open_doc_button = tk.Button(bottom_frame, text="Open Documentation", command=root.quit, width=25, height=1, bg="light blue", fg="white")
    open_doc_button.grid(row=0, column=1, padx=5)

    # Open configuration button
    open_config_button = tk.Button(bottom_frame, text="Open Configuration", command=root.quit, width=25, height=1, bg="light green", fg="white")
    open_config_button.grid(row=0, column=2, padx=5)


    # Pack buttons into the window
    button1.pack(pady=10)
    button2.pack(pady=10)
    button3.pack(pady=10)

def button1_action():
    print("Button 1 clicked")
    #Execute module named person-institution.py in modules/menu
    new_person_and_institution.person_institution()
    #Close the main window

def button2_action():
    print("Button 2 clicked")

def button3_action():
    print("Button 3 clicked")
