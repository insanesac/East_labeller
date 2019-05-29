#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 14:40:08 2019

@author: insanesac
"""

import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Button, Canvas, NW, messagebox, Frame, Entry, Label
import cv2, os
import numpy as np

direc = r'/home/insanesac/Desktop/tags/'
files = os.listdir(direc)
files = [x for x in files if 'txt' not in x]
path0 = direc+files[0]

r,c = 700,300
i = 0
j = 1
def tagImage():
    print('Calling East')

def validImage():
    global direc, files, i, innercanvas, area, cropped, crop1, crp_img, label_list
    path = direc+files[i]
    cropped,label_list = validator(path)
    
    B5 = Button(w, text='Next', command=nextCropButton).place(x =  c + 500, y = r/2 - 50)
    B6 = Button(w, text='Prev', command=prevCropButton).place(x =  c + 590, y = r/2 - 50) 
    crop1 = cropped[0]
    crp_img = ImageTk.PhotoImage(Image.fromarray(crop1))
    innercanvas.itemconfig(area, image = crp_img)
    label1 = label_list[0]
    innercanvas1.itemconfig(area, text = label1)
    entry = Entry(w,bd=5)
    entry.place(x = 850,y=200)
    
def validator(imgp):
    global canvas
    cropped = []
    label_list = []
    val_img_path = imgp
    val_base = val_img_path.split('.')[0]
    val_txt = val_base + '.txt'
    val_img = cv2.imread(val_img_path)
    with open(val_txt,'r') as t:
        lines = t.readlines()
    for i,line in enumerate(lines):
        split_line = line.split(',')
        y1,x1,y2,x2,y3,x3,y4,x4,label = split_line[:9]
                
        cropped.append(val_img[int(x1)-2:int(x3)+2,int(y1)-2:int(y3)+2]) 
        label_list.append(label)
        
    return cropped, label_list
    
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

def nextCropButton():
    global j,cropped
    j+=1
    if j >= len(cropped):
        messagebox.showinfo('ERROR','No new cropped ROI')
        j-=1
    else:
        w.after(10,update_crop)

def prevCropButton():
    global j,cropped
    j-=1
    if j < 0:
        messagebox.showinfo('ERROR','No Previous cropped ROI')
        j+=1
    else:
        w.after(10,update_crop)
        
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

def update_crop():
        global cropped, crop1, crp_img, area,innercanvas,label_list,innercanvas1
        crop1 = cropped[j]
        crp_img = ImageTk.PhotoImage(Image.fromarray(crop1))
        innercanvas.itemconfig(area, image = crp_img)
        label1 = label_list[j]
        innercanvas1.itemconfig(area, text = label1)
        
    
        
w = tk.Tk()
img = ImageTk.PhotoImage(resize_img(Image.open(path0)))  
#frame = Frame(w, ,width = 700, height = 250, bd = 1)
#frame.pack()
name = Label(w, text = "Name").place(x = 600,y = 150)  
canvas = Canvas(w, width = c+800, height = r+50)  
area = canvas.create_image(20, 20, anchor=NW, image=img) 
canvas.pack()
crop = cv2.imread(path0)[:60,:300,:]
crop[crop != 217] = 0
r_c,c_c = crop.shape[:2]
crop = ImageTk.PhotoImage(resize_img(Image.fromarray(crop))) 

innercanvas = Canvas(w, width=c_c, height=r_c)
canvas.create_window(350, 200, anchor=NW, window=innercanvas)
innerarea = innercanvas.create_image(0,0, anchor=NW)
innercanvas.place()

innercanvas1 = Canvas(w, width=c_c, height=r_c)
canvas.create_window(650, 200, anchor=NW, window=innercanvas1)
innerarea1 = innercanvas1.create_text(0,0, anchor=NW)
innercanvas1.place()



B0 = Button(w, text='Tagger', command=tagImage).place(x =  c + 120, y = 20 )
B1 = Button(w, text='Validator', command=validImage).place(x =  c + 320, y = 20 )
B2 = Button(w, text='Next', command=nextButton).place(x =  c + 290, y = r )
B3 = Button(w, text='Prev', command=prevButton).place(x =  c + 205, y = r ) 
B4 = Button(w, text="Quit", command=w.destroy).place(x =  c + 380, y = r )



w.mainloop()   