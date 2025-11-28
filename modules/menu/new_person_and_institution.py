def person_institution():
    import tkinter as tk
    from tkinter import ttk
    import pandas as pd
    import os
    #from modules.menu import main_menu

    #Lese die bereits vorhandenen Daten zu Personen und Institutionen aus der Excel-Datei ein
    excel_path = os.path.join(os.path.dirname(__file__), "../../metadata_tables/registered_persons.xlsx")
    registered_persons_df = pd.read_excel(excel_path)
    #print(registered_persons_df)

    # Create the main window
    root = tk.Tk()
    root.title("New Person / Institution")
    root.geometry("800x500")
    
    # Set custom icon using the helper function from main_menu
    #main_menu.set_window_icon(root)

    def go_back():
        print("Button 1 clicked")
        main_menu.main_menu_design()
        root.destroy()

    def toggle_institution_entry():
        if var.get() == "institution":
            entry_institution.config(state="disabled")
            print("Institution entry enabled")
        elif var.get() == "person":
            entry_institution.config(state="normal")
            print("Institution entry disabled")
        else:
            print("error")

    def save_person():
        name = entry_name.get()
        identifier = entry_identifier.get()
        email = entry_email.get()
        website = entry_website.get()
        institution = entry_institution.get() if var.get() == "person" else "not_defined"

        # Check if all required fields are filled
        if not name:
            #pop up a message box
            messagebox.showerror("Error", "Name is required.")
            return
        if not identifier:
            identifier = "not_defined"  # Default value if identifier is not provided
        if not email:
            email = "not_defined"
        if not website:
            website = "not_defined"
        if var.get() == "person" and not institution:
            messagebox.showerror("Error", "Institution is required for persons.")
            return

        # Save the new person or institution to the DataFrame
        new_entry = {
            "Name": name,
            "Identifier": identifier,
            "Email": email,
            "Homepage": website,
            "HasInstitution": institution
        }
        registered_persons_df.loc[len(registered_persons_df)] = new_entry

        # Save the updated DataFrame to the Excel file
        registered_persons_df.to_excel(excel_path, index=False, sheet_name="person")
        print("New person/institution saved successfully.")
        messagebox.showinfo("Success", "New person/institution saved successfully.")
        # Clear the input fields
        entry_name.delete(0, tk.END)
        entry_identifier.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_website.delete(0, tk.END)
        entry_institution.delete(0, tk.END)

    def open_documentation():
        """Open the documentation in a web browser"""
        #The file is /documentation/MTT_Readme.html
        doc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../documentation/MTT_Readme.html"))
        webbrowser.open_new(f"file:///{doc_path.replace(os.sep, '/')}")



    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)
    root.grid_rowconfigure(4, weight=1)
    root.grid_rowconfigure(5, weight=1)
    root.grid_rowconfigure(6, weight=1)
    root.grid_rowconfigure(7, weight=1)
    root.grid_rowconfigure(8, weight=1)
    root.grid_rowconfigure(9, weight=1)

    #Titel 1. Zeile
    label_title = tk.Label(root, text="Create a new Person or Institution", font=("Helvetica", 16, "bold"), anchor="w")
    label_title.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="nw")

    #Untertitel 2. Zeile
    label_subtitle = tk.Label(root, text="Make sure to check the correct type.", font=("Helvetica", 12, "bold"), anchor="w")
    label_subtitle.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="nw")

    #radio buttons for person or institution
    var = tk.StringVar(value="person")  # Default value
    person_radio = tk.Radiobutton(root, text="Person", variable=var, value="person", font=("Helvetica", 12), command=toggle_institution_entry)
    person_radio.grid(row=2, column=0, pady=10, padx=15, sticky="w")
    institution_radio = tk.Radiobutton(root, text="Institution", variable=var, value="institution", font=("Helvetica", 12), command=toggle_institution_entry)
    institution_radio.grid(row=2, column=1, pady=10, padx=15, sticky="w")

    #Get the name of the person or institution
    label_name = tk.Label(root, text="Name:", font=("Helvetica", 12), anchor="w")
    label_name.grid(row=3, column=0, pady=10, padx=15, sticky="w")
    entry_name = tk.Entry(root, font=("Helvetica", 12))
    entry_name.grid(row=3, column=1, pady=10, padx=15, sticky="w")

    #Get the identifier of the person or institution
    label_identifier = tk.Label(root, text="Identifier (e.g. ORCID for person, ROR for institution):", font=("Helvetica", 12), anchor="w")
    label_identifier.grid(row=4, column=0, pady=10, padx=15, sticky="w")
    entry_identifier = tk.Entry(root, font=("Helvetica", 12))
    entry_identifier.grid(row=4, column=1, pady=10, padx=15, sticky="w")

    #Get the email of the person or institution
    label_email = tk.Label(root, text="Email:", font=("Helvetica", 12), anchor="w")
    label_email.grid(row=5, column=0, pady=10, padx=15, sticky="w")
    entry_email = tk.Entry(root, font=("Helvetica", 12))
    entry_email.grid(row=5, column=1, pady=10, padx=15, sticky="w")

    #Get the website of the person or institution
    label_website = tk.Label(root, text="Website:", font=("Helvetica", 12), anchor="w")
    label_website.grid(row=6, column=0, pady=10, padx=15, sticky="w")
    entry_website = tk.Entry(root, font=("Helvetica", 12))
    entry_website.grid(row=6, column=1, pady=10, padx=15, sticky="w")

    #Get the institution of the person (if applicable)
    label_institution = tk.Label(root, text="Institution (if applicable):", font=("Helvetica", 12), anchor="w")
    label_institution.grid(row=7, column=0, pady=10, padx=15, sticky="w")
    entry_institution = tk.Entry(root, font=("Helvetica", 12))
    entry_institution.grid(row=7, column=1, pady=10, padx=15, sticky="w")
    # In dieses Feld kann nur bei Personen etwas eingetragen werden
    toggle_institution_entry()

    #Button Save Entries
    button5 = tk.Button(root, text="Save Entry", command=save_person, width=35, height=2)
    button5.grid(row=8, column=0, pady=10, padx=15, sticky="nw")

    
    



    # Back button
    back_button = tk.Button(root, text="Back", command=go_back, width=25, height=1, bg="orange", fg="white", font=("Helvetica", 10, "bold"))
    back_button.grid(row=9, column=0, columnspan=2, padx=10, pady=5, sticky="w")

    # Open documentation button
    open_doc_button = tk.Button(root, text="Open Documentation", command=open_documentation, width=25, height=1, bg="light blue", fg="white", font=("Helvetica", 10, "bold"))
    open_doc_button.grid(row=9, column=0, columnspan=2, padx=10, pady=5)

    # Cancel button
    cancel_button = tk.Button(root, text="Cancel without Saving", command=go_back, width=25, height=1, bg="red", fg="black", font=("Helvetica", 10, "bold"))
    cancel_button.grid(row=9, column=0, columnspan=2, padx=10, pady=5, sticky="e")

    
if __name__ == "__main__":
    import tkinter as tk
    from tkinter import messagebox
    import pandas as pd
    import os
    import webbrowser
    person_institution()
    tk.mainloop()
else:
    import tkinter as tk
    from tkinter import messagebox
    import pandas as pd
    import os
    import webbrowser
    from modules.menu import main_menu