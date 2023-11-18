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
import pickle
import socket
import time
import platform
import tkinter as tk
from tkinter import messagebox


ver = "1.0"
appname = "which_my_pc"
token = ""
lib_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "lib")
img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "img")

class List():
    file_name = "which_my_config.pkl"
    file_path = "./lib/" + file_name


if not os.path.isfile(List.file_path):
    if platform.system() == "Windows" and platform.release() == "10":
        reversion = platform.version().replace(".", "")
        if int(reversion) >= 10020000:
            pcos = "Windows 11"
        else:
            pcos = "Windows 10"
    else:
        pcos = platform.system() + " " + str(platform.release())

    dummylist = {
        "hostname": socket.gethostname(),
        "pcos": pcos,
        "pcname": socket.gethostname() + " | " + pcos,
        "pcspec": "no data",
        "sleep": "5"
    }

    with open(List.file_path, "wb") as list_write:
        pickle.dump(dummylist, list_write)

with open(List.file_path, "rb") as list_read:
    pclist = pickle.load(list_read)


class Status():
    def __init__(self):
        self.loop = 1
        self.exitflag = threading.Event()

    def run(self):
        time.sleep(int(pclist["sleep"]))
        try:
            ds_token = ds.Discord(token, ds.CreateFlags.default)
            ds_activity_manager = ds_token.get_activity_manager()
            ds_activity = ds.Activity()
            ds_activity.details = pclist["pcname"]
            ds_activity.state = pclist["pcspec"]
            ds_activity.party.id = "whichmypc"
            ds_activity.assets.large_image = "main512"
            def callback(result):
                if result == ds.Result.ok:
                    notify_result_ok = Notification(
                        app_id=appname,
                        title="アクティビティをセットしました",
                        msg="アクティビティがセットされました。現在のPCは " + pclist["hostname"] + " です。",
                        icon = img_path + r"\which_ok.png"
                    )
                    notify_result_ok.set_audio(audio.IM, loop=False)
                    notify_result_ok.show()

                    print("アクティビティがセットされました。現在のPCは " + pclist["hostname"] + " です。")
                else:
                    print("error")
                    "raise Exception(result)"

            ds_activity_manager.update_activity(ds_activity, callback)

            while not self.exitflag.is_set():
                time.sleep(1/10)
                ds_token.run_callbacks()

            return

        except:
            notify_result_no = Notification(
                app_id=appname,
                title="アクティビティはセットされていません",
                msg="エラーが発生しました。Discord が起動してからもう一度起動してみてください。",
                icon = img_path + r"\error.png"
            )
            notify_result_no.set_audio(audio.Default, loop=False)
            notify_result_no.show()
            print("エラーが発生しました。Discord が起動してからもう一度起動してみてください。")
            return


class Tray():
    def __init__(self):
        pass

    def run(self):
        def info():
            notify_ver_func()

        def launch_startup():
            subprocess.Popen(["explorer", "shell:startup"])
            notify_startup = Notification(
                app_id=appname,
                title="スタートアップに登録",
                msg="スタートアップ フォルダに " + appname + " のショートカットを作成してください。",
                icon = img_path + r"\info.png"
            )
            notify_startup.set_audio(audio.Default, loop=False)
            notify_startup.show()

        def launch_ui_settings():
            def run_settings():
                if __name__ == "__main__":
                    app = App()
                    app.mainloop()
            settings_thread = threading.Thread(target=run_settings())
            settings_thread.start()


        def which_exit():
            status_stop_thread = threading.Thread(target=status_stop_func())
            status_stop_thread.start()
            status_stop_thread.join()
            self.tray.stop()

        trayicon = Image.open(img_path + r"\logo\which_logo.ico")
        traymenu = Menu(
            MenuItem("バージョン " + ver, info),
            Menu.SEPARATOR,
            MenuItem("PC情報を編集", launch_ui_settings),
            MenuItem("スタートアップに登録", launch_startup),
            Menu.SEPARATOR,
            MenuItem("終了", which_exit)
        )

        self.tray = Icon(name=appname, title=appname,
                         icon=trayicon, menu=traymenu)
        self.tray.run()


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
            self.settings_pcname_frame, text="現在のPCの名前 : " + pclist["hostname"], font=self.ui_font, anchor=tk.W, width=428)
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
            self.settings_pcos_frame, text="現在のOS : " + pclist["pcos"], font=self.ui_font, anchor=tk.W, width=428)
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
            self.settings_pcspec_frame, text="現在のPCのスペック : " + pclist["pcspec"], font=self.ui_font, anchor=tk.W, width=428)
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
            self.settings_sleep_frame, text="現在の待機時間 : " + pclist["sleep"], font=self.ui_font, anchor=tk.W, width=428)
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
        notify_ver_func()

    def settings_save_check(self):
        if self.settings_sleep_textbox.get() == "":
            self.settings_save()
            self.destroy()
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
            else:
                messagebox.showerror(
                    appname + " | 入力値のエラー", "待機時間に入力された値は無効です。\n自然数で入力してから、もう一度お試しください。")

    def settings_save(self):
        if not (self.settings_pcname_textbox.get() == ""):
            pclist["hostname"] = self.settings_pcname_textbox.get()
            pclist["pcname"] = self.settings_pcname_textbox.get() + \
                " | " + pclist["pcos"]

        if not (self.settings_pcos_textbox.get() == ""):
            pclist["pcos"] = self.settings_pcos_textbox.get()
            pclist["pcname"] = pclist["hostname"] + \
                " | " + self.settings_pcos_textbox.get()

        if not (self.settings_pcspec_textbox.get() == ""):
            pclist["pcspec"] = self.settings_pcspec_textbox.get()

        if not (self.settings_sleep_textbox.get() == ""):
            pclist["sleep"] = self.settings_sleep_textbox.get()

        with open(List.file_path, "wb") as list_write:
            pickle.dump(pclist, list_write)

        print(pclist)

        notify_edit = Notification(
            app_id=appname,
            title="変更を保存しました",
            msg="変更を反映させるには、 " + appname + " を再起動してください。",
            icon = img_path + r"\info.png"
        )
        print(img_path + r"\info.png")
        notify_edit.set_audio(audio.Default, loop=False)
        notify_edit.show()


def notify_ver_func():
    notify_ver = Notification(
        app_id = appname,
        title = "バージョン " + ver,
        msg = "for Windows" + "\n日本語",
        icon = img_path + r"\logo\which_logo128.png"
    )
    notify_ver.set_audio(audio.Default, loop=False)
    notify_ver.show()


if __name__ == "__main__":
    status_instance = Status()
    tray_instance = Tray()

    def status_thread_func():
        status_instance.run()

    def tray_thread_func():
        tray_instance.run()

    def status_stop_func():
        status_instance.exitflag.set()
        status_thread.join()

    status_thread = threading.Thread(target=status_thread_func)
    tray_thread = threading.Thread(target=tray_thread_func)

    status_thread.start()
    tray_thread.start()