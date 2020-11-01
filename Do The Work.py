from tkinter import *
from PIL import ImageTk,Image
from TaskSet import TaskSet
from Task import Task
from TaskSetFile import TaskSetFile
from DailyTrackingFile import DailyTrackingFile
import os
import errno
import calendar

import datetime

class CreateToolTip(object):

    def __init__(self, widget, text='widget info'):
        self.waittime = 100     #miliseconds
        self.wraplength = 400   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()
            
class GoalSet(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)               
        self.master = master
        self.init_GoalSetWindow()

    numTasksOnDisplay=0
    addButtonPosition=2
    currentTaskSet=TaskSet() 
    
    removeButtonList=[]
    weightScaleList=[]
    taskDescEntryFieldList=[]
    taskDescLabelList=[]
    deleteBeforeSave=[]
    taskDescEntryField=0
    taskWeightScale=0
    
    #Creation of init_GoalSetWindow



    def init_GoalSetWindow(self):
        # changing the title of our master widget      
        self.master.title("Do The Work")

        # allowing the widget to take the full space of the root window
        self.grid(row=0)

        # remove --- from file menu
        self.master.option_add('*tearOff', False)
        
        # creating a button instance
        # quitButton = Button(self, text="Save", command=self.client_exit)

        # placing the button on my window
        #quitButton.place(x=0, y=575)

        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the file object)
        file = Menu(menu)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        file.add_command(label="Exit", command=self.client_exit)

        #added "file" to our menu
        menu.add_cascade(label="File", menu=file)

 
        s = Scale (root2, orient=HORIZONTAL, bg='white', bd=0, highlightbackground='white', from_=1, to=10)
        s.grid(row=self.numTasksOnDisplay+1, column=1)
        self.weightScaleList.append(s)
        
        instructionLabel = Label(root2, text="\nSet up cues and weights to get started! \n", background = 'white').grid(row=0, column=0, sticky='w', columnspan=3 , padx=(0,100))
        
        
        errorLabel = Label(root2, text="", background = 'white')
        errorLabel.grid(row=40, column=0, sticky='sw')

        image = Image.open("img/add.png")
        image = image.resize((15, 15), Image.ANTIALIAS)
        addPhoto = ImageTk.PhotoImage(image)

        image2 = Image.open("img/remove.png")
        image2 = image2.resize((15, 15), Image.ANTIALIAS)
        removePhoto = ImageTk.PhotoImage(image2)


        label1= Label(image=addPhoto, borderwidth=0, highlightthickness=0)
        label1.image = addPhoto

        label2= Label(image=removePhoto, borderwidth=0, highlightthickness=0)
        label2.image = removePhoto


        taskDesc = Entry(root2, relief=FLAT, bg='lightgrey')
        taskDesc.focus_set()
        taskDesc.config(width=50)
        taskDesc.grid(row=self.numTasksOnDisplay+1, column=0, sticky='s')

        self.taskDescEntryFieldList.append(taskDesc)
        
        #removeButton = Button(root2,image=removePhoto, command= lambda: destroyRow(localTaskPosition-1))
        #removeButton.grid(row=self.numTasksOnDisplay+1, column=3, sticky='sw')        
        
        
        localTaskPosition=self.numTasksOnDisplay

        def destroyRow(test):
            try:
                self.taskDescLabelList[test].destroy()
                self.removeButtonList[test].destroy()
                self.deleteBeforeSave.append(test)
            except IndexError as error:
                print("index out of bounds")
             

        self.numTasksOnDisplay+=1
        self.addButtonPosition+=1

        
        def addTask():

