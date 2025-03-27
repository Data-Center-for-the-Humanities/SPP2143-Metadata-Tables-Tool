import tkinter as tk

from modules.menu import main_menu

if __name__ == "__main__":
    root = tk.Tk()
     
    #hide the main window
    root.withdraw()
    
    main_menu.main_menu_design()

    root.mainloop()