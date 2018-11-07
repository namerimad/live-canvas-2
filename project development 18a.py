# check the camera
# check the arduino port


import Tkinter 

from Tkinter import *
import time
import threading
import random
import Queue

import Tkinter as tk # for importing image format need to be chaned


from PIL import ImageTk, Image


import win32com.client # import photoshop protocol



psApp = win32com.client.Dispatch("Photoshop.Application") #run photoshop or activate it
######
#psApp = win32com.client.GetActiveObject("Photoshop.Application") #run photoshop or activate it
#### can be used to get the same results
#### also it can be done on the applying sentense not here in the begin


import serial            # serial connecting protocol Arduino searial port
arduinoData = serial.Serial("COM3", 9600, timeout=0) # reading arduino
#from threading import Timer # enable Timer function
import threading # I am using only Timer function from this Library
import re   # think # read numbers



############## face detect #############
import cv2           # face recognition Library
import numpy as np
import sys

facePath = 'haarcascade_frontalface_default.xml'    # CV face recognition cascade 
smilePath = 'haarcascade_smile.xml'                 # CV smile recognition cascade 
faceCascade = cv2.CascadeClassifier(facePath)       # CV face recognition cascade 
smileCascade = cv2.CascadeClassifier(smilePath)     # CV smile recognition cascade 

cap = cv2.VideoCapture(2)       # run the camera #can change the (0) to select another camera
cap.set(3,320)                  # set camera window aspects ratio
cap.set(4,240)


os=1.2 # smile size variable (original smile)
ns=1.2 # new smile 

#cv2.flip

#sF = 1.05

########################################

"""global variables for the whole program"""
BPM=1  # Heart beats rate  the collected heart rate 
t1=1   # automatic time value    # think# the auto apply timer
var=1  # scale value
smileVar = 10 # smile slide defult value 

savedColorR = 0    # the first collected from Photoshopby "save current colour"
savedColorG = 0    # the first collected from Photoshopby "save current colour"
savedColorB = 0    # the first collected from Photoshopby "save current colour"

newR = 0        # the processed colour ready to go to Photoshop again
newG = 0        # the processed colour ready to go to Photoshop again
newB = 0        # the processed colour ready to go to Photoshop again

L=0

s = 0 # auto timer condition # 0 value to start the app with auto not activated
heartData = 1       # initial value for heartData
h=1                 #for label updating timer 
valueToApply = 5
solidcolor = win32com.client.Dispatch( "Photoshop.SolidColor" ) # create an array to hold the foreground color 3 values

smileC = 0       # main smile detector counter
smileA = 0       # second smile counter to be compared to smileCombi (the smile bar value) and to do the condition when reach the selected value

smileCombi = 10      # selected value on smile bar
smileAdd = 0         # 3rd smiles counter represent the total of smiles devided on the selected value on smile bar



t1 = 1000        #timer initial
l=1        #
arduinoLine = 1
mag= 1

valueToApply=1
heartData22=1
pulseStabilizer = 0

#def mainTimer():
#    threading.Timer(1, mainTimer).start()
#    print "RRRRRRRRRRRRRRRRRRR"
#    GuiPart.test()
#mainTimer()
hSymboleColour = 'yellow'




