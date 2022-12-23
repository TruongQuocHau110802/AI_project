# Khai báo và sử dụng các thư viện sau
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter.filedialog import *
from tkinter.messagebox import *
import time
import numpy as np
import os
import cv2
from tensorflow.keras.utils import load_img, img_to_array
from keras.models import load_model
Label1 = ''
Frame1 = ''
file =''
model_CNN = ''
os.environ['TF CPP MIN LOG LEVEL'] = '2'
model_CNN = load_model('musical.h5')
def GUI_2():
	global Frame1,Label4
	GUI_2 = Tk()
	GUI_2.geometry('500x650+430+50')
	GUI_2.resizable(False,False)
	GUI_2.title('Musical instrument identification')
	GUI_2.wm_iconbitmap("img/AIlogo.ico")
	canvas0 = Canvas(GUI_2, width = 500, height = 650)
	LabelFrame1 = LabelFrame(canvas0,bg = 'aqua',width = 499, height = 650)
	Frame1 = Frame(LabelFrame1,bg = 'white',width = 489, height = 490)
	Label3 = Label(LabelFrame1,text = "Result:",font = ('Arial',16),bg = 'aqua').place( x = 10, y = 600)
	Label4 = Label(LabelFrame1,text = "Status:",font = ('Arial',16),bg = 'aqua').place( x = 10, y = 560)
	Label3_value = Entry(LabelFrame1,width = 20,font = ('Arial',16))
	Label4_value = Entry(LabelFrame1,width = 20,font = ('Arial',16))
	canvas0.pack(fill = BOTH)
	LabelFrame1.place(x = 1, y = 0)
	Frame1.place(x  = 3, y = 3)
	Label3_value.place(x = 100, y = 600)
	Label4_value.place(x = 100, y = 560)
	def openfile():
		cancel()
		global Label1,Frame1,file
		file = askopenfilename(defaultextension = '.jpg',filetypes = [('All Files','*.*'),('JPG Files','*.jpg'),('PNG Files','*.png')])
		if file == '':
			showinfo('Notice','Please choose a photo!')
		else:
			openfile = Image.open(file)
			n_openfile = openfile.resize((485,490), Image.Resampling.LANCZOS)
			showfile = ImageTk.PhotoImage(n_openfile)
			Label1 = Label(Frame1,image = showfile)
			Label1.pack()
			mainloop()
	def cancel():
		global Label1,Frame1,file
		if Label1 == '':
			return
		else:
			Label1.destroy()
		file = ''
		Frame1.configure()
		Label3_value.delete(0,END)
		Label4_value.delete(0,END)
	def check():
		Frame1.configure()
		Label3_value.delete(0,END)
		Label4_value.delete(0,END)		
		global file,Label4,model_CNN
		if file =='':
			showinfo('Notice','Please choose a photo!')
		else:
			def Processing():
				img = load_img(file,target_size =(300,300))
				img = img_to_array(img)
				img = img.astype('float32')
				img = img/255
				img = np.expand_dims(img,axis=0)
				result = model_CNN.predict(img)
				classname = ['Sao truc', 'Song loan',"Dan T'rung",'Dan bau','Dan co','Dan nguyet',
				'Dan sen','Dan tranh','Dan ty ba','Dan day']
				for i in range (0,10):
					if round(result[0][i])== 1:
						prediction = classname[i]
				a = f"This is '{prediction}'"
				Label3_value.insert(0,a)
				Label4_value.insert(0,'Done')
			Processing()
	def camera():
		cancel()
		showinfo('Notice','Press SPACE to shoot and press ESC to exit!')
		global Label1,Frame1,file
		cam = cv2.VideoCapture(0)
		cv2.namedWindow("Camera")
		img_counter = 0
		folder = 'D:/Hau/AI/nhac_cu/code/capture'
		while True:
		    ret, frame = cam.read()
		    if not ret:
		        print("failed to grab frame")
		        break
		    cv2.imshow("Camera", frame)
		    k = cv2.waitKey(1)
		    if k%256 == 27:
		        # ESC pressed
		        showinfo('Notice','Got out of the camera!')
		        break
		    elif k%256 == 32:
		        # SPACE pressed
		        img_name = "opencv_frame_{}.jpg".format(img_counter)
		        cv2.imwrite(f'{folder}/{img_name}', frame)
		        img_counter += 1
		        showinfo('Notice','Photo was taken!')
		        file = f'{folder}/{img_name}'		       
		        if file == '':
		        	break
		        else:
		        	cv2.destroyAllWindows()
		        	cam.release()
		        	openfile = Image.open(file)
		        	n_openfile = openfile.resize((485,490), Image.Resampling.LANCZOS)
		        	showfile = ImageTk.PhotoImage(n_openfile)
		        	Label1 = Label(Frame1,image = showfile)
		        	Label1.pack()
		        	mainloop()
		cam.release()
		cv2.destroyAllWindows()
	button_camera = Button(LabelFrame1, text = 'Camera',width = 6,font = ('Arial', 16),command = camera)
	button_camera.place(x = 130, y = 510)
	button_upload = Button(LabelFrame1, text = 'Upload',width = 6,font = ('Arial', 16),command = openfile)
	button_upload.place(x = 220, y = 510)
	button_check = Button(LabelFrame1, text = 'Check',width = 6,font = ('Arial', 16),command = check)
	button_check.place(x = 310, y = 510)
	button_cancel = Button(LabelFrame1, text = 'Cancel',width = 6,font = ('Arial', 16), command = cancel)
	button_cancel.place(x = 400, y = 510)
	mainloop()
def open_GUI_1():
	GUI_1 = Tk()
	GUI_1.geometry('500x400+430+180')
	GUI_1.resizable(False,False)
	GUI_1.title('Musical instrument identification')
	GUI_1.wm_iconbitmap("img/AIlogo.ico")
	canvas = Canvas(GUI_1, width=500, height=400)
	img = ImageTk.PhotoImage(Image.open("img/GUI.jpg"))
	canvas.create_image(0,0,anchor = NW,image = img)
	canvas.pack()
	def open_GUI_2():
		quit_application()
		GUI_2()
	def quit_application():
		GUI_1.destroy()
	button_next = Button(GUI_1, text = 'Next',width = 5,font = ('Arial', 16) ,command = open_GUI_2).place(x = 330, y = 350)
	button_cancel = Button(GUI_1, text = 'Cancel',width = 5,font = ('Arial', 16), command = quit_application).place(x = 420, y = 350)
	mainloop()
open_GUI_1()
