import tkinter as tk
from tkinter import ttk
import os
import threading
import time

def show_splash_screen():
    """Shows a splash screen with the MTT logo immediately"""
    # Create root window for splash (use fixed size variables)
    splash_root = tk.Tk()
    splash_root.title("FAIR.rdm MTT")
    splash_root.resizable(False, False)

    # Compute script-relative paths so images load regardless of CWD
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, "modules", "menu", "MTT_favicon.ico")
    icon_ico_path = os.path.join(script_dir, "modules", "menu", "MTT_favicon.ico")
    logo_path = os.path.join(script_dir, "modules", "menu", "MTT_Logo.png")

    # Set custom icon for splash screen (try quietly)
    # Try .ico first (works best for Windows taskbar)
    try:
        if os.path.exists(icon_ico_path):
            splash_root.iconbitmap(icon_ico_path)
        elif os.path.exists(icon_path):
            # Fallback to PNG with iconphoto
            icon_photo = tk.PhotoImage(file=icon_path)
            splash_root.iconphoto(True, icon_photo)
    except Exception as e:
        print(f"Could not load splash icon: {e}")

    # Splash geometry (consistent)
    splash_w, splash_h = 400, 400
    splash_root.geometry(f"{splash_w}x{splash_h}")

    # Center the splash screen
    splash_root.update_idletasks()
    x = (splash_root.winfo_screenwidth() // 2) - (splash_w // 2)
    y = (splash_root.winfo_screenheight() // 2) - (splash_h // 2)
    splash_root.geometry(f"{splash_w}x{splash_h}+{x}+{y}")

    # Remove window decorations for cleaner look and keep on top while visible
    splash_root.overrideredirect(True)
    try:
        splash_root.attributes("-topmost", True)
    except Exception:
        # Some platforms may not support attributes; ignore
        pass
    splash_root.configure(bg="white")

    # Try to load and display the logo; be robust to Pillow versions and CWD
    logo_loaded = False
    image_display_size = 300

    if os.path.exists(logo_path):
        # 1) Prefer PIL if available so we can resize cleanly
        try:
            from PIL import Image, ImageTk
            image = Image.open(logo_path)
            # Backwards-compatible resampling selection
            try:
                resample = Image.Resampling.LANCZOS
            except Exception:
                # Pillow < 9 uses LANCZOS or ANTIALIAS
                resample = getattr(Image, 'LANCZOS', Image.ANTIALIAS)
            image = image.resize((image_display_size, image_display_size), resample)
            photo = ImageTk.PhotoImage(image)

            label_img = tk.Label(splash_root, image=photo, bg="white")
            label_img.image = photo  # Keep a reference to avoid GC
            label_img.pack(expand=True)
            logo_loaded = True
        except Exception as pil_err:
            # If PIL isn't available or fails, try Tk's native PhotoImage
            try:
                photo = tk.PhotoImage(file=logo_path)
                label_img = tk.Label(splash_root, image=photo, bg="white")
                label_img.image = photo
                label_img.pack(expand=True)
                logo_loaded = True
            except Exception as tk_err:
                print(f"Could not load image (PIL error: {pil_err}; Tk error: {tk_err})")
                logo_loaded = False
    
    # Fallback if image loading fails or doesn't exist
    if not logo_loaded:
        label_text = tk.Label(splash_root, text="FAIR.rdm MTT v 1.0", 
                            font=("Helvetica", 20, "bold"), bg="white", fg="navy")
        label_text.pack(expand=True)
    
    # Add loading text
    loading_label = tk.Label(splash_root, text="Loading modules...", 
                           font=("Helvetica", 10), bg="white", fg="gray")
    loading_label.pack(side=tk.BOTTOM, pady=20)
    
    # Update the display
    splash_root.update()
    
    return splash_root, loading_label

def load_modules_and_show_menu(splash_root, loading_label):
    """Loads modules and shows main menu"""
    try:
        # Update loading text
        loading_label.config(text="Importing main menu...")
        splash_root.update()
        
        # Import main menu module (this might take time)
        from modules.menu import main_menu
        
        # Show loading for a moment so user can see the logo
        loading_label.config(text="Initializing interface...")
        splash_root.update()
        time.sleep(1.5)  # Give user time to see the splash screen
        
        # Transform splash screen into main window instead of destroying it
        # Turn off topmost (if set) and restore window decorations
        try:
            splash_root.attributes("-topmost", False)
        except Exception:
            pass
        splash_root.overrideredirect(False)  # Restore window decorations

        # Set main window size and make resizable
        main_w, main_h = 800, 750
        splash_root.geometry(f"{main_w}x{main_h}")
        try:
            splash_root.resizable(True, True)
        except Exception:
            pass

        # Re-center the main window
        splash_root.update_idletasks()
        x = (splash_root.winfo_screenwidth() // 2) - (main_w // 2)
        y = (splash_root.winfo_screenheight() // 2) - (main_h // 2)
        splash_root.geometry(f"{main_w}x{main_h}+{x}+{y}")
        
        # Clear splash screen content
        for widget in splash_root.winfo_children():
            widget.destroy()
        
        # Pass the existing root to main menu
        main_menu.main_menu_design(splash_root)
        
        # Start main loop
        splash_root.mainloop()
        
    except Exception as e:
        # Handle errors gracefully
        loading_label.config(text=f"Error loading: {str(e)}")
        splash_root.update()
        time.sleep(3)
        splash_root.destroy()

if __name__ == "__main__":
    # Show splash screen immediately
    splash_root, loading_label = show_splash_screen()
    
    # Load modules and start application
    load_modules_and_show_menu(splash_root, loading_label)