class GuiPart:
    def __init__(self, master, queue, endCommand):
        global canvas2
        global rect2
        global canvas # make it gobal to be able to update it afterwards
        global rect1  # make it gobal to be able to update it afterwards
        global savedColour
        global newColour

        global rect3
        global canvas3
        
        self.queue = queue
        # Set up the GUI
        #console = Tkinter.Button(master, text='Done', command=endCommand)
        #console.pack(  )
        # Add more GUI stuff here depending on your specific needs



        
        savedColour= '#%02x%02x%02x' % (savedColorR, savedColorG, savedColorB)
        canvas  = Canvas(master, width=300 , height=50)
        canvas.place (x=50,y=120)
        rect1=canvas.create_rectangle(0,0,100,35, fill=savedColour)

        


        #savedColour= '#%02x%02x%02x' % (savedColorR, savedColorG, savedColorB)
        canvas3  = Canvas(master, width=35 , height=35)
        canvas3.place (x=180,y=460)
        rect3=canvas3.create_rectangle(0,0,35,35, fill=hSymboleColour)


        
        newColour= '#%02x%02x%02x' % (newR, newG, newB)

        canvas2  = Canvas(master, width=100 , height=50)
        canvas2.place (x=240,y=120)
        rect2=canvas2.create_rectangle(0,0,100,35, fill=newColour)
        
        

        



        self.applyButton = Button (master, text="Manual One Time Apply",command=self.applying)
        self.applyButton.place (x=110,y=350)

        self.autoB = Button(master, text="Auto Apply", command= self.auto_b)
        self.autoB.place (x=30, y=350)

        self.manualB = Button(master, text="Cancel '\n' Auto Apply", command= self.manual_b)
        self.manualB.place (x=300, y=320)




        self.barButton = Button(master, text="Main Applying Timer", command=self.bar_value)#create button to read the bar value
        self.barButton.place (x=30,y=320) # bar value button location

        global var                  # to make var variable global
        var = DoubleVar()           
        scale = Scale( root, variable = var, from_=1, to=15, orient=HORIZONTAL )  # to create a scale bar
        #scale.pack(anchor=W)   # to assign location (W,E,CENTER,N,S.... etc
        scale.place (x=170, y=305)# to assign location by axis

        #btn = Button(self, text="Start Auto Timer", command =autoTimer).place(x=100, y=40)



        self.saveButton = Button(master, text="Save current Heart Rate", command=self.pulseSaving)
        self.saveButton.place (x=30,y=460)


        self.heartLabel= Label(master,text = "LIVE Heart Pulse:", width=17)
        self.heartLabel.place (x=30 , y=490)

        self.heartLabe2= Label(master,width=5)
        self.heartLabe2.place (x=135 , y=490)
        self.heartLabe2.configure(text=heartData)


        self.heartValueName= Label(master,text="Heart Value to Apply:",width=20)
        self.heartValueName.place (x=10 , y=510)

        self.heartValue= Label(master,width=5)
        self.heartValue.place (x=135 , y=510)
        self.heartValue.configure(text=valueToApply)
        
        self.pulseStabilizerL= Label(master,width=20)
        self.pulseStabilizerL.place (x=30 , y=530)
        self.pulseStabilizerL.configure(text=("Saved Pulse Value:  ",pulseStabilizer))


        self.forceHeart = Entry(master)      #create a text input box for manual heartpulse entry 
        self.forceHeart.place (x=30 , y=560)

        self.forceHeartButton = Button (master, text="Force Heart Rate", command=self.forceHeartB)# text input heartpulse activating button
        self.forceHeartButton.place (x=160 , y=555)
        

################################################ 


        




#####################
        
        
        


        self.red= Label(master,width=25)
        self.red.place (x=10 , y=160)
        self.red.configure(text="Saved Foreground Colour")


        self.red= Label(master,width=20)
        self.red.place (x=30 , y=180)
        self.red.configure(text=("Red Channel",savedColorR))

        self.green= Label(master,width=20)
        self.green.place (x=30 , y=200)
        self.green.configure(text=("Green Channel",savedColorG))

        self.blue= Label(master,width=20)
        self.blue.place (x=30 , y=220)
        self.blue.configure(text=("Blue CHaneel",savedColorB))


        self.saveButton = Button(master, text="   Save Current Colour   ", command=self.colourSaving)
        self.saveButton.place (x=30,y=240)



        self.newTitle= Label(master,width=30)
        self.newTitle.place (x=190 , y=160)
        self.newTitle.configure(text="Processed Foreground Colour")

        self.newR= Label(master,width=20)
        self.newR.place (x=220 , y=180)
        self.newR.configure(text=("Red Channel",newR))

        self.newG= Label(master,width=20)
        self.newG.place (x=220 , y=200)
        self.newG.configure(text=("Green Chaneel",newG))

        self.newB= Label(master,width=20)
        self.newB.place (x=220 , y=220)
        self.newB.configure(text=("Blue Channel",newB))




