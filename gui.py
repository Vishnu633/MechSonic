import customtkinter as ctk
import threading
import sys
import os
import shutil
import time
from tkinter import filedialog
from pynput import keyboard
from sound_manager import SoundManager

# Theme Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue") 

class KeyboardApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Mechsonic // CONTROL DECK")
        
        # Monochrome Luxury Palette
        self.color_bg = "#121212"       # Rich Black
        self.color_panel = "#1E1E1E"    # Dark Gray
        self.color_surface = "#2C2C2C"  # Medium Gray (Input fields)
        self.color_text_primary = "#FFFFFF" # Pure White
        self.color_text_secondary = "#A0A0A0" # Light Gray
        self.color_border = "#333333"   # Subtle Border
        self.color_active = "#FFFFFF"   # Active Element (White)
        self.color_active_hover = "#E0E0E0" # Off-White
        
        self.configure(fg_color=self.color_bg)

        # Initialize SoundManager
        try:
            self.sound_manager = SoundManager()
        except Exception as e:
            print(f"Error initializing SoundManager: {e}")
            self.destroy()
            return

        # System State
        self.system_active = True 
        self.listener = None

        self.create_widgets()
        
        # Position Window Top-Right
        self.update_idletasks() # Ensure geometry check is accurate
        width = 500
        height = 650
        screen_width = self.winfo_screenwidth()
        x = screen_width - width - 20 # 20px padding from right
        y = 40 # 40px padding from top (account for menu bar usually)
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)
        
        # Start persistent listener
        self.start_persistent_listener()
        self.update_ui_state()

    def create_widgets(self):
        # Header Section
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=(45, 25), padx=20, fill="x")
        
        self.label_title = ctk.CTkLabel(
            self.header_frame, 
            text="MECHSONIC", 
            font=("Roboto", 36, "bold"),
            text_color=self.color_text_primary
        )
        self.label_title.pack()

        self.label_tagline = ctk.CTkLabel(
            self.header_frame, 
            text="Mechanical sound, without the hardware.", 
            font=("Roboto", 14),
            text_color=self.color_text_secondary
        )
        self.label_tagline.pack(pady=(0, 10))
        
        self.label_subtitle = ctk.CTkLabel(
            self.header_frame, 
            text="SYSTEM ONLINE", 
            font=("Roboto Mono", 11), # Monospaced for technical feel
            text_color=self.color_text_primary
        )
        self.label_subtitle.pack(pady=(5, 0))

        # Main Control Panel
        self.panel = ctk.CTkFrame(self, fg_color=self.color_panel, corner_radius=12, border_width=1, border_color=self.color_border)
        self.panel.pack(pady=10, padx=30, fill="both", expand=True)

        # Visualizer (Signal Bar - Grayscale)
        self.visualizer_frame = ctk.CTkFrame(self.panel, fg_color=self.color_surface, height=60, corner_radius=8)
        self.visualizer_frame.pack(pady=(35, 25), padx=25, fill="x")
        
        self.visualizer_label = ctk.CTkLabel(self.visualizer_frame, text="INPUT SIGNAL", font=("Roboto Mono", 10), text_color=self.color_text_secondary)
        self.visualizer_label.place(relx=0.5, rely=0.25, anchor="center")

        self.visualizer_bar = ctk.CTkProgressBar(
            self.visualizer_frame, 
            height=6, 
            corner_radius=3,
            progress_color=self.color_active, # White bar
            fg_color="#404040" # Dark gray track
        )
        self.visualizer_bar.place(relx=0.5, rely=0.7, anchor="center", relwidth=0.9)
        self.visualizer_bar.set(0)

        # Sound Pack Selection
        self.label_pack = ctk.CTkLabel(self.panel, text="SOUND PROFILE", font=("Roboto", 11, "bold"), text_color=self.color_text_secondary)
        self.label_pack.pack(pady=(10, 5), anchor="w", padx=30)
        
        self.available_packs = self.sound_manager.get_available_packs()
        
        self.pack_var = ctk.StringVar(value=self.sound_manager.pack_name)
        self.option_pack = ctk.CTkOptionMenu(
            self.panel, 
            values=self.available_packs, 
            command=self.change_pack, 
            variable=self.pack_var,
            fg_color=self.color_surface,
            button_color="#404040", # Subtle button
            button_hover_color="#505050",
            text_color=self.color_text_primary,
            dropdown_fg_color=self.color_panel,
            dropdown_text_color=self.color_text_primary,
            dropdown_hover_color=self.color_surface,
            width=250,
            height=45,
            font=("Roboto", 14),
            corner_radius=8
        )
        self.option_pack.pack(pady=5, padx=30, fill="x")

        # Volume Control
        self.label_volume = ctk.CTkLabel(self.panel, text="VOLUME", font=("Roboto", 11, "bold"), text_color=self.color_text_secondary)
        self.label_volume.pack(pady=(25, 5), anchor="w", padx=30)
        
        self.slider_volume = ctk.CTkSlider(
            self.panel, 
            from_=0, 
            to=1, 
            command=self.change_volume,
            button_color=self.color_active,
            button_hover_color=self.color_active_hover,
            progress_color=self.color_active,
            fg_color="#404040"
        )
        self.slider_volume.set(1.0)
        self.slider_volume.pack(pady=5, padx=30, fill="x")

        # Spacer
        ctk.CTkLabel(self.panel, text="").pack(expand=True)

        # Footer Actions
        self.btn_toggle = ctk.CTkButton(
            self, 
            text="DEACTIVATE SYSTEM", 
            command=self.toggle_system, 
            fg_color="#2C2C2C", # Dark Gray button (Subtle)
            border_color="#555555",
            border_width=1,
            hover_color="#3C3C3C",
            font=("Roboto", 13, "bold"),
            height=50,
            corner_radius=25,
            text_color=self.color_text_primary # White
        )
        self.btn_toggle.pack(pady=(20, 10), padx=30, fill="x")
        
        # IMPROVED VISIBILITY for Add Pack (Round 2)
        self.btn_add_pack = ctk.CTkButton(
            self, 
            text="+ IMPORT SOUND PACK", 
            command=self.add_sound_pack,
            fg_color="#333333", # Specifically lighter gray
            text_color="#FFFFFF", # Bold White
            hover_color="#444444",
            font=("Roboto", 13, "bold"),
            height=45,
            corner_radius=22,
            border_width=2,
            border_color="#666666" # Very distinct border
        )
        self.btn_add_pack.pack(pady=(10, 30))

    def start_persistent_listener(self):
        try:
            self.listener = keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release
            )
            self.listener.start()
        except Exception as e:
            print(f"Error starting listener: {e}")

    def change_pack(self, choice):
        threading.Thread(target=self.sound_manager.set_pack, args=(choice,), daemon=True).start()
        self.after(50, lambda: self.flash_visualizer())

    def change_volume(self, value):
        self.sound_manager.set_volume(value)

    def toggle_system(self):
        self.system_active = not self.system_active
        self.update_ui_state()

    def update_ui_state(self):
        if self.system_active:
            self.btn_toggle.configure(text="DEACTIVATE SYSTEM", fg_color="#2C2C2C", text_color=self.color_text_primary)
            self.label_subtitle.configure(text="SYSTEM ONLINE", text_color=self.color_text_primary) # White
            # Enable visualizer
        else:
            self.btn_toggle.configure(text="ACTIVATE SYSTEM", fg_color="#121212", text_color=self.color_text_secondary, border_color="#333333")
            self.label_subtitle.configure(text="SYSTEM IDLE", text_color=self.color_text_secondary) # Gray
            self.visualizer_bar.set(0)

    def on_press(self, key):
        if self.system_active:
            try:
                self.sound_manager.play_sound(key, 'press')
                self.after(0, self.flash_visualizer)
            except Exception as e:
                print(f"Error: {e}")

    def on_release(self, key):
        if self.system_active:
            try:
                self.sound_manager.play_sound(key, 'release')
            except Exception as e:
                print(f"Error: {e}")

    def flash_visualizer(self):
        if not self.system_active:
            return
        self.visualizer_bar.set(1.0)
        self.visualizer_bar.configure(progress_color=self.color_active)
        self.after(50, lambda: self.visualizer_bar.set(0.1))

    def add_sound_pack(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            pack_name = os.path.basename(folder_selected)
            target_dir = os.path.join(os.path.dirname(__file__), 'sounds', pack_name)
            
            if os.path.exists(target_dir):
                print("Pack already exists!")
                return
                
            try:
                shutil.copytree(folder_selected, target_dir)
                print(f"Added pack: {pack_name}")
                self.available_packs = self.sound_manager.get_available_packs()
                self.option_pack.configure(values=self.available_packs)
                self.pack_var.set(pack_name)
                threading.Thread(target=self.sound_manager.set_pack, args=(pack_name,), daemon=True).start()
            except Exception as e:
                print(f"Error adding pack: {e}")

    def on_closing(self):
        if self.listener:
            self.listener.stop()
        self.destroy()
        sys.exit(0)

if __name__ == "__main__":
    app = KeyboardApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
