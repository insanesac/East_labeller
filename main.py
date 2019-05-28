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
import numpy as np

direc = r'/home/insanesac/Desktop/tags/'
files = os.listdir(direc)
files = [x for x in files if 'txt' not in x]
i=0

def tagImage():
    print('Calling East')

def validImage():
    global direc, files, i
    path = direc+files[i]
    cropped = validator(path)
    print(len(cropped))

def validator(imgp):
    cropped = []
    val_img_path = imgp
    print(val_img_path)  
    val_base = val_img_path.split('.')[0]
    print(val_base)
    val_txt = val_base + '.txt'
    val_img = cv2.imread(val_img_path)
    with open(val_txt,'r') as t:
        lines = t.readlines()
    for i,line in enumerate(lines):
        split_line = line.split(',')
        y1,x1,y2,x2,y3,x3,y4,x4,label = split_line[:9]
#        cv2.rectangle(img,(int(x1),int(y1)),(int(x3),int(y3)),(0,200,0),3)
                
        cropped.append(val_img[int(x1):int(x3),int(y1):int(y3)])    
    return cropped
    
def nextButton():
    global files, i
    i+=1
    if i >= len(files):
        messagebox.showinfo('ERROR','No Next Image')
        i-=1
    else:
        w.after(10,update_image)

def prevButton():
    global files, i
    i-=1
    if i < 0:
        messagebox.showinfo('ERROR','No Previous Image')
        i+=1
    else:
        w.after(10,update_image)

def resize_img(pil_img):
    global r,c
    basewidth = c
    c1,r1 = pil_img.size
    if r1 > 720 or c1 > 320:
        wpercent = (basewidth/float(pil_img.size[0]))
        hsize = int((float(pil_img.size[1])*float(wpercent)))
        pil_img = pil_img.resize((basewidth,hsize), Image.ANTIALIAS)
        return pil_img
    else:
        return pil_img
    
def update_image():
        global tkimg1, canvas, area, direc, files, i
        path = direc + files[i]
        pil_img = Image.open(path)
        tkimg1 = ImageTk.PhotoImage(resize_img(pil_img))
        canvas.itemconfig(area, image = tkimg1)
        
w = tk.Tk()
path0 = direc+files[0]
r,c = 700,300
img = ImageTk.PhotoImage(resize_img(Image.open(path0)))  
canvas = Canvas(w, width = c+500, height = r+50)  
area = canvas.create_image(20, 20, anchor=NW, image=img) 
canvas.pack()

B0 = Button(w, text='Tagger', command=tagImage).place(x =  c + 120, y = 20 )
B1 = Button(w, text='Validator', command=validImage).place(x =  c + 320, y = 20 )
B2 = Button(w, text='Next', command=nextButton).place(x =  c+ 290, y = r )
B3 = Button(w, text='Prev', command=prevButton).place(x =  c+ 205, y = r ) 

w.mainloop()   