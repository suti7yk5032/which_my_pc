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
import sys


version = "2.0"
appname = "which_my_pc"
token = 1
app_dir = os.path.dirname(os.path.abspath(sys.argv[0])) + "\\"
os.chdir(app_dir)
lib_dir_path = app_dir + "lib" + "\\"
img_dir_path = app_dir + "img" + "\\"
config_path = lib_dir_path + "which_my_config.json"
dll_path = lib_dir_path + "discord_game_sdk.dll"
lang_path = lib_dir_path + "lang.json"

class Initial():
    def config(self):
        if os.path.isdir(lib_dir_path):
            pass
        else:
            os.mkdir(lib_dir_path)

        if os.path.isfile(config_path):
            return 0

        else:
            if platform.system() == "Windows" and platform.release() == "10":
                reversion = platform.version().replace(".", "")
                if int(reversion) >= 10020000:
                    pcos = "Windows 11"
                else:
                    pcos = "Windows 10"
            else:
                pcos = platform.system() + " " + str(platform.release())
            
            wmp_config = {
                "language": "ja",
                "rich": {
                    "hostname": socket.gethostname(),
                    "pcos": str(pcos),
                    "details": socket.gethostname() + " | " + str(pcos),
                    "state": "no data",
                    "large_image_key": "main512",
                    "small_image_key": "windows_1024",
                    "large_image_text": "which_my_pc",
                    "small_image_text": str(pcos),
                    "party_size": None,
                    "party_max": None
                },
                
                "sleep": 5
            }

            with open(config_path, "w", encoding="utf-8") as config_write:
                json.dump(wmp_config, config_write, indent=4, ensure_ascii=False)
            return 0

    def language(self):
        if os.path.isfile(lang_path):
            return 0
        else:
            return 1

    def dll(self):
        if os.path.isfile(dll_path):
            return 0
        else:
            return 1

    def discord(self):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        task_exist = subprocess.run('tasklist /fi "IMAGENAME eq Discord.exe"', startupinfo=startupinfo, stdout=subprocess.PIPE, text=True)
        if 'Discord.exe' in task_exist.stdout:
            return 0
        else:
            return 1
        
    def lang(self):
        if os.path.isfile(lang_path):
            return 0
        else:
            return 1

class Status():
    def __init__(self):
        self.flag = 0
        self.flag_restart = 0

    def run(self):
        self.flag = 1
        self.thread = threading.Thread(target=self.main)
        self.thread.start()

    def exit(self):
        self.flag = 0

    def restart(self):
        self.flag = 0
        time.sleep(1)
        self.flag_restart = 1
        self.run()
    
    def main(self):
        if self.flag_restart != 1:
            time.sleep(int(wmp_config["sleep"]))
        else:
            pass
        self.time_now = datetime.datetime.now().timestamp()
        try:
            self.ds_token = ds.Discord(token, ds.CreateFlags.default)
            self.ds_activity_manager = self.ds_token.get_activity_manager()
            self.ds_activity = ds.Activity()
            
            self.ds_activity.details = wmp_config["rich"]["details"]
            self.ds_activity.state = wmp_config["rich"]["state"]
            self.ds_activity.timestamps.start = self.time_now
            self.ds_activity.party.id = "whichmypc"
            if wmp_config["rich"]["party_size"] != None:
                self.ds_activity.party.size.current_size = wmp_config["rich"]["party_size"]
            if wmp_config["rich"]["party_max"] != None:
                self.ds_activity.party.size.max_size = wmp_config["rich"]["party_max"]
            if wmp_config["rich"]["large_image_key"] != None:
                self.ds_activity.assets.large_image = wmp_config["rich"]["large_image_key"]
            if wmp_config["rich"]["large_image_text"] != None:
                self.ds_activity.assets.large_text = wmp_config["rich"]["large_image_text"]
            if wmp_config["rich"]["small_image_key"] != None:
                self.ds_activity.assets.small_image = wmp_config["rich"]["small_image_key"]
            if wmp_config["rich"]["small_image_text"] != None:
                self.ds_activity.assets.small_text = wmp_config["rich"]["small_image_text"]
            
            def callback(result):
                if result == ds.Result.ok:
                    notify.activity_suc()
                    print(wmp_str["notify"]["success_activity"]["details"][0] + wmp_config["rich"]["hostname"] + wmp_str["notify"]["success_activity"]["details"][1])
                else:
                    print(result)
                    raise Exception(result)
                
            self.ds_activity_manager.update_activity(self.ds_activity, callback)
            while self.flag == 1:
                time.sleep(1/10)
                self.ds_token.run_callbacks()
            return

        except Exception as e:
            if str(e.__class__.__name__) == "not_running":
                tray.tray.stop()
                notify.close_discord()
                return 0
            else:
                notify.activity_error(exception_class_name=str(e.__class__.__name__), exception_detail=str(e))
                return 1


