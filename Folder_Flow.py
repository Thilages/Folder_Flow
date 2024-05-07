import os
import shutil
import time
import tkinter.messagebox
from datetime import datetime
from tkinter import Frame
import customtkinter
from customtkinter import *

# Global variables for file extensions
image_extenstion = ["jpg", "jpeg", "jpe", "jif", "jfif",
                    "png", "gif", "bmp", "tiff", "tif",
                    "webp", "svg", "svgz", "ico", "cur",
                    "psd", "ai", "eps", "raw",
                    "exif", "heif", "heic", "indd", "psb",
                    "jp2", "j2k", "jpf", "jpx", "jpm",
                    "mj2", "dng", "nef", "orf", "cr2",
                    "arw", "rw2", "raf", "sr2", "srf",
                    "3fr", "dcr", "k25", "raw", "pef",
                    "x3f"]

audio_extension = ["mp3", "wav", "flac", "aac", "m4a",
                   "ogg", "wma", "aiff", "ape", "alac",
                   "pcm", "au", "ra", "mid", "midi",
                   "mod", "s3m", "xm", "it", "mtm",
                   "umx", "ac3", "ec3", "dts", "mka",
                   "mp2", "mp1", "amr", "opus", "caf",
                   "wv", "tta", "dsd", "gsm", "awb",
                   "m4b", "m4p", "m4r", "m4v", "3ga",
                   "mpc", "m4r", "wv", "mpa", "oma"]
video_extension = ["mp4", "mkv", "avi", "mov", "wmv",
                   "flv", "webm", "m4v", "mpeg", "mpg",
                   "3gp", "3g2", "m2v", "m4p", "m4a",
                   "f4v", "ogv", "ogg", "ts", "mts",
                   "m2ts", "vob", "rm", "rmvb", "asf",
                   "divx", "swf", "mpg4", "mpe", "mp2",
                   "mpeg1", "mpeg2", "mpeg4", "mpegps", "mpegts",
                   "m1v", "m2v", "m2ts", "m4v", "mng",
                   "ogm", "tod", "vro", "dat", "amv"]

document_extention = ["pdf", "doc", "docx", "txt", "rtf",
                      "odt", "ott", "xls", "xlsx", "csv",
                      "ods", "ppt", "pptx", "odp", "odg",
                      "odc", "odf", "odb", "odm", "odp",
                      "odt", "ott", "odg", "otg", "odc",
                      "otc", "odf", "odft", "odp", "otp",
                      "ods", "ots", "odt", "odm", "ott",
                      "rtf", "xml", "html", "htm", "mht",
                      "mhtml", "xhtml", "xht", "php", "php3",
                      "php4", "php5", "phtml", "shtml", "jhtml"]

# Function to check if file creation date matches the specified date
def date_checker(file_date, user_date):
    file_d = datetime.strptime(file_date, "%a %b %d %H:%M:%S %Y")

    try:
        user = datetime.strptime(user_date, "%Y-%m")
        if user.year == file_d.year and user.month == file_d.month:
            return True
        else:
            return False
    except:
        user = datetime.strptime(user_date, "%Y")
        if user.year == file_d.year:
            return True
        else:
            return False

# Function to organize files by copying
def auto_organize_by_coping(source_path, destination_path, extension, date, create_folder):
    total_extenstion = []
    # Create destination folders if necessary
    if create_folder:
        for ext in extension:
            if ext == "image":
                total_extenstion = image_extenstion
            elif ext == "video":
                total_extenstion = video_extension
            elif ext == "document":
                total_extenstion = document_extention
            elif ext == "audio":
                total_extenstion = audio_extension
            try:
                os.mkdir(f"{destination_path}\\{ext}")
                new_path = f"{destination_path}\\{ext}"
                folder_extractor(source_path, new_path, total_extenstion, date)

            except:
                new_path = f"{destination_path}\\{ext}"
                # Copy files to destination folders
                folder_extractor(source_path, new_path, total_extenstion, date)
            finally:
                pass
    else:
        for ext in extension:
            if ext == "image":
                total_extenstion.extend(image_extenstion)
            if ext == "video":
                total_extenstion.extend(video_extension)
            if ext == "document":
                total_extenstion.extend(document_extention)
            if ext == "audio":
                total_extenstion.extend(audio_extension)
        folder_extractor(source_path, destination_path, total_extenstion, date)


