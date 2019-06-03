#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 14:40:08 2019

@author: insanesac
"""

import tkinter as tk
from tkinter import * #Button, Canvas, NW, messagebox, Frame, Entry, Label
import cv2, os
import numpy as np
from PIL import Image, ImageTk

direc = r'/home/insanesac/Desktop/tags/'
files = os.listdir(direc)
files = [x for x in files if 'txt' not in x]
path0 = os.path.join(direc,files[0])

r,c = 700,300
i = 0
j = 1
state = 0
count = 0
right_click_number = 0
left_click_number = 0
x1,y1 = [],[]

def draw_line(event):
    global right_click_number, left_click_count, count
    global x1,y1
    global canvas_id
    right_click_number+=1
    x1.append(event.x)
    y1.append(event.y)
    print(x1)
    print(y1)
    
    if right_click_number == 4:
        print(1)
    
def autoTrain():
    print('Calling East')

def manualTrain():
    canvas.bind('<Button-1>',draw_line)
    print('loading annotator')

def dispButton():
#    global B0,B1,B8,B9, B10
    B0.place(x =  c + 120, y = 20 )
    B1.place(x =  c + 320, y = 20 )
    B8.place_forget()
    B9.place_forget()
    B10.place_forget()
    
def tagImage():
    global B0,B1,B8,B9, B10
    B0.place_forget()
    B1.place_forget()
    B8 = Button(w, text='Auto', command=autoTrain)
    B8.place(x =  c + 120, y = 20 )
    B9 = Button(w, text='Manual', command=manualTrain)
    B9.place(x =  c + 220, y = 20) 
    B10 = Button(w, text='Back', command=dispButton)
    B10.place(x =  c + 320, y = 20) 
    

def fix_entry():
    global val_txt, j, cordinates, new_text, state
    if state == 0:
        j-=1
    with open(val_txt,'r') as t1:
        lines_fix = t1.readlines()
    print(j)
    print(cordinates[j])
    yn1,xn1,yn2,xn2,yn3,xn3,yn4,xn4 = cordinates[j].split(',')
    ordered_text = [yn1,xn1,yn2,xn2,yn3,xn3,yn4,xn4,new_text+'\n']
    ordered_text = ",".join(ordered_text)
    lines_fix[j]  = ordered_text
    
    os.remove(val_txt)
    
    with open(val_txt,'w') as t2:
        for lf in lines_fix:
            print(type(lf))
            print(lf)
            t2.write("%s"%lf)
            
    print('Over Written')
            
def getData():
    global entry, new_text
    new_text = None
    new_text = entry.get()
    fix_entry()
    
def validImage():
    global direc, files, i, innercanvas, area, cropped, crop1, crp_img, label_list
    global cnt, canvas, new_img, new_text, entry, cordinates
#    global B0,B1
#    B0.place_forget()
#    B1.place_forget()
    path = os.path.join(direc,files[i])
    
    B5 = Button(w, text='Next', command=nextCropButton)
    B5.place(x =  c + 590, y = r/2 - 50)
    B6 = Button(w, text='Prev', command=prevCropButton)
    B6.place(x =  c + 500, y = r/2 - 50) 
    
    cropped,label_list, cnt,cordinates = validator(path)
    
    new_img = ImageTk.PhotoImage(resize_img(Image.fromarray(cnt[0])))
    canvas.itemconfig(area, image = new_img)
    
    crop1 = cropped[0]
    crp_img = ImageTk.PhotoImage(Image.fromarray(crop1))
    innercanvas.itemconfig(area, image = crp_img)
    label1 = label_list[0]
    innercanvas1.itemconfig(area, text = label1)
    entry = Entry(w,bd=5)
    entry.place(x = 850,y=200)
    
    B7 = Button(w, text ="Submit", command = getData)
    B7.place(x =  c + 680, y = r/2 - 50)
    
     
    
def validator(imgp):
    global canvas, val_img, imgn, val_txt,cordinates
    cropped = []
    cnt = []
    label_list = []
    cordinates = []
    
    val_img = None
    val_img_path = imgp
    val_base = val_img_path.split('.')[0]
    val_txt = val_base + '.txt'
    val_img = cv2.imread(val_img_path)
    
    with open(val_txt,'r') as t:
        lines = t.readlines()
        
    for i,line in enumerate(lines):
        imgn = val_img.copy()
        split_line = line.split(',')
        y1,x1,y2,x2,y3,x3,y4,x4,label = split_line[:9]
        
        sub1 = abs(int(y1) - int(y3))
        sub2 = abs(int(x1) - int(x3)) 
        
        if sub1 > sub2:        
            cnt.append(cv2.rectangle(imgn,(int(y1),int(x1)),(int(y3),int(x3)),(0,200,0),3))
            cropped.append(val_img[int(x1)-2:int(x3)+2,int(y1)-2:int(y3)+2])
            cord = [y1,x1,y2,x2,y3,x3,y4,x4]
        else:
            cnt.append(cv2.rectangle(imgn,(int(x1),int(y1)),(int(x3),int(y3)),(0,200,0),3))
            cropped.append(val_img[int(y1)-2:int(y3)+2,int(x1)-2:int(x3)+2]) 
            cord = [x1,y1,x2,y2,x3,y3,x4,y4]
         
        cordinates.append(",".join(cord))
        label_list.append(label)

    return cropped, label_list, cnt,cordinates
    
def nextButton():
    global files, i, j
    i+=1
    j = 0
    if i >= len(files):
        messagebox.showinfo('ERROR','No Next Image')
        i-=1
    else:
        w.after(10,update_image)

def prevButton():
    global files, i, j 
    i-=1
    j = 0
    if i < 0:
        messagebox.showinfo('ERROR','No Previous Image')
        i+=1
    else:
        w.after(10,update_image)

def nextCropButton():
    global j,cropped, state
    j+=1
    state = 0
    if j >= len(cropped):
        messagebox.showinfo('ERROR','No new cropped ROI')
        j-=1
    else:
        w.after(10,update_crop)
        state = 1

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
    path = os.path.join(direc, files[i])
    pil_img = Image.open(path)
    tkimg1 = ImageTk.PhotoImage(resize_img(pil_img))
    canvas.itemconfig(area, image = tkimg1)

def update_crop():
    global cropped, crop1, crp_img, area,innercanvas,label_list,innercanvas1
    global tkimg2, canvas, area, cnt, current_img
    crop1 = cropped[j]
    crp_img = ImageTk.PhotoImage(Image.fromarray(crop1))
    innercanvas.itemconfig(area, image = crp_img)
    label1 = label_list[j]
    innercanvas1.itemconfig(area, text = label1)
    current_img = cnt[j]
    tkimg2 = ImageTk.PhotoImage(resize_img(Image.fromarray(current_img)))
    canvas.itemconfig(area, image = tkimg2)
        
    
        
w = tk.Tk()
img = ImageTk.PhotoImage(resize_img(Image.open(path0)))  
#frame = Frame(w, ,width = 700, height = 250, bd = 1)
#frame.pack()
w.geometry('900x900')
canvas = Canvas(w, width = c, height = r)  
area = canvas.create_image(20, 20, anchor=NW, image=img) 
canvas.pack(side=LEFT)
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



B0 = Button(w, text='Tagger - WiP', command=tagImage)
B0.place(x =  c + 120, y = 20 )
B1 = Button(w, text='Validator', command=validImage)
B1.place(x =  c + 320, y = 20 )
B2 = Button(w, text='Next', command=nextButton)
B2.place(x =  c + 290, y = r )
B3 = Button(w, text='Prev', command=prevButton)
B3.place(x =  c + 205, y = r ) 
B4 = Button(w, text="Quit", command=w.destroy)
B4.place(x =  c + 380, y = r )



w.mainloop()   