class Notify():
    def __init__(self):    
        self.detail_title = "title_example"
        self.detail_message = "message_example"
        self.detail_icon = img_dir_path + "which_ok.png"

    def load(self, audio):
        self.detail = Notification(
            app_id=appname,
            title=self.detail_title,
            msg=self.detail_message,
            icon=self.detail_icon
        )
        self.detail.set_audio(audio, loop=False)
        self.detail.show()

    def activity_suc(self):
        notify_str = wmp_str["notify"]["success_activity"]
        self.detail_title = notify_str["title"]
        self.detail_message = notify_str["details"][0] + wmp_config["rich"]["hostname"] + notify_str["details"][1]
        self.detail_icon = img_dir_path + "which_ok.png"
        self.load(audio.IM)

    def activity_error(self, **kwargs):
        notify_str = wmp_str["notify"]["error_acitivity"]
        self.detail_title = notify_str["title"]
        self.detail_message = notify_str["details"][0] + kwargs["exception_class_name"] + "\n" + kwargs["exception_detail"]
        self.detail_icon = img_dir_path + "error.png"
        self.load(audio.Default)
    
    def startup_info(self):
        notify_str = wmp_str["notify"]["info_startup_register"]
        self.detail_title = notify_str["title"]
        self.detail_message = notify_str["details"][0] + appname + notify_str["details"][1]
        self.detail_icon = img_dir_path + "info.png"
        self.load(audio.Default)

    def not_found_discord(self):
        notify_str = wmp_str["notify"]["not_found_discord"]
        self.detail_title = notify_str["title"]
        self.detail_message = notify_str["details"][0]
        self.detail_icon = img_dir_path + "info.png"
        self.load(audio.Default)

    def close_discord(self):
        notify_str = wmp_str["notify"]["close_discord"]
        self.detail_title = notify_str["title"]
        self.detail_message = notify_str["details"][0]
        self.detail_icon = img_dir_path + "info.png"
        self.load(audio.Default)
    
    def not_found_dll(self):
        notify_str = wmp_str["notify"]["not_found_dll"]
        self.detail_title = notify_str["title"]
        self.detail_message = notify_str["details"][0]
        self.detail_icon = img_dir_path + "error.png"
        self.load(audio.Default)

    def required_restart(self):
        notify_str = wmp_str["notify"]["required_restart"]
        self.detail_title = notify_str["title"]
        self.detail_message = notify_str["details"][0] + appname + notify_str["details"][1]
        self.detail_icon = img_dir_path + "info.png"
        self.load(audio.Default)

    def which_info(self):
        notify_str = wmp_str["notify"]["about_version"]
        self.detail_title = notify_str["title"] + version
        self.detail_message = notify_str["details"][0] + "Windows\n" + notify_str["details"][1]
        self.detail_icon = img_dir_path + "logo\\which_logo128.png"
        self.load(audio.Default)


