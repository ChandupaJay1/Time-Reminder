import tkinter as tk
from tkinter import ttk
from datetime import datetime
import threading
import time
import pygame  # type: ignore
import sys
import csv
import os

pygame.init()
pygame.mixer.init()

reminders = []
csv_file = "reminders.csv"

if not os.path.exists(csv_file):
    print("❌ reminders.csv not found. Please create it in the same folder.")
    sys.exit(1)

def parse_time_string(time_str):
    try:
        if len(time_str.strip().split(":")) == 2:
            return datetime.strptime(time_str.strip(), "%H:%M").time()
        elif len(time_str.strip().split(":")) == 3:
            return datetime.strptime(time_str.strip(), "%H:%M:%S").time()
        else:
            raise ValueError("Invalid time format")
    except Exception as e:
        print(f"Error parsing time '{time_str}': {e}")
        return None

with open(csv_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        time_obj = parse_time_string(row["time"])
        if time_obj:
            row["time_obj"] = time_obj
            reminders.append(row)

if not reminders:
    print("❌ No valid reminders found in CSV.")
    sys.exit(1)

played = set()

def play_sound(file_path, is_playlist=False, playlist_files=None, app_instance=None):
    """Play sound with playlist support for continuous playback"""
    try:

        if not os.path.exists(file_path):
            print(f"❌ Sound file not found: {file_path}")
            return
            
        print(f"🔊 Attempting to play: {file_path}")
        
        if is_playlist and playlist_files:
            play_playlist(playlist_files, app_instance)
            return
        
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            
            timeout = 300 
            start_time = time.time()
            while pygame.mixer.music.get_busy():
                if time.time() - start_time > timeout:
                    pygame.mixer.music.stop()
                    break
                time.sleep(0.1)
            print("✅ Sound played successfully with pygame.mixer.music")
            return
        except Exception as e:
            print(f"❌ pygame.mixer.music failed: {e}")
        
        
        try:
            sound_obj = pygame.mixer.Sound(file_path)
            sound_obj.play()
            
            while pygame.mixer.get_busy():
                time.sleep(0.1)
            print("✅ Sound played successfully with pygame.mixer.Sound")
            return
        except Exception as e:
            print(f"❌ pygame.mixer.Sound failed: {e}")
        
        
        try:
            import platform
            system = platform.system()
            if system == "Windows":
                import winsound
                winsound.PlaySound(file_path, winsound.SND_FILENAME)
                print("✅ Sound played successfully with winsound")
            elif system == "Darwin":  # macOS
                os.system(f"afplay '{file_path}'")
                print("✅ Sound played successfully with afplay")
            elif system == "Linux":
                os.system(f"aplay '{file_path}' 2>/dev/null || paplay '{file_path}' 2>/dev/null")
                print("✅ Sound played successfully with system command")
        except Exception as e:
            print(f"❌ System command fallback failed: {e}")
            
    except Exception as e:
        print(f"❌ All sound playing methods failed: {e}")

def play_playlist(playlist_files, app_instance=None):
    """Play a playlist of audio files continuously"""
    try:
        print(f"🎵 Starting playlist with {len(playlist_files)} tracks")
        if app_instance:
            app_instance.log_message(f"Starting playlist: {len(playlist_files)} tracks (31:45 duration)")
        
        for i, file_path in enumerate(playlist_files, 1):
            if not os.path.exists(file_path):
                print(f"❌ Playlist file not found: {file_path}")
                if app_instance:
                    app_instance.log_message(f"Track {i} not found: {file_path}")
                continue
                
            print(f"🎵 Playing track {i}/{len(playlist_files)}: {file_path}")
            if app_instance:
                app_instance.log_message(f"Playing track {i}/{len(playlist_files)}: {os.path.basename(file_path)}")
            
            try:
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                
                
                timeout = 600
                start_time = time.time()
                while pygame.mixer.music.get_busy():
                    if time.time() - start_time > timeout:
                        pygame.mixer.music.stop()
                        break
                    time.sleep(0.1)
                    
            except Exception as e:
                print(f"❌ Error playing track {i}: {e}")
                if app_instance:
                    app_instance.log_message(f"Error playing track {i}: {e}")
        
        print("✅ Playlist completed")
        if app_instance:
            app_instance.log_message("Playlist completed successfully")
            
    except Exception as e:
        print(f"❌ Playlist playback failed: {e}")
        if app_instance:
            app_instance.log_message(f"Playlist error: {e}")

class ModernReminder:
    def __init__(self):
        self.app = tk.Tk()
        self.app.iconbitmap("app_icon.ico")
        self.is_running = False
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        self.app.title("Time Reminder")
        
        window_width = 700
        window_height = 600
        
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()
        
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        
        self.app.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.app.configure(bg="#0f0f23")
        self.app.resizable(False, False)
        
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Modern.TFrame', background='#0f0f23')
        style.configure('Card.TFrame', background='#1a1a2e', relief='flat')
        
    def create_widgets(self):
        main_container = tk.Frame(self.app, bg="#0f0f23")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.create_header(main_container)
        
        self.create_clock_section(main_container)
        
        self.create_status_section(main_container)
        
        self.create_control_section(main_container)
        
        self.create_reminders_section(main_container)
        
        self.create_log_section(main_container)
        
    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg="#0f0f23")
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_label = tk.Label(header_frame, text="Time Reminder DR Fashion Factory", 
                              font=("Segoe UI", 28, "bold"),
                              fg="#ffffff", bg="#0f0f23")
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame, text="Stay on track with smart notifications", 
                                 font=("Segoe UI", 12),
                                 fg="#8892b0", bg="#0f0f23")
        subtitle_label.pack(pady=(5, 0))
        
    def create_clock_section(self, parent):
        clock_card = tk.Frame(parent, bg="#1a1a2e", relief="flat", bd=0)
        clock_card.pack(fill="x", pady=(0, 15))
        
        border_frame = tk.Frame(clock_card, bg="#64ffda", height=2)
        border_frame.pack(fill="x")
        
        clock_content = tk.Frame(clock_card, bg="#1a1a2e")
        clock_content.pack(fill="x", padx=30, pady=20)
        
        clock_title = tk.Label(clock_content, text="Current Time", 
                              font=("Segoe UI", 14, "bold"),
                              fg="#64ffda", bg="#1a1a2e")
        clock_title.pack()
        
        self.clock_label = tk.Label(clock_content, text="", 
                                   font=("JetBrains Mono", 32, "bold"),
                                   fg="#ffffff", bg="#1a1a2e")
        self.clock_label.pack(pady=(10, 0))
        
    def create_status_section(self, parent):
        status_card = tk.Frame(parent, bg="#1a1a2e", relief="flat", bd=0)
        status_card.pack(fill="x", pady=(0, 15))
        
        status_content = tk.Frame(status_card, bg="#1a1a2e")
        status_content.pack(fill="x", padx=30, pady=20)
        
        status_title = tk.Label(status_content, text="Status", 
                               font=("Segoe UI", 14, "bold"),
                               fg="#ff6b6b", bg="#1a1a2e")
        status_title.pack(anchor="w")
        
        self.status_label = tk.Label(status_content, text="● Ready to start", 
                                    font=("Segoe UI", 12),
                                    fg="#8892b0", bg="#1a1a2e")
        self.status_label.pack(anchor="w", pady=(5, 0))
        
    def create_control_section(self, parent):
        control_frame = tk.Frame(parent, bg="#0f0f23")
        control_frame.pack(fill="x", pady=(0, 20))
        
        self.start_btn = tk.Button(control_frame, text="▶  Start Monitoring", 
                                  font=("Segoe UI", 14, "bold"),
                                  bg="#64ffda", fg="#0f0f23",
                                  activebackground="#4fd3a7",
                                  relief="flat", bd=0,
                                  padx=40, pady=12,
                                  cursor="hand2",
                                  command=self.toggle_reminder)
        self.start_btn.pack()
        
        self.start_btn.bind("<Enter>", lambda e: self.start_btn.config(bg="#4fd3a7"))
        self.start_btn.bind("<Leave>", lambda e: self.start_btn.config(bg="#64ffda"))
        
    def create_reminders_section(self, parent):
        reminders_card = tk.Frame(parent, bg="#1a1a2e", relief="flat", bd=0)
        reminders_card.pack(fill="both", expand=True, pady=(0, 15))
        
        reminders_content = tk.Frame(reminders_card, bg="#1a1a2e")
        reminders_content.pack(fill="both", expand=True, padx=20, pady=15)
        
        reminders_title = tk.Label(reminders_content, text=f"Upcoming Reminders ({len(reminders)} total)", 
                                  font=("Segoe UI", 14, "bold"),
                                  fg="#ffd93d", bg="#1a1a2e")
        reminders_title.pack(anchor="w", pady=(0, 10))
        
        reminders_container = tk.Frame(reminders_content, bg="#1a1a2e")
        reminders_container.pack(fill="both", expand=True)
        
        if reminders:
            for i, reminder in enumerate(reminders):
                reminder_item = tk.Frame(reminders_container, bg="#16213e", relief="flat", bd=1)
                reminder_item.pack(fill="x", pady=2, padx=5)
                
                time_label = tk.Label(reminder_item, text=reminder.get("time", "N/A"), 
                                     font=("JetBrains Mono", 11, "bold"),
                                     fg="#64ffda", bg="#16213e")
                time_label.pack(side="left", padx=15, pady=8)
                
                name_label = tk.Label(reminder_item, text=reminder.get("name", "Unknown"), 
                                     font=("Segoe UI", 11),
                                     fg="#ffffff", bg="#16213e")
                name_label.pack(side="left", padx=(10, 0), pady=8)
                
                sound_indicator = tk.Label(reminder_item, text="🔊", 
                                         font=("Segoe UI", 10),
                                         fg="#8892b0", bg="#16213e")
                sound_indicator.pack(side="right", padx=5, pady=8)
                
                is_played = reminder.get("time", "") in played
                status_dot = tk.Label(reminder_item, text="●", 
                                     font=("Segoe UI", 12),
                                     fg="#64ffda" if is_played else "#8892b0", 
                                     bg="#16213e")
                status_dot.pack(side="right", padx=10, pady=8)
        else:

            no_reminders_label = tk.Label(reminders_container, 
                                         text="No reminders loaded from CSV file", 
                                         font=("Segoe UI", 12),
                                         fg="#ff6b6b", bg="#1a1a2e")
            no_reminders_label.pack(pady=20)
        
    def create_log_section(self, parent):
        log_card = tk.Frame(parent, bg="#1a1a2e", relief="flat", bd=0)
        log_card.pack(fill="x")
        
        log_content = tk.Frame(log_card, bg="#1a1a2e")
        log_content.pack(fill="x", padx=20, pady=15)
        
        log_title = tk.Label(log_content, text="Activity Log", 
                            font=("Segoe UI", 14, "bold"),
                            fg="#ff6b6b", bg="#1a1a2e")
        log_title.pack(anchor="w", pady=(0, 10))
        
        log_frame = tk.Frame(log_content, bg="#0f0f23", relief="flat", bd=1)
        log_frame.pack(fill="x")
        
        self.log_text = tk.Text(log_frame, height=6, 
                               font=("JetBrains Mono", 10),
                               bg="#0f0f23", fg="#8892b0",
                               relief="flat", bd=0,
                               wrap="word",
                               insertbackground="#64ffda")
        self.log_text.pack(fill="x", padx=10, pady=10)
        self.log_text.insert("1.0", f"● System initialized\n● Loaded {len(reminders)} reminders from CSV\n● Waiting for start command...\n")
        if reminders:
            for reminder in reminders[:3]: 
                self.log_text.insert("end", f"● Found: {reminder.get('time', 'N/A')} - {reminder.get('name', 'Unknown')}\n")
        self.log_text.config(state="disabled")
        
    def log_message(self, message):
        self.log_text.config(state="normal")
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"● [{timestamp}] {message}\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")
        
    def toggle_reminder(self):
        if not self.is_running:
            self.start_reminders()
        else:
            self.stop_reminders()
            
    def start_reminders(self):
        self.is_running = True
        self.start_btn.config(text="⏸  Stop Monitoring", bg="#ff6b6b", activebackground="#ff5252")
        self.start_btn.bind("<Enter>", lambda e: self.start_btn.config(bg="#ff5252"))
        self.start_btn.bind("<Leave>", lambda e: self.start_btn.config(bg="#ff6b6b"))
        
        self.status_label.config(text="● Monitoring active", fg="#64ffda")
        self.log_message("Reminder monitoring started")
        
        threading.Thread(target=self.reminder_loop, daemon=True).start()
        
    def stop_reminders(self):
        self.is_running = False
        self.start_btn.config(text="▶  Start Monitoring", bg="#64ffda", activebackground="#4fd3a7")
        self.start_btn.bind("<Enter>", lambda e: self.start_btn.config(bg="#4fd3a7"))
        self.start_btn.bind("<Leave>", lambda e: self.start_btn.config(bg="#64ffda"))
        
        self.status_label.config(text="● Monitoring stopped", fg="#ff6b6b")
        self.log_message("Reminder monitoring stopped")
        
    def reminder_loop(self):
        global played
        
        while self.is_running:
            now_str = datetime.now().strftime("%H:%M:%S")
            
            for reminder in reminders:
                reminder_time_str = reminder["time_obj"].strftime("%H:%M:%S")
                if reminder_time_str == now_str and reminder["time"] not in played:
                    self.status_label.config(text=f"🔔 {reminder['name']} - ACTIVE!", fg="#ffd93d")
                    self.log_message(f"Reminder triggered: {reminder['name']} at {reminder['time']}")

                    sound_file = reminder.get("sound", "")
                    
                    if "Karaniya Meththa Suthraya" in reminder.get('name', ''):
                        self.log_message("Starting 31:45 minute playlist after Karaniya Meththa Suthraya")
                        playlist_files = [
                            "karaneeya-meththa-suthraya.mp3",
                            "jaya-piritha-pirith.mp3",  
                            "mora-piritha-pirith.mp3",
                            "surya-piritha-sinhala-pirith.mp3",
                            "dasa-disa-piritha-pirith.mp3",
                            "rathnamali-gatha-rathnaya-pirith.mp3",
                            "dutugemunu-arakshaka-gatha-pirith.mp3"
                        ]

                        threading.Thread(target=play_sound, 
                                       args=(sound_file, True, playlist_files, self), 
                                       daemon=True).start()
                    elif sound_file:
                        self.log_message(f"Playing sound: {sound_file}")

                        threading.Thread(target=play_sound, args=(sound_file,), daemon=True).start()
                    else:
                        self.log_message("No sound file specified for this reminder")
                    
                    played.add(reminder["time"])
                    

                    self.refresh_reminders_display()
                    
                    self.app.after(5000, lambda: self.status_label.config(text="● Monitoring active", fg="#64ffda"))
            
            time.sleep(1)
    
    def refresh_reminders_display(self):
        pass
            
    def update_clock(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=now)
        self.app.after(1000, self.update_clock)
        
    def run(self):
        self.update_clock()
        self.app.mainloop()

def main():
    app = ModernReminder()
    app.run()

if __name__ == "__main__":
    main()