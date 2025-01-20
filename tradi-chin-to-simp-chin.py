import tkinter as tk
import opencc

def convert_text():
    text = text_box.get("1.0", "end-1c")
    converter = opencc.OpenCC('t2s')  # s2t: Simplified to Traditional
    simplified_text = converter.convert(text)
    text_box.delete("1.0", "end")
    text_box.insert("1.0", simplified_text)

# 创建主窗口
window = tk.Tk()
window.title("繁体转简体转换器")

# 创建文本框
text_box = tk.Text(window, height=10, width=40)
text_box.pack()

# 创建转换按钮
convert_button = tk.Button(window, text="转换", command=convert_text)
convert_button.pack()

window.mainloop()