def folder_extractor(path_of_folder, end_folder, extension, date):
    folders_in_folder = os.listdir(path_of_folder)

    for file in folders_in_folder:
        print(f"Current file:{path_of_folder}\\{file}")
        ti_c = os.path.getmtime(f"{path_of_folder}\\{file}")
        file_ct_date = time.ctime(ti_c)
        try:

            if date:
                if (os.path.splitext(file)[1].replace(".", "") in extension) and date_checker(file_ct_date, date):
                    shutil.copy2(f"{path_of_folder}\\{file}", end_folder)
                else:

                    if os.path.isdir(f"{path_of_folder}\\{file}"):
                        folder_extractor(f"{path_of_folder}\\{file}", end_folder, extension, date)
                    else:
                        pass
            else:
                if os.path.splitext(file)[1].replace(".", "") in extension:
                    shutil.copy2(f"{path_of_folder}\\{file}", end_folder)
                else:

                    if os.path.isdir(f"{path_of_folder}\\{file}"):
                        folder_extractor(f"{path_of_folder}\\{file}", end_folder, extension, date)
                    else:
                        pass

        except Exception as e:
            print(e)

# Function to handle GUI events and start file organization
def main():
    sort_files = []
    create_folder = True

    source_path = source_button.cget("text")
    destination_path = destination_button.cget("text")

    if source_button.cget("text") == "Choose the Source":
        tkinter.messagebox.showinfo(title="Source not defined", message="Please Select a source")
    elif destination_button.cget("text") == "Choose the Destination":
        tkinter.messagebox.showinfo(title="Destination not defined", message="Please Select a Destination")
    elif destination_button.cget("text") == source_button.cget("text"):
        tkinter.messagebox.showinfo(title="Invalid file locations",
                                    message="Please Select a unique source and destination dumbass")

    if all_var.get() == "on":
        sort_files.extend(["image", "audio", "video", 'document'])
    else:
        if image_var.get() == "on":
            sort_files.append("image")
        if video_var.get() == "on":
            sort_files.append("video")
        if audio_var.get() == "on":
            sort_files.append("audio")
        if document_var.get() == "on":
            sort_files.append("document")

    if folder_var.get() == "off":
        create_folder = False
    date = ""

    if month_var.get() == "on" and year_var.get() == "on":
        date = f"{year_option_var.get()} {month_option_var.get()} "
        input_date = datetime.strptime(date, "%Y %B ")
        formatted_date = input_date.strftime("%Y-%m")

    elif year_var.get() == "on":
        formatted_date = year_option.get()

    else:
        formatted_date = False

    if folder_var.get() == "off":
        create_folder = False

    auto_organize_by_coping(source_path, destination_path, sort_files, formatted_date, create_folder)

    root.quit()

# GUI setup and configuration
def source_choise():
    path = filedialog.askdirectory()
    source_button.configure(text=path)


def destination_choise():
    path = filedialog.askdirectory()
    destination_button.configure(text=path)


def all_checkbox_command():
    if all_var.get() == "off":
        image_checkbox.configure(state=NORMAL)
        Audio_checkbox.configure(state=NORMAL)
        Video_checkbox.configure(state=NORMAL)
        Document_checkbox.configure(state=NORMAL)
    if all_var.get() == "on":
        image_var.set("off")
        audio_var.set("off")
        video_var.set("off")
        document_var.set("off")
        image_checkbox.configure(state=DISABLED)
        Audio_checkbox.configure(state=DISABLED)
        Video_checkbox.configure(state=DISABLED)
        Document_checkbox.configure(state=DISABLED)


def year_update():
    if year_var.get() == "off":
        year_option.configure(state=DISABLED)
    elif year_var.get() == "on":
        year_option.configure(state=NORMAL)


def month_update():
    if year_var.get() == "on" and month_var.get() == "on":
        month_option.configure(state=NORMAL)
    elif month_var.get() == "off":
        month_option.configure(state=DISABLED)


# def date_update():
#     if date_var.get() == "on":
#         date_option.configure(state=NORMAL)
#     elif date_var.get() == "off":
#         date_option.configure(state=DISABLED)


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
root.resizable(False, False)

root.geometry('500x730')

option_label = CTkLabel(root, text="The file organizing mode", font=("", 12, "roman"))
option_label.pack()

option_var = customtkinter.StringVar(value="Copy Files")
segemented_button = CTkSegmentedButton(root, values=["Copy Files"],
                                       # command=optionmenu_callback,
                                       width=300,
                                       height=40,
                                       font=(" Times", 16),
                                       variable=option_var)
segemented_button.set("Copy Files")
segemented_button.pack()

horizontal = Frame(root, bg="grey", height=1, width=600)
horizontal.place(x=10, y=110)

source_label = CTkLabel(root, text="Source Directory:", font=("", 16, "bold"))
source_label.pack(pady=(40, 0), padx=10)