##############################################
        ######################################### 
        ############################################
        self.hRateAffectedC = Button(master, text="Colour Channel'\n' Affected by Heart Rate", command=self.hRateAffectedColourBtn)#create button to read the bar value
        self.hRateAffectedC.place (x=230,y=455) # bar value button location


        global redRate  # represent the new chanel value after heart rate applied
        global greenRate  # represent the new chanel value after heart rate applied
        global blueRate  # represent the new chanel value after heart rate applied
        
        redRate=IntVar()
        rCheckRate=Checkbutton(master,text="RED",state=ACTIVE, variable=redRate)
        rCheckRate.place (x=300,y=500)
        
        greenRate=IntVar()
        gCheckRate=Checkbutton(master,text="GREEN",state=ACTIVE, variable=greenRate)
        gCheckRate.place (x=300,y=520)
            
        blueRate=IntVar()
        bCheckRate=Checkbutton(master,text="BLUE",state=ACTIVE, variable=blueRate)
        bCheckRate.place (x=300,y=540)

####################### labels


        #self.saveButton = Button(master, text="Save Current Colour and Heart Rate", command=self.saving)
        #self.saveButton.place (x=10,y=500)






########### smile counter active slide#######################
        global smileVar                  
        smileVar = DoubleVar()           
        smileScale = Scale( root, variable = smileVar, from_=1, to=50, orient=HORIZONTAL )  # to create a scale bar
        #scale.pack(anchor=W)   # to assign location (W,E,CENTER,N,S.... etc
        smileScale.place (x=170, y=615)# to assign location by axis
        smileScale.set(10)  #set an intial value 


        self.smileButton = Button(master, text="Effective Smiles Step", command=self.smileButton)#create button to read the bar value
        self.smileButton.place (x=30,y=630) # bar value button location



        self.smile= Label(master,text = "LIVE Smile Counter:", width=20)
        self.smile.place (x=230, y=700)

        self.smileC = Label(master,width=5)
        self.smileC.place (x=350 , y=700)
        self.smileC.configure(text=smileC)

        

        self.smileAffectedC = Button(master, text="Smile Affected Colours", command=self.affectedColourButton)#create button to read the bar value
        self.smileAffectedC.place (x=110,y=700) # bar value button location


############checkbox
        global varR
        global varG
        global varB
        #colourCheckR=Checkbutton(master, text = "Red", variable = CheckVar1, onvalue = 1, offvalue=0,height=5, width=20)
        varR=IntVar()
        colourCheckR=Checkbutton(master,text="RED",state=ACTIVE, variable=varR)
        colourCheckR.place (x=30,y=670)
        
        varG=IntVar()
        colourCheckR=Checkbutton(master,text="GREEN",state=ACTIVE, variable=varG)
        colourCheckR.place (x=30,y=690)
            
        varB=IntVar()
        colourCheckR=Checkbutton(master,text="BLUE",state=ACTIVE, variable=varB)
        colourCheckR.place (x=30,y=710)




        self.smileAdd= Label(master,width=20)
        self.smileAdd.place (x=30 , y=750)
        self.smileAdd.configure(text=("Smile Effective Value=",smileAdd))


