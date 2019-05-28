#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 14:40:08 2019

@author: insanesac
"""

import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Button, Canvas, NW, messagebox
import cv2, os

direc = r'/home/insanesac/Desktop/tags/'
files = os.listdir(direc)
i=0

def nextButton():
    global i,files,direc
    i+=1
    if i >= len(files):
        msg = messagebox.showinfo('ERROR','No Next Image')
        i-=1
#        w.destroy()
    else:
        w.after(10,update_image)

def prevButton():
    global i,files,direc
    i-=1
    if i < 0:
        msg = messagebox.showinfo('ERROR','No Previous Image')
        i+=1
    else:
        w.after(10,update_image)

def update_image():
        global tkimg1,canvas,area,i,direc,files
        path = direc + files[i]
        tkimg1 = ImageTk.PhotoImage(Image.open(path))
        canvas.itemconfig(area, image = tkimg1)
        canvas.after(1000, update_image)
 
w = tk.Tk()
path0 = direc+files[0]
img = ImageTk.PhotoImage(Image.open(path0))  
cv_img = cv2.imread(path0)
r,c = cv_img.shape[:2]
canvas = Canvas(w, width = c+500, height = r+50)  
area = canvas.create_image(20, 20, anchor=NW, image=img) 
canvas.pack()
          
B1 = Button(w, text='Next', command=nextButton).place(x =  c+ 290, y = r )
B2 = Button(w, text='Prev', command=prevButton).place(x =  c+ 205, y = r ) 
w.mainloop()   