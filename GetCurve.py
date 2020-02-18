from tkinter import *
import tkinter.filedialog
import numpy as np
import pandas as pd
from PIL import Image

def Ouvrir():
    filename = tkinter.filedialog.askopenfilename(title="Ouvrir une image",filetypes=[('all files','.*')])
    dict["filename"] = filename
    Path = Label(MainWindow, text = "filepath : " + dict["filename"])
    Path.grid(row=0, column=1, columnspan=3)
    print("Path OK -> Step 2")
    return None
    
def DefineAxis():
    del AxisCollector[:]
    import matplotlib.pylab as plt
    import numpy as np
    from PIL import Image
    
    img = Image.open(dict["filename"])
    arr = np.array(img)
    figure = plt.figure()
    ax1 = figure.add_subplot(111)
    ax1.imshow(arr)
    plt.tight_layout()
    cid = figure.canvas.mpl_connect('key_press_event', OnClickAxis)
    plt.show()
    
def DefineObject():
    import matplotlib.pylab as plt
    import numpy as np
    from PIL import Image
    
    img = Image.open(dict["filename"])
    arr = np.array(img)
    figure = plt.figure()
    ax1 = figure.add_subplot(111)
    ax1.imshow(arr)
    plt.tight_layout()
    cid = figure.canvas.mpl_connect('key_press_event', OnClickObject)
    plt.show()

def OnClickAxis(event):
    if event.key == " ":
        AxisCollector.append([event.xdata, event.ydata])
        print(len(AxisCollector),[event.xdata, event.ydata])
    else:
        None
        
def OnClickObject(event):
    if event.key == "a":
        CurveCollector.append([event.xdata, event.ydata])
        print("a", CurveCollector)
    if event.key == "z":
        PointCollector.append([event.xdata, event.ydata])
        print("z", PointCollector)
    else:
        None
        
def Filtrage(DataFrame):
    xsave = []
    ysave = []
    
    xtemp = DataFrame["X"][0]
    ytemp = []
    
    for i in range(len(DataFrame)):
        if DataFrame["X"][i] == xtemp:
            ytemp.append(DataFrame["Y"][i])
        else:
            xsave.append(xtemp)
            ysave.append(np.mean(ytemp))
            ytemp = []
            ytemp.append(DataFrame["Y"][i])
            xtemp = DataFrame["X"][i]
    return pd.DataFrame(np.transpose([xsave,ysave]), columns=["X","Y"])

def moulinette():  
    x1, x2, y1, y2, xscale, yscale = x0val.get(), x1val.get(), y0val.get(), y1val.get(), xlog.get(), ylog.get()
    
    img = Image.open(dict["filename"])
    arr = np.array(img)
    
    if xscale == 1:
        xscale = "log"
    else:
        xscale = "linear"
        
    if yscale == 1:
        yscale = "log"
    else:
        yscale = "linear"
    
    print(x1,x2,y1,y2, )
    
    def XReal(Kx, Kxp, Xg,scale):
        if scale == "linear":
            return (Xg-Kxp)/Kx
        if scale == "log":
            return 10**((Xg-Kxp)/Kx)
        
    def YReal(Ky, Kyp, Yg,scale):
        if scale == "linear":
            return (Yg-Kyp)/Ky
        if scale == "log":
            return 10**((Yg-Kyp)/Ky)
    
    if xscale == "log":
        x1, x2 = np.log10(x1), np.log10(x2)
    if yscale == "log":
        y1, y2 = np.log10(y1), np.log10(y2)

    ## Pour X
    # Xgraph1 = Xreel1*K+K'
    # Xgraph2 = Xreel2*K+K'
    Kx = (AxisCollector[1][0]-AxisCollector[0][0])/(x2-x1)
    Kxp = AxisCollector[0][0]-x1*Kx

    ## Pour Y
    Ky = (AxisCollector[3][1]-AxisCollector[2][1])/(y2-y1)
    Kyp = AxisCollector[2][1]-y1*Ky
    
    CurveListe = []
    for i in CurveCollector:
        Filter = np.where((arr[:,:,0] == arr[int(i[1]),int(i[0]),0]) &
                          (arr[:,:,1] == arr[int(i[1]),int(i[0]),1]) &
                          (arr[:,:,2] == arr[int(i[1]),int(i[0]),2]), 0, 1)
        Y, X = np.where(Filter==0)
        X = XReal(Kx,Kxp,X,xscale)
        Y = YReal(Ky,Kyp,Y,yscale)
        DF = pd.DataFrame(np.transpose([X,Y]), columns=["X","Y"])
        DF = DF.sort_values(["X"]).reset_index(drop=True)
        if SETfiltrage.get() ==1:
            DF = Filtrage(DF)
        else:
            None
        CurveListe.append(DF)
            
    XPoint = []
    YPoint = []
    for i in PointCollector:
        XPoint.append(int(i[0]))
        YPoint.append(int(i[1]))
    XPoint = XReal(Kx,Kxp,np.array(XPoint),xscale)
    YPoint = YReal(Ky,Kyp,np.array(YPoint),yscale)
    DFP = pd.DataFrame([XPoint,YPoint], ["X","Y"]).transpose()
        
    dict["Curve"] = CurveListe
    dict["DFP"] = DFP
    print("OK pour export")
    return None