class Tray():
    def run(self):
        self.thread = threading.Thread(target=self.main)
        self.thread.start()

    def exit(self):
        status.exit()
        self.tray.stop()

    def restart(self):
        status.restart()

    def which_info(self):
        notify.which_info()
    
    def startup_launch(self):
        subprocess.Popen(["explorer", "shell:startup"])
        notify.startup_info()

    def settings_launch(self):
        def run_settings():
                if __name__ == "__main__":
                    app = App()
                    app.mainloop()
        self.settings_thread = threading.Thread(target=run_settings)
        self.settings_thread.start()
    
    def main(self):
        self.tray_str = wmp_str["tray"]
        self.trayicon = Image.open(img_dir_path + r"\logo\which_logo.ico")
        self.traymenu = Menu(
            MenuItem(self.tray_str["version"] + version, self.which_info),
            Menu.SEPARATOR,
            MenuItem(self.tray_str["open_settings"], self.settings_launch),
            MenuItem(self.tray_str["register_startup"], self.startup_launch),
            Menu.SEPARATOR,
            MenuItem(self.tray_str["restart"], self.restart),
            MenuItem(self.tray_str["exit"], self.exit)
        )

        self.tray = Icon(name=appname, title=appname,
                         icon=self.trayicon, menu=self.traymenu)
        self.tray.run()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.app_str = wmp_str["app"]
        self.app_title_str = wmp_str["app"]["title"]
        self.app_button_str = wmp_str["app"]["button"]
        self.app_label_str = wmp_str["app"]["label"]
        self.app_msgbox_str = wmp_str["app"]["msgbox"]

        self.title(appname + self.app_title_str["settings"])
        self.iconbitmap(img_dir_path + r"\logo\which_logo.ico")
        self.geometry("828x460")
        self.resizable(height=False, width=False)
        self.pady = 4
        self.padx = 10
        self.width = 240

        self.logo_icon = customtkinter.CTkImage(Image.open(os.path.join(img_dir_path + r"\logo\which_logo32.png")), size=(32, 32))
        self.info_icon = customtkinter.CTkImage(Image.open(os.path.join(img_dir_path + r"\info.png")), size=(32, 32))
        self.title_font = customtkinter.CTkFont(family="meiryo", size=17, weight="bold")
        self.info_font = customtkinter.CTkFont(family="meiryo", size=14)
        self.ui_font = customtkinter.CTkFont(family="meiryo", size=12)
        self.button_font = customtkinter.CTkFont(family="meiryo", size=14, weight="bold")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=32)
        self.grid_columnconfigure(2, weight=32)
        self.grid_columnconfigure(3, weight=32)

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
        self.settings_pcname_frame.grid(row=0, column=0, padx=self.padx, pady=self.pady)
        self.settings_pcname_info_label = customtkinter.CTkLabel(
            self.settings_pcname_frame, text=self.app_label_str["change_pc_name"], font=self.title_font, anchor=tk.W, justify=tk.LEFT, width=self.width, wraplength=self.width)
        self.settings_pcname_info_label.grid(row=0, column=0)
        self.settings_pcname_original_label = customtkinter.CTkLabel(
            self.settings_pcname_frame, text=self.app_label_str["current_pc_name"] + wmp_config["rich"]["hostname"], font=self.ui_font, anchor=tk.W, justify=tk.LEFT, width=self.width, wraplength=self.width)
        self.settings_pcname_original_label.grid(row=1, column=0)
        self.settings_pcname_textbox = customtkinter.CTkEntry(
            self.settings_pcname_frame, placeholder_text=self.app_label_str["enter_pc_name"], width=self.width, font=self.ui_font)
        self.settings_pcname_textbox.grid(row=2, column=0, pady=self.pady)

        self.settings_pcos_frame = customtkinter.CTkFrame(
            self.settings_frame, fg_color="transparent")
        self.settings_pcos_frame.grid(row=1, column=0, padx=self.padx, pady=self.pady)
        self.settings_pcos_info_label = customtkinter.CTkLabel(
            self.settings_pcos_frame, text=self.app_label_str["change_os_name"], font=self.title_font, anchor=tk.W, justify=tk.LEFT, width=self.width, wraplength=self.width)
        self.settings_pcos_info_label.grid(row=0, column=0)
        self.settings_pcos_original_label = customtkinter.CTkLabel(
            self.settings_pcos_frame, text=self.app_label_str["current_os_name"] + wmp_config["rich"]["pcos"], font=self.ui_font, anchor=tk.W, justify=tk.LEFT, width=self.width, wraplength=self.width)
        self.settings_pcos_original_label.grid(row=1, column=0)
        self.settings_pcos_textbox = customtkinter.CTkEntry(
            self.settings_pcos_frame, placeholder_text=self.app_label_str["enter_os_name"], width=self.width, font=self.ui_font)
        self.settings_pcos_textbox.grid(row=2, column=0, pady=self.pady)

        self.settings_pcspec_frame = customtkinter.CTkFrame(
            self.settings_frame, fg_color="transparent")
        self.settings_pcspec_frame.grid(row=2, column=0, padx=self.padx, pady=self.pady)
        self.settings_pcspec_info_label = customtkinter.CTkLabel(
            self.settings_pcspec_frame, text=self.app_label_str["change_pc_specs"], font=self.title_font, anchor=tk.W, justify=tk.LEFT, width=self.width, wraplength=self.width)
        self.settings_pcspec_info_label.grid(row=0, column=0)
        self.settings_pcspec_original_label = customtkinter.CTkLabel(
            self.settings_pcspec_frame, text=self.app_label_str["current_pc_specs"] + wmp_config["rich"]["state"], font=self.ui_font, anchor=tk.W, justify=tk.LEFT, width=self.width, wraplength=self.width)
        self.settings_pcspec_original_label.grid(row=1, column=0)
        self.settings_pcspec_textbox = customtkinter.CTkEntry(
            self.settings_pcspec_frame, placeholder_text=self.app_label_str["enter_pc_specs"], width=self.width, font=self.ui_font)
        self.settings_pcspec_textbox.grid(row=2, column=0, pady=self.pady)

        self.settings_large_image_text_frame = customtkinter.CTkFrame(
            self.settings_frame, fg_color="transparent")
        self.settings_large_image_text_frame.grid(row=0, column=1, padx=self.padx, pady=self.pady)
        self.settings_large_text_image_label = customtkinter.CTkLabel(
            self.settings_large_image_text_frame, text=self.app_label_str["change_large_image_text"], font=self.title_font, anchor=tk.W, justify=tk.LEFT, width=self.width, wraplength=self.width)
        self.settings_large_text_image_label.grid(row=0, column=0)
        self.settings_large_image_text_original_label = customtkinter.CTkLabel(
            self.settings_large_image_text_frame, text=self.app_label_str["current_large_image_text"] + wmp_config["rich"]["large_image_text"], font=self.ui_font, anchor=tk.W, justify=tk.LEFT, width=self.width, wraplength=self.width)
        self.settings_large_image_text_original_label.grid(row=1, column=0)
        self.settings_large_image_text_textbox = customtkinter.CTkEntry(
            self.settings_large_image_text_frame, placeholder_text=self.app_label_str["enter_large_image_text"], width=self.width, font=self.ui_font)
        self.settings_large_image_text_textbox.grid(row=2, column=0, pady=self.pady)

        self.settings_small_image_text_frame = customtkinter.CTkFrame(
            self.settings_frame, fg_color="transparent")
        self.settings_small_image_text_frame.grid(row=1, column=1, padx=self.padx, pady=self.pady)
        self.settings_small_text_image_label = customtkinter.CTkLabel(
            self.settings_small_image_text_frame, text=self.app_label_str["change_small_image_text"], font=self.title_font, anchor=tk.W, justify=tk.LEFT, width=self.width, wraplength=self.width)
        self.settings_small_text_image_label.grid(row=0, column=0)
        self.settings_small_image_text_original_label = customtkinter.CTkLabel(
            self.settings_small_image_text_frame, text=self.app_label_str["current_small_image_text"] + wmp_config["rich"]["small_image_text"], font=self.ui_font, anchor=tk.W, justify=tk.LEFT, width=self.width, wraplength=self.width)
        self.settings_small_image_text_original_label.grid(row=1, column=0)
        self.settings_small_image_text_textbox = customtkinter.CTkEntry(
            self.settings_small_image_text_frame, placeholder_text=self.app_label_str["enter_small_image_text"], width=self.width, font=self.ui_font)
        self.settings_small_image_text_textbox.grid(row=2, column=0, pady=self.pady)

        self.settings_language_frame = customtkinter.CTkFrame(
            self.settings_frame, fg_color="transparent")
        self.settings_language_frame.grid(row=2, column=1, padx=self.padx, pady=self.pady)
        self.settings_language_info_label = customtkinter.CTkLabel(
            self.settings_language_frame, text=self.app_label_str["select_language"], font=self.title_font, anchor=tk.W, justify=tk.LEFT, width=self.width, wraplength=self.width)
        self.settings_language_info_label.grid(row=0, column=0)
        self.settings_language_original_label = customtkinter.CTkLabel(
            self.settings_language_frame, text=self.app_label_str["current_language"] + wmp_config["language"], font=self.ui_font, anchor=tk.W, justify=tk.LEFT, width=self.width, wraplength=self.width)
        self.settings_language_original_label.grid(row=1, column=0)
        self.settings_language_combobox = customtkinter.CTkComboBox(
            self.settings_language_frame, values=wmp_lang_list, width=self.width, font=self.ui_font)
        self.settings_language_combobox.set(wmp_config["language"])
        self.settings_language_combobox.grid(row=2, column=0, pady=self.pady)

        self.settings_party_size_frame = customtkinter.CTkFrame(
            self.settings_frame, fg_color="transparent")
        self.settings_party_size_frame.grid(row=0, column=2, padx=self.padx, pady=self.pady)
        self.settings_small_text_image_label = customtkinter.CTkLabel(
            self.settings_party_size_frame, text=self.app_label_str["change_party_size"], font=self.title_font, anchor=tk.W, justify=tk.LEFT, width=self.width, wraplength=self.width)
        self.settings_small_text_image_label.grid(row=0, column=0)
        self.settings_party_size_original_label = customtkinter.CTkLabel(
            self.settings_party_size_frame, text=self.app_label_str["current_party_size"] + str(wmp_config["rich"]["party_size"]), font=self.ui_font, anchor=tk.W, justify=tk.LEFT, width=self.width, wraplength=self.width)
        self.settings_party_size_original_label.grid(row=1, column=0)
        self.settings_party_size_textbox = customtkinter.CTkEntry(
            self.settings_party_size_frame, placeholder_text=self.app_label_str["enter_party_size"], width=self.width, font=self.ui_font)
        self.settings_party_size_textbox.grid(row=2, column=0, pady=self.pady)

        self.settings_party_max_frame = customtkinter.CTkFrame(
            self.settings_frame, fg_color="transparent")
        self.settings_party_max_frame.grid(row=1, column=2, padx=self.padx, pady=self.pady)
        self.settings_small_text_image_label = customtkinter.CTkLabel(
            self.settings_party_max_frame, text=self.app_label_str["change_party_max"], font=self.title_font, anchor=tk.W, justify=tk.LEFT, width=self.width, wraplength=self.width)
        self.settings_small_text_image_label.grid(row=0, column=0)
        self.settings_party_max_original_label = customtkinter.CTkLabel(
            self.settings_party_max_frame, text=self.app_label_str["current_party_max"] + str(wmp_config["rich"]["party_max"]), font=self.ui_font, anchor=tk.W, justify=tk.LEFT, width=self.width, wraplength=self.width)
        self.settings_party_max_original_label.grid(row=1, column=0)
        self.settings_party_max_textbox = customtkinter.CTkEntry(
            self.settings_party_max_frame, placeholder_text=self.app_label_str["enter_party_max"], width=self.width, font=self.ui_font)
        self.settings_party_max_textbox.grid(row=2, column=0, pady=self.pady)

        self.settings_sleep_frame = customtkinter.CTkFrame(
            self.settings_frame, fg_color="transparent")
        self.settings_sleep_frame.grid(row=2, column=2, padx=self.padx, pady=self.pady)
        self.settings_sleep_info_label = customtkinter.CTkLabel(
            self.settings_sleep_frame, text=self.app_label_str["change_sleep_time"], font=self.title_font, anchor=tk.W, justify=tk.LEFT, width=self.width, wraplength=self.width)
        self.settings_sleep_info_label.grid(row=0, column=0)
        self.settings_sleep_original_label = customtkinter.CTkLabel(
            self.settings_sleep_frame, text=self.app_label_str["current_sleep_time"] + str(wmp_config["sleep"]), font=self.ui_font, anchor=tk.W, justify=tk.LEFT, width=self.width, wraplength=self.width)
        self.settings_sleep_original_label.grid(row=1, column=0)
        self.settings_sleep_textbox = customtkinter.CTkEntry(
            self.settings_sleep_frame, placeholder_text=self.app_label_str["enter_sleep_time"], width=self.width, font=self.ui_font)
        self.settings_sleep_textbox.grid(row=2, column=0, pady=self.pady)

        self.settings_button_frame = customtkinter.CTkFrame(
            self.settings_frame, fg_color="transparent")
        self.settings_button_frame.grid(row=3, column=1, pady=8)
        self.settings_save_button = customtkinter.CTkButton(
            self.settings_button_frame, text=self.app_button_str["save"], font=self.button_font, command=self.settings_save_check)
        self.settings_save_button.grid(row=0, column=0, padx=self.pady)

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
        notify.which_info()

    def settings_save_check(self):
        if self.settings_language_combobox.get() in wmp_lang_list:
            lang_check = 0
        else:
            lang_check = 1

        if self.settings_sleep_textbox.get() == "":
            sleep_check = 0
        elif self.settings_sleep_textbox.get().isdecimal():
            if int(self.settings_sleep_textbox.get()) >= 240:
                sleep_warning = messagebox.askyesno(appname + self.app_msgbox_str["long_sleep_time"]["title"], self.app_msgbox_str["long_sleep_time"]["details"])
                if sleep_warning:
                    sleep_check = 0
                else:
                    sleep_check = 2
            else:
                sleep_check = 0
        else:
            sleep_check = 1

        party_size = wmp_config["rich"]["party_size"]
        party_max = wmp_config["rich"]["party_max"]

        if self.settings_party_size_textbox.get() == "":
            party_size_check = 0
        elif self.settings_party_size_textbox.get().isdecimal():
            party_size_check = 0
            if self.settings_party_size_textbox.get() == "0":
                party_size = None
            else:
                party_size = self.settings_party_size_textbox.get()
        else:
            party_size_check = 1
        
        if self.settings_party_max_textbox.get() == "":
            party_max_check = 0
        elif self.settings_party_max_textbox.get().isdecimal():
            party_max_check = 0
            if self.settings_party_max_textbox.get() == "0":
                party_max = None
            else:
                party_max = self.settings_party_max_textbox.get()
        else:
            party_max_check = 1

        if party_size == None or party_max == None:
            if party_size == None and party_max == None:
                party_check = 0
            else:
                party_check = 1
        else:
            party_check = 0

        if lang_check == 0 and sleep_check == 0 and party_size_check == 0 and party_max_check == 0 and party_check == 0:
            settings_save = self.settings_save()
            if settings_save == 0:
                self.destroy()
                status.restart()
            else:
                self.destroy()
                tray.exit()
                notify.required_restart()

        elif sleep_check == 1:
            messagebox.showerror(appname + self.app_msgbox_str["invalid_sleep_value"]["title"], self.app_msgbox_str["invalid_sleep_value"]["details"])
        elif party_size_check == 1:
            messagebox.showerror(appname + self.app_msgbox_str["invalid_party_value"]["title"], self.app_msgbox_str["invalid_party_value"]["details"])
        elif party_max_check == 1:
            messagebox.showerror(appname + self.app_msgbox_str["invalid_party_max_value"]["title"], self.app_msgbox_str["invalid_party_max_value"]["details"])
        elif lang_check == 1:
            messagebox.showerror(appname + self.app_msgbox_str["invalid_language"]["title"], self.app_msgbox_str["invalid_language"]["details"])
        elif party_check == 1:
            messagebox.showerror(appname + self.app_msgbox_str["invalid_party_size"]["title"], self.app_msgbox_str["invalid_party_size"]["details"])
        elif sleep_check == 2:
            pass


    def settings_save(self):
        if not (self.settings_pcname_textbox.get() == ""):
            print(wmp_config)
            wmp_config["rich"]["hostname"] = self.settings_pcname_textbox.get()
            wmp_config["rich"]["details"] = self.settings_pcname_textbox.get() + \
                " | " + wmp_config["rich"]["pcos"]

        if not (self.settings_pcos_textbox.get() == ""):
            wmp_config["rich"]["pcos"] = self.settings_pcos_textbox.get()
            wmp_config["rich"]["details"] = wmp_config["rich"]["hostname"] + \
                " | " + self.settings_pcos_textbox.get()

        if not (self.settings_pcspec_textbox.get() == ""):
            wmp_config["rich"]["state"] = self.settings_pcspec_textbox.get()

        if not (self.settings_large_image_text_textbox.get() == ""):
            wmp_config["rich"]["large_image_text"] = self.settings_large_image_text_textbox.get()

        if not (self.settings_small_image_text_textbox.get() == ""):
            wmp_config["rich"]["small_image_text"] = self.settings_small_image_text_textbox.get()

        if (self.settings_party_size_textbox.get() == "0"):
            wmp_config["rich"]["party_size"] = None
        elif not (self.settings_party_size_textbox.get() == ""):
            wmp_config["rich"]["party_size"] = int(self.settings_party_size_textbox.get())
        
        if (self.settings_party_max_textbox.get() == "0"):
            wmp_config["rich"]["party_max"] = None
        elif not (self.settings_party_max_textbox.get() == ""):
            wmp_config["rich"]["party_max"] = int(self.settings_party_max_textbox.get())

        if not (self.settings_sleep_textbox.get() == ""):
            wmp_config["sleep"] = int(self.settings_sleep_textbox.get())
        
        old_lang = wmp_config["language"]

        wmp_config["language"] = self.settings_language_combobox.get()

        with open(config_path, "w", encoding="utf-8") as list_write:
            json.dump(wmp_config, list_write, indent=4, ensure_ascii=False)

        if old_lang == wmp_config["language"]:
            return 0
        else:
            return 1


