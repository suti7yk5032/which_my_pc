"""

Copylight (C) 2023 suti7yk5032

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
details.

You should have received a copy of the GNU Lesser General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

"""

import discordsdk as ds
import threading
from pystray import Icon, Menu, MenuItem
from PIL import Image
from winotify import Notification, audio
import customtkinter
import subprocess
import os
import json
import socket
import time
import platform
import tkinter as tk
from tkinter import messagebox
import datetime


ver = "1.1"
lang = "English"
appname = "which_my_pc"
token = 1
lib_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "lib")
img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "img")


class General():
    file_name = "which_my_config.json"
    file_path = "./lib/" + file_name

    def __init__(self):
        if not os.path.isfile(General.file_path):
            if platform.system() == "Windows" and platform.release() == "10":
                self.reversion = platform.version().replace(".", "")
                if int(self.reversion) >= 10020000:
                    self.pcos = "Windows 11"
                else:
                    self.pcos = "Windows 10"
            else:
                self.pcos = platform.system() + " " + str(platform.release())

            self.dummylist = {
                "hostname": socket.gethostname(),
                "pcos": self.pcos,
                "pcname": socket.gethostname() + " | " + self.pcos,
                "pcspec": "no data",
                "sleep": "5"
            }

            with open(General.file_path, "w") as list_write:
                json.dump(self.dummylist, list_write, indent=4)

        with open(General.file_path, "r") as list_read:
            General.pclist = json.load(list_read)


class Status():
    flag = 0
    flag_restart = 0

    def run(self):
        Status.flag = 1
        self.thread = threading.Thread(target=self.main)
        self.thread.start()

    def exit(self):
        Status.flag = 0

    def restart(self):
        Status.flag = 0
        time.sleep(1)
        Status.flag_restart = 1
        self.run()
    
    def main(self):
        if Status.flag_restart != 1:
            time.sleep(int(General.pclist["sleep"]))
        else:
            pass
        self.time_now = datetime.datetime.now().timestamp()
        try:
            self.ds_token = ds.Discord(token, ds.CreateFlags.default)
            self.ds_activity_manager = self.ds_token.get_activity_manager()
            self.ds_activity = ds.Activity()
            self.ds_activity.details = General.pclist["pcname"]
            self.ds_activity.state = General.pclist["pcspec"]
            self.ds_activity.timestamps.start = self.time_now
            self.ds_activity.party.id = "whichmypc"
            self.ds_activity.assets.large_image = "main512"
            def callback(result):
                if result == ds.Result.ok:
                    Notify().activity_suc()
                    print("The activity is set as PC name " + General.pclist["hostname"] + ".")
                else:
                    print("error")
                    raise Exception(result)
                
            self.ds_activity_manager.update_activity(self.ds_activity, callback)
            while Status.flag == 1:
                time.sleep(1/10)
                self.ds_token.run_callbacks()
            return

        except:
            Notify().activity_error()
            print("An error has occurred, please start Discord and try again.")
            return
        

class Notify():
    detail_title = "title_example"
    detail_message = "message_example"
    detail_icon = img_path + r"\which_ok.png"

    def load(self, audio):
        self.detail = Notification(
            app_id=appname,
            title=Notify.detail_title,
            msg=Notify.detail_message,
            icon=Notify.detail_icon
        )
        self.detail.set_audio(audio, loop=False)
        self.detail.show()

    def activity_suc(self):
        Notify.detail_title = "Activity has been set."
        Notify.detail_message = "The activity is set as PC name " + General.pclist["hostname"] + "." + "\nThe application is resident in the taskbar."
        Notify.detail_icon = img_path + r"\which_ok.png"
        Notify().load(audio.IM)

    def activity_error(self):
        Notify.detail_title = "Activity is not set."
        Notify.detail_message = "An error has occurred, please start Discord and try again."
        Notify.detail_icon = img_path + r"\error.png"
        Notify().load(audio.Default)
    
    def startup_info(self):
        Notify.detail_title = "Add to Startup"
        Notify.detail_message = "Create a shortcut to " + appname + " in the startup folder."
        Notify.detail_icon = img_path + r"\info.png"
        Notify().load(audio.Default)
    
    def which_info(self):
        Notify.detail_title = "Version " + ver
        Notify.detail_message = "for Windows" + "\n" + lang
        Notify.detail_icon = img_path + r"\logo\which_logo128.png"
        Notify().load(audio.Default)