######################
    def forceHeartB(self):  # to reaad the manually intered Heart pulse value as a saved pulse
        #global L
        global pulseStabilizer
        #print "forced Heart value"

        fv = self.forceHeart.get() #Forced Value
        if fv.isdigit():
            print fv
            if int(fv) > 20 :
                if int(fv) < 120:
                    #print "20000000000000000000000000000"
  
                    pulseStabilizer = int(fv)
                    
 

    def affectedColourButton(self):   #(need to check)
        print "Afected Colours"
        print varR.get()
        print varG.get()
        print varB.get()
        
    def hRateAffectedColourBtn(self):

        print"heartRate affected Channels"
        print redRate.get()
        print greenRate.get()
        print blueRate.get()

        
    @classmethod  
    def test(self):
        print "TEST TEST TEST"


    def bar_value(self):
        global t1

        selection = var.get()
        print selection
        t1 = int(selection * 1000)

    def smileButton(self):  #activate the selected number of smiles that will be counted as 1 effective number
        global smileCombi   # selected value on smile bar

        selection = smileVar.get()
        print selection
        smileCombi = int(selection) # to make the smileCombi as the selected on smile bar 




        

    def saving(self):
        global savedColorR # to make this variable global so it will work within any def, it must be befor assigning the value to it
        global savedColorG # to make this variable global so it will work within any def, it must be befor assigning the value to it
        global savedColorB # to make this variable global so it will work within any def, it must be befor assigning the value to it
              
        global solidcolor
        global pulseStabilizer


        solidcolor = win32com.client.Dispatch( "Photoshop.SolidColor" ) # create an array to hold the foreground color 3 values
        solidcolor.rgb.red = psApp.foregroundColor.rgb.red      #read photoshop foreground color RED
        solidcolor.rgb.green = psApp.foregroundColor.rgb.green  #read photoshop foreground color GREEN
        solidcolor.rgb.blue = psApp.foregroundColor.rgb.blue    #read photoshop foreground color BLUE
        

        savedColorR = int(solidcolor.rgb.red)
        savedColorG = int(solidcolor.rgb.green)
        savedColorB = int(solidcolor.rgb.blue)
         
        print "Saving", savedColorR , savedColorG , savedColorB

        pulseStabilizer = heartData22
        #print pulseStabilizer
         

    def colourSaving(self):
        global savedColorR # to make this variable global so it will work within any def, it must be befor assigning the value to it
        global savedColorG # to make this variable global so it will work within any def, it must be befor assigning the value to it
        global savedColorB # to make this variable global so it will work within any def, it must be befor assigning the value to it
              
        global solidcolor
        global savedColor


        solidcolor = win32com.client.Dispatch( "Photoshop.SolidColor" ) # create an array to hold the foreground color 3 values
        solidcolor.rgb.red = psApp.foregroundColor.rgb.red      #read photoshop foreground color RED
        solidcolor.rgb.green = psApp.foregroundColor.rgb.green  #read photoshop foreground color GREEN
        solidcolor.rgb.blue = psApp.foregroundColor.rgb.blue    #read photoshop foreground color BLUE
        

        savedColorR = int(solidcolor.rgb.red)
        savedColorG = int(solidcolor.rgb.green)
        savedColorB = int(solidcolor.rgb.blue)
        
        
        print "Saved Colour", savedColorR , savedColorG , savedColorB


        savedColour= '#%02x%02x%02x' % (savedColorR, savedColorG, savedColorB)
        canvas.itemconfig(rect1, fill = savedColour)
        #print savedColour





    def pulseSaving(self):
        global pulseStabilizer

        pulseStabilizer = heartData22
        #print pulseStabilizer



    def auto_b (self):
        global s
        print "Auto"
        s = 1 # to start the auto timer (timer 2)

    
    def manual_b (self):
        global s
        print "Manual"
        s = 0   # set s to 0 so timer2 will not apply the value but keep counting





    @classmethod  
    def applying(self):


        solidcolor.rgb.red = newR   #savedColorR + valueToApply2   # + (valueToApply * 4 - 150)   # add specific value to the red channell
        solidcolor.rgb.green = newG #savedColorG + valueToApply2   # + (valueToApply * 2 - 50)    # add specific value to the green channell
        solidcolor.rgb.blue = newB  #savedColorB + valueToApply2   # + (valueToApply * 2 - 50)    # add specific value to


        psApp.foregroundColor = solidcolor #applying solidColor array to photoshop foreground color

        print savedColorR , savedColorG , savedColorB
        print solidcolor.rgb.red,solidcolor.rgb.green,solidcolor.rgb.blue

        """
        global valueToApply
        print"apply"
        global newR
        global newG
        global newB


        #heartData2 = int(heartData) - 60
        #valueToApply = (int(heartData2)/3)*2 # BPM in arduino



        #heartData2 = int(heartData) - 60
        #valueToApply = int(heartData2)*5 # BPM in arduino
       
        #print "applied Heart rate", valueToApply
        #print "Original Saved Colour", savedColorR , savedColorG , savedColorB
        #print "photoshop Current front colour" , int(solidcolor.rgb.red),int(solidcolor.rgb.green),int(solidcolor.rgb.blue)

        valueToApply2 = valueToApply * 4
        
        if savedColorR + valueToApply2 > 255:
            valueToApply2 = 255 - savedColorR
            
        if savedColorG + valueToApply2 > 255:
            valueToApply2 = 255 - savedColorG
            
        if savedColorB + valueToApply2 > 255:
            valueToApply2 = 255 - savedColorB
        
        if savedColorR + valueToApply2 < 0:
            valueToApply2 = 0
            
        if savedColorG + valueToApply2 < 0:
            valueToApply2 = 0
            
        if savedColorB + valueToApply2 < 0:
            valueToApply2 = 0


        newR = savedColorR + valueToApply2
        newG = savedColorG + valueToApply2
        newB = savedColorB + valueToApply2
        """        
        



    def processIncoming(self):
        """Handle all messages currently in the queue, if any.""" # timer loop I used in oiginal written code
        #print "00000000000000000000000000000"

        global heartData22
        global valueToApply
        global valueToApply2
        global newR  # the actual colour channel value that will be send directly to photoshop 
        global newG  # through the the global function
        global newB  #########
        
       
        while self.queue.qsize(  ):
            #print "1111111111111111111111"

            try:
                msg = self.queue.get(0)
                # Check contents of message and do whatever is needed. As a
                # simple test, print it (in real life, you would
                # suitably update the GUI's display in a richer fashion).


                self.heartLabe2.configure(text=heartData22)
                self.smileC.configure(text=smileC)
                self.heartValue.configure(text=valueToApply)

                self.pulseStabilizerL.configure(text=("Saved Pulse Value:   ",pulseStabilizer))

                self.red.configure(text=("Red Channel",savedColorR))
                self.green.configure(text=("Green Channel",savedColorG))
                self.blue.configure(text=("Blue  Channel",savedColorB))

                self.newR.configure(text=("Red Channel",newR))
                self.newG.configure(text=("Green Channel",newG))
                self.newB.configure(text=("Blue Channel",newB))

                self.smileAdd.configure(text=("Smile Effective Value=" , smileAdd))


                newColour= '#%02x%02x%02x' % (newR, newG, newB)
                canvas2.itemconfig(rect2, fill = newColour)
                #print savedColour
                print newColour


                canvas3.itemconfig(rect3, fill=hSymboleColour)

                  

                #heartData2 = int(heartData) - 60
                #valueToApply = (int(heartData2)/3)*2 # BPM in arduino


                #print heartData
                #if " " in heartData:
                #    print "Spaceeeeeeeeeeee"


               
                heartData22= heartData
                #print heartData2
                valueToApply = heartData22 - pulseStabilizer
                #print valueToApply
                print "Current Heart Rate", heartData
                #if heartData2 - pluseStabilizer > 0:
                #   valueToApply = 
                #print pulseStabilizer