# if there are no tasks, then only for the FIRST task,
    # create entry field for desc and weight
    # add the fields to the lists
    # lists will be used to create labels and then delete the field
    
                if(self.taskDescEntryFieldList[self.numTasksOnDisplay-1].get()==""):
                    errorLabel.config(text="Fill in item details before adding new task", fg="red")
    
                else:
                    errorLabel.config(text="")
                    taskDescLabel=Label(root2, text=self.taskDescEntryFieldList[self.numTasksOnDisplay-1].get(), background='white')
                    self.taskDescEntryFieldList[self.numTasksOnDisplay-1].destroy()
                    #self.weightScaleList[self.numTasksOnDisplay-1].config(state=DISABLED)
                    taskDescLabel.grid(row=self.numTasksOnDisplay,column=0, sticky='se')
                    self.taskDescLabelList.append(taskDescLabel)
                    

                    weightScale = Scale (root2, orient=HORIZONTAL, bg='white', bd=0, highlightbackground='white', from_=1, to=10)
                    weightScale.grid(row=self.numTasksOnDisplay+1, column=1)
                    self.weightScaleList.append(weightScale)

                    taskDesc = Entry(root2, relief=FLAT, bg='lightgrey')
                    taskDesc.focus_set()
                    taskDesc.config(width=50)
                    taskDesc.grid(row=self.numTasksOnDisplay+1, column=0, sticky='s')        
                    self.taskDescEntryFieldList.append(taskDesc)
                    
                    localTaskPosition=self.numTasksOnDisplay
                    
                    def destroyRow(test):
                        try:
                            self.taskDescLabelList[test].destroy()
                            self.weightScaleList[test].destroy()
                            self.removeButtonList[test].destroy()
                            self.deleteBeforeSave.append(test)
                        except IndexError as error:
                            print("index out of bounds")
                    removeButton = Button(root2,image=removePhoto, command= lambda: destroyRow(localTaskPosition-1))
                    removeButton.grid(row=self.numTasksOnDisplay, column=3, sticky='sw')
                    self.removeButtonList.append(removeButton)

                    self.numTasksOnDisplay+=1
                    self.addButtonPosition+=1
            
            
        b1 = Button(root2,image=addPhoto, command=addTask)
        b1.grid(row=0, column=3, sticky='w')                                                   

        

        def callback():

            if(self.taskDescEntryFieldList[self.numTasksOnDisplay-1].get()=="" and self.numTasksOnDisplay==1):
                errorLabel.config(text="Enter at least 1 item", fg="red")

            else:
                    
                for i in sorted(self.deleteBeforeSave, reverse=True):
                    self.taskDescLabelList.pop(i)
                    self.weightScaleList.pop(i)


                finalTaskList=[]
                
                
                for f,b in zip(self.taskDescLabelList, self.weightScaleList):
                    task=Task()
                    task.description=f.cget("text")
                    task.weight=str(b.get())
                    finalTaskList.append(task)

                if(self.taskDescEntryFieldList[self.numTasksOnDisplay-1].get()!=""):
                    task=Task()
                    task.description=self.taskDescEntryFieldList[self.numTasksOnDisplay-1].get()
                    task.weight=str(self.weightScaleList[self.numTasksOnDisplay-1].get())
                    finalTaskList.append(task)
                
               
               
                finalTaskSet=TaskSet()
                finalTaskSet.taskList=finalTaskList
                finalTaskSet.version="0"
                finalTaskSet.active="Y"
                finalTaskSet.name="Mithul's task set"
                finalTaskSet.dateCreated=datetime.date.today().strftime("%d%m%Y")





                #finalTaskSet.viewTaskSet()
                finalTaskSet.saveToFile("data/TaskSets.dat")

                def clearScreen():
                    for i in self.taskDescLabelList:
                        i.destroy()
                        
                    for i in self.weightScaleList:
                        i.destroy()
                        
                    for i in self.removeButtonList:
                        i.destroy()
                        
                    for i in self.taskDescEntryFieldList:
                        i.destroy()
            
                root3=Toplevel()
                root3.geometry('+%d+%d'%(self.winfo_rootx(),self.winfo_rooty()))
                app2=DailyTracking(root3)
                root2.withdraw()
                
                clearScreen()
                
               

                    
        b = Button(root2,text="Next",command=callback)
        b.grid(row=40, column=1, sticky='w')

    def client_exit(self):
        exit()


