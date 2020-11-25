import numpy as np
import cv2
import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import database
from datetime import datetime, timedelta
from tkcalendar import DateEntry
import shutil

from multiprocessing import Pool


class mainWindow:

    def __init__(self, window):
        self.window = window
        self.labelFrame = tk.Frame(window, width=330, height=50)
        self.labelFrame.pack_propagate(0)
        self.header = tk.Label(self.labelFrame, text='CDAC1', fg='#777777', font=("Impact", 26), anchor=tk.NW)
        self.header.pack()
        self.labelFrame.pack(side=tk.TOP, fill=tk.X)

        # mainFrame divided in 2 parts for video capture and graph
        self.mainFrame = tk.Frame(window, height=500, width=self.window.winfo_width())
        self.mainFrame.pack_propagate(0)
        # self.mainFrame.bind("<Configure>", self.configure)

        self.imageNb = ttk.Notebook(self.mainFrame,width=600,height=500)

        #tab1 for cam1
        self.VideoFrame1 = tk.Frame(self.imageNb,width=600,height=500)
        # self.imageFrame.pack_propagate(0)
        self.imageNb.add(self.VideoFrame1, text="Cam1")


        #tab2 for cam2
        self.VideoFrame2 = tk.Frame(self.imageNb,width=600,height=500)
        self.imageNb.add(self.VideoFrame2, text="Cam2")

        #tab2 for cam2
        self.VideoFrame3 = tk.Frame(self.imageNb,width=600,height=500)
        self.imageNb.add(self.VideoFrame3, text="Cam3")


        #tab2 for cam2
        self.VideoFrame4 = tk.Frame(self.imageNb,width=600,height=500)
        self.imageNb.add(self.VideoFrame4, text="Cam4")


#4 canvases for 4 tabs ,each canvas is placed inside the respective frame

        self.Canvas1 = tk.Canvas(self.VideoFrame1, width=600, height=500)
        self.Canvas2 = tk.Canvas(self.VideoFrame2, width=600, height=500)
        self.Canvas3 = tk.Canvas(self.VideoFrame3, width=600, height=500)
        self.Canvas4 = tk.Canvas(self.VideoFrame4, width=600, height=500)


