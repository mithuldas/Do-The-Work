from TaskSet import TaskSet
from Task import Task

class TaskSetFile:
    fileName=""
    allTaskSets=[]
    taskSetStrings=[]
    
    def getFileName(self):
        return self.fileName
       
    def loadAllTaskSets(self):

        self.allTaskSets=[]
        self.taskSetStrings=[]
        
        with open(self.fileName) as f:
            taskstring=""
            for line in f:
                taskSet=TaskSet()
                if(line[:2]!="ET" and line!="\n"):
                
                    taskstring=taskstring+line
                
                if(line[:2]=="ET"):
                    taskstring=taskstring+line
                    self.taskSetStrings.append(taskstring)
                    taskstring=""
            
        f.close()

        for i in self.taskSetStrings:            
            self.allTaskSets.append(self.convertTaskSetStringToTaskSet(i))

            
        
    
    def convertTaskSetStringToTaskSet(self,taskSetString):

        descriptionList=[]
        weightList=[]
        positionList=[]
        taskList=[]
        taskSet=TaskSet()
        
        position=0
        
        for line in taskSetString.splitlines():
            task=Task()
            
            if(line[:2]=="TS"):
                taskSet.active=line[3]
                taskSet.dateCreated=line[5:13]
                taskSet.version=self.getVersion(line)
                taskSet.name=self.getName(line)
                
            if(line[:2]=="TD"):
                descriptionList.append(line[3:])
                positionList.append(position)
                position=position+1
        
            if(line[:2]=="TW"):
                weightList.append(line[3:])
    
        
        for d, w, p in zip(descriptionList, weightList, positionList):
            task=Task()
            task.description=d
            task.weight=w
            task.position=p
            taskList.append(task)
            
        taskSet.taskList=taskList
        
        return taskSet

    def getVersion(self, headerString):
        version=""
        spaceCounter=0
        for i in headerString:
            if(i==' '):
                spaceCounter=spaceCounter+1
            if spaceCounter==3 and i!=" ":
                version=version+i
        
        return version
        
        
        
    def getName(self, headerString):
        name=""
        spaceCounter=0
        for i in headerString:
            if(i==' '): 
                spaceCounter=spaceCounter+1
            if spaceCounter>3:
                name=name+i
        
        name=name[1:]
        return name        
        
        
    def getActiveTaskSet(self):
    
        taskSet=TaskSet()
        
        for i in self.allTaskSets:
            if(i.isActive()):
                return i
                
    def hasActiveTaskSet(self):
        taskSet=TaskSet()
        counter=0
        for i in self.allTaskSets:
            if(i.isActive()):
                counter=counter+1
        
        if counter>0:
            return True
        else:
            return False
    
    def addNote(self, taskSetVersionAndName, taskDescription, note):
        
        note=note.replace("\n","{n}")
        
        try:
            with open(self.fileName, "r") as f:
                contents= f.readlines()
                insertPosition=0
                entryLine=0
                
                for i in contents:
                    insertPosition=insertPosition+1
                    if i.find(taskDescription)!=-1:
                        entryLine=insertPosition
                
                #set note insert position after TD and TW
                entryLine=entryLine+1
                if(contents[entryLine][:2]!="TN"):
                    contents.insert(entryLine, "TN "+ note + "\n")
                
                if(contents[entryLine][:2]=="TN"):    
                    contents[entryLine]="TN "+ note + "\n"
                
                contents = "".join(contents)
        except IOError:
            print ("couldn't read file")
        
        try:        
            with open(self.fileName, "w") as f:
                print("Updating notes for " + taskSetVersionAndName + " " + taskDescription)
                f.write(contents)
                return "Note saved"
        except IOError:
            return "Failed to write to file"
        
        
    
    def getNote(self, taskDescription):
        f = open(self.fileName, "r")
        contents= f.readlines()
        insertPosition=0
        noteLine=0
        
        for i in contents:
            insertPosition=insertPosition+1
            if i.find(taskDescription)!=-1:
                noteLine=insertPosition
        noteLine=noteLine+1
        
        if(contents[noteLine][:2]=="TN"):
            string=contents[noteLine][3:]
            string=string.replace("{n}","\n")
            return string
            
        else:
            return ""
                