class GoalUpdate(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)               
        self.master = master
        self.init_GoalUpdateWindow()

    numTasksOnDisplay=0
    addButtonPosition=2
    currentTaskSet=TaskSet() 
    
    removeButtonList=[]
    weightScaleList=[]
    taskDescEntryFieldList=[]
    taskDescLabelList=[]
    deleteBeforeSave=[]
    
    #Creation of init_GoalSetWindow



    def init_GoalUpdateWindow(self):
         
        
        # changing the title of our master widget      
        self.master.title("Update tasks")

        # allowing the widget to take the full space of the root window
        self.grid(row=0)

        # remove --- from file menu
        self.master.option_add('*tearOff', False)
        
        # creating a button instance
        # quitButton = Button(self, text="Save", command=self.client_exit)

        # placing the button on my window
        #quitButton.place(x=0, y=575)

        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the file object)
        file = Menu(menu)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        file.add_command(label="Exit", command=self.client_exit)

        #added "file" to our menu
        menu.add_cascade(label="File", menu=file)

        taskSetFile=TaskSetFile()
        taskSetFile.fileName="data/TaskSets.dat"   
        taskSetFile.loadAllTaskSets()
        
        activeTaskSet=taskSetFile.getActiveTaskSet()
        
        instructionLabel = Label(root2, text="\nAdd or remove tasks! \n", background = 'white').grid(row=0, column=0, sticky='w', columnspan=3 , padx=(0,100))
        
        
        errorLabel = Label(root2, text="", background = 'white')
        errorLabel.grid(row=40, column=0, sticky='sw')

        image = Image.open("img/add.png")
        image = image.resize((15, 15), Image.ANTIALIAS)
        addPhoto = ImageTk.PhotoImage(image)

        image2 = Image.open("img/remove.png")
        image2 = image2.resize((15, 15), Image.ANTIALIAS)
        removePhoto = ImageTk.PhotoImage(image2)


        label1= Label(image=addPhoto, borderwidth=0, highlightthickness=0)
        label1.image = addPhoto

        label2= Label(image=removePhoto, borderwidth=0, highlightthickness=0)
        label2.image = removePhoto
        
        #clearing out lists because I fucked up scope somehow
        self.weightScaleList=[]
        self.taskDescLabelList=[]
        self.removeButtonList=[]
        self.deleteBeforeSave=[]
        
        for i in activeTaskSet.taskList:
            taskDescLabel=Label(root2, text=i.description, background='white')
            taskDescLabel.grid(row=self.numTasksOnDisplay+1,column=0, sticky='se')
            self.taskDescLabelList.append(taskDescLabel)

            
            weightScale = Scale (root2, orient=HORIZONTAL, bg='white', bd=0, highlightbackground='white', from_=1, to=10)
            weightScale.set(i.weight)
            weightScale.grid(row=self.numTasksOnDisplay+1, column=1)
            self.weightScaleList.append(weightScale) 
            
            localTaskPosition=self.numTasksOnDisplay
            removeButton = Button(root2,image=removePhoto, command= lambda localTaskPosition=localTaskPosition: destroyRow(localTaskPosition))
            removeButton.grid(row=self.numTasksOnDisplay+1, column=3, sticky='sw')
            self.removeButtonList.append(removeButton)

            
            self.numTasksOnDisplay+=1       
            
        self.taskDescEntryField = Entry(root2, relief=FLAT, bg='lightgrey')
        self.taskDescEntryField.focus_set()
        self.taskDescEntryField.config(width=50)
        self.taskDescEntryField.grid(row=self.numTasksOnDisplay+1, column=0, sticky='s')

        self.taskWeightScale = Scale (root2, orient=HORIZONTAL, bg='white', bd=0, highlightbackground='white', from_=1, to=10)
        self.taskWeightScale.grid(row=self.numTasksOnDisplay+1, column=1)        
        
        
        localTaskPosition=self.numTasksOnDisplay

        def destroyRow(test):
            try:
                self.taskDescLabelList[test].destroy()
                self.removeButtonList[test].destroy()
                self.weightScaleList[test].destroy()
                self.deleteBeforeSave.append(test)
            except IndexError as error:
                print("index out of bounds")
             

        self.numTasksOnDisplay+=1
        self.addButtonPosition+=1


        def addTask():