#######################

##### 

                valueToApply2 = valueToApply * 6 #the value that will be applied to each colour channel

                if redRate.get()== 1:               #check if the effective colour checkbox is selected
                    if savedColorR + valueToApply2 > 255: # check the final colour value not to exceed 255
                        valueToApply2 = 255 - savedColorR # trim the value to not exeed 255
                    
                    if savedColorR + valueToApply2 < 0:   # check the final colour valuenot to be in minus
                        valueToApply2 = 0
                    
                    newR = savedColorR + valueToApply2    # store the vew colour value after meeting all conditions
                else:
                    newR = savedColorR

                if greenRate.get()== 1:               #check if the effective colour checkbox is selected
                    if savedColorG + valueToApply2 > 255: # check the final colour value not to exceed 255
                        valueToApply2 = 255 - savedColorG # trim the value to not exeed 255
                    
                    if savedColorG + valueToApply2 < 0:   # check the final colour valuenot to be in minus
                        valueToApply2 = 0
                    
                    newG = savedColorG + valueToApply2    # store the vew colour value after meeting all conditions
                else:
                    newG = savedColorG


                if blueRate.get()== 1:               #check if the effective colour checkbox is selected
                    if savedColorB + valueToApply2 > 255: # check the final colour value not to exceed 255
                        valueToApply2 = 255 - savedColorB # trim the value to not exeed 255
                    
                    if savedColorB + valueToApply2 < 0:   # check the final colour valuenot to be in minus 
                        valueToApply2 = 0
                    
                    newB = savedColorB + valueToApply2    # store the vew colour value after meeting all conditions

                else:
                    newB = savedColorB

 
                
                #if savedColorR + valueToApply2 > 255:
                    #valueToApply2 = 255 - savedColorR
                    
                #if savedColorG + valueToApply2 > 255:
                    #valueToApply2 = 255 - savedColorG
                    
                #if savedColorB + valueToApply2 > 255:
                    #valueToApply2 = 255 - savedColorB
                
                #if savedColorR + valueToApply2 < 0:
                    #valueToApply2 = 0
                    
                #if savedColorG + valueToApply2 < 0:
                    #valueToApply2 = 0
                    
                #if savedColorB + valueToApply2 < 0:
                    #valueToApply2 = 0


                #newR = savedColorR + valueToApply2 # + smileAdd
                #newG = savedColorG + valueToApply2
                #newB = savedColorB + valueToApply2


                #hSymboleColour = 'yellow'



