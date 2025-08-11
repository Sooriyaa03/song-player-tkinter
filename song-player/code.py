import tkinter as tk
from tkinter import ttk
import pafy
import _thread
from time import sleep
from youtubesearchpython import VideosSearch
import vlc
from sys import exit
import pickle
import os
import random

# thread function
def check_state():
    while True:
        if player.get_state() ==  vlc.State.Ended or player.get_state() == vlc.State.NothingSpecial:
            vlc_state()

        sleep(0.5)

        if play_bool:
            set_duration_value()


def shuffle_play_function():
    if output.size() != 0:
        random_song_index = random.randrange(len(playlst))
        random_song = playlst.get(list(playlst.keys())[random_song_index])
        output.selection_clear(0,tk.END)
        output.selection_set(random_song_index)
        random_song = 'storage\\'+random_song
        playf(random_song)

def order_play_function():
    current_song = output.curselection()
    if current_song != ():
        if player.get_state() ==  vlc.State.Ended:
            if current_song[0]+1 != output.size():
                next_song = current_song[0]+1
            else:
                next_song = 0
            output.selection_clear(0,tk.END)
            output.selection_set(next_song)
            order_song = playlst.get(output.get(output.curselection()))
            order_song = 'storage\\'+order_song
            playf(order_song)

def after_song():
    stopf()
    if not pause_resume_bool:
        pause_resume()
    current_song = output.curselection()
    if current_song != ():
        if player.get_state() ==  vlc.State.Stopped:
            if current_song[0]+1 != output.size():
                after_song = current_song[0]+1
            else:
                after_song = 0
            output.selection_clear(0,tk.END)
            output.selection_set(after_song)
            order_song = playlst.get(output.get(output.curselection()))
            order_song = 'storage\\'+order_song
            playf(order_song)

def before_song():
    stopf()
    if not pause_resume_bool:
        pause_resume()
    current_song = output.curselection()
    if current_song != ():
        if player.get_state() ==  vlc.State.Stopped:
            if current_song[0] != 0:
                prev_song = current_song[0] - 1
            else:
                prev_song = output.size()-1
            output.selection_clear(0,tk.END)
            output.selection_set(prev_song)
            order_song = playlst.get(output.get(output.curselection()))
            order_song = 'storage\\'+order_song
            playf(order_song)

def click_play(event = None):
    if player.get_state() ==  vlc.State.Playing:
        stopf()
    if not pause_resume_bool:
        pause_resume()
    try:
        click_song = playlst.get(output.get(output.curselection()))
        click_song = 'storage\\'+click_song
        playf(click_song)
    except:
        pass


def vlc_state():
    if shuffle_play:
        shuffle_play_function()
    else:
        order_play_function()

play_bool = False
def playf(a):
    global play_bool
    play_bool = False
    global total_duration
    media = instance.media_new(a)
    player.set_media(media)
    player.play()
    sleep(0.1)
    total_duration = player.get_length()
    sleep(0.1)
    play_bool = True

def pausef():
    player.set_pause(1)

def resumef():
    player.set_pause(0)

def stopf():
    player.stop()


def write_lst(obj):
    os.chdir(path)
    with open(r'storage\file.playlist', 'wb') as f:
        pickle.dump(obj,f)

x = 10
y = 10

root = tk.Tk()
root.title('Console')
root.resizable(False, False)
root.geometry('800x500+{}+{}'.format(x,y))
root.configure(bg='#303841')
root.overrideredirect(True)

minimize_bool = False
def minimize():
    global minimize_bool
    if minimize_bool:
        root.geometry('800x500+{}+{}'.format(x,y))
        minimize_bool = False
    else:
        root.geometry('800x25+{}+{}'.format(x,y))
        minimize_bool = True