if __name__ == "__main__":
    status = Status()
    tray = Tray()
    wmp_init = Initial()
    notify = Notify()
    lang_init_result = wmp_init.language()
    if lang_init_result == 0:
        with open(lang_path, "r", encoding="utf-8") as lang_read:
            wmp_lang = json.load(lang_read)
        wmp_lang_list = list(wmp_lang.keys())
        print(wmp_lang_list)

        config_init_result = wmp_init.config()
        if config_init_result == 0:
            with open(config_path, "r", encoding="utf-8") as config_read:
                wmp_config = json.load(config_read)
            wmp_str = wmp_lang[wmp_config["language"]]

            dll_init_result = wmp_init.dll()

            if dll_init_result == 0:
                import discordsdk as ds
                run_switch = 0
                discord_init_loop_count = 0

                while discord_init_loop_count != 10:
                    discord_init_result = wmp_init.discord()
                    if discord_init_result == 0:
                        run_switch = 1
                        discord_init_loop_count = 10
                    else:
                        time.sleep(int(wmp_config["sleep"]))
                        discord_init_loop_count += 1
                        print(wmp_str["initial"]["waiting_discord"])

                if run_switch == 1:
                    status.run()
                    tray.run()
                else:
                    notify.not_found_discord()
                    print(wmp_str["initial"]["not_found_discord"])

            else:
                notify.not_found_dll()
                print(wmp_str["initial"]["not_found_dll"])
    else:
        print("Language file not found. Place the language file properly and try again.")
        messagebox.showerror(appname + " | Serious error", "Language file not found.\nPlace the language file properly and try again.")