def SaveDFP():
    dict["DFP"].to_csv(Savetext.get()+".txt", sep="\t", header=["X","Y"], index=None)
    print(dict["DFP"])
    print("Export point OK")
    
def SaveDFC():
    for i in range(len(dict["Curve"])):
        print(i)
        dict["Curve"][i].to_csv(Savetext.get()+"_%1.0f.txt"%i, sep="\t", header=["X","Y"], index=None)
        print(dict["Curve"][i])
        print("Export curve OK")
    None
        
dict={}
dict["filename"] = ""

AxisCollector = []
PointCollector = []
CurveCollector = []

# Création de la fenêtre principale (main window)
MainWindow = Tk()
MainWindow.title('Get Curve')
#MainWindow.geometry('1000x200')

MainWindow.rowconfigure(0, weight=1)
MainWindow.columnconfigure(0, weight=1)

BoutonOuvrir = Button(MainWindow, text ='1. Ouvrir', command = Ouvrir)
BoutonOuvrir.grid(row=0, column=0)
Path = Label(MainWindow, text = "filepath : " + dict["filename"])
Path.grid(row=0, column=1, columnspan=3)

BoutonAxis = Button(MainWindow, text ='2. Define Axis', command = DefineAxis)
BoutonAxis.grid(row=2, column=0)

x0val = DoubleVar()
x0text = Entry(MainWindow, textvariable = x0val)
x0label = Label(MainWindow, text = "x0")
x0label.grid(row=3, column=0)
x0text.grid(row=3, column=1)
x1val = DoubleVar()
x1text = Entry(MainWindow, textvariable = x1val)
x1label = Label(MainWindow, text = "x1")
x1label.grid(row=3, column=2)
x1text.grid(row=3, column=3)

xlog = IntVar()
xlog.set(0)
xlogCheck = Checkbutton(MainWindow,text="xlog", variable= xlog)
xlogCheck.grid(row=3,column=4)

y0val = DoubleVar()
y0text = Entry(MainWindow, textvariable = y0val)
y0label = Label(MainWindow, text = "y0")
y0label.grid(row=4, column=0)
y0text.grid(row=4, column=1)
y1val = DoubleVar()
y1text = Entry(MainWindow, textvariable = y1val)
y1label = Label(MainWindow, text = "y1")
y1label.grid(row=4, column=2)
y1text.grid(row=4, column=3)

ylog = IntVar()
ylog.set(0)
ylogCheck = Checkbutton(MainWindow, text="ylog",variable=ylog )
ylogCheck.grid(row=4,column=4)

ObjectAxis = Button(MainWindow, text ='3. Define Object', command = DefineObject)
ObjectAxis.grid(row=5, column=0)
Label(MainWindow, text = "Press (a) for curve, press (z) for point").grid(row=5, column=1)

GOButton = Button(MainWindow, text ='4. GO !', command = moulinette)
GOButton.grid(row=6, column=0)

SETfiltrage = IntVar()
SETfiltrage.set(0)
Checkbutton(MainWindow,text="Filtrage", variable= SETfiltrage).grid(row=6,column=1)

SaveButtonDFP = Button(MainWindow, text ='5.a Save (Point)', command = SaveDFP)
SaveButtonDFP.grid(row=7, column=0)

SaveButtonDFC = Button(MainWindow, text ='5.b Save (Curve)', command = SaveDFC)
SaveButtonDFC.grid(row=7, column=1)

SaveTextLabel = Label(MainWindow, text = "Filename")
SaveTextLabel.grid(row=7, column=2)
Savetext = StringVar()
SaveFile = Entry(MainWindow, textvariable = Savetext)
SaveFile.grid(row=7, column=3)

MainWindow.mainloop()