def get_input(event = None):
    success = True
    value = cmd_line.get()
    cmd_line.delete(0,tk.END)
    if (value.replace(' ','')).isalpha():
        value = value.capitalize()
        if value not in playlst:
            videosSearch = VideosSearch((value + ' song'), limit = 1)
            video_result = videosSearch.result()
            video_link = video_result.get('result')[0].get('link')
            os.chdir(path)
            os.chdir('storage\\')
            
            try:
                video = pafy.new(video_link)
                best = video.getbestaudio()
                best.download()
            except:
                success = False

            os.chdir(path)
            if success:
                video_title = video.title
        
                for i in range(len(video_title)):
        
                    if video_title[i] in ['/','\\','*','?','<','>','"',':','|']:
                        video_title = video_title[:i]+'_'+video_title[i+1:]
        
                lst = os.listdir('storage\\')
                
                for name in lst:
                    if video_title in name:
                        playlst[value] = name
                        write_lst(playlst)
                        output.insert(tk.END,value)
            else:
                pass

def song_bin():

    os.chdir(path)
    try:
        value = output.get(output.curselection())
        key_lst = []
        file_name = playlst.get(value)
        for i in list(playlst.keys()):
            if playlst.get(i) == file_name:
                key_lst.append(i)
        stopf()
        os.remove('storage\\'+file_name)
        after_song()
        for l in key_lst:
            playlst.pop(l)
            output.delete(output.get(0, tk.END).index(l))
        write_lst(playlst)
    except:
        pass




pause_resume_bool = True
def pause_resume():
    global pause_resume_bool
    if pause_resume_bool:
        button4.configure(image = resume)
        pausef()
        pause_resume_bool = False
    else:
        button4.configure(image = pause)
        resumef()
        pause_resume_bool = True

def close_program():
    exit()

volume_value = tk.IntVar()
def slider_changed(event):
    player.audio_set_volume(volume_value.get())

shuffle_play = False
def shuffle():
    global shuffle_play
    if shuffle_play:
        button8.configure(image = shuffle_off)
        shuffle_play = False
    else:
        button8.configure(image = shuffle_on)
        shuffle_play = True

duration_value = tk.IntVar()
def change_duration(event):
    try:
        player.set_time(int(duration_value.get()*total_duration/100))
    except:
        pass

current_duration = 0
def set_duration_value():
    try:
        current_duration = player.get_time()
        duration_value.set(current_duration/total_duration*100)
        string_total_duration = str(total_duration/1000/60)
        string_current_duration = str(current_duration/1000/60)
        t_dot = string_total_duration.find('.')
        c_dot = string_current_duration.find('.')
        duration_display.configure(text = string_current_duration[:c_dot]+string_current_duration[c_dot:c_dot+3]+' / '+string_total_duration[:t_dot]+string_total_duration[t_dot:t_dot+3])
    except:
        pass

def move_window(event):
    global x
    global y
    root.geometry('+{}+{}'.format(event.x_root-35, event.y_root-15))
    x = event.x_root-35
    y = event.y_root-15

style = ttk.Style()
style.configure('myStyle.Horizontal.TScale', background='#2a2a2a')

style2 = ttk.Style()
style2.configure('myStyle2.Horizontal.TScale', background='#2a2a2a')

instance = vlc.Instance()
instance.log_unset()
player = instance.media_player_new()

path = os.getcwd()

red_circle = tk.PhotoImage(file = 'files/red_circle.png')
yellow_circle = tk.PhotoImage(file = 'files/yellow_circle.png')
green_circle = tk.PhotoImage(file = 'files/green_circle.png') 
pause = tk.PhotoImage(file = 'files/pause.png')
resume = tk.PhotoImage(file = 'files/resume.png')
change = tk.PhotoImage(file = 'files/next.png')
prev = tk.PhotoImage(file = 'files/prev.png')
bin_ = tk.PhotoImage(file = 'files/bin.png')
shuffle_off = tk.PhotoImage(file = 'files/shuffle_off.png')
shuffle_on = tk.PhotoImage(file = 'files/shuffle_on.png')


