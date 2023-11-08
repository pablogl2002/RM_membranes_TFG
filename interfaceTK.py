import re
import tkinter as tk
from tkinter import scrolledtext


def get_code():
    l = [a for a in code_textbox.get("1.0", "end-1c").split("\n|\t") if a != '']
    print(l)

root = tk.Tk()
#root.geometry("1200x675")

code_textbox = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=30)
#code_textbox.pack(fill=tk.BOTH, side="left")

code_textbox.grid(row=0, column=0, padx=5, pady=5)

# inst_textbox = tk.Text(root, height=15)
# inst_textbox.insert("1.0", "suc(i)\npre(i)")
# inst_textbox.configure(state='disabled')
# #inst_textbox.pack(side="right")
# inst_textbox.grid(row=0, column=1, padx=5, pady=5)

button = tk.Button(root, text="EJECUTAR", bg="blue", fg="white", command=get_code)
#button.pack(side=tk.RIGHT, pady=10)
button.grid(row=1,column=0,padx=5,pady=5)


root.mainloop()
