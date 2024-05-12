import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar
from tkinter.ttk import Style
from PIL import Image, ImageTk
import os
import pygame
import threading
import time

pygame.mixer.init()

current = 0
paused = False
folder = ""

def update_progress():
    global current, paused
    while True:
        if pygame.mixer.music.get_busy() and not paused:
            current = pygame.mixer.music.get_pos() / 1000
            pbar["value"] = current
            
            if current >= pbar["maximum"]:
                stop_music()
                pbar["value"] = 0
            
            window.update()
        time.sleep(0.1)

pt = threading.Thread(target=update_progress)
pt.daemon = True
pt.start()

def select_folder():
    global folder
    folder = filedialog.askdirectory()
    if folder:
        lbox.delete(0, tk.END)
        for filename in os.listdir(folder):
            if filename.endswith(".mp3"):
                lbox.insert(tk.END, filename)

def pre_btn():
    if len(lbox.curselection()) > 0:
        index = lbox.curselection()[0]
        if index > 0:
            lbox.selection_clear(0, tk.END)
            lbox.selection_set(index - 1)
            play_select()

def next_btn():
    if len(lbox.curselection()) > 0:
        index = lbox.curselection()[0]
        if index < lbox.size() - 1:
            lbox.selection_clear(0, tk.END)
            lbox.selection_set(index + 1)
            play_select()

def play_btn():
    global paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        play_select()

def play_select():
    global current, paused
    if len(lbox.curselection()) > 0:
        index = lbox.curselection()[0]
        select_song = lbox.get(index)
        fullpath = os.path.join(folder, select_song)
        pygame.mixer.music.load(fullpath)
        pygame.mixer.music.play(start=current)
        paused = False
        audio = MP3(fullpath)  
        song_duration = audio.info.length
        pbar["maximum"] = song_duration

def pause_btn():
    global paused
    pygame.mixer.music.pause()
    paused = True

def stop_music():
    global paused
    pygame.mixer.music.stop()
    paused = False

window = tk.Tk()
window.title("MUSIC PLAYER APP")
window.geometry("800x600")
window.configure(bg="lightPink")

# Function for resizing images
def resize_image(image_path, width, height):
    img = Image.open(image_path)
    img = img.resize((width, height), Image.LANCZOS)
    return ImageTk.PhotoImage(img)

# Load and resize the logo image
logo_img = resize_image("logo.jpg", 200, 200)
logo_label = tk.Label(window, image=logo_img)
logo_label.pack(pady=20)

# Heading Label
heading_label = tk.Label(window, text="MELODIC", font=("Helvetica", 30))
heading_label.pack()

# Select Folder Button
selectbtn = tk.Button(window, text="SELECT MUSIC FOLDER", command=select_folder, font=("Helvetica", 14), bg="black", fg="white")
selectbtn.pack(pady=20)

# Listbox for Songs
lbox = tk.Listbox(window, width=50, height=10, font=("Helvetica", 12) , bg="grey")
lbox.pack(pady=10)

# Buttons Frame
btn_frame = tk.Frame(window)
btn_frame.pack(pady=20)

# Load and resize button images
play_img = resize_image("play.png", 50, 50)
pause_img = resize_image("pause.png", 50, 50)
pre_img = resize_image("previous.png", 50, 50)
next_img = resize_image("next.png", 50, 50)

# Previous Button
pre = tk.Button(btn_frame, image=pre_img, command=pre_btn, bd=0)
pre.grid(row=0, column=0, padx=10)

# Play Button
play = tk.Button(btn_frame, image=play_img, command=play_btn, bd=0)
play.grid(row=0, column=1, padx=10)

# Pause Button
pause = tk.Button(btn_frame, image=pause_img, command=pause_btn, bd=0)
pause.grid(row=0, column=2, padx=10)

# Next Button
next = tk.Button(btn_frame, image=next_img, command=next_btn, bd=0)
next.grid(row=0, column=3, padx=10)

# Progress Bar
style = Style()
style.theme_use('default')
style.configure("Custom.Horizontal.TProgressbar", background='lightBlue', troughcolor='white', bordercolor='white', lightcolor='lightBlue', darkcolor='lightBlue')
style.map("Custom.Horizontal.TProgressbar",
            background=[('active', 'green'), ('!active', 'pink')])

# Progress Bar
pbar = Progressbar(window, length=600, mode="determinate", style="Custom.Horizontal.TProgressbar")
pbar.pack(pady=10)

window.mainloop()