# if there are no tasks, then only for the FIRST task,
    # create entry field for desc and weight
    # add the fields to the lists
    # lists will be used to create labels and then delete the field
    
                if(self.taskDescEntryField.get()==""):
                    errorLabel.config(text="Fill in item details before adding new task", fg="red")
    
                else:
                    errorLabel.config(text="")
                    taskDescLabel=Label(root2, text=self.taskDescEntryField.get(), background='white')
                    print(self.taskDescEntryField.get())
                    #self.taskDescEntryFieldList[self.numTasksOnDisplay-1].destroy()
                    taskDescLabel.grid(row=self.numTasksOnDisplay,column=0, sticky='se')
                    self.taskDescLabelList.append(taskDescLabel)
                    

                    weightScale = Scale (root2, orient=HORIZONTAL, bg='white', bd=0, highlightbackground='white', from_=1, to=10)
                    weightScale.set(self.taskWeightScale.get())
                    weightScale.grid(row=self.numTasksOnDisplay, column=1)
                    self.weightScaleList.append(weightScale)

                    self.taskDescEntryField.grid(row=self.numTasksOnDisplay+1, column=0, sticky='s')
                    self.taskDescEntryField.delete(0,'end')
                    self.taskWeightScale.grid(row=self.numTasksOnDisplay+1, column=1)
                    self.taskWeightScale.set(1)
                    
                    
                    localTaskPosition=self.numTasksOnDisplay
                    
                    def destroyRow(test):
                        try:
                            self.taskDescLabelList[test].destroy()
                            self.weightScaleList[test].destroy()
                            self.removeButtonList[test].destroy()
                            self.deleteBeforeSave.append(test)
                        except IndexError as error:
                            print("index out of bounds")
                    removeButton = Button(root2,image=removePhoto, command= lambda: destroyRow(localTaskPosition-1))
                    removeButton.grid(row=self.numTasksOnDisplay, column=3, sticky='sw')
                    self.removeButtonList.append(removeButton)

                    self.numTasksOnDisplay+=1
                    self.addButtonPosition+=1
            
            
        b1 = Button(root2,image=addPhoto, command=addTask)
        b1.grid(row=0, column=3, sticky='w')                                                   

        

        def callback():

            if(self.taskDescEntryField.get()=="" and self.numTasksOnDisplay==1):
                errorLabel.config(text="Enter at least 1 item", fg="red")

            else:
                    
                for i in sorted(self.deleteBeforeSave, reverse=True):
                    self.taskDescLabelList.pop(i)
                    self.weightScaleList.pop(i)


                finalTaskList=[]
                
                for f,b in zip(self.taskDescLabelList, self.weightScaleList):
                    task=Task()
                    task.description=f.cget("text")
                    task.weight=str(b.get())
                    finalTaskList.append(task)

                if(self.taskDescEntryField.get()!=""):
                    task=Task()
                    task.description=self.taskDescEntryField.get()
                    
                    task.weight=self.taskWeightScale.get()
                    finalTaskList.append(task)
                              
                
                finalTaskSet=TaskSet()
                finalTaskSet.taskList=finalTaskList
                finalTaskSet.active="Y"
                finalTaskSet.name="Mithul's task set"
                finalTaskSet.version=activeTaskSet.version
                finalTaskSet.dateCreated=datetime.date.today().strftime("%d%m%Y")


                
                if(activeTaskSet.isDifferent(finalTaskSet)):
                    print("Taskset has changed. Appending new version to TaskSetFile")
                    finalTaskSet.version=str(int(finalTaskSet.version)+1)
                    finalTaskSet.addNewVersionToFile("data/TaskSets.dat")
                else:
                    print("No changes found in taskset")
            

                root3.geometry('+%d+%d'%(self.winfo_rootx(),self.winfo_rooty()))
                root3.deiconify()


                app.init_DailyTrackingWindow()
                root2.withdraw()
                clearScreen()
                    
        b = Button(root2,text="Update",command=callback)
        b.grid(row=40, column=1, sticky='w')


        

        def clearScreen():
            for i in self.taskDescLabelList:
                i.destroy()
                
            for i in self.weightScaleList:
                i.destroy()
                
            for i in self.removeButtonList:
                i.destroy()
                
            self.taskDescEntryField.destroy()

    def client_exit(self):
        exit()