output_frame = tk.Frame(root, bg='#2e3238')
output_frame.place(x = 20, y = 50, height= 380, width= 755)

output = tk.Listbox(output_frame, bg = '#303841', bd = 1, fg = 'gray', font = 'ariel', activestyle = 'none')
output.place(x = -1, y = -1, height= 383, width= 758)

top_frame = tk.Frame(root, bg='#2a2a2a')
top_frame.place(height=25, width=800)

button1 = tk.Button(top_frame, command = close_program, bg='#2a2a2a', image = red_circle, borderwidth = 0)
button1.pack(side = tk.LEFT, padx = 2, pady = 3)

button2 = tk.Button(top_frame, bg='#2a2a2a', image = yellow_circle, borderwidth = 0)
button2.bind('<B1-Motion>', move_window)
button2.pack(side = tk.LEFT, padx = 2, pady = 3)

button3 = tk.Button(top_frame, command = minimize, bg='#2a2a2a', image = green_circle, borderwidth = 0)
button3.pack(side = tk.LEFT, padx = 2, pady = 3)

button4 = tk.Button(top_frame, command = pause_resume, bg='#2a2a2a', image = pause, borderwidth = 0)
button4.pack(side = tk.RIGHT, padx = 4, pady = 3)

button5 = tk.Button(top_frame, command = after_song, bg = '#2a2a2a', image = change, borderwidth = 0)
button5.pack(side = tk.RIGHT, padx = 8, pady = 3)

button6 = tk.Button(top_frame, command = before_song, bg = '#2a2a2a', image = prev, borderwidth = 0)
button6.pack(side = tk.RIGHT, padx = 8, pady = 3)

slider = ttk.Scale(top_frame,from_=0,to=100,orient='horizontal',command=slider_changed,variable=volume_value, style = 'myStyle.Horizontal.TScale',length =70)
slider.pack(side = tk.RIGHT, padx = 8, pady = 3)

button7 = tk.Button(top_frame, command = song_bin, bg = '#2a2a2a', image = bin_, borderwidth = 0)
button7.pack(side = tk.RIGHT, padx = 8, pady = 3)

button8 = tk.Button(top_frame, command = shuffle,bg = '#2a2a2a', image = shuffle_off, borderwidth = 0)
button8.pack(side = tk.RIGHT, padx = 8, pady = 3)

inside_top_frame = tk.Frame(top_frame, bg='#2a2a2a', height = 25, width = 445)
inside_top_frame.pack(side = tk.RIGHT, padx = 8, pady = 3)

duration_display = tk.Label(inside_top_frame,text = "00.00 / 00.00", bg = '#2a2a2a', fg = 'white')
duration_display.pack(side = tk.LEFT, padx = 5)

druation_slider = ttk.Scale(inside_top_frame,from_=0,to=100,orient='horizontal',command=change_duration,variable=duration_value, style = 'myStyle2.Horizontal.TScale', length = 400)
druation_slider.pack(side = tk.LEFT)


cmd_frame = tk.Frame(root, bg='#2a2a2a')
cmd_frame.place(x = 20, y = 450, height=25, width=755)

cmd_line = tk.Entry(cmd_frame, bg = '#2e3238', fg = 'white')
cmd_line.place(x = -1, y = -1, height=29, width=758)

cmd_line.focus_set()

root.bind('<Return>', get_input)
output.bind("<<ListboxSelect>>", click_play)

player.audio_set_volume(0)

try:
    os.chdir('storage\\')
    os.chdir(path)
except:
    os.mkdir('storage')

try:
    with open(r'storage\file.playlist', 'rb') as f:
        playlst = pickle.load(f)
        for song_name in playlst:
            output.insert(tk.END,song_name)

except:
    playlst = dict()
    write_lst(playlst)

_thread.start_new_thread(check_state,())


root.mainloop()