######################                
            except Queue.Empty:
                # just on general principles, although we don't
                # expect this branch to be taken in this case

                pass

            #else:
                #pass   #this solved the issue of GUI freez when move it, it pass theprocess if GUI i sbusy 
                #print "GUI is BUSY"
                
class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    #print "2222222222222222"
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O).
        """
        self.master = master

        # Create the queue
        self.queue = Queue.Queue(  )

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.endApplication)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start(  )

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall(  )
        self.timer2(  )

    def periodicCall(self):
        global ns
        #print "33333333333333333333"
        #self.heartLabel.configure(text=heartData)
        #self.smileC.configure(text=b) 



        #GuiPart.ex.heartLabe2['text'] = heartData


        #self.heartLabe2= Label(master,width=5)
        #self.heartLabe2.place (x=300 , y=50)
        #self.heartLabe2.configure(text=heartData)

        



        

############## camera and features detection

        ret, frame = cap.read() # Capture frame-by-frame
        img = frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(gray,1.3,5)

            #gray,
            #scaleFactor= sF,
            #minNeighbors=8,
            #minSize=(55, 55),
            #flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        #)
        # ---- Draw a rectangle around the faces
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            #print y
            #print "os=", h
            
            # to adjust smile sensitivity in relation to the hight of
            # the red rectangle that border the fce (far or close)
            # the more the very sensitive the close the very hard to detect
            if 120<= h <= 200:
                if h>= 125:
                    ns = 1.4
                    if h>=135:
                        ns = 1.5
                        if h>= 145:
                            ns = 1.6
                            if h>= 170:
                                ns = 1.8
                                if h>= 190:
                                    ns = 1.9
                                    
                #print "h=", h # the current face rectangle hight 
                #print "ns=", ns # the mew smile distanse value
                
            smile = smileCascade.detectMultiScale(
                roi_gray,
                scaleFactor= ns, # adjust smile sensitivity (original was 1.7 # decreased after decresed the size of camera window
                minNeighbors=22,
                minSize=(10, 10), #was 25,25 decreased for decreasing the size of the camera screen
                flags=cv2.cv.CV_HAAR_SCALE_IMAGE
                )

            # Set region of interest for smiles
            for (x, y, w, h) in smile:
                global smileC # send the main smile counter value to the global area
                global smileA # second smile counter to be compared to smileCombi (the smile bar value) and to do the condition when reach the selected value
                global smileCombi # selected value on smile bar
                global smileAdd   # 3rd smiles counter represent the total of smiles devided on the selected value on smile bar



                print "Found", len(smile), "smiles!"
                cv2.rectangle(roi_color, (x, y), (x+w, y+h), (255, 0, 0), 1)
                #print "!!!!!!!!!!!!!!!!!"
                smileC = smileC+1 # main smile detector counter
                smileA = smileA+1 # add 1 to smile counter that will be compared to smileCombi
                if smileA > smileCombi: # compare the smile activate counter not to exceed the selected value
                                        # on bar also to record the combined smil
                    smileAdd = smileAdd +1    # 3rd smiles counter represent the total of smiles devided on the selected value on smile bar

                    #print "smileAdd=", smileAdd
                    smileA = 0   # second smile counter to be compared to smileCombi (the smile bar value) and to do the condition when reach the selected value


                    
                print "smileA= ", smileA
                #f = 1



                
        #cv2.cv.Flip(frame, None, 1)
        cv2.imshow('Smile Detector', frame)
        c = cv2.cv.WaitKey(7) % 0x100
        #if c == 27:
        #    break
        ##############################################


######### reading arduino  ##############
        global heartData
        global mag  # store the previous heartData

        #global hSymboleColour
        #hSymboleColour = 'yellow'

        arduinoLine = arduinoData.readline()
        if not arduinoLine == "":         # if there is data from arduino then take all of the line      
            global hSymboleColour
            #print arduinoLine[1:4]
            hSymboleColour = 'red' #change the heart symbole into red with every avilable data


            #heartDataA = arduinoLine[1:3]  # this solved the problem of getting incomplete data   
            #if heartDataA.isdigit():      # to check that arduinoData is a digits ONLY
                #heartData = int(arduinoLine[1:4])



### this solved the issue that serial port can contain letters and unwanted charachters
### so the program is check if the condition of [1-3] are numbers and if yes it checks if
### [1-4] are numbers and if yes too this number will be recorded and if no the [1-3] wll be recorded
### and in case that {1-3] isnot numbers from begin this will ignore it and print (Wrog Data)

            heartDataA = arduinoLine[1:3]  # this solved the problem of getting incomplete data   
            if heartDataA.isdigit():      # to check that arduinoData is a digits ONLY
                heartDataA = arduinoLine[1:4]
                if heartDataA.isdigit():      # to check that arduinoData is a digits ONLY
                    heartData = int(arduinoLine[1:4])
                    print "Got Heart Rate:", heartData
                else:
                    heartData = int(arduinoLine[1:3])
                    print "Got Heart Rate:", heartData


                
            else:
                print "Wrongggggggggg Dta", heartDataA

            #if int(heartData) > 135:      # filter the wrong data when unattache the sensor
            #print "Heart Sensor not attached"
                

            #else:
            #print "Got Heart Rate:", heartData
            #mag=heartData
            #hSymboleColour = 'yellow'

            
        else:
            hSymboleColour = 'yellow' #change the heart symbole into yellow while there is no data

            #print "empty"  # show NO pulse data
            #heartData = 0
        #     print "aaaaaaaaaa"
        
############################################




        #putting this in the begin abstracted the GUI keep here or remove is fine
        """
        Check every 200 ms if there is something new in the queue.
        """
        self.gui.processIncoming(  )
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(100, self.periodicCall)



        #hSymboleColour = 'yellow'




    def timer2(self): #auto apply timer with adjustable t1 timing
       
        if s==1:
            #print "TTTTTTTTTTTTTTTTTTTTTTTTTT"
            #GuiPart.applying()
            try:
                GuiPart.applying()# Using Try solved the issue when Photoshop is Busy
                                  # will not break the Timer
            except:              
                print"BUSY"

            else:
                print"OK"
                
        
        self.master.after(t1, self.timer2)



 

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select(  )'. One important thing to remember is that the thread has
        to yield control pretty regularly, by select or otherwise.
        """
        while self.running:
            # To simulate asynchronous I/O, we create a random number at
            # random intervals. Replace the following two lines with the real
            # thing.
            time.sleep(rand.random(  ) * 0.4)
            msg = rand.random(  )
            self.queue.put(msg)

    def endApplication(self):
        self.running = 1




rand = random.Random(  )
root = Tkinter.Tk(  )

root.title("Drawing by Emotions")
#root.configure(background='grey')
root.geometry("400x800") # window saize


#### adding a heading image to the GUI ######################################

path= "de1.jpg"   # the title image path
img = ImageTk.PhotoImage(Image.open(path)) 
panel = tk.Label(root, image = img, width=400, height=100)
panel.place (x=0 , y=0)

####################################################################################



client = ThreadedClient(root)
#root.update()
root.mainloop()
