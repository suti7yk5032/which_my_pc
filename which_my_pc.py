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
lang = "日本語"
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
                    print("アクティビティがセットされました。現在のPCは " + General.pclist["hostname"] + " です。")
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
            print("エラーが発生しました。Discord が起動してからもう一度起動してみてください。")
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
        Notify.detail_title = "アクティビティをセットしました"
        Notify.detail_message = "現在のPCは " + General.pclist["hostname"] + " です。\nアプリはタスクバーに収納されています。"
        Notify.detail_icon = img_path + r"\which_ok.png"
        Notify().load(audio.IM)

    def activity_error(self):
        Notify.detail_title = "アクティビティはセットされていません"
        Notify.detail_message = "エラーが発生しました。\nDiscord が起動してからもう一度起動してみてください。"
        Notify.detail_icon = img_path + r"\error.png"
        Notify().load(audio.Default)
    
    def startup_info(self):
        Notify.detail_title = "スタートアップに登録"
        Notify.detail_message = "スタートアップ フォルダに " + appname + " のショートカットを作成してください。"
        Notify.detail_icon = img_path + r"\info.png"
        Notify().load(audio.Default)
    
    def which_info(self):
        Notify.detail_title = "バージョン " + ver
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
            MenuItem("バージョン " + ver, self.which_info),
            Menu.SEPARATOR,
            MenuItem("PC情報を編集", self.settings_launch),
            MenuItem("スタートアップに登録", self.startup_launch),
            Menu.SEPARATOR,
            MenuItem("再起動", self.restart),
            MenuItem("終了", self.exit)
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

        self.title(appname + " | 設定")
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
            self.settings_pcname_frame, text="PCの名前の変更", font=self.title_font, anchor=tk.W, width=428)
        self.settings_pcname_info_label.grid(row=0, column=0)
        self.settings_pcname_original_label = customtkinter.CTkLabel(
            self.settings_pcname_frame, text="現在のPCの名前 : " + General.pclist["hostname"], font=self.ui_font, anchor=tk.W, width=428)
        self.settings_pcname_original_label.grid(row=1, column=0)
        self.settings_pcname_textbox = customtkinter.CTkEntry(
            self.settings_pcname_frame, placeholder_text="PCの名前を入力", width=428, font=self.ui_font)
        self.settings_pcname_textbox.grid(row=2, column=0, pady=2)

        self.settings_pcos_frame = customtkinter.CTkFrame(
            self.settings_frame, fg_color="transparent")
        self.settings_pcos_frame.grid(row=1, column=0, padx=20, pady=8)
        self.settings_pcos_info_label = customtkinter.CTkLabel(
            self.settings_pcos_frame, text="OSの変更", font=self.title_font, anchor=tk.W, width=428)
        self.settings_pcos_info_label.grid(row=0, column=0)
        self.settings_pcos_original_label = customtkinter.CTkLabel(
            self.settings_pcos_frame, text="現在のOS : " + General.pclist["pcos"], font=self.ui_font, anchor=tk.W, width=428)
        self.settings_pcos_original_label.grid(row=1, column=0)
        self.settings_pcos_textbox = customtkinter.CTkEntry(
            self.settings_pcos_frame, placeholder_text="OSの名前を入力", width=428, font=self.ui_font)
        self.settings_pcos_textbox.grid(row=2, column=0, pady=2)

        self.settings_pcspec_frame = customtkinter.CTkFrame(
            self.settings_frame, fg_color="transparent")
        self.settings_pcspec_frame.grid(row=2, column=0, padx=20, pady=8)
        self.settings_pcspec_info_label = customtkinter.CTkLabel(
            self.settings_pcspec_frame, text="PCのスペックの変更", font=self.title_font, anchor=tk.W, width=428)
        self.settings_pcspec_info_label.grid(row=0, column=0)
        self.settings_pcspec_original_label = customtkinter.CTkLabel(
            self.settings_pcspec_frame, text="現在のPCのスペック : " + General.pclist["pcspec"], font=self.ui_font, anchor=tk.W, width=428)
        self.settings_pcspec_original_label.grid(row=1, column=0)
        self.settings_pcspec_textbox = customtkinter.CTkEntry(
            self.settings_pcspec_frame, placeholder_text="PCのスペックを入力", width=428, font=self.ui_font)
        self.settings_pcspec_textbox.grid(row=2, column=0, pady=2)

        self.settings_sleep_frame = customtkinter.CTkFrame(
            self.settings_frame, fg_color="transparent")
        self.settings_sleep_frame.grid(row=3, column=0, padx=20, pady=8)
        self.settings_sleep_info_label = customtkinter.CTkLabel(
            self.settings_sleep_frame, text="待機時間の変更", font=self.title_font, anchor=tk.W, width=428)
        self.settings_sleep_info_label.grid(row=0, column=0)
        self.settings_sleep_original_label = customtkinter.CTkLabel(
            self.settings_sleep_frame, text="現在の待機時間 : " + General.pclist["sleep"], font=self.ui_font, anchor=tk.W, width=428)
        self.settings_sleep_original_label.grid(row=1, column=0)
        self.settings_sleep_textbox = customtkinter.CTkEntry(
            self.settings_sleep_frame, placeholder_text="待機時間を秒単位で入力", width=428, font=self.ui_font)
        self.settings_sleep_textbox.grid(row=2, column=0, pady=2)

        self.settings_button_frame = customtkinter.CTkFrame(
            self.settings_frame, fg_color="transparent")
        self.settings_button_frame.grid(row=4, column=0, pady=8)

        self.settings_save_button = customtkinter.CTkButton(
            self.settings_button_frame, text="保存", font=self.button_font, command=self.settings_save_check)
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
                        appname + " | 入力値の確認", "待機時間が非常に長いようです。\nこのまま保存した場合、次回起動時になかなか起動しないなどの問題が発生する可能性があります。\n保存しますか？")
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
                    appname + " | 入力値のエラー", "待機時間に入力された値は無効です。\n自然数で入力してから、もう一度お試しください。")

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