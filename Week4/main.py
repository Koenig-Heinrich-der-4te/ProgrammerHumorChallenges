import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from io import BytesIO
import requests
from yt import load_json, extract_details, extract_sources
import os
import random

def get_link_details():
    global img, description_visible, videos, audios, video_names, audio_names
    link = link_entry.get()
    if random.randint(1, 20) == 1:
        link = "https://youtu.be/dQw4w9WgXcQ"
    try:
        data, jsurl = load_json(link)
        details = extract_details(data)
        
        title = details["title"]
        description = details["description"]
        thumbnail = details["thumbnail"]
        
        title_label.config(text=title)
        description_toggle.grid()
        description_label.config(text=description)
        description_label.grid_remove()
        description_visible = False
        
        
        response = requests.get(thumbnail)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = ImageTk.PhotoImage(img.resize((img.width * 128 // img.height, 128)))
        thumbnail_label.config(image=img)

        videos, audios = extract_sources(data, jsurl)
        video_names = [video["name"] for video in videos]
        audio_names = [audio["name"] for audio in audios]

        video_option_var.set(video_names[0])
        video_dropdown.config(textvariable=video_option_var, values=video_names, state="readonly")
        video_audio_option_var.set("None")
        video_audio_dropdown.config(textvariable=video_audio_option_var, values=audio_names+["None"], state="readonly")
        audio_option_var.set(audio_names[0])
        audio_dropdown.config(textvariable=audio_option_var, values=audio_names, state="readonly")

        download_options.grid() #ungrid it before



    except requests.exceptions.MissingSchema:
        title_label.config(text="Invalid Link! Can't your stupid ass paste an actual link?")
        description_label.config(text="")
        thumbnail_label.config(text="")
        description_toggle.grid_remove()
        download_options.grid_remove()
    except Exception as e:
        title_label.config(text="Error Occurred! Maybe you should try entering an actually good youtube video")
        description_label.config(text="")
        thumbnail_label.config(text="")
        description_toggle.grid_remove()
        download_options.grid_remove()
        print(e)

description_visible = True
def toggle_description():
    global description_visible
    if description_visible:
        description_label.grid_remove()
        description_toggle.config(text="Show Description")
    else: 
        description_label.grid()
        description_toggle.config(text="Hide Description")
    description_visible = not description_visible

def download_video():
    source = videos[video_names.index(video_option_var.get())]
    additional_source_name = video_audio_option_var.get()
    if additional_source_name != "None":
        additional_source = audios[audio_names.index(additional_source_name)]
        additional_source_input = f"-i \"{additional_source['url']}\""
    else:
        additional_source = None
        additional_source_input = ""
    ffmpeg_options = video_ffmpeg_options_entry.get()
    filename = video_filename_entry.get()
    codec_option = "-c copy" if filename.endswith(source["format"]) and (additional_source is None or filename.endswith(additional_source["format"])) and len(ffmpeg_options) == 0 else ""
    start_option = f"-ss {video_clip_start_entry.get()}" if len(video_clip_start_entry.get()) > 0 else ""
    end_option = f"-to {video_clip_end_entry.get()}" if len(video_clip_end_entry.get()) > 0 else ""
    command = f"ffmpeg -y -i \"{source['url']}\" {additional_source_input} {start_option} {end_option} {codec_option} {ffmpeg_options} \"{filename}\""
    print(command)
    result = os.system(command)
    if result == 0:
        print("success")
    else:
        print("Failed to download")
# code duplication go brr
def download_audio():
    source = audios[audio_names.index(audio_option_var.get())]
    
    ffmpeg_options = audio_ffmpeg_options_entry.get()
    filename = audio_filename_entry.get()
    codec_option = "-c copy" if filename.endswith(source["format"]) and len(ffmpeg_options) == 0 else ""
    start_option = f"-ss {audio_clip_start_entry.get()}" if len(audio_clip_start_entry.get()) > 0 else ""
    end_option = f"-to {audio_clip_end_entry.get()}" if len(audio_clip_end_entry.get()) > 0 else ""
    command = f"ffmpeg -y -i \"{source['url']}\" {start_option} {end_option} {codec_option} {ffmpeg_options} \"{filename}\""
    print(command)
    result = os.system(command)
    if result == 0:
        print("success")
    else:
        print("Failed to download")




# Create the main application window
root = tk.Tk()
root.title("FFmpeg Youtube Downloader")
root.iconphoto(False, ImageTk.PhotoImage(Image.open(BytesIO(requests.get("https://www.youtube.com/s/desktop/51e20ad6/img/favicon_144x144.png").content))))

# Create and place widgets
# Why is ui always pain?
link_label = ttk.Label(root, text="Enter YT Link:")
link_label.grid(row=0, column=0, pady=10)

link_entry = ttk.Entry(root, width=50)
link_entry.grid(row=1, column=0, pady=5)

fetch_button = ttk.Button(root, text="Load", command=get_link_details)
fetch_button.grid(row=2, column=0, pady=10)

title_label = ttk.Label(root)
title_label.grid(row=3, column=0)

thumbnail_label = ttk.Label(root)
thumbnail_label.grid(row=4, column=0)

# download
download_options = ttk.Notebook(root)
download_options.grid(row=5, column=0)

# video
video_tab = ttk.Frame(download_options)
download_options.add(video_tab, text="Video")
video_option_var = tk.StringVar()
video_dropdown = ttk.Combobox(video_tab, state="readonly", width=64)
video_dropdown.grid(row=0, column=0)

video_audio_option_var = tk.StringVar()
video_audio_dropdown = ttk.Combobox(video_tab, state="readonly", width=64)
video_audio_dropdown.grid(row=1, column=0)

video_filename = ttk.Frame(video_tab)
video_filename.grid(row=2, column=0, pady=5, sticky=tk.W)
video_filename_prompt = ttk.Label(video_filename, text="Enter filename:")
video_filename_prompt.pack(side=tk.LEFT)
video_filename_entry = ttk.Entry(video_filename, width=48)
video_filename_entry.insert(0, "video.webm")
video_filename_entry.pack(side=tk.LEFT)

video_clip = ttk.Frame(video_tab)
video_clip.grid(row=3, column=0, pady=5, sticky=tk.W)
video_clip_start_label = ttk.Label(video_clip, text="Start:")
video_clip_start_label.pack(side=tk.LEFT)
video_clip_start_entry = ttk.Entry(video_clip)
video_clip_start_entry.pack(side=tk.LEFT, padx=10)
video_clip_end_label = ttk.Label(video_clip, text="End:")
video_clip_end_label.pack(side=tk.LEFT)
video_clip_end_entry = ttk.Entry(video_clip)
video_clip_end_entry.pack(side=tk.LEFT, padx=10)

video_ffmpeg_options = ttk.Frame(video_tab)
video_ffmpeg_options.grid(row=4, column=0, pady=5, sticky=tk.W)
video_ffmpeg_options_label = ttk.Label(video_ffmpeg_options, text="FFmpeg options:")
video_ffmpeg_options_label.pack(side=tk.LEFT)
video_ffmpeg_options_entry = ttk.Entry(video_ffmpeg_options, width=32)
video_ffmpeg_options_entry.pack(side=tk.LEFT, padx=10)

video_download_button = ttk.Button(video_tab, text="Download Video", command=download_video)
video_download_button.grid(row=5, column=0, pady=5)

# audio
audio_tab = ttk.Frame(download_options)
download_options.add(audio_tab, text="Audio")
audio_option_var = tk.StringVar()
audio_dropdown = ttk.Combobox(audio_tab, state="readonly", width=64)
audio_dropdown.grid(row=0, column=0)

audio_filename = ttk.Frame(audio_tab)
audio_filename.grid(row=1, column=0, pady=5, sticky=tk.W)
audio_filename_prompt = ttk.Label(audio_filename, text="Enter filename:")
audio_filename_prompt.pack(side=tk.LEFT)
audio_filename_entry = ttk.Entry(audio_filename, width=48)
audio_filename_entry.insert(0, "audio.webm")
audio_filename_entry.pack(side=tk.LEFT)

audio_clip = ttk.Frame(audio_tab)
audio_clip.grid(row=2, column=0, pady=5, sticky=tk.W)
audio_clip_start_label = ttk.Label(audio_clip, text="Start:")
audio_clip_start_label.pack(side=tk.LEFT)
audio_clip_start_entry = ttk.Entry(audio_clip)
audio_clip_start_entry.pack(side=tk.LEFT, padx=10)
audio_clip_end_label = ttk.Label(audio_clip, text="End:")
audio_clip_end_label.pack(side=tk.LEFT)
audio_clip_end_entry = ttk.Entry(audio_clip)
audio_clip_end_entry.pack(side=tk.LEFT, padx=10)

audio_ffmpeg_options = ttk.Frame(audio_tab)
audio_ffmpeg_options.grid(row=3, column=0, pady=5, sticky=tk.W)
audio_ffmpeg_options_label = ttk.Label(audio_ffmpeg_options, text="ffmpeg options:")
audio_ffmpeg_options_label.pack(side=tk.LEFT)
audio_ffmpeg_options_entry = ttk.Entry(audio_ffmpeg_options, width=32)
audio_ffmpeg_options_entry.pack(side=tk.LEFT, padx=10)

audio_download_button = ttk.Button(audio_tab, text="Download Audio", command=download_audio)
audio_download_button.grid(row=4, column=0, pady=5)

download_options.grid_remove()

description_toggle = ttk.Button(root, text="Show Description", command=toggle_description)
description_toggle.grid(row=6, column=0)
description_toggle.grid_remove()
description_label = ttk.Label(root)
description_label.grid(row=7, column=0)

# Start the main event loop
print("FFmpeg Youtube Downloader started!")
root.mainloop()