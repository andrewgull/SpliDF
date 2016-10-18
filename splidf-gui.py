#!/usr/bin/python3
import pandas as pd
import numpy as np
import os
import sys
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askokcancel
from tkinter import messagebox


def dir_creator():
    wdir = "STADS_results"
    if not os.path.exists(wdir):
        os.makedirs(wdir)
    os.chdir(wdir)
    return

def ask_file():
    ftypes = [('text files', '*.csv'), ('All files', '*')]
    file = askopenfilename(filetypes=ftypes)
    if file == '':
        messagebox.showerror("Ошибка", "Вы не выбрали таблицу")
    handle = open("file.tmp", 'w')
    handle.write(file)
    handle.close()

def write_column(entry, popup):
    par_tmp = open('par.tmp', 'w')
    if entry.get() == '':
        messagebox.showerror("Ошибка", "Вы не ввели параметр")
    par_tmp.write(entry.get())  # retrieve text from entry object
    par_tmp.close()
    popup.destroy()

def ask_column():
    popup = Tk()
    popup.wm_title("STADS")
    row = Frame(popup)  # create new row
    lab = Label(row, width=12, text='Параметр')  # add label
    ent = Entry(row, width=12)
    row.pack(side=TOP, fill=X)
    lab.pack(side=LEFT, fill=X)
    ent.pack(side=RIGHT, expand=YES, fill=X)
    popup.bind('<Return>', lambda event: write_column(ent, popup))
    Button(popup, text='Ok', command=(lambda: write_column(ent, popup))).pack()
    popup.grab_set()
    popup.focus_set()
    popup.wait_window()
    popup.mainloop()
    return

def write_range(entry, popup):
    num_tmp = open('num.tmp', 'w')
    num_tmp.write(entry.get())
    num_tmp.close()
    popup.destroy()

def ask_range():
    popup = Tk()
    popup.wm_title("Введите диапазон")
    row = Frame(popup)
    lab = Label(row, width=12, text='от-до')
    ent = Entry(row, width=16)
    row.pack(side=TOP, fill=X)
    lab.pack(side=LEFT)
    ent.pack(side=RIGHT, expand=YES, fill=X)
    popup.bind('<Return>', lambda event: write_range(ent, popup))
    Button(popup, text='Ok', command=(lambda: write_range(ent, popup))).pack()
    popup.grab_set()
    popup.focus_set()
    popup.wait_window()

def run_stads():
    dec_sign = '.'  # to define it only once
    tbl_name = open('file.tmp')
    tbl_path = tbl_name.read()
    par_name = open('par.tmp')
    par = par_name.read()
    try:
        tbl = pd.read_csv(tbl_path, delimiter=",", decimal=dec_sign)
    except OSError:
        messagebox.showerror("Ошибка", "Такой таблицы не существует!")
        sys.exit()
    headers = list(tbl.columns.values)
    while par not in headers:
        messagebox.showinfo("Ошибка", "Такого параметра не существует!")
        ask_column()
    tbl = pd.read_csv(tbl_path, delimiter=",", decimal=dec_sign)
    numbool = tbl.applymap(np.isreal).all()
    if numbool[par]:
        ask_range()
        num_name = open("num.tmp")
        num = num_name.read()
        if num == "":
            fr = min(tbl[par])
            to = max(tbl[par])
        else:
            nums = num.split('-')
            fr = int(nums[0])
            to = int(nums[1])
        subset = tbl.loc[(tbl[par]>=fr) & (tbl[par]<=to),:]
        subset.to_csv(par + num + ".csv", delimiter=',', decimal=dec_sign)
        subset_dscrb = subset.describe().round(2)
        subset_dscrb.to_csv(par + num + "_stat.csv", delimiter=',', decimal=dec_sign)
    else:
        grouped = tbl.groupby(par)
        for group in grouped:
            fname = group[0]+'.csv'
            group[1].to_csv(fname, delimiter=',', decimal=dec_sign)
        grouped_dscrb = grouped.describe().round(2)
        grouped_dscrb.to_csv(par + "_stat.csv", delimiter=',', decimal=dec_sign)

    for item in ['file.tmp', 'par.tmp', 'num.tmp']:
        try:
            os.remove(item)
        except FileNotFoundError:
            pass
    messagebox.showinfo("STADS", "Готово")

def quitter():
    ans = askokcancel('Verify exit', 'Надоело работать?')
    if ans:
        sys.exit()

def main_win():
    root = Tk()
    root.wm_title("STADS")
    tbl_btn = Button(root, text="Выбрать таблицу", width=30, height=3, command=(lambda: ask_file()))
    par_btn = Button(root, text="Ввести параметр", width=30, height=3, command=(lambda: ask_column()))
    strt_btn = Button(root, text="Старт!", width=30, height=3, command=(lambda: run_stads()))
    quit_btn = Button(root, text="Выход", width=30, height=3, command=(lambda: quitter()))
    # settngs_btn = Button(root, text="Настройки", width=30, height=3, command=root.quit())
    tbl_btn.pack(side=TOP, fill=X)
    par_btn.pack(side=TOP, fill=X)
    strt_btn.pack(side=TOP, fill=X)
    quit_btn.pack(side=TOP, fill=X)
    # settngs_btn.pack(side=BOTTOM, expand=YES)
    root.geometry("300x250")
    root.mainloop()

if __name__ == '__main__':
    main_win()
