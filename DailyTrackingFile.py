from TaskSet import TaskSet
from Task import Task

import datetime

class DailyTrackingFile:

    allTaskSets=[]
    allDateEntries=[]
    filename=""

    def __init__(self, filename):
        self.filename=filename
        self.populateAllTaskSets()
        
    def hasActiveTaskSetEntryForToday(self, versionAndName, date):
    
        if(self.taskSetDayExists(taskSet.getVersionAndName(), datetime.date.today().strftime("%d%m%Y"))==True):
            return True
        
            
    def populateAllTaskSets(self):
        taskSetCount=0
        
        #reset arrays (clear them out before repopulating)
        self.allDateEntries=[]
        self.allTaskSets=[]
        
        with open(self.filename) as f:
            for line in f:
                if(line[:2]=="TS"):
                    self.allDateEntries.append([])
                    self.allTaskSets.append(self.getTaskSetVersionAndName(line).strip('\n'))
                    
                    
                    taskSetCount=taskSetCount+1
                    
                if(line[:2]=="DT"):
                    self.allDateEntries[(taskSetCount-1)].append((line[3:].strip('\n')))
                    
            
    def taskSetExists(self, versionAndName):
        for i in self.allTaskSets:
            if i==versionAndName:
                return True
            
    
    def taskSetDayExists(self, versionAndName, date):
        
        
        for i in range(len(self.allDateEntries)):
            for j in range(len(self.allDateEntries[i])):
                if (self.allTaskSets[i]==versionAndName and self.allDateEntries[i][j][:8]==date): 
                    return True
    
            
    def initialize(self,taskSet,activeDate):
                
        #if tasket doesn't exist in the file, then append TS lines at the end
        if(self.taskSetExists(taskSet.getVersionAndName())!=True):
            print ("Taskset + version doesn't exist in file. Adding new taskset to file...")
            f = open(self.filename, "a")
            f.write("TS "+ taskSet.version + " " + taskSet.name + "\n")
            f.close()
            self.populateAllTaskSets()
        
        #if (or when) taskset already exists in the file, and if DT entry for selected date doesn't exist, write DT entries from last DT entry position onward
        if(self.taskSetExists(taskSet.getVersionAndName())==True and self.taskSetDayExists(taskSet.getVersionAndName(), activeDate)!=True):
            print ("Taskset found, but no entry for " + activeDate)
            f = open(self.filename, "r")
            contents= f.readlines()
            f.close()   
            
            taskSetIndex=self.allTaskSets.index(taskSet.getVersionAndName())

            insertPosition=0
            
            for i in range(len(self.allDateEntries)):
                if(i<=taskSetIndex):
                    insertPosition=insertPosition+1
                for j in range(len(self.allDateEntries[i])):
                    if(i<=taskSetIndex):
                            insertPosition=insertPosition+1
                            
            contents.insert(insertPosition, "DT "+ activeDate + " " + taskSet.createinitCheckBoxVarListStorageString()+ " N N\n")
            f = open(self.filename, "w")
            contents = "".join(contents)
            print("Adding an entry for " + activeDate + " into DailyTrackingFile for taskset " + taskSet.getVersionAndName())
            f.write(contents)
            f.close()
            self.populateAllTaskSets()
        
    def update(self,taskSet, date, sickVar, leaveVar):
        # if we reach here, it means that taskset exists in the file, and date (DT) exists in the file
        # just find the index and update the row if needed
        
        # if storage string differs), then update the relevant DT line
        print ("taskset exists, " + date + " entry exists, making updates to it...")
        f = open(self.filename, "r")
        contents= f.readlines()
        
        f.close()   

        insertPosition=0
        
        taskSetIndex=self.allTaskSets.index(taskSet.getVersionAndName())
        
        for i in range(len(self.allDateEntries)):
            if(i<=taskSetIndex):
                insertPosition=insertPosition+1
                for j in range(len(self.allDateEntries[i])):
                    insertPosition=insertPosition+1
                    if(self.allDateEntries[i][j][:8]==date):
                        break

        contents[insertPosition-1]="DT "+ date + " " + taskSet.convertToOriginalString(taskSet.createCheckBoxVarListStorageString())
        
        if(sickVar==1):
             contents[insertPosition-1]=contents[insertPosition-1]+ " Y"
        else:
            contents[insertPosition-1]=contents[insertPosition-1]+ " N"       

        if(leaveVar==1):
            contents[insertPosition-1]=contents[insertPosition-1]+ " Y"
        else:
            contents[insertPosition-1]=contents[insertPosition-1]+ " N"
            
        contents[insertPosition-1]=contents[insertPosition-1]+"\n"
        

        f = open(self.filename, "w")
        contents = "".join(contents)
        taskSet.logLabel.config(text="Updated day " + date + " in " + taskSet.getVersionAndName())
        f.write(contents)
        f.close()
        self.populateAllTaskSets()         
        

    def updateCheckBoxVarListFromString(self, taskSet, date):
        for i in range(len(self.allDateEntries)):
            for j in range(len(self.allDateEntries[i])):
                if (self.allTaskSets[i]==taskSet.getVersionAndName() and self.allDateEntries[i][j][:8]==date):
                    string=(self.allDateEntries[i][j][9:])
                    
                    counter=0
                    for i in string:
                        taskSet.checkBoxVarList[counter].set(i)
                        counter=counter+1         
            
    def updateSortedCheckBoxVarListFromString(self, taskSet, date):

        matchFound=False
        
        for i in range(len(self.allDateEntries)):
            if (matchFound==True):
                break
            for j in range(len(self.allDateEntries[i])):       
                if (self.allTaskSets[i]==taskSet.getVersionAndName() and self.allDateEntries[i][j][:8]==date):
                    

                    string=taskSet.convertToSortedString(self.allDateEntries[i][j][9:])
                    matchFound=True
                    counter=0
                    for i in string:
                        taskSet.checkBoxVarList[counter].set(i)
                        counter=counter+1
                    break

    def getSickAndOffVars(self, taskSet, date):
        
        matchFound=False
        list=[]
        
        for i in range(len(self.allDateEntries)):
            if (matchFound==True):
                break
            for j in range(len(self.allDateEntries[i])):       
                if (self.allTaskSets[i]==taskSet.getVersionAndName() and self.allDateEntries[i][j][:8]==date):

                    list=self.allDateEntries[i][j].split()
                    break
        
        
        if(len(list)<3):
            list=[0,0]
            
        if(len(list)==4):
            del(list[0:2])
            #first item in list is sickvar, second is off        
        
        
        if(list[0]=="N"):
            list[0]=0
        if(list[0]=="Y"):
            list[0]=1
        if(list[1]=="N"):
            list[1]=0
        if(list[1]=="Y"):
            list[1]=1
            

            
        return list

    def getDailyTrackingString(self, taskSet, date):
        string=""
        for i in range(len(self.allDateEntries)):
            for j in range(len(self.allDateEntries[i])):
                if (self.allTaskSets[i]==taskSet.getVersionAndName() and self.allDateEntries[i][j][:8]==date):
                    string=(self.allDateEntries[i][j][9:])


        return string
        
    def getTaskSetVersionAndName(self, headerString):
        version=""
        spaceCounter=0
        for i in headerString:
            if(i==' '):
                spaceCounter=spaceCounter+1
            if spaceCounter==1 and i!=" ":
                version=version+i        
        
        
        name=""
        spaceCounter=0
        for i in headerString:
            if(i==' '): 
                spaceCounter=spaceCounter+1
            if spaceCounter>1:
                name=name+i
        
        name=name[1:]           

        return str(version) + " " + str(name)