class Tray():
    def run(self):
        self.thread = threading.Thread(target=self.main)
        self.thread.start()

    def exit(self):
        Status().exit()
        self.tray.stop()

    def restart(self):
        Status().restart()

    def main(self):
        self.trayicon = Image.open(img_path + r"\logo\which_logo.ico")
        self.traymenu = Menu(
            MenuItem("Version " + ver, self.which_info),
            Menu.SEPARATOR,
            MenuItem("Edit Activity", self.settings_launch),
            MenuItem("Add to Startup", self.startup_launch),
            Menu.SEPARATOR,
            MenuItem("Restart", self.restart),
            MenuItem("Close", self.exit)
        )

        self.tray = Icon(name=appname, title=appname,
                         icon=self.trayicon, menu=self.traymenu)
        self.tray.run()

    def which_info(self):
        Notify().which_info()
    
    def startup_launch(self):
        subprocess.Popen(["explorer", "shell:startup"])
        Notify().startup_info()

    def settings_launch(self):
        def run_settings():
                if __name__ == "__main__":
                    app = App()
                    app.mainloop()
        self.settings_thread = threading.Thread(target=run_settings)
        self.settings_thread.start()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title(appname + " | Settings")
        self.iconbitmap(img_path + r"\logo\which_logo.ico")
        self.geometry("520x480")
        self.resizable(height=False, width=False)


        self.logo_icon = customtkinter.CTkImage(Image.open(os.path.join(img_path + r"\logo\which_logo32.png")), size=(32, 32))
        self.info_icon = customtkinter.CTkImage(Image.open(os.path.join(img_path + r"\info.png")), size=(32, 32))
        self.title_font = customtkinter.CTkFont(family="meiryo", size=18, weight="bold")
        self.info_font = customtkinter.CTkFont(family="meiryo", size=14)
        self.ui_font = customtkinter.CTkFont(family="meiryo", size=12)
        self.button_font = customtkinter.CTkFont(family="meiryo", size=14, weight="bold")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=6)

        self.frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_rowconfigure(4, weight=1)

        self.settings_frame_button = customtkinter.CTkButton(self.frame, width=32, height=36, border_spacing=4, image=self.logo_icon,
                                                             text="", fg_color="transparent", hover_color=("gray70", "gray30"), command=self.frame_select_settings)
        self.settings_frame_button.grid(row=0, column=0, sticky="ew")

        self.info_button = customtkinter.CTkButton(self.frame, width=32, height=36, border_spacing=4, image=self.info_icon,
                                                   text="", fg_color="transparent", hover_color=("gray70", "gray30"), command=self.app_info)
        self.info_button.grid(row=1, column=0, sticky="ew")

        self.settings_frame = customtkinter.CTkFrame(
            self, fg_color="transparent")
        self.settings_frame.grid(row=0, column=1, sticky="nsew")

        self.settings_pcname_frame = customtkinter.CTkFrame(
            self.settings_frame, fg_color="transparent")
        self.settings_pcname_frame.grid(row=0, column=0, padx=20, pady=8)
        self.settings_pcname_info_label = customtkinter.CTkLabel(
            self.settings_pcname_frame, text="Rename PC", font=self.title_font, anchor=tk.W, width=428)
        self.settings_pcname_info_label.grid(row=0, column=0)
        self.settings_pcname_original_label = customtkinter.CTkLabel(
            self.settings_pcname_frame, text="Current PC Name : " + General.pclist["hostname"], font=self.ui_font, anchor=tk.W, width=428)
        self.settings_pcname_original_label.grid(row=1, column=0)
        self.settings_pcname_textbox = customtkinter.CTkEntry(
            self.settings_pcname_frame, placeholder_text="Enter a new name for the PC", width=428, font=self.ui_font)
        self.settings_pcname_textbox.grid(row=2, column=0, pady=2)

        self.settings_pcos_frame = customtkinter.CTkFrame(
            self.settings_frame, fg_color="transparent")
        self.settings_pcos_frame.grid(row=1, column=0, padx=20, pady=8)
        self.settings_pcos_info_label = customtkinter.CTkLabel(
            self.settings_pcos_frame, text="Rename OS", font=self.title_font, anchor=tk.W, width=428)
        self.settings_pcos_info_label.grid(row=0, column=0)
        self.settings_pcos_original_label = customtkinter.CTkLabel(
            self.settings_pcos_frame, text="Current OS Name : " + General.pclist["pcos"], font=self.ui_font, anchor=tk.W, width=428)
        self.settings_pcos_original_label.grid(row=1, column=0)
        self.settings_pcos_textbox = customtkinter.CTkEntry(
            self.settings_pcos_frame, placeholder_text="Enter a new name for the OS", width=428, font=self.ui_font)
        self.settings_pcos_textbox.grid(row=2, column=0, pady=2)

        self.settings_pcspec_frame = customtkinter.CTkFrame(
            self.settings_frame, fg_color="transparent")
        self.settings_pcspec_frame.grid(row=2, column=0, padx=20, pady=8)
        self.settings_pcspec_info_label = customtkinter.CTkLabel(
            self.settings_pcspec_frame, text="Change PC specs", font=self.title_font, anchor=tk.W, width=428)
        self.settings_pcspec_info_label.grid(row=0, column=0)
        self.settings_pcspec_original_label = customtkinter.CTkLabel(
            self.settings_pcspec_frame, text="Current PC specs : " + General.pclist["pcspec"], font=self.ui_font, anchor=tk.W, width=428)
        self.settings_pcspec_original_label.grid(row=1, column=0)
        self.settings_pcspec_textbox = customtkinter.CTkEntry(
            self.settings_pcspec_frame, placeholder_text="Enter PC specs", width=428, font=self.ui_font)
        self.settings_pcspec_textbox.grid(row=2, column=0, pady=2)

        self.settings_sleep_frame = customtkinter.CTkFrame(
            self.settings_frame, fg_color="transparent")
        self.settings_sleep_frame.grid(row=3, column=0, padx=20, pady=8)
        self.settings_sleep_info_label = customtkinter.CTkLabel(
            self.settings_sleep_frame, text="Change waiting time", font=self.title_font, anchor=tk.W, width=428)
        self.settings_sleep_info_label.grid(row=0, column=0)
        self.settings_sleep_original_label = customtkinter.CTkLabel(
            self.settings_sleep_frame, text="Current waiting time : " + General.pclist["sleep"], font=self.ui_font, anchor=tk.W, width=428)
        self.settings_sleep_original_label.grid(row=1, column=0)
        self.settings_sleep_textbox = customtkinter.CTkEntry(
            self.settings_sleep_frame, placeholder_text="Enter waiting time (sec)", width=428, font=self.ui_font)
        self.settings_sleep_textbox.grid(row=2, column=0, pady=2)

        self.settings_button_frame = customtkinter.CTkFrame(
            self.settings_frame, fg_color="transparent")
        self.settings_button_frame.grid(row=4, column=0, pady=8)

        self.settings_save_button = customtkinter.CTkButton(
            self.settings_button_frame, text="Save", font=self.button_font, command=self.settings_save_check)
        self.settings_save_button.grid(row=0, column=0, padx=10)

        self.select_frame("settings_frame")

    def select_frame(self, name):
        self.settings_frame_button.configure(
            fg_color=("gray75", "gray25") if name == "settings_frame" else "transparent")

        if name == "settings_frame":
            self.settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_frame.grid_forget()

    def frame_select_settings(self):
        self.select_frame("settings_frame")

    def app_info(self):
        Notify().which_info()

    def settings_save_check(self):
        if self.settings_sleep_textbox.get() == "":
            self.settings_save()
            self.destroy()
            Status().restart()
        else:
            if self.settings_sleep_textbox.get().isdecimal():
                if int(self.settings_sleep_textbox.get()) >= 240:
                    sleep_warning = messagebox.askyesno(
                        appname + " | Attention", "The waiting time seems to be long.\nIf the file is saved as is, problems may occur, such as the file not starting up easily the next time it is launched.\nDo you still want to save it?")
                    if sleep_warning:
                        self.settings_save()
                        self.destroy()
                    else:
                        pass
                else:
                    self.settings_save()
                    self.destroy()
                    Status().restart()
            else:
                messagebox.showerror(
                    appname + " | Error", "The value entered for the wait time is invalid.\nPlease try again.")

    def settings_save(self):
        if not (self.settings_pcname_textbox.get() == ""):
            General.pclist["hostname"] = self.settings_pcname_textbox.get()
            General.pclist["pcname"] = self.settings_pcname_textbox.get() + \
                " | " + General.pclist["pcos"]

        if not (self.settings_pcos_textbox.get() == ""):
            General.pclist["pcos"] = self.settings_pcos_textbox.get()
            General.pclist["pcname"] = General.pclist["hostname"] + \
                " | " + self.settings_pcos_textbox.get()

        if not (self.settings_pcspec_textbox.get() == ""):
            General.pclist["pcspec"] = self.settings_pcspec_textbox.get()

        if not (self.settings_sleep_textbox.get() == ""):
            General.pclist["sleep"] = self.settings_sleep_textbox.get()

        with open(General.file_path, "w") as list_write:
            json.dump(General.pclist, list_write, indent=4)

        print(General.pclist)


if __name__ == "__main__":
    status_thread = threading.Thread(target=Status().run)
    tray_thread = threading.Thread(target=Tray().run)
    
    General()
    status_thread.start()
    tray_thread.start()