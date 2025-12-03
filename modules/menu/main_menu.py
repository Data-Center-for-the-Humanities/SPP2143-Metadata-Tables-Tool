def set_window_icon(window):
    """Helper function to set the custom icon for any tkinter window"""
    try:
        icon_path = os.path.join(os.path.dirname(__file__), "MTT_favicon.png")
        if os.path.exists(icon_path):
            from PIL import Image, ImageTk
            icon_image = Image.open(icon_path)
            icon_photo = ImageTk.PhotoImage(icon_image)
            window.iconphoto(True, icon_photo)
    except Exception as e:
        print(f"Could not load icon: {e}")

def main_menu_design(root=None):
    # Use provided root or create new one
    if root is None:
        mainmenu = tk.Tk()
    else:
        mainmenu = root
        
    mainmenu.title("FAIR.rdm MTT Beta 1.0")
    mainmenu.geometry("800x750")
    mainmenu.configure(bg="#f0f0f0")
    
    # Set custom icon
    set_window_icon(mainmenu)

    def button1_action():
        print("Button 1 clicked")
        #Execute module named person-institution.py in modules/menu
        new_person_and_institution.person_institution()
        #Close the main window
        mainmenu.destroy()

    def button2_action():
        print("Button 2 clicked")
        open_dialog(mainmenu)

    def open_dialog(parent):
        """
        Öffnet ein neues Top-Level-Fenster (Dialogfenster), um den Datensatz-Typ abzufragen.
        """
        dialog = tk.Toplevel(parent)
        dialog.title("Initial Input")
        dialog.geometry("300x250")
        
        # Zentriert das Dialogfenster über dem Hauptfenster
        parent.update_idletasks()
        main_x = parent.winfo_x()
        main_y = parent.winfo_y()
        main_width = parent.winfo_width()
        main_height = parent.winfo_height()
        dialog_width = dialog.winfo_width()
        dialog_height = dialog.winfo_height()
        
        dialog.geometry(
            f"+{main_x + (main_width - dialog_width) // 2}"
            f"+{main_y + (main_height - dialog_height) // 2}"
        )

        # Stellt sicher, dass das Hauptfenster nicht bedienbar ist,
        # solange der Dialog offen ist
        dialog.transient(parent)
        dialog.grab_set()

        # UI-Elemente im Dialogfenster
        label = ttk.Label(dialog, text="Please choose the suitable type:")
        label.pack(pady=10)

        radio_frame = ttk.Frame(dialog)
        radio_frame.pack(pady=5)

        # Variable für die Radiobuttons (specify dialog as master)
        choice_var = tk.StringVar(master=dialog, value="nd")

        # Radiobuttons für die Auswahl des Datensatz-Typs
        radio_collection = ttk.Radiobutton(
            radio_frame,
            text="Collection",
            value="collection",
            variable=choice_var,
        )
        radio_collection.pack(side="left", padx=10)

        radio_individual = ttk.Radiobutton(
            radio_frame,
            text="Individual Data Resource",
            value="individual",
            variable=choice_var,
        )
        radio_individual.pack(side="left", padx=10)

        # Print the selected dataset type whenever a radio button is selected
        def update_dataset_type(*args):
            print(f"Selected dataset type: {choice_var.get()}")
            dataset_type = choice_var.get()
            return dataset_type
        choice_var.trace_add("write", update_dataset_type)
        print(f"Initial dataset type: {choice_var.get()}")
        
        # Load suggestions from metadata_tables directory
        metadata_tables_path = os.path.join(os.path.dirname(__file__), "../../metadata_tables")
        name_suggestions = []
        
        try:
            if os.path.exists(metadata_tables_path):
                metadata_files = [f for f in os.listdir(metadata_tables_path) if os.path.isfile(os.path.join(metadata_tables_path, f))]
                for file in metadata_files:
                    #if file.startswith('P') or file.startswith('S'):
                        # Remove file extension and add to suggestions
                        name_without_extension = os.path.splitext(file)[0]
                        name_suggestions.append(name_without_extension)
        except Exception as e:
            print(f"Could not load metadata files: {e}")
            # Fallback to default suggestions if directory can't be read
            name_suggestions = [
                "Something's wrong",
                "This is probably an error", 
                "Folder can't be read or is missing"
            ]
    
        #Enter the datasets name with autocomplete
        label_name = ttk.Label(dialog, text="Dataset Name:")
        label_name.pack(pady=5)
        
        # Create frame for entry and suggestions
        name_frame = ttk.Frame(dialog)
        name_frame.pack(pady=5, padx=10, fill=tk.X)
        
        dialog.entry_name = ttk.Entry(name_frame)
        dialog.entry_name.pack(fill=tk.X)
        
        # Create listbox for suggestions (initially hidden)
        suggestions_listbox = tk.Listbox(name_frame, height=5)
        suggestions_listbox.pack(fill=tk.X)
        suggestions_listbox.pack_forget()  # Hide initially
        
        def on_name_keyup(event):
            """Filter suggestions based on user input"""
            current_text = dialog.entry_name.get().lower()
            
            if current_text:
                # Filter suggestions that contain the current text
                filtered_suggestions = [s for s in name_suggestions if current_text in s.lower()]
                
                if filtered_suggestions:
                    suggestions_listbox.delete(0, tk.END)
                    for suggestion in filtered_suggestions[:5]:  # Show max 5 suggestions
                        suggestions_listbox.insert(tk.END, suggestion)
                    suggestions_listbox.pack(fill=tk.X)
                else:
                    suggestions_listbox.pack_forget()
            else:
                suggestions_listbox.pack_forget()
        
        def on_suggestion_select(event):
            """Handle suggestion selection"""
            selection = suggestions_listbox.curselection()
            if selection:
                selected_text = suggestions_listbox.get(selection[0])
                dialog.entry_name.delete(0, tk.END)
                dialog.entry_name.insert(0, selected_text)
                suggestions_listbox.pack_forget()
        
        def hide_suggestions(event):
            """Hide suggestions when clicking outside"""
            suggestions_listbox.pack_forget()
        
        # Bind events
        dialog.entry_name.bind('<KeyRelease>', on_name_keyup)
        suggestions_listbox.bind('<Double-Button-1>', on_suggestion_select)
        dialog.bind('<Button-1>', hide_suggestions)
        
        #Enter the datasets uri
        label_uri = ttk.Label(dialog, text="Dataset URI:")
        label_uri.pack(pady=5)
        dialog.entry_uri = ttk.Entry(dialog)
        dialog.entry_uri.pack(pady=5, padx=10, fill=tk.X)
        # Default value for the entry fields
        dialog.entry_uri.insert(0, "blank")

        ok_button = ttk.Button(dialog, text="OK", command=lambda: on_dialog_close(choice_var.get(), dialog.entry_name.get(), dialog.entry_uri.get(), name_suggestions))
        ok_button.pack(pady=10)

        # Warte, bis das Dialogfenster geschlossen wird
        #parent.wait_window(dialog)


    def on_dialog_close(dataset_type, dataset_name, dataset_uri, name_suggestions): 
        """
        Wird aufgerufen, wenn der OK-Button im Dialogfenster gedrückt wird.
        Holt die Auswahl und schließt das Dialogfenster.
        """
        print(f"Type: {dataset_type}")
        print(f"Dataset Name: {dataset_name}")
        print(f"Dataset URI: {dataset_uri}")

        #dataset_name has to be new. It cannot be an existing name like in suggestions
        if dataset_name in name_suggestions:
            messagebox.showerror("Error", "Dataset name already exists. Please choose a different name.")
            return

        if dataset_type == "collection":
            print("Collection selected")
            #Create a copy of SPP2143_ARIADNE_Collection_Import_Template.xlsx from templates in the metadata_tables directory
            #name it with the dataset_name and save it in the metadata_tables directory
            metadata_tables_path = os.path.join(os.path.dirname(__file__), "../../metadata_tables")
            template_path = os.path.join(os.path.dirname(__file__), "../../templates", "SPP2143_ARIADNE_Collection_Import_Template.xlsx")
            shutil.copy(template_path, os.path.join(metadata_tables_path, f"{dataset_name}.xlsx"))
        else:
            print("Individual Data Resource selected")
            #Copy of SPP2143_ARIADNE_IDR_Import_Template.xlsx
            metadata_tables_path = os.path.join(os.path.dirname(__file__), "../../metadata_tables")
            template_path = os.path.join(os.path.dirname(__file__), "../../templates", "SPP2143_ARIADNE_IDR_Import_Template.xlsx")
            shutil.copy(template_path, os.path.join(metadata_tables_path, f"{dataset_name}.xlsx"))
        
        if dataset_uri == "blank":
            print("loading empty template")
            #Read in the template and fill in the dataset_name
            wb = load_workbook(os.path.join(metadata_tables_path, f"{dataset_name}.xlsx"))
            ws = wb['metadata']
            # Find the row with 'has_identifier' and update column B (2nd column)
            for row in ws.iter_rows():
                if row[0].value == 'has_identifier':
                    row[1].value = dataset_name
                    # Optionally add formatting to the new value
                    row[1].font = Font(bold=True)
                    break
            #Insert current date in "was_issued"
            for row in ws.iter_rows():
                if row[0].value == 'was_issued':
                    current_date = datetime.now().strftime("%Y-%m-%d")
                    row[1].value = current_date
                    break
            #And current date in "was_modified"
            for row in ws.iter_rows():
                if row[0].value == 'was_modified':
                    current_date = datetime.now().strftime("%Y-%m-%d")
                    row[1].value = current_date
                    break
            # Save the file with preserved formatting
            wb.save(os.path.join(metadata_tables_path, f"{dataset_name}.xlsx"))
            print("File saved with preserved formatting!")

        else:
            print(f"Preparing Template for: {dataset_uri}")
            #Read in the template and fill in the dataset_name and dataset_uri
            wb = load_workbook(os.path.join(metadata_tables_path, f"{dataset_name}.xlsx"))
            ws = wb['metadata']

            # Find the row with 'has_identifier' and update column B (2nd column)
            for row in ws.iter_rows():
                if row[0].value == 'has_identifier':
                    row[1].value = dataset_name
                    # Optionally add formatting to the new value
                    row[1].font = Font(bold=True)
                    break
            for row in ws.iter_rows():
                if row[0].value == 'has_landing_page':
                    row[1].value = dataset_uri
                    break
            #Insert current date in "was_issued"
            for row in ws.iter_rows():
                if row[0].value == 'was_issued':
                    current_date = datetime.now().strftime("%Y-%m-%d")
                    row[1].value = current_date
                    break
            #And current date in "was_modified"
            for row in ws.iter_rows():
                if row[0].value == 'was_modified':
                    current_date = datetime.now().strftime("%Y-%m-%d")
                    row[1].value = current_date
                    break
            
            # Save the file with preserved formatting
            wb.save(os.path.join(metadata_tables_path, f"{dataset_name}.xlsx"))
            print("File saved with preserved formatting!")

        mainmenu.destroy()  # Schließt das Hauptfenster
        new_dataset.new_dataset()
    
    ###

    def button3_action():
        '''
        Open the menu to update or delete an existing dataset
        '''
        print("Button 3 clicked")
        #Get the file currently selected in the value_list Listbox
        selected_file = None
        try:
            selected_file = value_list.get(value_list.curselection())
            print(f"Selected file: {selected_file}")
        except Exception as e:
            messagebox.showerror("Error", "Please select a dataset from the Data Selector list.")
            return
        mainmenu.destroy()
        change_dataset.change_dataset(selected_file=selected_file)

    def button4_action():
        '''
        Sync the content of metadata_mirror to GitLab
        '''
        print("Button 4 clicked")
        #Execute the sync function from the sync module
        metadata_mirror_path = os.path.join(os.path.dirname(__file__), f"../../{mtt_config.local_folder}")
        sync.mirror_to_gitlab(metadata_mirror_path, mtt_config.repo_url, mtt_config.target_subdir, mtt_config.token, mtt_config.branch)
        #Show a messagebox while syncing is in progress
        
    def button5_action():
        '''
        Open the online infrastructure links in the default web browser
        '''
        print("Button 5 clicked")
        #Open a new tab in the default web browser with the links to the online infrastructure
        webbrowser.open_new_tab(mtt_config.git_repo)
        webbrowser.open_new_tab(mtt_config.oai_pmh_status)
        webbrowser.open_new_tab(mtt_config.oai_pmh_list)
        webbrowser.open_new_tab(mtt_config.ariadne)

    mainmenu.grid_columnconfigure(0, weight=1)
    mainmenu.grid_columnconfigure(1, weight=1)
    mainmenu.grid_rowconfigure(0, weight=1)
    mainmenu.grid_rowconfigure(1, weight=1)
    mainmenu.grid_rowconfigure(2, weight=1)
    mainmenu.grid_rowconfigure(3, weight=1)
    mainmenu.grid_rowconfigure(4, weight=1)
    mainmenu.grid_rowconfigure(5, weight=1)
    mainmenu.grid_rowconfigure(6, weight=1)
    mainmenu.grid_rowconfigure(7, weight=1)
    mainmenu.grid_rowconfigure(8, weight=1)

    #Titel 1. Zeile
    label_title = tk.Label(mainmenu, text="FAIR.rdm Metadata Tables Tool Beta 1.0", font=("Helvetica", 16, "bold"), anchor="w")
    label_title.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="nw")

    #Untertitel 2. Zeile
    label_subtitle = tk.Label(mainmenu, text="Metadata Converter from multiple repositories to ARIADNE Portal", font=("Helvetica", 12, "bold"), anchor="w")
    label_subtitle.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="nw")

    #Button 3. Zeile
    button1 = tk.Button(mainmenu, text="New Person / Institution", command=button1_action, width=35, height=2)
    button1.grid(row=2, column=0, pady=10, padx=15, sticky="nw")

    #Button 4. Zeile
    button2 = tk.Button(mainmenu, text="New Data Record", command=button2_action, width=35, height=2)
    button2.grid(row=3, column=0, pady=10, padx=15, sticky="nw")

    #Button 5. Zeile
    button3 = tk.Button(mainmenu, text="Change Data Record", command=button3_action, width=35, height=2)
    button3.grid(row=4, column=0, pady=10, padx=15, sticky="nw")

    #Button 6. Zeile
    button4 = tk.Button(mainmenu, text="Push to GitLab", command=button4_action, width=35, height=2)
    button4.grid(row=5, column=0, pady=10, padx=15, sticky="nw")

    #Button 7. Zeile
    button5 = tk.Button(mainmenu, text="View Online Infrastructure", command=button5_action, width=35, height=2)
    button5.grid(row=6, column=0, pady=10, padx=15, sticky="nw")

    
    #Data Selector in Zeile 8
    scrollbar_frame = tk.Frame(mainmenu)
    scrollbar_frame.grid(row=7, column=0, pady=10, padx=15, sticky="w")

    label_list = tk.Label(scrollbar_frame, text="Data Selector", font=("Helvetica", 8), anchor="w")
    label_list.grid(sticky="w")

    scrollbar = tk.Scrollbar(scrollbar_frame)
    scrollbar.grid(row=0, column=1, sticky='ns')
    value_list = tk.Listbox(scrollbar_frame, yscrollcommand=scrollbar.set, width=40, height=15)
    #for i in range(100):
        #value_list.insert(tk.END, str(i))
    #List all files in metadata_tables
    metadata_tables_path = os.path.join(os.path.dirname(__file__), "../../metadata_tables")
    metadata_files = [f for f in os.listdir(metadata_tables_path) if os.path.isfile(os.path.join(metadata_tables_path, f))]
    for file in metadata_files:
        if "log" not in file and "registered_persons" not in file and file.endswith('.xlsx'):
            value_list.insert(tk.END, file)

    value_list.grid(row=0, column=0, sticky='nsew')
    scrollbar.config(command=value_list.yview)
    value_list.bind('<<ListboxSelect>>', lambda event: on_select(event))

    #Selected file in value_list to dataframe and display in the data viewer
    # This function will be called when an item in the listbox is selected
    def on_select(event):
        selected_file = value_list.get(value_list.curselection())
        file_path = os.path.join(metadata_tables_path, selected_file)
        df = pd.read_excel(file_path, sheet_name="metadata")  # Assuming the files are Excel files
        df = df.fillna('not_defined')  # Fill NaN values with empty strings
        # Clear the treeview
        for item in tree.get_children():
            tree.delete(item)
        # Insert new data into the treeview
        for index, row in df.iterrows():
            tree.insert('', tk.END, values=(row['Metadata Property'], row['Metadata Value']))  # Adjust column names as needed
    
    def open_documentation():
        """Open the documentation in a web browser"""
        #The file is /documentation/MTT_Readme.html
        doc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../documentation/MTT_Readme.html"))
        webbrowser.open_new(f"file:///{doc_path.replace(os.sep, '/')}")

    def open_config():
        """Open the configuration file in the default text editor"""
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../mtt_config.py"))
        try:
            if os.name == 'nt':  # For Windows
                os.startfile(config_path)
        except AttributeError:
            messagebox.showerror("Error", f"Could not open configuration file.")
            

    #Data Viewer in Spalte 2

    viewer_frame = tk.Frame(mainmenu)
    viewer_frame.grid(column=1, row=2, rowspan=6, pady=10, padx=15, sticky="nsew")
    # Allow the viewer_frame to expand
    mainmenu.grid_columnconfigure(1, weight=3)
    mainmenu.grid_rowconfigure(2, weight=3)

    df_test = pd.DataFrame({
        'Metadata Property': ['Property1', 'Property2', 'Property3'],
        'Metadata Value': ['Value1', 'Value2', 'Value3']
    })

    tree = ttk.Treeview(viewer_frame, columns=('Metadata Property', 'Metadata Value'), show='headings')
    tree.heading('Metadata Property', text='Metadata Property')
    tree.heading('Metadata Value', text='Metadata Value')

    for index, row in df_test.iterrows():
        tree.insert('', tk.END, values=(row['Metadata Property'], row['Metadata Value']))

    tree.pack(pady=10, padx=15, fill=tk.BOTH, expand=True)



    # Exit button
    exit_button = tk.Button(mainmenu, text="Exit", command=mainmenu.quit, width=25, height=1, bg="red", fg="white", font=("Helvetica", 10, "bold"))
    exit_button.grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky="w")

    # Open documentation button
    open_doc_button = tk.Button(mainmenu, text="Open Documentation", command=open_documentation, width=25, height=1, bg="light blue", fg="white", font=("Helvetica", 10, "bold"))
    open_doc_button.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

    # Open configuration button
    open_config_button = tk.Button(mainmenu, text="Open Configuration", command=open_config, width=25, height=1, bg="light green", fg="white", font=("Helvetica", 10, "bold"))
    open_config_button.grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky="e")

if __name__ == "__main__":
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox
    import pandas as pd
    import os
    import subprocess
    import tempfile
    from datetime import datetime
    import shutil
    import webbrowser
    from openpyxl import load_workbook
    from openpyxl.styles import Font, PatternFill
    main_menu_design()
    # Start the main loop
    tk.mainloop()
else:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox
    import pandas as pd
    from modules.menu import new_person_and_institution
    from modules.menu import new_dataset
    from modules.menu import change_dataset
    from modules import mtt_config
    from modules import sync
    from openpyxl import load_workbook
    from openpyxl.styles import Font, PatternFill
    import os
    import subprocess
    import tempfile
    from datetime import datetime
    import shutil
    import webbrowser


