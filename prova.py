import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import customtkinter as ctk
import os

class MaiDiaryClass():
    def __init__(self, master):
        self.master = master
        self.master.title("MaiDiary")
        self.master.geometry("800x600")
        self.master.resizable(False, False)
        self.master.iconbitmap("icon.ico")

        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill="both", expand=True)

        self.frame1 = ttk.Frame(self.notebook)
        self.notebook.add(self.frame1, text="Diary")

        self.frame2 = ttk.Frame(self.notebook)
        self.notebook.add(self.frame2, text="Graphs")

        self.frame3 = ttk.Frame(self.notebook)
        self.notebook.add(self.frame3, text="Settings")

        self.create_widgets()
    
    def create_widgets(self):
        self.create_widgets_frame1()
        self.create_widgets_frame2()
        self.create_widgets_frame3()

    def create_widgets_frame1(self):
        self.text = tk.Text(self.frame1, wrap="word")
        self.text.pack(fill="both", expand=True)
        self.text.tag_configure("center", justify="center")
        self.text.tag_add("center", "1.0", "end")
        self.text.bind("<Control-S>", self.save_diary)
        self.text.bind("<Control-O>", self.save_diary)

    def create_widgets_frame2(self):
        self.button = ttk.Button(self.frame2, text="Plot", command=self.plot)
        self.button.pack()

    def create_widgets_frame3(self):
        self.label = ttk.Label(self.frame3, text="Settings")
        self.label.pack()

    def save_diary(self, event):
        if event.keysym == "s":
            filename = "diary.txt"
            with open(filename, "w") as file:
                file.write(self.text.get("1.0", "end"))
            messagebox.showinfo("Save", "Diary saved successfully!")
        elif event.keysym == "o":
            messagebox.showinfo("Open", "Diary opened successfully!")

    def plot(self):
        x = [1, 2, 3, 4, 5]
        y = [1, 4, 9, 16, 25]
        fig, ax = plt.subplots()
        ax.plot(x, y)
        canvas = FigureCanvasTkAgg(fig, master=self.frame2)
        canvas.draw()
        canvas.get_tk_widget().pack()

def main():
    root = tk.Tk()
    app = MaiDiaryClass(root)
    root.mainloop()

if __name__ == "__main__":
    main()