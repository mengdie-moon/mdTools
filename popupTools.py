"""
@Author   : 梦蝶
@Contact  : 3257053519@qq.com
@CallMe   : 3257053519
@Copyright: (c) 2025 by 梦蝶, Inc. All Rights Reserved.
"""
from mdToolsError import mdToolsErros
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Optional, Callable

class mdTools_popup:
    def __init__(self):
        self._init_tk()
    
    def _init_tk(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def MPopup_messagebox(self, content: str, title: Optional[str] = "提示", type: str = "info") -> Optional[bool]:
        """
        :param content: 弹窗内容（必传）
        :param title: 弹窗标题（默认"提示"）
        :param type: 弹窗类型（info/warning/error/askokcancel/askquestion，默认info）
        :return: 确认类弹窗返回bool，其他返回None
        """
        if not content:
            raise mdToolsErros("ToolsError: Pop up content cannot be empty")
        
        popup_map = {
            "info": lambda: messagebox.showinfo(title, content),
            "warning": lambda: messagebox.showwarning(title, content),
            "error": lambda: messagebox.showerror(title, content),
            "askokcancel": lambda: messagebox.askokcancel(title, content),
            "askquestion": lambda: messagebox.askquestion(title, content)
        }
        
        try:
            handler = popup_map[type.lower()]
        except KeyError:
            raise mdToolsErros(f"ToolsError: Unsupported pop-up window type: {type}")
        
        result = handler()
        
        return {
            "askokcancel": lambda: result is True,
            "askquestion": lambda: result == "yes"
        }.get(type, lambda: None)()
    
    def MPopup_prompt(self, prompt: str, title: Optional[str] = "Prompt Popup", isPassword: bool = False, validate: Optional[Callable[[str], bool]] = None) -> Optional[str]:
        """
        :param prompt: 输入框提示信息
        :param title: 弹窗标题（默认"Prompt Popup"）
        :param isPassword: 是否为密码模式（默认False）
        :param validate: 自定义验证函数，传入用户输入的字符串，返回True表示验证通过，返回False表示验证失败
        :return: 用户输入的字符串，如果用户取消则返回None
        """
        if not prompt:
            raise mdToolsErros("ToolsError: Prompt message cannot be empty")
        
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        
        style = ttk.Style()
        style.configure('TLabel', font=('微软雅黑', 12))
        style.configure('TEntry', font=('微软雅黑', 12), padding=4)
        style.configure('TButton', font=('微软雅黑', 12), padding=6)
        
        dialog.grid_columnconfigure(0, weight=1)
        dialog.grid_rowconfigure(0, weight=1)
        
        label = ttk.Label(dialog, text=prompt, style='TLabel')
        label.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        
        entry = ttk.Entry(dialog, show='*' if isPassword else '', font=('微软雅黑', 12), width=30)
        entry.grid(row=1, column=0, padx=10, pady=5, sticky='ew')
        entry.focus_set()
        
        error_label = ttk.Label(dialog, text="", foreground="red", style='TLabel')
        error_label.grid(row=2, column=0, padx=10, pady=5, sticky='ew')
        
        def on_ok():
            user_input = entry.get()
            if validate:
                if not validate(user_input):
                    error_label.config(text="Invalid input")
                    return
            dialog.destroy()
            self.result = user_input
        
        def on_cancel():
            dialog.destroy()
            self.result = None
        
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=3, column=0, padx=10, pady=10, sticky='ew')
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        
        ok_button = ttk.Button(button_frame, text="Confirm", command=on_ok, style='TButton')
        ok_button.grid(row=0, column=0, padx=10, pady=5, sticky='ew')
        
        cancel_button = ttk.Button(button_frame, text="Cancel", command=on_cancel, style='TButton')
        cancel_button.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
        
        dialog.bind('<Return>', lambda event: on_ok())
        dialog.bind('<Escape>', lambda event: on_cancel())
        
        dialog.grab_set()
        dialog.wait_window()
        
        return self.result

    def cleanup(self):
        self.root.destroy()