import sys
from gui import KeyboardApp
import customtkinter as ctk

def main():
    print("Initializing Mechanical Keyboard Simulator...")
    if sys.platform == 'darwin':
        print("Note: On macOS, you may need to grant Accessibility permissions to your terminal.")
    
    app = KeyboardApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()

if __name__ == "__main__":
    main()