class DailyTracking(Frame):

    dailyTrackingFileName="data/DailyTracking.dat"
    activeDate=datetime.date.today().strftime("%d%m%Y") 
    dailyTrackingFile=DailyTrackingFile(dailyTrackingFileName)
    
    rowStart=2
    
    def __init__(self, master=None):
        Frame.__init__(self, master)               
        self.master = master

        self.init_DailyTrackingWindow()
        

    def init_DailyTrackingWindow(self):    
    
        self.master.title("Do The Work")

        self.grid(row=0)

        self.master.option_add('*tearOff', False)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)



        menu.add_cascade(label="File", menu=file)
        

        self.configure(bg='white')
        
        taskSetFile1=TaskSetFile()
        taskSetFile1.fileName="data/TaskSets.dat"
        taskSetFile1.loadAllTaskSets()
        
   
        
        
        f = open(taskSetFile1.fileName, "r")
        contents= f.read()
        
        activeTaskSet=taskSetFile1.getActiveTaskSet()

        
        activeTaskSet.taskList.sort(key=lambda x: (int(x.weight),int(x.position)), reverse=True)

        descriptionList =[]
        weightList= []


        fillerLabel = Label(self, text="", background = "white", width=37, height=1)
        fillerLabel.grid(row=1, column=0, sticky='n', columnspan=3)        
        dayName = calendar.day_name[datetime.datetime.strptime(self.activeDate, "%d%m%Y").weekday()]
        dateLabelText=dayName[:3] + " " + datetime.datetime.strptime(self.activeDate, "%d%m%Y").strftime("%d %b")
        
        
        dateLabel=Label(self, text=dateLabelText, background = 'white', width=32, font=("TkDefaultFont",10))
        dateLabel.grid(row=0, column=0, sticky='n', columnspan=3)
                
        
        
        activeTaskSet.checkBoxVarList=[]
        
        def updateNote(test):
            root4 = Toplevel()
            root4.resizable(False,False)
            root4.title(test.cget("text"))
            taskNotes = Text(root4, relief=FLAT, bg='lightgrey', width=70, height=4, font="TkDefaultFont", wrap = "word")
            taskNotes.grid(row=0, column=0, columnspan=2)
            statusLabel=Label(root4, text="", bg=root["bg"])
            statusLabel.grid(row=1, column=0, sticky='w')
            
            existingNote=taskSetFile1.getNote(test.cget("text"))
            taskNotes.insert("1.0",existingNote)
            
            saveStatus=''
            
            def saveNote():
                saveStatus=taskSetFile1.addNote(activeTaskSet.getVersionAndName(), test.cget("text"), (taskNotes.get("1.0",END)).rstrip())
                statusLabel.config(text=saveStatus)
                

                self.rowStart=2
                
                displayCombo(self.activeDate)
                root4.destroy()

            def deleteNote():
                saveStatus=taskSetFile1.addNote(activeTaskSet.getVersionAndName(), test.cget("text"), "")
                statusLabel.config(text=saveStatus)
                

                self.rowStart=2
                
                displayCombo(self.activeDate)
                root4.destroy()
            
            saveButton = Button(root4,text="Save",command=saveNote)
            saveButton.grid(row=1, column=1, sticky='e', padx=(0,45))
            deleteButton = Button(root4,text="Delete", command=deleteNote)
            deleteButton.grid(row=1, column=1, sticky='e')

        pointsTotalLabel=Label(self, text=activeTaskSet.getTotalPointsForDay(), background = 'white', font=("Courier", 30))

        sickVar=IntVar()
        offVar=IntVar()
        
        image = Image.open("img/sick.png")
        image = image.resize((40, 40), Image.ANTIALIAS)
        sick = ImageTk.PhotoImage(image)     

        image2 = Image.open("img/leave.png")
        image2 = image2.resize((50, 50), Image.ANTIALIAS)
        leave = ImageTk.PhotoImage(image2)             
        
        sickBox= Checkbutton(self, variable=sickVar, background="white", text="SICK", image=sick )
        sickBox.image = sick     

        
        leaveBox= Checkbutton(self, variable=offVar, background="white", text="OFF", image=leave)
        leaveBox.image=leave
        
        
        sick_ttp = CreateToolTip(sickBox, "Sick day")
        leave_ttp = CreateToolTip(leaveBox, "Off day")        
        
        
        def updatePointsLabel():
            pointsTotalLabel.config(text=activeTaskSet.getTotalPointsForDay())

                    
        def initDisplay():

            self.rowStart=2
            
            activeTaskSet.checkBoxVarList=[]
            
            for i in descriptionList:
                i.destroy()
            
            for i in weightList:
                i.destroy()

            for i in activeTaskSet.checkBoxList:
                i.destroy()
            
            for i in activeTaskSet.taskList:
                var=IntVar()
                checkBox= Checkbutton(self, variable=var, background="white", command=updatePointsLabel)
                checkBox.grid(row=self.rowStart, column=0, sticky='e')
                activeTaskSet.checkBoxList.append(checkBox)
                activeTaskSet.checkBoxVarList.append(var)
                
                
                labelDesc=Label(self, text=i.description, background = 'white')
                labelDesc.grid(row=self.rowStart, column=2, sticky='w')
                
                note=(taskSetFile1.getNote(labelDesc.cget("text"))).strip('\n')
                
                if(note!=""):
                    labelDesc_ttp = CreateToolTip(labelDesc, note)
                    labelDesc.configure(foreground="brown")
                
                descriptionList.append(labelDesc)
                
                

                points=int(round(int(i.weight) * activeTaskSet.getPointsPerWeight()))
                
                weightDesc=Label(self, text=points, background = 'white')
                weightDesc.grid(row=self.rowStart, column=1, sticky='w')
                weightList.append(weightDesc)

                self.rowStart=self.rowStart+1
                
                labelDesc.bind("<Button-1>", lambda event, labelDesc=labelDesc: updateNote(labelDesc))
                #lambda self:open_url(event,name)

        
      
        def updateGUI(date):
            self.activeDate=date
            
            self.dailyTrackingFile.initialize(activeTaskSet, date)
            #if taskset and current date exists in file, then load and set var values
            if(self.dailyTrackingFile.taskSetDayExists(activeTaskSet.getVersionAndName(), date)==True):
                print("Taskset found and entry for " + date + " exists. Loading...")
                self.dailyTrackingFile.updateSortedCheckBoxVarListFromString(activeTaskSet,date)
                sickOffList=self.dailyTrackingFile.getSickAndOffVars(activeTaskSet, date)
                sickVar.set(sickOffList[0])
                offVar.set(sickOffList[1])
                
            
            else:
                print("not found for " + date)
                
            pointsTotalLabel.config(text=activeTaskSet.getTotalPointsForDay())
            pointsTotalLabel.grid(row=self.rowStart+1, column=0, columnspan=3, sticky='e') 

            leaveBox.grid(row=self.rowStart+1, column=0, columnspan=3, padx=(0,117), sticky='e')
            sickBox.grid(row=self.rowStart+1, column=0, columnspan=3, sticky='w')
            
            dayName = calendar.day_name[datetime.datetime.strptime(self.activeDate, "%d%m%Y").weekday()]
            dateLabelText=dayName[:3] + " " + datetime.datetime.strptime(self.activeDate, "%d%m%Y").strftime("%d %b")
            dateLabel.config(text=dateLabelText)
            
            
        def displayCombo(date):
            initDisplay()
            updateGUI(date)
        
        displayCombo(self.activeDate)
        
        def editTasks():
        
            pointsTotalLabel.destroy()
            for i in descriptionList:
                i.destroy()
            
            for i in weightList:
                i.destroy()

            for i in activeTaskSet.checkBoxList:
                i.destroy()
            
            root2.deiconify()
            root2.configure(bg='white')
            root3.withdraw()

            app =   GoalUpdate(root2)   

        

        file.add_command(label="Edit Tasks", command=editTasks)

        def goBackADay():
            activeTaskSet.logLabel.config(text="")
            updateDailyTrackingFile(self.dailyTrackingFile.getDailyTrackingString(activeTaskSet,self.activeDate), sickVar.get(), offVar.get())
            displayCombo((datetime.datetime.strptime(self.activeDate, "%d%m%Y")-datetime.timedelta(days=1)).strftime("%d%m%Y"))
            
            
        def goForwardADay():      
            activeTaskSet.logLabel.config(text="")
            updateDailyTrackingFile(self.dailyTrackingFile.getDailyTrackingString(activeTaskSet,self.activeDate), sickVar.get(), offVar.get())
            displayCombo((datetime.datetime.strptime(self.activeDate, "%d%m%Y")+datetime.timedelta(days=1)).strftime("%d%m%Y"))
            
            
            
        image = Image.open("img/back.png")
        image = image.resize((20, 20), Image.ANTIALIAS)
        backPhoto = ImageTk.PhotoImage(image)

        image2 = Image.open("img/forward.png")
        image2 = image2.resize((20, 20), Image.ANTIALIAS)
        forwardPhoto = ImageTk.PhotoImage(image2)
        
        label1= Label(image=backPhoto, borderwidth=0, highlightthickness=0)
        label1.image = backPhoto     

        label2= Label(image=backPhoto, borderwidth=0, highlightthickness=0)
        label2.image = forwardPhoto                
        
        b1 = Button(self,image=backPhoto, bg="white", relief=FLAT, command=goBackADay)
        b1.grid(row=0, column=0, sticky='w') 
        
        b2 = Button(self,image=forwardPhoto, bg="white", relief=FLAT, command=goForwardADay)
        b2.grid(row=0, column=2, sticky='e')         
        

        
        def updateDailyTrackingFile(beforeString, sickVar, offVar):
        
            afterString=activeTaskSet.convertToOriginalString(activeTaskSet.createCheckBoxVarListStorageString())
            
            if(sickVar==0):
                afterString=afterString+ " N"
            else:
                afterString=afterString+ " Y"
            
            if(offVar==0):
                afterString=afterString+ " N"
            else:
                afterString=afterString+ " Y"            
            
            
            if(beforeString!=afterString):
                #add another if check here to check if leave/sick status has changed
                self.dailyTrackingFile.update(activeTaskSet, self.activeDate, sickVar, offVar)
            
    
        activeTaskSet.logLabel = Label(self, text="", background = 'lightblue', width=37, height=1)
        activeTaskSet.logLabel.grid(row=self.rowStart+2, column=0, sticky='s', columnspan=3)           
   
        def on_closing():

            updateDailyTrackingFile(self.dailyTrackingFile.getDailyTrackingString(activeTaskSet,self.activeDate), sickVar.get(), offVar.get())
            root.destroy()
            root2.destroy()
            root3.destroy()

            
        root3.protocol("WM_DELETE_WINDOW", on_closing)
      
        
root = Tk()

filename = "data/TaskSets.dat"
filename2= "data/DailyTracking.dat"

if not os.path.exists(os.path.dirname(filename)):
    try:
        os.makedirs(os.path.dirname(filename))
        
        
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

f = open(filename, "a")
f.close()

f1 = open(filename2, "a")
f1.close()

taskSetFile=TaskSetFile()
taskSetFile.fileName="data/TaskSets.dat"
taskSetFile.loadAllTaskSets()

# check if an active task set exists in the file, and if so, load the contents onto the screen

root2=Toplevel()
root2.withdraw()

root3=Toplevel()
root3.withdraw()

if(taskSetFile.hasActiveTaskSet()):
    app=DailyTracking(root3)
    root3.deiconify()
    root.withdraw()
else:

    root2.configure(bg='white')
    root2.deiconify()
    root.withdraw()
    

    app = GoalSet(root2)

def on_closing():
        root.destroy()
        root2.destroy()
        root3.destroy()
        

root2.protocol("WM_DELETE_WINDOW", on_closing)
#root3.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()  