source_button = CTkButton(root, text="Choose the Source", width=400, height=40, font=("", 16), command=source_choise)
source_button.pack(pady=(5, 0), padx=10)

destination_label = CTkLabel(root, text="Destination Directory:", font=("", 16, "bold"))
destination_label.pack(pady=(10, 0), padx=10)

destination_button = CTkButton(root, text="Choose the Destination", width=400, height=40, font=("", 16),
                               command=destination_choise)
destination_button.pack(pady=(5, 0), padx=10)

horizontal1 = Frame(root, bg="grey", height=1, width=600)
horizontal1.place(x=10, y=360)

sort_label = CTkLabel(root, text="Select the extensions to organize")
sort_label.pack(pady=(40, 0))

frame = Frame(root, background="#1a1a1a")
frame.pack()

image_var = customtkinter.StringVar(value="off")
image_checkbox = CTkCheckBox(frame, text="Images", font=("hevetica", 16, "bold"), onvalue="on", offvalue="off",
                             variable=image_var)
image_checkbox.grid_configure(column=0, row=0, padx=40, pady=10)

audio_var = customtkinter.StringVar(value="off")
Audio_checkbox = CTkCheckBox(frame, text="Audios", font=("hevetica", 16, "bold"), onvalue="on", offvalue="off",
                             variable=audio_var)
Audio_checkbox.grid_configure(column=0, row=1, padx=40, pady=10)

video_var = customtkinter.StringVar(value="off")
Video_checkbox = CTkCheckBox(frame, text="Videos", font=("hevetica", 16, "bold"), onvalue="on", offvalue="off",
                             variable=video_var)
Video_checkbox.grid_configure(column=1, row=0, padx=40, pady=10)

document_var = customtkinter.StringVar(value="off")
Document_checkbox = CTkCheckBox(frame, text="Documents", font=("hevetica", 16, "bold"), onvalue="on", offvalue="off",
                                variable=document_var)
Document_checkbox.grid_configure(column=1, row=1, padx=40, pady=10)

all_var = customtkinter.StringVar(value="on")
all_checkbox = CTkCheckBox(frame, text="Auto Organizer", font=("hevetica", 16, "bold"), onvalue="on", offvalue="off",
                           variable=all_var, command=all_checkbox_command)
all_checkbox.grid_configure(column=0, row=2, columnspan=2, padx=40, pady=(10, 20))
all_checkbox.setvar("on")

folder_var = customtkinter.StringVar(value="on")
folder_switch = CTkSwitch(frame, text="Create Folder Automatically", variable=folder_var, onvalue="on",
                          offvalue='off', )
folder_switch.grid_configure(columnspan=2, column=0, row=3)

horizontal1 = Frame(root, bg="grey", height=1, width=600)
horizontal1.place(x=10, y=620)

date_sort_label = CTkLabel(root, text="Select the date to organize")
date_sort_label.pack(pady=(30, 0))

frame1 = Frame(root, background="#1a1a1a")
frame1.pack()

month_var = customtkinter.StringVar(value="off")
month_checkbox = CTkCheckBox(frame1, text="By Month", font=("hevetica", 16, "bold"), onvalue="on", offvalue="off",
                             variable=month_var, command=month_update)
month_checkbox.grid_configure(column=1, row=0, padx=20, pady=10)

year_var = customtkinter.StringVar(value="on")
year_checkbox = CTkCheckBox(frame1, text="By Year", font=("hevetica", 16, "bold"), onvalue="on", offvalue="off",
                            variable=year_var, command=year_update)
year_checkbox.grid_configure(column=2, row=0, padx=20, pady=10)

month_option_var = customtkinter.StringVar(value="February")
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
          "December"]
month_option = CTkOptionMenu(frame1, values=months, variable=month_option_var)
month_option.grid_configure(column=1, row=1, padx=10, pady=10)
month_option.set("February")
month_option.configure(state=DISABLED)

year_option_var = customtkinter.StringVar(value="2005")
year_option = CTkOptionMenu(frame1, values=[f"{i}" for i in range(2000, 2025)], variable=year_option_var)
year_option.grid_configure(column=2, row=1, padx=10, pady=10)

organize_button = CTkButton(root, text="Organize", width=150, height=40, font=("", 16, "bold"), command=main)
organize_button.pack(pady=(20, 20))

if all_var.get() == "on":
    image_checkbox.configure(state=DISABLED)
    Audio_checkbox.configure(state=DISABLED)
    Video_checkbox.configure(state=DISABLED)
    Document_checkbox.configure(state=DISABLED)

root.mainloop()