#pack the canvas inside the frame
        self.Canvas1.pack(fill="both",expand=1)
        self.Canvas2.pack(fill="both",expand=1)
        self.Canvas3.pack(fill="both",expand=1)
        self.Canvas4.pack(fill="both",expand=1)

        # self.imageNb.pack(expand=1, fill='y')
        self.imageNb.grid(row=0,column=0)
        self.imageNb.bind("<<NotebookTabChanged>>", self.tabchanged)
        self.mainFrame.pack(fill=tk.BOTH, side=tk.TOP)


        #Graph part
        # Frame2 shows graph and is divided in two tabs
        self.Frame2 = ttk.Notebook(self.mainFrame)
        self.graphFrame2 = ttk.Frame(self.Frame2)
        self.Frame2.add(self.graphFrame2, text="Statistics")
        self.graphFrame1 = ttk.Frame(self.Frame2)
        self.Frame2.add(self.graphFrame1, text="Custom input")

        self.InputFrame1 = ttk.Frame(self.graphFrame1, width=300, height=100)
        self.InputFrame1.pack(side=tk.TOP)
        self.inputDate1 = DateEntry(self.InputFrame1, width=12, background='darkblue', foreground='white',
                                    borderwidth=2)
        self.inputDate1.grid(row=0, column=1, padx=2)
        self.inputDate1.focus_set()
        self.label1 = ttk.Label(self.InputFrame1, text="Enter date1")
        self.label1.grid(row=0, column=0)
        self.inputDate2 = DateEntry(self.InputFrame1, width=12, background='darkblue', foreground='white',
                                    borderwidth=2)
        self.inputDate2.grid(row=1, column=1, padx=2)
        self.inputDate2.focus_set()
        self.label2 = tk.Label(self.InputFrame1, text="Enter date2")
        self.label2.grid(row=1, column=0)
        self.button1 = tk.Button(self.InputFrame1, text="Show Graph")
        self.button1.grid(row=3, column=1, padx=30, pady=10)
        self.v = tk.IntVar()
        self.v.set(0)  # initializing the choice, i.e. Python
        options = [
            "Line Graph",
            "Bar Graph"
        ]
        for val, option in enumerate(options):
            tk.Radiobutton(self.InputFrame1,
                           text=option,
                           padx=20,
                           variable=self.v,
                           value=val).grid(row=2, column=val, padx=30)

        self.fig = plt.figure(1, figsize=(10, 8), dpi=55)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graphFrame1)
        self.InputFrame2 = ttk.Frame(self.graphFrame2, width=300, height=100)
        self.InputFrame2.pack(side=tk.TOP)
        self.inputDate3 = DateEntry(self.InputFrame2, width=12, background='darkblue', foreground='white',
                                    borderwidth=2)
        self.inputDate3.grid(row=0, column=1, padx=2)
        self.label3 = ttk.Label(self.InputFrame2, text="Enter date")
        self.label3.grid(row=0, column=0)
        self.button2 = tk.Button(self.InputFrame2, text="Show Graph")
        self.button2.grid(row=4, column=1, padx=30, pady=10)
        self.v1 = tk.IntVar()
        self.v1.set(0)
        options1 = [
            "Line Graph",
            "Bar Graph"
        ]
        for val, option in enumerate(options1):
            tk.Radiobutton(self.InputFrame2,
                           text=option,
                           padx=20,
                           variable=self.v1,
                           value=val).grid(row=2, column=val, padx=30)
        self.v2 = tk.IntVar()
        self.v2.set(0)
        options2 = [
            "Daily",
            "Weekly",
            "Monthly"
        ]
        for val, option in enumerate(options2):
            tk.Radiobutton(self.InputFrame2,
                           text=option,
                           padx=20,
                           variable=self.v2,
                           value=val).grid(row=3, column=val, padx=10)

        self.fig1 = plt.figure(2, figsize=(10, 8), dpi=55)
        self.canvas5 = FigureCanvasTkAgg(self.fig1, master=self.graphFrame2)

        #uncomment below code for ip cameras
        # make four video captures by getting urls from database
        # linkarray = database.getVideoLinks()
        # print(linkarray)
        # self.link_arr = linkarray
        self.cap0 = cv2.VideoCapture(0)
        self.cap1 = cv2.VideoCapture(0)
        self.cap2 = cv2.VideoCapture(0)
        self.cap3 = cv2.VideoCapture(0)

        # 4 connectors for 4 different databases
        self.d1 = database.db("cam1")
        self.d2 = database.db("cam2")
        self.d3 = database.db("cam3")
        self.d4 = database.db("cam4")

        # Progress Bar and refresh button for showing disk space
        self.progressLabel = tk.Label(window, text="Used Space")
        self.progressLabel.pack()
        self.freeSpaceBar = Progressbar(window, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.freeSpaceBar.pack()
        self.refreshButton = tk.Button(window, text="Refresh")
        self.refreshButton.pack()
        self.refreshButton.bind("<Button-1>", self.findSpace)
        self.afterId = 0

        # self.showLiveAll()


    def findSpace(self, event):
        total, used, free = shutil.disk_usage("/")
        self.freeSpaceBar['value'] = (used / total) * 100



    # Function is used to display the default data for the current date
    def func(self, obj):
        self.Frame2.grid(row=0, column=1)
        self.fig.clf()
        plt.figure(1)
        y = obj.currentdata()
        if self.v.get() == 0:
            plt.plot(np.array(y)[:, 1], np.array(y)[:, 0], color='blue')
        else:
            plt.bar(np.array(y)[:, 1], np.array(y)[:, 0], color='blue', width=.5)
        plt.xticks(rotation=45)
        plt.title("Hourly Count", fontsize=10)
        plt.ylabel("No of people", fontsize=10)
        plt.xlabel("Hour", fontsize=10)
        self.canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH, side=tk.TOP)
        # self.canvas.get_tk_widget().grid(row=0, column=0)

        self.canvas.draw()
        self.fig1.clf()
        plt.figure(2)
        if self.v1.get() == 0:
            plt.plot(np.array(y)[:, 1], np.array(y)[:, 0], color='blue')
        else:
            plt.bar(np.array(y)[:, 1], np.array(y)[:, 0], color='blue', width=.5)
        plt.xticks(rotation=45)
        plt.title("Hourly Count", fontsize=10)
        plt.ylabel("No of people", fontsize=10)
        plt.xlabel("Hour", fontsize=10)
        self.canvas5.get_tk_widget().pack(expand=True, fill=tk.BOTH, side=tk.TOP)
        self.canvas5.draw()

    # Used to display video capture for camera1
    def Enlarge1(self):
        try:

            _, frame = self.cap0.read()
            # frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame).resize((600, 500)))
            self.Canvas1.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.Canvas1.create_line(0, 300, 700, 300, fill="green")
            self.Canvas1.create_text(500, 400, text="Apoorv", fill="red")
            self.afterId = self.imageNb.after(15, self.Enlarge1)
        except:
            # self.cap0 = cv2.VideoCapture(self.link_arr[0])
            self.cap0=cv2.VideoCapture(0)
            self.afterId = self.imageNb.after(15, self.Enlarge1)  #collects the id thats required to stop the execution of this function
            #function is stopped and started in self.tabchanged ()


    # Used to display video capture for camera2
    def Enlarge2(self):
        try:

            _, frame = self.cap1.read()
            # frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame).resize((600, 500)))
            self.Canvas2.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.Canvas2.create_line(0, 300, 700, 300, fill="green")
            self.Canvas2.create_text(500, 400, text="Apoorv", fill="red")
            self.afterId = self.imageNb.after(15, self.Enlarge2)
        except:
            # self.cap1 = cv2.VideoCapture(self.link_arr[1])
            self.cap1=cv2.VideoCapture(0)

            self.afterId = self.imageNb.after(15, self.Enlarge2)

    # Used to display video capture for camera3
    def Enlarge3(self):
        try:
            _, frame = self.cap2.read()
            # frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame).resize((600, 500)))
            self.Canvas3.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.Canvas3.create_line(0, 300, 700, 300, fill="green")
            self.Canvas3.create_text(500, 400, text="Apoorv", fill="red")
            self.afterId = self.imageNb.after(15, self.Enlarge3)
        except:
            # self.cap2 = cv2.VideoCapture(self.link_arr[2])
            self.cap2=cv2.VideoCapture(0)

            self.afterId = self.imageNb.after(15, self.Enlarge3)

    # Used to display video capture for camera4
    def Enlarge4(self):
        try:


            _, frame = self.cap3.read()
            # frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame).resize((600, 500)))
            self.Canvas4.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.Canvas4.create_line(0, 300, 700, 300, fill="green")
            self.Canvas4.create_text(500, 400, text="Apoorv", fill="red")
            self.afterId = self.imageNb.after(15, self.Enlarge4)
        except:
            # self.cap3 = cv2.VideoCapture(self.link_arr[2])
            self.cap3=cv2.VideoCapture(0)

            self.afterId = self.imageNb.after(15, self.Enlarge4)


    # Used to display video capture for all cameras
    # def get_multiple_stream(cap):
    #     print("here")
    #     return cap.read()


    def tabchanged(self, event):
        if event.widget.index("current") == 0:
            try:

                self.imageNb.after_cancel(self.afterId)  #stops the previously running enlarge function on the notebook
                print("cam1")
                self.func(self.d1)
                self.button1.bind("<Button-1>", lambda event, ob1=self.d1: self.plot(event, ob1))
                self.button2.bind("<Button-1>", lambda event, ob1=self.d1: self.plot1(event, ob1))
                self.Enlarge1()
            except:

                self.func(self.d1)
                self.button1.bind("<Button-1>", lambda event, ob1=self.d1: self.plot(event, ob1))
                self.button2.bind("<Button-1>", lambda event, ob1=self.d1: self.plot1(event, ob1))
                print("cam1")
                self.Enlarge1()
        elif event.widget.index("current")==1:
            try:

                self.imageNb.after_cancel(self.afterId)
                print("cam2")
                #to show graphs in Frame2
                self.func(self.d2)
                self.button1.bind("<Button-1>", lambda event, obj=self.d2: self.plot(event, obj))
                self.button2.bind("<Button-1>", lambda event, obj=self.d2: self.plot1(event, obj))
                #to show video
                self.Enlarge2()
            except:
                self.func(self.d2)
                self.button1.bind("<Button-1>", lambda event, obj=self.d2: self.plot(event, obj))
                self.button2.bind("<Button-1>", lambda event, obj=self.d2: self.plot1(event, obj))
                print("cam2")
                self.Enlarge2()
        elif event.widget.index("current")==2:
            try:
                self.func(self.d3)
                self.button1.bind("<Button-1>", lambda event, obj=self.d3: self.plot(event, obj))
                self.button2.bind("<Button-1>", lambda event, obj=self.d3: self.plot1(event, obj))
                self.imageNb.after_cancel(self.afterId)
                print("cam3")
                self.Enlarge3()
            except:
                self.func(self.d3)
                self.button1.bind("<Button-1>", lambda event, obj=self.d3: self.plot(event, obj))
                self.button2.bind("<Button-1>", lambda event, obj=self.d3: self.plot1(event, obj))
                print("cam3")
                self.Enlarge3()
        else:
            try:
                self.func(self.d4)
                self.button1.bind("<Button-1>", lambda event, obj=self.d4: self.plot(event, obj))
                self.button2.bind("<Button-1>", lambda event, obj=self.d4: self.plot1(event, obj))
                self.imageNb.after_cancel(self.afterId)
                print("cam1")
                self.Enlarge4()
            except:
                self.func(self.d4)
                self.button1.bind("<Button-1>", lambda event, obj=self.d4: self.plot(event, obj))
                self.button2.bind("<Button-1>", lambda event, obj=self.d4: self.plot1(event, obj))
                print("cam4")
                self.Enlarge4()




    # Used to disappear video capture if width decreases below a threshold

    # Function used to plot graph for custom inputs
    def plot(self, event, obj):
        plt.figure(1)
        self.fig.clf()
        inputDateStr1 = str(self.inputDate1.get_date())
        inputDateStr2 = str(self.inputDate2.get_date())
        inputDateStr1 = inputDateStr1 + ' 00:00:00'
        inputDateStr2 = inputDateStr2 + ' 00:00:00'
        date1 = datetime.strptime(inputDateStr1, "%Y-%m-%d %H:%M:%S")
        date2 = datetime.strptime(inputDateStr2, "%Y-%m-%d %H:%M:%S")
        delta = date2 - date1
        interval1 = timedelta(days=1)
        interval2 = timedelta(days=365 / 12)

        if delta < interval1:
            inputDateStr1 = "'" + inputDateStr1 + "'"
            inputDateStr2 = "'" + inputDateStr2 + "'"
            y = obj.hourlyCount(inputDateStr1, inputDateStr2)
            if self.v.get() == 0:
                plt.plot(np.array(y)[:, 1], np.array(y)[:, 0], color='blue')
            else:
                plt.bar(np.array(y)[:, 1], np.array(y)[:, 0], color='blue', width=.5)
            plt.xticks(rotation=45)
            plt.title("Daily Count", fontsize=10)
            plt.ylabel("No of people", fontsize=10)
            plt.xlabel("Hours", fontsize=10)
            self.canvas.draw()
        elif delta < interval2:
            inputDateStr1 = "'" + inputDateStr1 + "'"
            inputDateStr2 = "'" + inputDateStr2 + "'"
            y = obj.weeklyCount(inputDateStr1, inputDateStr2)
            if self.v.get() == 0:
                plt.plot(np.array(y)[:, 1], np.array(y)[:, 0], color='blue')
            else:
                plt.bar(np.array(y)[:, 1], np.array(y)[:, 0], color='blue', width=.5)
            plt.xticks(rotation=45)
            plt.title("Daily Count", fontsize=10)
            plt.ylabel("No of people", fontsize=10)
            plt.xlabel("Date", fontsize=10)
            self.canvas.draw()
        else:
            inputDateStr1 = "'" + inputDateStr1 + "'"
            inputDateStr2 = "'" + inputDateStr2 + "'"
            y = obj.monthlyCount(inputDateStr1, inputDateStr2)
            if self.v.get() == 0:
                plt.plot(np.array(y)[:, 1], np.array(y)[:, 0], color='blue')
            else:
                plt.bar(np.array(y)[:, 1], np.array(y)[:, 0], color='blue', width=.5)
            plt.xticks(rotation=45)
            plt.title("Daily Count", fontsize=10)
            plt.ylabel("No of people", fontsize=10)
            plt.xlabel("Month", fontsize=10)
            self.canvas.draw()

    def plot1(self, event, obj):
        plt.figure(2)
        self.fig1.clf()
        inputDateStr1 = str(self.inputDate3.get_date())
        inputDateStr1 = inputDateStr1 + ' 00:00:00'

        if self.v2.get() == 0:
            inputDateStr1 = "'" + inputDateStr1 + "'"
            y = obj.hourlyCount(inputDateStr1, inputDateStr1)
            if self.v1.get() == 0:
                plt.plot(np.array(y)[:, 1], np.array(y)[:, 0], color='blue')
            else:
                plt.bar(np.array(y)[:, 1], np.array(y)[:, 0], color='blue', width=.5)
            plt.xticks(rotation=45)
            plt.title("Daily Count", fontsize=10)
            plt.ylabel("No of people", fontsize=10)
            plt.xlabel("Hours", fontsize=10)
            self.canvas5.draw()
        elif self.v2.get() == 1:
            inputDateStr1 = "'" + inputDateStr1 + "'"
            y = obj.weekdata(inputDateStr1)
            if self.v1.get() == 0:
                plt.plot(np.array(y)[:, 1], np.array(y)[:, 0], color='blue')
            else:
                plt.bar(np.array(y)[:, 1], np.array(y)[:, 0], color='blue', width=.5)
            plt.xticks(rotation=45)
            plt.title("Daily Count", fontsize=10)
            plt.ylabel("No of people", fontsize=10)
            plt.xlabel("Date", fontsize=10)
            self.canvas5.draw()
        else:
            inputDateStr1 = "'" + inputDateStr1 + "'"
            y = obj.monthdata(inputDateStr1)
            if self.v1.get() == 0:
                plt.plot(np.array(y)[:, 1], np.array(y)[:, 0], color='blue')
            else:
                plt.bar(np.array(y)[:, 1], np.array(y)[:, 0], color='blue', width=.5)
            plt.xticks(rotation=45)
            plt.title("Daily Count", fontsize=10)
            plt.ylabel("No of people", fontsize=10)
            plt.xlabel("Month", fontsize=10)
            self.canvas5.draw()


# Set up GUI
window = tk.Tk()  # Makes main window
window.wm_title("Survillience App")
window.config(background="#FFFFFF")

window.geometry("1500x1000")

wobj = mainWindow(window)

window.mainloop()
